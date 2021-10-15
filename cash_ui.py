import datetime
import PySimpleGUI as sg


###
class CashUi:
    def __init__(self, window, denomination_list):
        self.__window = window

        self.__transaction_type_search = ''
        self.__transaction_context_search = ''

        self.__cashs_list = []
        self.__cash_line = []
        self.__cash_idx = 0
        self.__name = ''
        self.__transaction_type = ''
        self.__transaction_context = ''
        self.__transaction_reference = ''
        self.__transaction_date = 0.00
        self.__receipt_amount = 0.00
        self.__payment_amount = 0.00
        
        self.__user_id = ''
        self.__terminal_id = ''
        self.__branch_id = ''
        self.__current_date = datetime.datetime(1900, 1, 1)

        self.__denomination_list = denomination_list
        self.__denomination_name = ''
        self.__denomination_count = 0
        self.__denomination_amount = 0.00

        self.__received_amount = 0.00
        self.__paid_amount = 0.00
        self.__balance_amount = 0.00

        for denomination in denomination_list:
            self.__window[denomination + '_count'].Widget.config(takefocus=0)
            self.__window[denomination + '_amount'].Widget.config(takefocus=0)
            self.__window.Element(denomination + '_count').update(value = 0)
            self.__window.Element(denomination + '_amount').update(value = 0.00)

        self.__window["_CASH_LIST_RECEIPT_"].Widget.config(takefocus=0)
        self.__window["_CASH_LIST_PAYMENT_"].Widget.config(takefocus=0)
        self.__window["_CASH_LIST_DENOMINATION_"].Widget.config(takefocus=0)
        self.__window["_CASH_LIST_ESC_"].Widget.config(takefocus=0)
        self.__window["_CASH_LIST_SEARCH_"].Widget.config(takefocus=0)
        self.__window['_LEFT_PANES_'].Widget.configure(borderwidth=1, relief=sg.DEFAULT_FRAME_RELIEF)
        self.__window['_RIGHT_PANES_'].Widget.configure(borderwidth=1, relief=sg.DEFAULT_FRAME_RELIEF)

        self.__window['_USER_ID_'].Widget.config(takefocus=0)
        self.__window['_TERMINAL_ID_'].Widget.config(takefocus=0)
        self.__window['_BRANCH_ID_'].Widget.config(takefocus=0)
        self.__window['_CURRENT_DATE_'].Widget.config(takefocus=0)
        
        self.__window['_RECEIVED_AMOUNT_'].Widget.config(takefocus=0)
        self.__window['_PAID_AMOUNT_'].Widget.config(takefocus=0)
        self.__window['_BALANCE_AMOUNT_'].Widget.config(takefocus=0)


    # Setters and Getters
    def set_transaction_type_search(self, transaction_type_search):
        self.__transaction_type_search = transaction_type_search
        self.__window.Element('_TRANSACTION_TYPE_SEARCH_').update(value = self.__transaction_type_search)
        
    def get_transaction_type_search(self):
        self.__transaction_type_search = self.__window.Element('_TRANSACTION_TYPE_SEARCH_').get()        
        return self.__transaction_type_search
        
    def set_transaction_context_search(self, transaction_context_search):
        self.__transaction_context_search = transaction_context_search
        self.__window.Element('_TRANSACTION_CONTEXT_SEARCH_').update(value = self.__transaction_context_search)
        
    def get_transaction_context_search(self):
        self.__transaction_context_search = self.__window.Element('_TRANSACTION_CONTEXT_SEARCH_').get()        
        return self.__transaction_context_search
        
    def set_cashs_list(self, cashs_list):
        self.__cashs_list = cashs_list
        self.__window.Element('_CASH_LIST_').update(values = self.__cashs_list)
        
    def get_cashs_list(self):
        self.__cashs_list = self.__window.Element('_CASH_LIST_').get()
        return self.__cashs_list
              
    def set_cash_line(self, cash_line):
        self.__cash_line = cash_line
        
    def get_cash_line(self):
        self.__cash_line = self.__cashs_list[self.__cash_idx]
        return self.__cash_line
    
    def set_name(self, name):
        self.__name = name
        
    def get_name(self):
        return self.__name
        
    def set_transaction_type(self, transaction_type):
        self.__transaction_type = transaction_type
        
    def get_transaction_type(self):
        return self.__transaction_type
        
    def set_transaction_context(self, transaction_context):
        self.__transaction_context = transaction_context
        
    def get_transaction_context(self):
        return self.__transaction_context
        
    def set_transaction_reference(self, transaction_reference):
        self.__transaction_reference = transaction_reference
        
    def get_transaction_reference(self):
        return self.__transaction_reference

    def set_transaction_date(self, transaction_date):
        self.__transaction_date = transaction_date
        
    def get_transaction_date(self):
        return self.__transaction_date

    def set_receipt_amount(self, receipt_amount):
        self.__receipt_amount = receipt_amount
        
    def get_receipt_amount(self):
        return self.__receipt_amount

    def set_payment_amount(self, payment_amount):
        self.__payment_amount = payment_amount
        
    def get_payment_amount(self):
        return self.__payment_amount

    def set_cash_idx(self, cash_idx):
        self.__cash_idx = cash_idx
        
    def get_cash_idx(self):
        return self.__cash_idx  

    def set_user_id(self, user_id):
        self.__user_id = user_id
        self.__window.Element('_USER_ID_').update(value = self.__user_id)
        
    def get_user_id(self):
        self.__user_id = self.__window.Element('_USER_ID_').get()
        return self.__user_id
        
    def set_terminal_id(self, terminal_id):
        self.__terminal_id = terminal_id
        self.__window.Element('_TERMINAL_ID_').update(value = self.__terminal_id)        
        
    def get_terminal_id(self):
        self.__terminal_id = self.__window.Element('_TERMINAL_ID_').get()    
        return self.__terminal_id
        
    def set_branch_id(self, branch_id):
        self.__branch_id = branch_id
        self.__window.Element('_BRANCH_ID_').update(value = self.__branch_id)        
        
    def get_branch_id(self):
        self.__branch_id = self.__window.Element('_BRANCH_ID_').get()    
        return self.__branch_id
        
    def set_current_date(self, current_date):
        self.__current_date = current_date
        self.__window.Element('_CURRENT_DATE_').update(value = self.__current_date)        
        
    def get_current_date(self):
        self.__current_date = self.__window.Element('_CURRENT_DATE_').get()        
        return self.__current_date

    def set_denomination_name(self, denomination_name):
        self.__denomination_name = denomination_name
        
    def get_denomination_name(self):
        return self.__denomination_name
        
    def set_denomination_count(self, denomination_count):
        self.__denomination_count = denomination_count
        self.__window.Element(self.__denomination_name + '_count').update(value = self.__denomination_count)
        
    def get_denomination_count(self):
        self.__denomination_count = self.__window.Element(self.__denomination_name + '_count').get()        
        return self.__denomination_count
               
    def set_denomination_amount(self, denomination_amount):
        self.__denomination_amount = denomination_amount
        self.__window.Element(self.__denomination_name + '_amount').update(value = "{:.2f}".format(self.__denomination_amount))
        
    def get_denomination_amount(self):
        self.__denomination_amount = self.__window.Element(self.__denomination_name + '_amount').get()        
        return self.__denomination_amount
               
    def set_received_amount(self, received_amount):
        self.__received_amount = received_amount
        self.__window.Element('_RECEIVED_AMOUNT_').update(value = "{:.2f}".format(self.__received_amount))
        
    def get_received_amount(self):
        self.__received_amount = self.__window.Element('_RECEIVED_AMOUNT_').get()        
        return self.__received_amount
               
    def set_paid_amount(self, paid_amount):
        self.__paid_amount = paid_amount
        self.__window.Element('_PAID_AMOUNT_').update(value = "{:.2f}".format(self.__paid_amount))
        
    def get_paid_amount(self):
        self.__paid_amount = self.__window.Element('_PAID_AMOUNT_').get()        
        return self.__paid_amount
               
    def set_balance_amount(self, balance_amount):
        self.__balance_amount = balance_amount
        self.__window.Element('_BALANCE_AMOUNT_').update(value = "{:.2f}".format(self.__balance_amount))
        
    def get_balance_amount(self):
        self.__balance_amount = self.__window.Element('_BALANCE_AMOUNT_').get()        
        return self.__balance_amount
               
               
    # Focus
    
    def focus_transaction_type_search(self):
        self.__window.Element('_TRANSACTION_TYPE_SEARCH_').set_focus(force = True)

    def focus_cash_list(self):
        self.__window['_CASH_LIST_'].Widget.config(takefocus=1)
        self.__window.Element('_CASH_LIST_').set_focus(force = True)        
        if len(self.__cashs_list) > 0:        
            table_row = self.__window['_CASH_LIST_'].Widget.get_children()[0]
            self.__window['_CASH_LIST_'].Widget.selection_set(table_row)  # move selection
            self.__window['_CASH_LIST_'].Widget.focus(table_row)  # move focus
            self.__window['_CASH_LIST_'].Widget.see(table_row)  # scroll to show i

    def focus_cash_list_row(self, idx):
        self.__window['_CASH_LIST_'].Widget.config(takefocus=1)
        self.__window.Element('_CASH_LIST_').set_focus(force = True)
        table_row = self.__window['_CASH_LIST_'].Widget.get_children()[idx]
        self.__window['_CASH_LIST_'].Widget.selection_set(table_row)  # move selection
        self.__window['_CASH_LIST_'].Widget.focus(table_row)  # move focus
        self.__window['_CASH_LIST_'].Widget.see(table_row)  # scroll to show i

    def focus_denomination_count(self):
        self.__window.Element(self.__denomination_name + '_count').SetFocus()
        self.__window.Element(self.__denomination_name + '_count').update(select=True)        
    
    def clear_ui_cash_list(self):
        self.__ui_cashs_list.clear()
        self.__window.Element('_CASH_LIST_').update(values = self.__ui_cashs_list)

    def elements_to_cash_line(self):
        self.__cash_line.append(self.__name)        
        self.__cash_line.append(self.__transaction_type)
        self.__cash_line.append(self.__transaction_context)        
        self.__cash_line.append(self.__transaction_reference)
        self.__cash_line.append(self.__transaction_date)                
        self.__cash_line.append("{:.2f}".format(float(self.__receipt_amount)))        
        self.__cash_line.append("{:.2f}".format(float(self.__payment_amount)))        

       
    def cash_line_to_elements(self, idx):
        self.__cash_line = self.__cashs_list[idx]
        self.__name = self.__cash_line[0]
        self.__transaction_type = self.__cash_line[1]
        self.__transaction_context = self.__cash_line[2]
        self.__transaction_reference = self.__cash_line[3]
        self.__transaction_date = self.__cash_line[4]
        self.__receipt_amount = self.__cash_line[5]
        self.__payment_amount = self.__cash_line[6]

    def add_cash_line(self):
        self.__cash_line = []
        self.elements_to_cash_line()    
        self.__cashs_list.append(self.__cash_line)
        self.__window.Element('_CASH_LIST_').update(values = self.__cashs_list)

    # Properties   
    cashs_list = property(get_cashs_list, set_cashs_list)
    cash_line = property(get_cash_line, set_cash_line)
    cash_idx = property(get_cash_idx, set_cash_idx)
    transaction_type_search = property(get_transaction_type_search, set_transaction_type_search)
    transaction_context_search = property(get_transaction_context_search, set_transaction_context_search)
    name = property(get_name, set_name)
    transaction_type = property(get_transaction_type, set_transaction_type)
    transaction_context = property(get_transaction_context, set_transaction_context)
    transaction_reference = property(get_transaction_reference, set_transaction_reference)
    transaction_date = property(get_transaction_date, set_transaction_date)
    receipt_amount = property(get_receipt_amount, set_receipt_amount)
    payment_amount = property(get_payment_amount, set_payment_amount)
    user_id = property(get_user_id, set_user_id) 
    terminal_id = property(get_terminal_id, set_terminal_id)
    branch_id = property(get_branch_id, set_branch_id)
    current_date = property(get_current_date, set_current_date)
    denomination_name = property(get_denomination_name, set_denomination_name)     
    denomination_count = property(get_denomination_count, set_denomination_count)     
    denomination_amount = property(get_denomination_amount, set_denomination_amount)     
    received_amount = property(get_received_amount, set_received_amount)
    paid_amount = property(get_paid_amount, set_paid_amount)
    balance_amount = property(get_balance_amount, set_balance_amount)

 
class DrawerTrnUi:
    def __init__(self, popup):
        self.__popup = popup
        self.__item_name = ''
        self.__supervisor_user_id = ''
        self.__supervisor_passwd = ''

        self.__popup["_TRANSACTION_TYPE_"].Widget.config(takefocus=0)
        self.__popup["_DRAWER_TRN_OK_"].Widget.config(takefocus=0) 
        self.__popup["_DRAWER_TRN_ESC_"].Widget.config(takefocus=0)
        self.__popup["_KEYPAD_"].Widget.config(takefocus=0)
        self.__popup["_CASH_DENOMINATION_"].Widget.config(takefocus=0)
       
        #self.__popup['_DRAWER_TRN_'].Widget.configure(borderwidth=1, relief=sg.DEFAULT_FRAME_RELIEF)
        
    def set_transaction_type(self, transaction_type):
        self.__transaction_type = transaction_type
        self.__popup.Element('_TRANSACTION_TYPE_').update(value = self.__transaction_type)
        
    def get_transaction_type(self):
        return self.__transaction_type
        
    def set_transaction_amount(self, transaction_amount):
        if transaction_amount == '':
            transaction_amount = 0
        self.__transaction_amount = transaction_amount
        self.__popup.Element('_TRANSACTION_AMOUNT_').update(value = "{:.2f}".format(float(self.__transaction_amount)))
       
    def get_transaction_amount(self):
        self.__transaction_amount = self.__popup.Element('_TRANSACTION_AMOUNT_').get()        
        return self.__transaction_amount

    def set_supervisor_user_id(self, supervisor_user_id):
        self.__supervisor_user_id = supervisor_user_id
        self.__popup.Element('_SUPERVISOR_USER_ID_').update(value = self.__supervisor_user_id)
        
    def get_supervisor_user_id(self):
        self.__supervisor_user_id = self.__popup.Element('_SUPERVISOR_USER_ID_').get()        
        return self.__supervisor_user_id
        
    def set_supervisor_passwd(self, supervisor_passwd):
        self.__supervisor_passwd = supervisor_passwd
        self.__popup.Element('_SUPERVISOR_PASSWD_').update(value = self.__supervisor_passwd)
        
    def get_supervisor_passwd(self):
        self.__supervisor_passwd = self.__popup.Element('_SUPERVISOR_PASSWD_').get()        
        return self.__supervisor_passwd
        
    def focus_transaction_amount(self):
        self.__popup.Element('_TRANSACTION_AMOUNT_').SetFocus() 
        self.__popup.Element('_TRANSACTION_AMOUNT_').update(select=True)        

    def append_char(self, key, char):
        if self.__popup[key].Widget.select_present():
            self.__transaction_amount = ''
            self.__popup.Element(key).update(value = self.__transaction_amount)
        
        self.__transaction_amount = self.__popup.Element('_TRANSACTION_AMOUNT_').get()        
        self.__transaction_amount = str(self.__transaction_amount) + char
        self.__popup.Element(key).update(value = self.__transaction_amount)

    transaction_type = property(get_transaction_type, set_transaction_type)     
    transaction_amount = property(get_transaction_amount, set_transaction_amount) 
    supervisor_user_id = property(get_supervisor_user_id, set_supervisor_user_id)     
    supervisor_passwd = property(get_supervisor_passwd, set_supervisor_passwd)     


class DrawerChangeUi:
    def __init__(self, popup):
        self.__popup = popup
        self.__item_name = ''

        self.__popup["_DRAWER_CHANGE_OK_"].Widget.config(takefocus=0) 
        self.__popup["_DRAWER_CHANGE_ESC_"].Widget.config(takefocus=0)
        self.__popup["_KEYPAD_"].Widget.config(takefocus=0)
        self.__popup["_FROM_DENOMINATION_"].Widget.config(takefocus=0)
        self.__popup["_TO_DENOMINATION_"].Widget.config(takefocus=0)
       
        
    def set_change_amount(self, change_amount):
        if change_amount == '':
            change_amount = 0
        self.__change_amount = change_amount
        self.__popup.Element('_CHANGE_AMOUNT_').update(value = "{:.2f}".format(float(self.__change_amount)))
       
    def get_change_amount(self):
        self.__change_amount = self.__popup.Element('_CHANGE_AMOUNT_').get()        
        return self.__change_amount

    def focus_change_amount(self):
        self.__popup.Element('_CHANGE_AMOUNT_').SetFocus() 
        self.__popup.Element('_CHANGE_AMOUNT_').update(select=True)        

    def append_char(self, key, char):
        if self.__popup[key].Widget.select_present():
            self.__exchange_amount = ''
            self.__popup.Element(key).update(value = self.__change_amount)
        
        self.__change_amount = self.__popup.Element('_CHANGE_AMOUNT_').get()        
        self.__change_amount = str(self.__change_amount) + char
        self.__popup.Element(key).update(value = self.__change_amount)

    change_amount = property(get_change_amount, set_change_amount) 


