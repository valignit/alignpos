import datetime


###
# Signin Interface
class SigninUi:

    def __init__(self, window):
        self.__window = window
        self.__signin_user_id = ''
        self.__signin_passwd = ''
        self.__window['_SIGNIN_TERMINAL_ID_'].Widget.config(takefocus=0)
       

    def set_signin_terminal_id(self, signin_terminal_id):
        self.__signin_terminal_id = signin_terminal_id
        self.__window.Element('_SIGNIN_TERMINAL_ID_').update(value = self.__signin_terminal_id)
        
    def get_signin_terminal_id(self):
        self.__signin_terminal_id = self.__window.Element('_SIGNIN_TERMINAL_ID_').get()        
        return self.__signin_terminal_id
        
    def set_signin_user_id(self, signin_user_id):
        self.__signin_user_id = signin_user_id
        self.__window.Element('_SIGNIN_USER_ID_').update(value = self.__signin_user_id)
        
    def get_signin_user_id(self):
        self.__signin_user_id = self.__window.Element('_SIGNIN_USER_ID_').get()        
        return self.__signin_user_id
        
    def set_signin_passwd(self, signin_passwd):
        self.__signin_passwd = signin_passwd
        self.__window.Element('_SIGNIN_PASSWD_').update(value = self.__signin_passwd)
        
    def get_signin_passwd(self):
        self.__signin_passwd = self.__window.Element('_SIGNIN_PASSWD_').get()        
        return self.__signin_passwd
        
    def focus_signin_user_id(self):
        self.__window.Element('_SIGNIN_USER_ID_').SetFocus()
        self.__window.Element('_SIGNIN_USER_ID_').update(select=True)        
        
    def focus_signin_passwd(self):
        self.__window.Element('_SIGNIN_PASSWD_').SetFocus()
        self.__window.Element('_SIGNIN_PASSWD_').update(select=True)        
       
       
    signin_terminal_id = property(get_signin_terminal_id, set_signin_terminal_id)     
    signin_user_id = property(get_signin_user_id, set_signin_user_id)     
    signin_passwd = property(get_signin_passwd, set_signin_passwd)     


###
# Keypad Popup Interface
class KeypadUi:

    def __init__(self, popup):
        self.__popup = popup
        self.__pad_input = ''

    def set_pad_input(self, pad_input):
        self.__pad_input = pad_input
        self.__popup.Element('_PAD_INPUT_').update(value = self.__pad_input)
        
    def get_pad_input(self):
        self.__pad_input = self.__popup.Element('_PAD_INPUT_').get()        
        return self.__pad_input
        
    def focus_pad_input(self):
        self.__popup.Element('_PAD_INPUT_').SetFocus()
        self.__popup.Element('_PAD_INPUT_').update(select=True, move_cursor_to='none')        
        
       
    pad_input = property(get_pad_input, set_pad_input)     


class ItemListUi:
    def __init__(self, window):
        self.__window = window

        self.__items_list = []
        self.__item_line = []
        self.__item_idx = 0
        self.__item_code = ''
        self.__item_name = ''
        self.__stock = float(0.00)
        self.__selling_price = float(0.00)
               
    # Setters and Getters
    def set_items_list(self, items_list):
        self.__items_list = items_list
        self.__window.Element('_ITEMS_LIST_').update(values = self.__items_list)
        
    def get_items_list(self):
        self.__items_list = self.__window.Element('_ITEMS_LIST_').get()
        return self.__items_list
              
    def set_item_line(self, item_line):
        self.__item_line = item_line
        
    def get_item_line(self):
        self.__item_line = self.__items_list[self.__item_idx]
        return self.__item_line
           
    def set_item_code(self, item_code):
        self.__item_code = item_code
        
    def get_item_code(self):
        return self.__item_code
        
    def set_item_name(self, item_name):
        self.__item_name = item_name
        
    def get_item_name(self):
        return self.__item_name
        
    def set_stock(self, stock):
        self.__stock = stock
        
    def get_stock(self):
        return self.__stock
        
    def set_selling_price(self, selling_price):
        self.__selling_price = selling_price
        
    def get_selling_price(self):
        return self.__selling_price
        
    def set_item_idx(self, item_idx):
        self.__item_idx = item_idx
        
    def get_item_idx(self):
        return self.__item_idx  

    # Focus        
    def focus_items_list(self):
        self.__window['_ITEMS_LIST_'].Widget.config(takefocus=1)
        self.__window.Element('_ITEMS_LIST_').set_focus(force = True)
        if len(self.__items_list) > 0:        
            table_row = self.__window['_ITEMS_LIST_'].Widget.get_children()[0]
            self.__window['_ITEMS_LIST_'].Widget.selection_set(table_row)  # move selection
            self.__window['_ITEMS_LIST_'].Widget.focus(table_row)  # move focus
            self.__window['_ITEMS_LIST_'].Widget.see(table_row)  # scroll to show i

    def focus_items_list_row(self, idx):
        self.__window['_ITEMS_LIST_'].Widget.config(takefocus=1)        
        self.__window.Element('_ITEMS_LIST_').set_focus(force = True)
        table_row = self.__window['_ITEMS_LIST_'].Widget.get_children()[idx]
        self.__window['_ITEMS_LIST_'].Widget.selection_set(table_row)  # move selection
        self.__window['_ITEMS_LIST_'].Widget.focus(table_row)  # move focus
        self.__window['_ITEMS_LIST_'].Widget.see(table_row)  # scroll to show i
    
    def clear_ui_items_list(self):
        self.__ui_item_list.clear()
        self.__window.Element('_ITEMS_LIST_').update(values = self.__ui_item_list)

    def elements_to_item_line(self):
        self.__item_line.append(self.__item_code)
        self.__item_line.append(self.__item_name)        
        self.__item_line.append("{:.2f}".format(float(self.__stock)))      
        self.__item_line.append("{:.2f}".format(float(self.__selling_price)))       
       
    def item_line_to_elements(self, idx):
        self.__item_line = self.__items_list[idx]
        self.__item_code = self.__item_line[0]
        self.__item_name = self.__item_line[1]
        self.__stock = self.__item_line[2]
        self.__selling_price = self.__item_line[3]

    def add_item_line(self):
        self.__item_line = []
        self.elements_to_item_line()    
        self.__items_list.append(self.__item_line)
        self.__window.Element('_ITEMS_LIST_').update(values = self.__items_list)

    # Properties   
    items_list = property(get_items_list, set_items_list)
    item_line = property(get_item_line, set_item_line)
    item_idx = property(get_item_idx, set_item_idx)
    item_code = property(get_item_code, set_item_code)
    item_name = property(get_item_name, set_item_name)
    stock = property(get_stock, set_stock)
    selling_price = property(get_selling_price, set_selling_price)


class CustomerListUi:
    def __init__(self, window):
        self.__window = window

        self.__customers_list = []
        self.__customer_line = []
        self.__customer_idx = 0
        self.__customer_number = ''
        self.__customer_number_search = ''
        self.__mobile_number = ''
        self.__mobile_number_search = ''
        
        self.__window["_CUSTOMER_LIST_OK_"].Widget.config(takefocus=0)
        self.__window["_CUSTOMER_LIST_ESC_"].Widget.config(takefocus=0)
        self.__window["_CUSTOMER_LIST_SEARCH_"].Widget.config(takefocus=0)
       
    # Setters and Getters
    def set_customers_list(self, customers_list):
        self.__customers_list = customers_list
        self.__window.Element('_CUSTOMERS_LIST_').update(values = self.__customers_list)
        
    def get_customers_list(self):
        self.__customers_list = self.__window.Element('_CUSTOMERS_LIST_').get()
        return self.__customers_list
              
    def set_customer_line(self, customer_line):
        self.__customer_line = customer_line
        
    def get_customer_line(self):
        self.__customer_line = self.__customers_list[self.__item_idx]
        return self.__customer_line
    
    def set_customer_number_search(self, customer_number_search):
        self.__customer_number_search = customer_number_search
        self.__window.Element('_CUSTOMER_NUMBER_SEARCH_').update(value = self.__customer_number_search)
        
    def get_customer_number_search(self):
        self.__customer_number_search = self.__window.Element('_CUSTOMER_NUMBER_SEARCH_').get()        
        return self.__customer_number_search
        
    def set_mobile_number_search(self, mobile_number_search):
        self.__mobile_number_search = mobile_number_search
        self.__window.Element('_MOBILE_NUMBER_SEARCH_').update(value = self.__mobile_number_search)
        
    def get_mobile_number_search(self):
        self.__mobile_number_search = self.__window.Element('_MOBILE_NUMBER_SEARCH_').get()        
        return self.__mobile_number_search
        
    def set_customer_number(self, customer_number):
        self.__customer_number = customer_number
        
    def get_customer_number(self):
        return self.__customer_number
        
    def set_mobile_number(self, mobile_number):
        self.__mobile_number = mobile_number
        
    def get_mobile_number(self):
        return self.__mobile_number
        
    def set_customer_name(self, customer_name):
        self.__customer_name = customer_name
        
    def get_customer_name(self):
        return self.__customer_name
        
    def set_customer_type(self, customer_type):
        self.__customer_type = customer_type
        
    def get_customer_type(self):
        return self.__customer_type

    def set_customer_idx(self, customer_idx):
        self.__customer_idx = customer_idx
        
    def get_customer_idx(self):
        return self.__customer_idx  

    # Focus        
    def focus_customers_list(self):
        self.__window['_CUSTOMERS_LIST_'].Widget.config(takefocus=1)
        self.__window.Element('_CUSTOMERS_LIST_').set_focus(force = True)        
        if len(self.__customers_list) > 0:        
            table_row = self.__window['_CUSTOMERS_LIST_'].Widget.get_children()[0]
            self.__window['_CUSTOMERS_LIST_'].Widget.selection_set(table_row)  # move selection
            self.__window['_CUSTOMERS_LIST_'].Widget.focus(table_row)  # move focus
            self.__window['_CUSTOMERS_LIST_'].Widget.see(table_row)  # scroll to show i

    def focus_estimates_list_row(self, idx):
        self.__window['_CUSTOMERS_LIST_'].Widget.config(takefocus=1)
        self.__window.Element('_CUSTOMERS_LIST_').set_focus(force = True)
        table_row = self.__window['_CUSTOMERS_LIST_'].Widget.get_children()[idx]
        self.__window['_CUSTOMERS_LIST_'].Widget.selection_set(table_row)  # move selection
        self.__window['_CUSTOMERS_LIST_'].Widget.focus(table_row)  # move focus
        self.__window['_CUSTOMERS_LIST_'].Widget.see(table_row)  # scroll to show i
    
    def clear_ui_customers_list(self):
        self.__ui_customer_list.clear()
        self.__window.Element('_CUSTOMERS_LIST_').update(values = self.__ui_customer_list)

    def elements_to_customer_line(self):
        self.__customer_line.append(self.__customer_number)
        self.__customer_line.append(self.__mobile_number)        
        self.__customer_line.append(self.__customer_name)        
        self.__customer_line.append(self.__customer_type)        

       
    def customer_line_to_elements(self, idx):
        self.__customer_line = self.__customers_list[idx]
        self.__customer_number = self.__customer_line[0]
        self.__mobile_number = self.__customer_line[1]
        self.__customer_name = self.__customer_line[2]
        self.__customer_type = self.__customer_line[3]

    def add_customer_line(self):
        self.__customer_line = []
        self.elements_to_customer_line()    
        self.__customers_list.append(self.__customer_line)
        self.__window.Element('_CUSTOMERS_LIST_').update(values = self.__customers_list)

    # Properties   
    customers_list = property(get_customers_list, set_customers_list)
    customer_line = property(get_customer_line, set_customer_line)
    customer_idx = property(get_customer_idx, set_customer_idx)
    customer_number_search = property(get_customer_number_search, set_customer_number_search)
    mobile_number_search = property(get_mobile_number_search, set_mobile_number_search)
    customer_number = property(get_customer_number, set_customer_number)
    mobile_number = property(get_mobile_number, set_mobile_number)
    customer_name = property(get_customer_name, set_customer_name)
    customer_type = property(get_customer_type, set_customer_type)
       