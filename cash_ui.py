import datetime


###
class CashUi:
    def __init__(self, window):
        self.__window = window

        self.__cashs_list = []
        self.__cash_line = []
        self.__cash_idx = 0
        self.__transaction_type_search = ''
        self.__transaction_context_search = ''
        self.__name = ''
        self.__transaction_type = ''
        self.__transaction_context = ''
        self.__transaction_reference = ''
        self.__receipt_amount = 0.00
        self.__payment_amount = 0.00
        self.__balance = 0.00
        
        self.__window["_CASH_LIST_RECEIPT_"].Widget.config(takefocus=0)
        self.__window["_CASH_LIST_PAYMENT_"].Widget.config(takefocus=0)
        self.__window["_CASH_LIST_DENOMINATION_"].Widget.config(takefocus=0)
        self.__window["_CASH_LIST_ESC_"].Widget.config(takefocus=0)
        self.__window["_CASH_LIST_SEARCH_"].Widget.config(takefocus=0)
       
    # Setters and Getters
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

    def set_receipt_amount(self, receipt_amount):
        self.__receipt_amount = receipt_amount
        
    def get_receipt_amount(self):
        return self.__receipt_amount

    def set_payment_amount(self, payment_amount):
        self.__payment_amount = payment_amount
        
    def get_payment_amount(self):
        return self.__payment_amount

    def set_balance(self, balance):
        self.__balance = balance
        
    def get_balance(self):
        return self.__balance

    def set_cash_idx(self, cash_idx):
        self.__cash_idx = cash_idx
        
    def get_cash_idx(self):
        return self.__cash_idx  

    # Focus        
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
    
    def clear_ui_cash_list(self):
        self.__ui_cashs_list.clear()
        self.__window.Element('_CASH_LIST_').update(values = self.__ui_cashs_list)

    def elements_to_cash_line(self):
        self.__cash_line.append(self.__name)        
        self.__cash_line.append(self.__transaction_type)
        self.__cash_line.append(self.__transaction_context)        
        self.__cash_line.append(self.__transaction_reference)
        
        self.__cash_line.append("{:.2f}".format(float(self.__receipt_amount)))        
        self.__cash_line.append("{:.2f}".format(float(self.__payment_amount)))        
        self.__cash_line.append(self.__balance)        

       
    def cash_line_to_elements(self, idx):
        self.__cash_line = self.__cashs_list[idx]
        self.__name = self.__cash_line[0]
        self.__transaction_type = self.__cash_line[1]
        self.__transaction_context = self.__cash_line[2]
        self.__transaction_reference = self.__cash_line[3]
        self.__receipt_amount = self.__cash_line[4]
        self.__payment_amount = self.__cash_line[5]
        self.__balance = self.__cash_line[6]

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
    receipt_amount = property(get_receipt_amount, set_receipt_amount)
    payment_amount = property(get_payment_amount, set_payment_amount)
    balance = property(get_balance, set_balance)
 

