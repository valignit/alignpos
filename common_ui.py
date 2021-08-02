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
# Item Name Popup Interface
class ItemLookupUi:

    def __init__(self, popup):
        self.__popup = popup
        self.__item_code = ''
        self.__item_name = ''
        self.__item_list = []
        self.__item_line = []
        self.__idx = 0

    def set_item_code(self, item_code):
        self.__item_code = item_code
        
    def get_item_code(self):
        return self.__item_code

    def set_item_name(self, item_name):
        self.__item_name = item_name
        
    def get_item_name(self):
        return self.__item_name

    def set_item_list(self, item_list):
        self.__item_list = item_list
        self.__popup.Element('_ITEM_NAME_LIST_').update(values = self.__item_list, set_to_index=self.__idx)
        
    def get_item_list(self):
        return self.__item_list
        
    def get_item_line(self):
        return self.__popup.Element('_ITEM_NAME_LIST_').get()

    def set_item_line(self, item_line):
        self.__item_line = item_line

    def elements_to_item_line(self):
        self.__item_line.append(self.__item_code)
        self.__item_line.append('|')
        self.__item_line.append(self.__item_name.replace(' ', '-')) #otherwise item name will be embedded with {}
       
    def item_line_to_elements(self, idx):
        self.__item_line = self.__items_list[idx]
        self.__item_code = self.__item_line[0]
        self.__item_name = self.__item_line[1]
        
    def add_item_line(self):
        self.__item_line = []
        self.elements_to_item_line()
        self.__item_list.append(self.__item_line)
        self.__popup.Element('_ITEM_NAME_LIST_').update(values = self.__item_list)

    def prev_item_line(self):
        idx = self.__idx
        if idx > 0:
            idx = idx - 1
            self.__idx = idx
            self.__popup.Element('_ITEM_NAME_LIST_').update(set_to_index=self.__idx)
            
    def next_item_line(self):
        idx = self.__idx
        if idx < len(self.__item_list) - 1:
            idx = idx + 1
            self.__idx = idx
            self.__popup.Element('_ITEM_NAME_LIST_').update(set_to_index=self.__idx)
                   
    def focus_item_list(self):
        self.__popup.Element('_ITEM_NAME_LIST_').SetFocus()
        
    def get_item_idx(self):
        return self.__idx
        
    def set_item_idx(self, idx):
        self.__idx = idx
        self.__popup.Element('_ITEM_NAME_LIST_').update(set_to_index=self.__idx)       
        
    item_list = property(get_item_list, set_item_list)     
    item_code = property(get_item_code, set_item_code)
    item_name = property(get_item_name, set_item_name)
    item_line = property(get_item_line, set_item_line)
    idx = property(get_item_idx, set_item_idx)


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
       