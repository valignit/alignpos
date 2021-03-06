import os
import PySimpleGUI as sg
import json
from pynput.keyboard import Key, Controller

from config import Config
from utilities import Message, Keypad
from db_orm import DbConn, DbTable, DbQuery
from db_nosql import KvDatabase

from common_layout import SigninCanvas, ItemListCanvas, CustomerListCanvas, DenominationCanvas
from common_ui import SigninUi, ItemListUi, CustomerListUi, DenominationUi

sg.theme('DefaultNoMoreNagging')


class Signin():
    
    def __init__(self):
        config = Config()
        
        self.__terminal_id = config.terminal_id
        self.__branch_id = config.branch_id
        self.__language = config.language

        self.__kv_settings = KvDatabase('kv_settings')
        self.__current_date = self.__kv_settings.get('current_date')
        self.__current_status = self.__kv_settings.get('current_status')
       
        self.__canvas = SigninCanvas()

        self.__window = sg.Window(self.__canvas.title, 
                        self.__canvas.layout,
                        background_color = 'White',
                        keep_on_top = True, 
                        return_keyboard_events = True, 
                        modal=True, 
                        icon='c:/alignpos/images/favicon.ico',
                        finalize=True,                  
                        text_justification = self.__canvas.justification,
                        element_justification = self.__canvas.justification
                    )

        self.__ui = SigninUi(self.__window)

        self.__db_conn = DbConn()
        self.__db_session = self.__db_conn.session
        
        self.__db_user_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabUser)        

        self.__window.bind('<FocusIn>', '+FOCUS IN+')
        self.__window.bind('<FocusOut>', '+FOCUS OUT+')

        self.__window["_OK_"].Widget.config(takefocus=0) 
        self.__window["_CANCEL_"].Widget.config(takefocus=0)

        self.__type = type
        self.__ok = False

        self.__ui.signin_terminal_id = self.__terminal_id
        self.__ui.signin_branch_id = self.__branch_id
        self.__ui.focus_signin_user_id()
        
        self.handler()

    def handler(self):
        if self.__type == 'OK':
            self.__window.Element("_CANCEL_").update(visible=False)
        else:
            self.__window.Element("_CANCEL_").update(visible=True)

        while True:
            event, values = self.__window.read()
            #print('signin:', event, values)

            ### following code will be removed later
            if event in ('F1', 'F1:112'):
                self.__ui.signin_user_id = 'administrator'
                self.__ui.signin_passwd = 'welcome'              
                if self.validate_user():
                    self.__ok = True
                    break              
            ###
            
            if event in ('_OK_', '\r'):
                if self.validate_user():
                    self.__ok = True
                    break              
            
            if event in ('Escape:27', '_CANCEL_', sg.WIN_CLOSED):
                self.__ok = False
                break
                
        self.__window.close()

    def validate_user(self):
        db_query = DbQuery(self.__db_conn, 'select name, DECODE(passwd, "secret") as passwd, role, enabled from tabUser where name = "{}"'.format(self.__ui.signin_user_id))
        if  db_query.result:
            for db_row in db_query.result:
                if self.__ui.signin_passwd == db_row[1].decode("utf-8"):
                    if db_row[3] == 1:
                        self.__ui.signin_role = db_row[2]
                        return True
                    else:
                        message = '???????????? ?????? ??????' if self.__language == 'ar' else 'Inactive User'
                        Message('STOP', message)
                        self.__ui.focus_signin_user_id()
                        return False                                   
                else:
                    message = '???????? ???????????? ?????? ??????????????' if self.__language == 'ar' else 'Password mismatch'
                    Message('STOP', message)
                    self.__ui.focus_signin_passwd()
                    return False
            else:
                message = '?????? ???????????????? ?????? ????????' if self.__language == 'ar' else 'Invalid User'
                Message('STOP', message)
                self.__ui.focus_signin_user_id()
                return False           
        else:
            message = '?????? ???????????????? ?????? ????????' if self.__language == 'ar' else 'Invalid User'
            Message('STOP', message)
            self.__ui.focus_signin_user_id()
            return False
   
    def get_ok(self):
        return self.__ok

    def get_sign_in_user_id(self):
        return self.__ui.signin_user_id
 
    def get_sign_in_terminal_id(self):
        return self.__ui.signin_terminal_id

    def get_sign_in_branch_id(self):
        return self.__ui.signin_branch_id

    def get_current_date(self):
        return self.__current_date

    def get_current_status(self):
        return self.__current_status
 
    def get_sign_in_role(self):
        return self.__ui.signin_role
 
    ok = property(get_ok)         
    user_id = property(get_sign_in_user_id)         
    terminal_id = property(get_sign_in_terminal_id)         
    branch_id = property(get_sign_in_branch_id)         
    current_date = property(get_current_date)         
    current_status = property(get_current_status)         
    role = property(get_sign_in_role)         

    
class ItemList:
    def __init__(self, filter):    
        self.__item_code = ''

        self.__db_conn = DbConn()

        db_item_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabItem)
        
        self.__filter=filter
        db_item_cursor = db_item_table.list(filter)

        if (len(db_item_cursor) == 0):
            sg.popup('Item(s) not found', keep_on_top = True, icon='images/INFO.png')
            return
       
        kb = Controller()
        self.__kb = kb
        
        self.__canvas = ItemListCanvas()
        self.__window = sg.Window("List Item",
                        self.__canvas.layout,
                        location=(300,250), 
                        size=(495,200), 
                        modal=True, 
                        finalize=True,
                        return_keyboard_events=True,
                        no_titlebar = False,
                        icon='images/favicon.ico',
                        keep_on_top = True,                    
                    )
    
        self.__ui = ItemListUi(self.__window)
        
        self.__ui.items_list = []

        for db_item_row in db_item_cursor:
            self.__ui.item_code = db_item_row.item_code
            self.__ui.item_name = db_item_row.item_name
            self.__ui.stock = db_item_row.stock
            self.__ui.selling_price = db_item_row.standard_selling_price
            self.__ui.add_item_line()

        self.__ui.item_idx = 0
        self.__ui.focus_items_list()
        
        self.handler()

    def handler(self):  
        prev_event = ''    
        prev_values = ''    
        item_idx  = 0    
        while True:
            event, values = self.__window.read()
                
            if event in ("Exit", '_ITEM_LIST_ESC_', 'Escape:27') or event == sg.WIN_CLOSED:
                break

            if event == '\r':
                # Cancelling the unwanted initial Enter key event passed from the previous window                 
                continue
                
            if event in ('_ITEM_LIST_OK_', 'F12', 'F12:123'):
                item_idx = values['_ITEMS_LIST_'][0]
                self.__ui.item_line_to_elements(item_idx)
                self.__item_code = self.__ui.item_code
                break

            if event == prev_event and values == prev_values:
                item_idx = values['_ITEMS_LIST_'][0]
                self.__ui.item_line_to_elements(item_idx)
                self.__item_code = self.__ui.item_code
                break
            
            if event not in ('\t', 'Up:38', 'Down:40', 'UP', 'DOWN'):               
                prev_event = event
            prev_values = values
            
        self.__db_conn.close()           
        self.__window.close()    
     
    def get_item_code(self):
        return self.__item_code

    
    item_code = property(get_item_code)


class CustomerList:
    def __init__(self):    
        self.__customer_number = ''
        self.__mobile_number = ''

        self.__db_conn = DbConn()

        db_customer_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabCustomer)
        filter=''
        db_customer_cursor = db_customer_table.list(filter)

        if (len(db_customer_cursor) == 0):
            sg.popup('Customer(s) not found', keep_on_top = True, icon='images/INFO.png')                    
            return
       
        kb = Controller()
        self.__kb = kb
        
        self.__canvas = CustomerListCanvas()
        self.__window = sg.Window("List Customer",
                        self.__canvas.layout,
                        location=(100,100), 
                        size=(800,360), 
                        modal=True, 
                        finalize=True,
                        return_keyboard_events=True, 
                        icon='images/favicon.ico',
                        keep_on_top = True,                    
                    )
    
        self.__ui = CustomerListUi(self.__window)
                
        self.__ui.customers_list = []

        self.__base_query = 'select tabCustomer.name, \
        tabCustomer.mobile_number, \
        tabCustomer.customer_name, \
        tabCustomer.customer_type, \
        tabCustomer.customer_group \
        from tabCustomer \
        where tabCustomer.name = tabCustomer.name'
        
        db_query = DbQuery(self.__db_conn, self.__base_query)        
        if  db_query.result:
            self.__ui.customers_list = []                        
            for db_row in db_query.result:
                self.__ui.customer_number = db_row[0]
                self.__ui.mobile_number = db_row[1]
                self.__ui.customer_name = db_row[2]
                self.__ui.customer_type = db_row[3]
                self.__ui.customer_group = db_row[4]
                self.__ui.add_customer_line()

        self.__ui.customer_idx = 0
        self.__ui.focus_customers_list()
       
        self.handler()


    def handler(self):  
        prev_event = ''
        prev_values = ''
        
        while True:
            event, values = self.__window.read()
            #print('customer_list=', event, prev_event, values)
            if event in ("Exit", '_CUSTOMER_LIST_ESC_', 'Escape:27') or event == sg.WIN_CLOSED:
                break

            if event in ('_CUSTOMER_LIST_SEARCH_', 'F11', 'F11:122'):
                this_query = ''
                if self.__ui.customer_number_search:
                    if not self.__ui.customer_number_search == '':
                        this_query = ' and tabCustomer.name = "' + self.__ui.customer_number_search + '"'
                if self.__ui.mobile_number_search:
                    if not self.__ui.mobile_number_search == '':
                        this_query = ' and tabCustomer.mobile_number = "' + self.__ui.mobile_number_search + '"'
                db_query = DbQuery(self.__db_conn, self.__base_query + this_query)        
                if  db_query.result:
                    self.__ui.customers_list = []                        
                    for db_row in db_query.result:
                        self.__ui.customer_number = db_row[0]
                        self.__ui.mobile_number = db_row[1]
                        self.__ui.customer_name = db_row[2]
                        self.__ui.customer_type = db_row[3]
                        self.__ui.customer_group = db_row[4]
                        self.__ui.add_customer_line()

            if event in ('_CUSTOMER_LIST_OK_', '\r', 'F12', 'F12:123'):
                customer_idx = values['_CUSTOMERS_LIST_'][0]
                self.__ui.customer_line_to_elements(customer_idx)
                self.__customer_number = self.__ui.customer_number
                self.__mobile_number = self.__ui.mobile_number
                break
            
            if event == prev_event and values == prev_values:
                customer_idx = values['_CUSTOMERS_LIST_'][0]
                self.__ui.customer_line_to_elements(customer_idx)
                self.__customer_number = self.__ui.customer_number
                self.__mobile_number = self.__ui.mobile_number
                break
            
            if event not in ('\t', 'Up:38', 'Down:40', 'UP', 'DOWN'):               
                prev_event = event
            prev_values = values
           
        self.__db_conn.close()           
        self.__window.close()    

      
    def get_customer_number(self):
        return self.__customer_number

    def get_mobile_number(self):
        return self.__mobile_number

    
    customer_number = property(get_customer_number)
    mobile_number = property(get_mobile_number)


class Denomination:
    def __init__(self, payment_amount, mode):
        self.__payment_amount = payment_amount
        self.__mode = mode

        self.__denomination_name = ''
        self.__denomination_count = ''

        self.__db_conn = DbConn()

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

        self.__canvas = DenominationCanvas(self.__denomination_list, self.__mode)
        self.__window = sg.Window("Denomination",
                        self.__canvas.layout,
                        location=(100,100), 
                        size=(280,400), 
                        modal=True,
                        finalize=True,
                        return_keyboard_events=True, 
                        icon='images/favicon.ico',
                        keep_on_top = True,                    
                    )
    
        self.__ui = DenominationUi(self.__window, self.__denomination_list)
        idx = 0
        self.__total_amount = 0
        for denomination in self.__denomination_list:
            self.__ui.denomination_name = denomination
            if denomination in self.__payment_amount:
                self.__ui.denomination_count = int(float(self.__payment_amount[denomination]))
                self.__ui.denomination_amount = float(self.__denomination_value_list[idx])  * float(self.__ui.denomination_count)
                self.__total_amount += float(self.__ui.denomination_amount)
            idx += 1
        
        self.__ui.focus_denomination_count() 
        
        self.handler()
        
        self.__denomination_count_dict = dict()
        
        self.set_return_value()
        

    def handler(self):  
        prev_event = ''
        prev_values = ''
        
        while True:
            event, values = self.__window.read()
            #print('denomination=', event, prev_event, values)

            if event in ('_DENOMINATION_ESC_', 'Exit', 'Escape:27') or event == sg.WIN_CLOSED:
                break

            if event in ('_DENOMINATION_OK_', '\r', 'F12', 'F12:123'):
                total_amount = 0.00
                for denomination in self.__denomination_list:
                    self.__ui.denomination_name = denomination
                    total_amount += float(self.__ui.denomination_amount)
                    
                if float(total_amount) != float(self.__total_amount):
                    #Message('INFO', 'Denomination amount mismatch ' + str(total_amount))
                    self.__ui.focus_denomination_count()      
                    continue
                    
                break
                
            idx = 0
            for denomination in self.__denomination_list:
                if event == denomination + '_count':
                    self.__ui.denomination_name = denomination
                    if self.__ui.denomination_count == '':
                        self.__ui.denomination_count = 0
                    self.__ui.denomination_amount = float(self.__denomination_value_list[idx]) * float(self.__ui.denomination_count)
                idx+=1
                
        self.__db_conn.close()           
        self.__window.close()    


    def set_return_value(self):
        for denomination in self.__denomination_list:
            self.__ui.denomination_name = denomination
            self.__denomination_count_dict[self.__ui.denomination_name] = self.__ui.denomination_count
    
    def get_denomination_count_dict(self):
        return self.__denomination_count_dict

    denomination_count_dict = property(get_denomination_count_dict)
    
        

    