import os
from datetime import datetime
import PySimpleGUI as sg
import json
from pynput.keyboard import Key, Controller

from config import Config
from utilities import Message, Keypad
from db_orm import DbConn, DbTable, DbQuery
from cash_layout import CashCanvas, DrawerTrnCanvas, DrawerChangeCanvas
from cash_ui import CashUi, DrawerTrnUi, DrawerChangeUi
from common import ItemList, CustomerList, Denomination


class Cash:
    def __init__(self, menu_opt, user_id, terminal_id, branch_id):    

        config = Config()

        self.__terminal_id = terminal_id
        self.__branch_id = branch_id

        w, h = sg.Window.get_screen_size()
        #w = w - 55
        #h = h - 60
        
        self.__name = ''

        self.__db_conn = DbConn()
        self.__db_session = self.__db_conn.session

        self.__db_cash_transaction_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabCash_Transaction)
        filter='terminal_id = {}'.format(self.__terminal_id)
        db_cash_transaction_cursor = self.__db_cash_transaction_table.list(filter)
      
        self.__db_cash_transaction_denomination_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabCash_Transaction_Denomination)

        db_denomination_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabDenomination)
        filter=''
        order='sort_order'
        db_denomination_cursor = db_denomination_table.list(filter, order)

        if (len(db_denomination_cursor) == 0):
            sg.popup('Denomination(s) not found', keep_on_top = True, icon='images/INFO.png')
            return

        self.__denomination_list = []
        self.__denomination_value_list = []
        for db_denomination_row in db_denomination_cursor:
            self.__denomination_list.append(db_denomination_row.name)
            self.__denomination_value_list.append(db_denomination_row.cash_value)       
            
        kb = Controller()
        self.__kb = kb
        
        self.__canvas = CashCanvas(self.__denomination_list)

        title = 'Cash'

        self.__window = sg.Window(title, 
                        self.__canvas.layout,
                        font='Helvetica 11', 
                        finalize=True, 
                        location=(-8,0), 
                        size=(w,h-50),
                        keep_on_top=False, 
                        resizable=False,
                        return_keyboard_events=True, 
                        use_default_focus=False,
                        icon='images/favicon.ico',
                        modal=True
                    )
    
        self.__ui = CashUi(self.__window, self.__denomination_list)

        self.initialize_ui()     
        self.__ui.user_id = user_id
        self.__ui.terminal_id = terminal_id    
        self.__ui.branch_id = branch_id   
                
        self.__ui.cashs_list = []

        self.__base_query = 'select \
        ct.name, \
        ct.transaction_type, \
        ct.transaction_context, \
        ct.transaction_reference, \
        ct.transaction_date, \
        ct.receipt_amount, \
        ct.payment_amount \
        from tabCash_Transaction ct \
        where ct.branch_id = "' + self.__branch_id + '" and ct.terminal_id = "' + self.__terminal_id + '"'

        self.__order_query = ' order by ct.name  DESC '
        self.__this_query = ''
       
        db_query = DbQuery(self.__db_conn, self.__base_query + self.__order_query)        
        if  db_query.result:
            self.__ui.cashs_list.clear()
            for db_row in db_query.result:
                self.__ui.name = db_row[0]
                self.__ui.transaction_type = db_row[1]
                self.__ui.transaction_context = db_row[2]
                self.__ui.transaction_reference = db_row[3]
                self.__ui.transaction_date = db_row[4]
                self.__ui.receipt_amount = db_row[5]
                self.__ui.payment_amount = db_row[6]
                self.__ui.add_cash_line()

        self.__ui.cash_idx = 0
        self.__ui.focus_cash_list()
        
        self.refresh_summary_pane()
        self.refresh_total_pane()

        self.__transaction_type = ''
        self.__transaction_amount = 0.00
        self.__transaction_denomonation_dict = dict()
        self.__approved_by = ''

        self.__change_amount = 0.00
        self.__from_denomonation_dict = dict()
        self.__to_denomonation_dict = dict()
        
        #self.__ui.focus_transaction_type_search()
        self.__ui.focus_cash_list()
        self.handler()


    def handler(self):  
        prev_event = ''
        prev_values = ''
        
        while True:
            event, values = self.__window.read()
            #print('customer_list=', event, prev_event, values)
            if event in ("Exit", '_CASH_LIST_ESC_', 'Escape:27') or event == sg.WIN_CLOSED:
                break

            if event in ('_CASH_LIST_SEARCH_', 'F11', 'F11:122'):
                self.__this_query = ''
                if self.__ui.transaction_type_search:
                    if not self.__ui.transaction_type_search == '':
                        self.__this_query += ' and ct.transaction_type = "' + self.__ui.transaction_type_search + '"'

                if self.__ui.transaction_context_search:
                    if not self.__ui.transaction_context_search == '':
                        self.__this_query += ' and ct.transaction_context = "' + self.__ui.transaction_context_search + '"'

                self.__ui.cashs_list = []
                        
                db_query = DbQuery(self.__db_conn, self.__base_query + self.__this_query + self.__order_query)
                if  db_query.result:
                    
                    for db_row in db_query.result:
                        self.__ui.name = db_row[0]
                        self.__ui.transaction_type = db_row[1]
                        self.__ui.transaction_context = db_row[2]
                        self.__ui.transaction_reference = db_row[3]
                        self.__ui.transaction_date = db_row[4]
                        self.__ui.receipt_amount = db_row[5]
                        self.__ui.payment_amount = db_row[6]
                        self.__ui.add_cash_line()
                    self.refresh_summary_pane()
                    self.refresh_total_pane()
                    
            if event in ('_CASH_LIST_DENOMINATION_', '\r', 'F3', 'F3:114'):
                cash_idx = values['_CASH_LIST_'][0]
                self.__ui.cash_line_to_elements(cash_idx)
                self.__name = self.__ui.name
                
                default_amount_dict = dict()
    
                filter = "parent='{}'"
                db_cash_transaction_denomination_cursor = self.__db_cash_transaction_denomination_table.list(filter.format(self.__name))
                for db_cash_transaction_denomination_row in db_cash_transaction_denomination_cursor:
                    default_amount_dict[db_cash_transaction_denomination_row.denomination] = db_cash_transaction_denomination_row.count
                
                self.denomination(default_amount_dict, 'view')
                        
            if event in ('_CASH_LIST_RECEIPT_', '\r', 'F1', 'F1:112'):
                self.__transaction_amount, self.__transaction_denomination_dict, self.__approved_by = self.receipt()
                self.__transaction_type = 'Receipt'
                self.update_transaction()
                self.refresh_detail_pane()
                self.refresh_summary_pane()
                self.refresh_total_pane()
                self.__ui.focus_cash_list()
                
            if event in ('_CASH_LIST_PAYMENT_', '\r', 'F2', 'F2:113'):
                self.__transaction_amount, self.__transaction_denomination_dict, self.__approved_by = self.payment()
                self.__transaction_type = 'Payment'
                self.update_transaction()
                self.refresh_detail_pane()
                self.refresh_summary_pane()
                self.refresh_total_pane()
                self.__ui.focus_cash_list()

            if event in ('_CASH_LIST_CHANGE_', '\r', 'F3', 'F3:114'):
                self.__change_amount, self.__from_denomination_dict, self.__to_denomination_dict = self.change()
                self.update_change()
                self.refresh_detail_pane()
                self.refresh_summary_pane()
                self.refresh_total_pane()
                self.__ui.focus_cash_list()

            if event not in ('\t', 'Up:38', 'Down:40', 'UP', 'DOWN'):               
                prev_event = event
            prev_values = values
           
        self.__db_conn.close()           
        self.__window.close()    

      
    def initialize_footer_pane(self):
        self.__ui.user_id = ''
        self.__ui.terminal_id = ''
        self.__ui.branch_id = ''
        self.__ui.current_date = '2021/06/13'

    def initialize_ui(self):
        self.initialize_footer_pane()

    def clear_ui(self):
        None
        
    ######
    # Wrapper function for Denomination
    def denomination(self, amount, mode):
        denomination = Denomination(amount, mode)
        return denomination.denomination_count_dict

    ######
    # Wrapper function for Transaction
    def receipt(self):
        receipt = DrawerTrn('Receipt')
        return receipt.transaction_amount, receipt.transaction_denomination_dict, receipt.approved_by

    ######
    # Wrapper function for Transaction
    def payment(self):
        payment = DrawerTrn('Payment')
        return payment.transaction_amount, payment.transaction_denomination_dict, payment.approved_by

    ######
    # Wrapper function for Exchange
    def change(self):
        change = DrawerChange()
        return change.change_amount, change.from_denomination_dict, change.to_denomination_dict

    def refresh_detail_pane(self):
        
        db_query = DbQuery(self.__db_conn, self.__base_query + self.__this_query + self.__order_query)        
        if  db_query.result:
            self.__ui.cashs_list.clear()
            for db_row in db_query.result:
                self.__ui.name = db_row[0]
                self.__ui.transaction_type = db_row[1]
                self.__ui.transaction_context = db_row[2]
                self.__ui.transaction_reference = db_row[3]
                self.__ui.transaction_date = db_row[4]
                self.__ui.receipt_amount = db_row[5]
                self.__ui.payment_amount = db_row[6]
                self.__ui.add_cash_line()

    def refresh_summary_pane(self):
        idx = 0
        for denomination in self.__denomination_list:

            self.__ui.denomination_name = denomination
            summary_query = 'select IFNULL(sum(count),0) receipt from \
            tabCash_Transaction_Denomination ctd, \
            tabCash_Transaction ct \
            where ctd.denomination = "' + denomination + '" and ctd.parent = ct.name and ct.transaction_type = "Receipt" and terminal_id = "' + self.__terminal_id + '"' 

            db_query = DbQuery(self.__db_conn, summary_query + self.__this_query)        
            if  db_query.result:
                for db_row in db_query.result:
                    if db_row[0] == None:
                        receipt_count = 0
                    else:
                        receipt_count = int(db_row[0])
                        
            summary_query = 'select IFNULL(sum(count),0) payment from \
            tabCash_Transaction_Denomination ctd, \
            tabCash_Transaction ct \
            where ctd.denomination = "' + denomination + '" and ctd.parent = ct.name and ct.transaction_type = "Payment" and terminal_id = "' + self.__terminal_id + '"' 

            db_query = DbQuery(self.__db_conn, summary_query + self.__this_query)        
            if  db_query.result:
                for db_row in db_query.result:
                    if db_row[0] == None:
                        payment_count = 0
                    else:
                        payment_count = int(db_row[0])

            self.__ui.denomination_count = receipt_count - payment_count
            self.__ui.denomination_amount = int(self.__ui.denomination_count) * float(self.__denomination_value_list[idx])                    

            idx += 1

    def refresh_total_pane(self):
        total_query = 'select IFNULL(sum(receipt_amount),0) received_amount from \
        tabCash_Transaction ct where ct.terminal_id = "' + self.__terminal_id + '"'

        db_query = DbQuery(self.__db_conn, total_query + self.__this_query)        
        if  db_query.result:
            for db_row in db_query.result:
                if db_row[0] == None:
                    received_amount = 0
                else:
                    received_amount = float(db_row[0])

        self.__ui.received_amount = received_amount
        
        total_query = 'select IFNULL(sum(payment_amount),0) paid_amount from \
        tabCash_Transaction ct where ct.terminal_id = "' + self.__terminal_id + '"'

        db_query = DbQuery(self.__db_conn, total_query + self.__this_query)        
        if  db_query.result:
            for db_row in db_query.result:
                if db_row[0] == None:
                    paid_amount = 0
                else:
                    paid_amount = float(db_row[0])
        
        self.__ui.paid_amount = paid_amount
        self.__ui.balance_amount = float(received_amount) - float(paid_amount)
    

    def update_transaction(self):
        if float(self.__transaction_amount) > 0:
            db_query = DbQuery(self.__db_conn, 'SELECT nextval("DRAWER_TRANSACTION_REFERENCE")')
            for db_row in db_query.result:
                transaction_reference = db_row[0]

            db_query = DbQuery(self.__db_conn, 'SELECT nextval("CASH_TRANSACTION_ENTRY")')
            for db_row in db_query.result:
                cash_transaction_number = db_row[0]

            db_cash_transaction_row = self.__db_cash_transaction_table.new_row()

            db_cash_transaction_row.name = cash_transaction_number
            db_cash_transaction_row.transaction_type = self.__transaction_type     
            db_cash_transaction_row.transaction_context = 'Drawer'
            db_cash_transaction_row.transaction_reference = transaction_reference
            db_cash_transaction_row.transaction_date = self.__ui.current_date
            if self.__transaction_type == 'Receipt':
                db_cash_transaction_row.receipt_amount = self.__transaction_amount
                db_cash_transaction_row.payment_amount = 0
            else:
                db_cash_transaction_row.payment_amount = self.__transaction_amount
                db_cash_transaction_row.receipt_amount = 0
            
            db_cash_transaction_row.party_type = 'User'
            db_cash_transaction_row.customer = self.__ui.user_id
            db_cash_transaction_row.branch_id = self.__branch_id
            db_cash_transaction_row.terminal_id = self.__terminal_id
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S.000001")
            db_cash_transaction_row.creation = dt_string
            db_cash_transaction_row.owner = self.__ui.user_id
            db_cash_transaction_row.approved_by = self.__approved_by
            
            self.__db_cash_transaction_table.create_row(db_cash_transaction_row)

            if not self.__transaction_denomination_dict:
                self.__transaction_denomination_dict['None'] = int(float(self.__transaction_amount))

            for denomination, count in self.__transaction_denomination_dict.items():
                if int(count) > 0:
                    db_cash_transaction_denomination_row = self.__db_cash_transaction_denomination_table.new_row()
                    db_cash_transaction_denomination_row.name = str(cash_transaction_number) + denomination
                    db_cash_transaction_denomination_row.parent = str(cash_transaction_number)
                    db_cash_transaction_denomination_row.denomination = denomination
                    db_cash_transaction_denomination_row.count = count
                    self.__db_cash_transaction_denomination_table.create_row(db_cash_transaction_denomination_row)

            self.__db_session.commit()

    def update_change(self):
        if float(self.__change_amount) > 0:
            db_query = DbQuery(self.__db_conn, 'SELECT nextval("CHANGE_TRANSACTION_REFERENCE")')
            for db_row in db_query.result:
                transaction_reference = db_row[0]

            db_query = DbQuery(self.__db_conn, 'SELECT nextval("CASH_TRANSACTION_ENTRY")')
            for db_row in db_query.result:
                cash_transaction_number = db_row[0]

            db_cash_transaction_row = self.__db_cash_transaction_table.new_row()

            db_cash_transaction_row.name = cash_transaction_number
            db_cash_transaction_row.transaction_type = 'Receipt'
            db_cash_transaction_row.transaction_context = 'Change'
            db_cash_transaction_row.transaction_reference = transaction_reference
            db_cash_transaction_row.transaction_date = self.__ui.current_date
            db_cash_transaction_row.receipt_amount = self.__change_amount
            db_cash_transaction_row.payment_amount = 0
            
            db_cash_transaction_row.party_type = 'User'
            db_cash_transaction_row.customer = self.__ui.user_id
            db_cash_transaction_row.branch_id = self.__branch_id
            db_cash_transaction_row.terminal_id = self.__terminal_id
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S.000001")
            db_cash_transaction_row.creation = dt_string
            db_cash_transaction_row.owner = self.__ui.user_id
            db_cash_transaction_row.approved_by = self.__ui.user_id
            
            self.__db_cash_transaction_table.create_row(db_cash_transaction_row)

            if not self.__from_denomination_dict:
                self.__from_denomination_dict['None'] = int(float(self.__change_amount))

            for denomination, count in self.__from_denomination_dict.items():
                if int(count) > 0:
                    db_cash_transaction_denomination_row = self.__db_cash_transaction_denomination_table.new_row()
                    db_cash_transaction_denomination_row.name = str(cash_transaction_number) + denomination
                    db_cash_transaction_denomination_row.parent = str(cash_transaction_number)
                    db_cash_transaction_denomination_row.denomination = denomination
                    if denomination == 'None':
                        db_cash_transaction_denomination_row.count = float(count)
                    else:
                        db_cash_transaction_denomination_row.count = int(count)
                    self.__db_cash_transaction_denomination_table.create_row(db_cash_transaction_denomination_row)


            db_query = DbQuery(self.__db_conn, 'SELECT nextval("CASH_TRANSACTION_ENTRY")')
            for db_row in db_query.result:
                cash_transaction_number = db_row[0]

            db_cash_transaction_row = self.__db_cash_transaction_table.new_row()

            db_cash_transaction_row.name = cash_transaction_number
            db_cash_transaction_row.transaction_type = 'Payment'
            db_cash_transaction_row.transaction_context = 'Change'
            db_cash_transaction_row.transaction_reference = transaction_reference
            db_cash_transaction_row.transaction_date = self.__ui.current_date
            db_cash_transaction_row.payment_amount = self.__change_amount
            db_cash_transaction_row.receipt_amount = 0
            
            db_cash_transaction_row.party_type = 'User'
            db_cash_transaction_row.customer = self.__ui.user_id
            db_cash_transaction_row.branch_id = self.__branch_id
            db_cash_transaction_row.terminal_id = self.__terminal_id
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S.000001")
            db_cash_transaction_row.creation = dt_string
            db_cash_transaction_row.owner = self.__ui.user_id
            db_cash_transaction_row.approved_by = self.__ui.user_id
            
            self.__db_cash_transaction_table.create_row(db_cash_transaction_row)

            if not self.__to_denomination_dict:
                self.__to_denomination_dict['None'] = int(float(self.__change_amount)) 

            for denomination, count in self.__to_denomination_dict.items():
                if int(count) > 0:
                    db_cash_transaction_denomination_row = self.__db_cash_transaction_denomination_table.new_row()
                    db_cash_transaction_denomination_row.name = str(cash_transaction_number) + denomination
                    db_cash_transaction_denomination_row.parent = str(cash_transaction_number)
                    db_cash_transaction_denomination_row.denomination = denomination
                    if denomination == 'None':
                        db_cash_transaction_denomination_row.count = float(count)
                    else:
                        db_cash_transaction_denomination_row.count = int(count)
                    self.__db_cash_transaction_denomination_table.create_row(db_cash_transaction_denomination_row)

            self.__db_session.commit()


class DrawerTrn:

    def __init__(self, transaction_type):
        self.__kb = Controller()
        
        self.__transaction_type = transaction_type
        self.__transaction_amount = 0.00
        self.__approved_by = ''
 
        self.__db_conn = DbConn()
        self.__db_cash_transaction_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabCash_Transaction)
        self.__db_cash_transaction_denomination_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabCash_Transaction_Denomination)
 
        self.__canvas = DrawerTrnCanvas(transaction_type)
        
        self.__window = sg.Window(transaction_type, 
                        self.__canvas.layout, 
                        location=(300,250), 
                        size=(400,250), 
                        modal=True, 
                        finalize=True,
                        keep_on_top = True,
                        icon='images/favicon.ico',
                        return_keyboard_events=True,
                    )

        self.__ui = DrawerTrnUi(self.__window)

        self.__ui.transaction_type = transaction_type
        self.__transaction_denomination_dict = dict()
        
        self.handler()
        
    def handler(self):
        prev_event = '' 
        focus = None
        while True:
            event, values = self.__window.read()
            #print('drawer_trn_popup=', event, values)
            
            if self.__window.FindElementWithFocus():
                focus = self.__window.FindElementWithFocus().Key
            #print('drawer_trn=', event, 'prev=', prev_event, 'focus:', focus)
                            
            if event == '_KEYPAD_':
                result = self.keypad(self.__ui.transaction_amount)
                self.__ui.transaction_amount = result
                self.__ui.transaction_amount_f = self.__ui.transaction_amount
                self.__ui.focus_transaction_amount()

            if event == '_CASH_DENOMINATION_':
                if not self.__ui.transaction_amount.replace('.','').isdigit():
                    self.__ui.transaction_amount = 0.00
                    self.__ui.focus_transaction_amount()
                    continue
                    
                if float(self.__ui.transaction_amount) > 0:
                    default_amount_dict = dict()
                    default_amount_dict['None'] = self.__ui.transaction_amount
                    self.__transaction_denomination_dict = self.denomination(default_amount_dict, 'edit')

            if event == '\t':
                if prev_event == '_TRANSACTION_AMOUNT_':
                    self.__ui.transaction_amount = self.__ui.transaction_amount                    

            if event in ('Exit', '_DRAWER_TRN_ESC_', 'Escape:27', sg.WIN_CLOSED):
                break             
            
            if event in ('_DRAWER_TRN_OK_', 'F12:123', '\r'):
                if self.__ui.transaction_amount == '':
                    sg.popup('Amount cannot be zero', keep_on_top = True, icon='images/INFO.png')                    
                    continue                
                if float(self.__ui.transaction_amount) == 0:
                    sg.popup('Amount cannot be zero', keep_on_top = True, icon='images/INFO.png')                    
                    continue
                if self.__ui.supervisor_user_id == '' or self.__ui.supervisor_passwd == '':
                    sg.popup('User Id & Passwd mandatory', keep_on_top = True, icon='images/INFO.png')                    
                    continue                
                if self.validate_supervisor():
                    self.__transaction_amount = self.__ui.transaction_amount
                    self.__approved_by = self.__ui.supervisor_user_id                 
                    break
                sg.popup('Invalid Authorization', keep_on_top = True, icon='images/INFO.png')                    
                
            prev_event = event

        self.__window.close()

    ######
    # Wrapper function for Keypad
    def keypad(self, current_value):
        keypad = Keypad(current_value)
        return(keypad.input_value)

    ######
    # Wrapper function for Denomination
    def denomination(self, amount, mode):
        denomination = Denomination(amount, mode)
        return denomination.denomination_count_dict    

    def validate_supervisor(self):
        db_query = DbQuery(self.__db_conn, 'select name, DECODE(passwd, "secret") as passwd, role, enabled from tabUser where name = "{}"'.format(self.__ui.supervisor_user_id))
        if  db_query.result:
            for db_row in db_query.result:
                if self.__ui.supervisor_passwd == db_row[1].decode("utf-8"):
                    if db_row[3] == 1:
                        if db_row[2] == 'Alignpos Manager':
                            return True   
        return False
        
    def set_transaction_amount(self, transaction_amount):
        self.__transaction_amount = transaction_amount
        
    def get_transaction_amount(self):
        return self.__transaction_amount

    def get_transaction_denomination_dict(self):
        return self.__transaction_denomination_dict

    def get_approved_by(self):
        return self.__approved_by

    transaction_amount = property(get_transaction_amount, set_transaction_amount)
    transaction_denomination_dict = property(get_transaction_denomination_dict)
    approved_by = property(get_approved_by)


class DrawerChange:

    def __init__(self):
        self.__kb = Controller()
        
        self.__exchange_amount = 0.00
 
        self.__db_conn = DbConn()
        self.__db_cash_transaction_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabCash_Transaction)
        self.__db_cash_transaction_denomination_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabCash_Transaction_Denomination)
 
        self.__canvas = DrawerChangeCanvas()
        
        self.__window = sg.Window('Cash Change',
                        self.__canvas.layout, 
                        location=(300,250), 
                        size=(450,220), 
                        modal=True, 
                        finalize=True,
                        keep_on_top = True,
                        icon='images/favicon.ico',
                        return_keyboard_events=True,
                    )

        self.__ui = DrawerChangeUi(self.__window)

        self.__from_denomination_dict = dict()
        self.__to_denomination_dict = dict()
        
        self.handler()
        
    def handler(self):
        prev_event = '' 
        focus = None
        while True:
            event, values = self.__window.read()
            #print('drawer_change_popup=', event, values)
            
            if self.__window.FindElementWithFocus():
                focus = self.__window.FindElementWithFocus().Key
            #print('drawer_change=', event, 'prev=', prev_event, 'focus:', focus)
                            
            if event == '_KEYPAD_':
                result = self.keypad(self.__ui.change_amount)
                self.__ui.change_amount = result
                self.__ui.change_amount = self.__ui.change_amount
                self.__ui.focus_change_amount()

            if event == '_FROM_DENOMINATION_':
                if not self.__ui.change_amount.replace('.','').isdigit():
                    self.__ui.change_amount = 0.00
                    self.__ui.focus_change_amount()
                    continue
                    
                if float(self.__ui.change_amount) > 0:
                    default_amount_dict = dict()
                    default_amount_dict['None'] = self.__ui.change_amount
                    self.__from_denomination_dict = self.denomination(default_amount_dict, 'edit')
                    self.__ui.change_amount = self.__ui.change_amount
                    self.__ui.focus_change_amount()

            if event == '_TO_DENOMINATION_':
                if not self.__ui.change_amount.replace('.','').isdigit():
                    self.__ui.change_amount = 0.00
                    self.__ui.focus_change_amount()
                    continue
                    
                if float(self.__ui.change_amount) > 0:
                    default_amount_dict = dict()
                    default_amount_dict['None'] = self.__ui.change_amount
                    self.__to_denomination_dict = self.denomination(default_amount_dict, 'edit')
                    self.__ui.change_amount = self.__ui.change_amount
                    self.__ui.focus_change_amount()

            if event == '\t':
                if prev_event == '_EXCHANGE_AMOUNT_':
                    self.__ui.change_amount = self.__ui.change_amount
                    self.__ui.focus_change_amount()

            if event in ('Exit', '_DRAWER_CHANGE_ESC_', 'Escape:27', sg.WIN_CLOSED):
                break             
            
            if event in ('_DRAWER_CHANGE_OK_', 'F12:123', '\r'):
                if not self.__from_denomination_dict:
                    self.__from_denomination_dict['None'] = int(float(self.__ui.change_amount))
                    
                if not self.__to_denomination_dict:
                    self.__to_denomination_dict['None'] = int(float(self.__ui.change_amount))

                if self.__ui.change_amount == '':
                    sg.popup('Amount cannot be zero', keep_on_top = True, icon='images/INFO.png')                    
                    continue                

                if float(self.__ui.change_amount) == 0:
                    sg.popup('Amount cannot be zero', keep_on_top = True, icon='images/INFO.png')                    
                    continue
                    
                if self.__from_denomination_dict == self.__to_denomination_dict:
                    sg.popup('Receipt and Payment cannot have same denominations', keep_on_top = True, icon='images/INFO.png')                    
                    continue
                    
                self.__change_amount = self.__ui.change_amount
                break                

            prev_event = event

        self.__window.close()

    ######
    # Wrapper function for Keypad
    def keypad(self, current_value):
        keypad = Keypad(current_value)
        return(keypad.input_value)

    ######
    # Wrapper function for Denomination
    def denomination(self, amount, mode):
        denomination = Denomination(amount, mode)
        return denomination.denomination_count_dict    
       
    def set_change_amount(self, change_amount):
        self.__change_amount = change_amount
        
    def get_change_amount(self):
        return self.__change_amount

    def get_from_denomination_dict(self):
        return self.__from_denomination_dict

    def get_to_denomination_dict(self):
        return self.__to_denomination_dict

    change_amount = property(get_change_amount, set_change_amount)
    from_denomination_dict = property(get_from_denomination_dict)
    to_denomination_dict = property(get_to_denomination_dict)

