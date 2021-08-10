import PySimpleGUI as sg
import json
from pynput.keyboard import Key, Controller

from alignpos_db import DbConn, DbTable, DbQuery
from common_layout import SigninCanvas, MessageCanvas, KeypadCanvas, ItemListCanvas, CustomerListCanvas
from common_ui import SigninUi, KeypadUi, ItemListUi, CustomerListUi

sg.theme('DefaultNoMoreNagging')

 
class Signin():
    
    def __init__(self):
        with open('./alignpos.json') as file_config:
          config = json.load(file_config)

        self.__terminal_id = config["terminal_id"]
        
        self.__canvas = SigninCanvas()

        self.__window = sg.Window("AlignPOS Signin", 
                        self.__canvas.layout,
                        background_color = 'White',
                        keep_on_top = True, 
                        return_keyboard_events = True, 
                        modal=True, 
                        icon='images/favicon.ico',
                        finalize=True
                    )

        self.__ui = SigninUi(self.__window)

        self.__db_conn = DbConn()
        self.__db_session = self.__db_conn.session
        self.__db_user_table = DbTable(self.__db_conn, 'tabUser')

        self.__window.bind('<FocusIn>', '+FOCUS IN+')
        self.__window.bind('<FocusOut>', '+FOCUS OUT+')

        self.__window["_OK_"].Widget.config(takefocus=0) 
        self.__window["_CANCEL_"].Widget.config(takefocus=0)

        self.__type = type
        self.__ok = False

        self.__ui.signin_terminal_id = self.__terminal_id
        self.__ui.focus_signin_user_id()
        
        self.handler()

    def handler(self):
        if self.__type == 'OK':
            self.__window.Element("_CANCEL_").update(visible=False)
        else:
            self.__window.Element("_CANCEL_").update(visible=True)

        while True:
            event, values = self.__window.read()
            print('signin:', event, values)

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
                #print('passwd:', db_row[0], self.__ui.signin_passwd, db_row[1].decode("utf-8"))
                if self.__ui.signin_passwd == db_row[1].decode("utf-8"):
                    if db_row[3] == 1:                    
                        return True
                    else:
                        Message('STOP', 'Inactive User')
                        self.__ui.focus_signin_user_id()
                        return False                                   
                else:
                    Message('STOP', 'Password mismatch')
                    self.__ui.focus_signin_passwd()
                    return False                
        else:
            Message('STOP', 'Invalid User')
            self.__ui.focus_signin_user_id()
            return False
   
    def get_ok(self):
        return self.__ok

    def get_sign_in_user_id(self):
        return self.__ui.signin_user_id
 
    def get_sign_in_terminal_id(self):
        return self.__ui.signin_terminal_id

    ok = property(get_ok)         
    user_id = property(get_sign_in_user_id)         
    terminal_id = property(get_sign_in_terminal_id)         

    
class Message():
    
    def __init__(self, type, message):
        self.__type = type
        self.__message = message


        switcher = {
            'INFO': 'Information',
            'OPT': 'Option',
            'STOP': 'Error',
            'WARN': 'Warning',
        }
        caption = switcher.get(type)
        
        self.__canvas = MessageCanvas(type)
        self.__window = sg.Window(caption, 
                        self.__canvas.layout,
                        keep_on_top = True, 
                        return_keyboard_events = True, 
                        modal=True, 
                        icon='images/favicon.ico',
                        background_color = 'White',
                        finalize=True
                    )

        self.__window.bind('<FocusIn>', '+FOCUS IN+')
        self.__window.bind('<FocusOut>', '+FOCUS OUT+')

        self.__window.Element("_MESSAGE_").update(value=message)       
        self.__window["_OK_"].Widget.config(takefocus=0) 
        self.__window["_CANCEL_"].Widget.config(takefocus=0)


        self.__ok = False

        if self.__type == 'OPT':
            self.__window.Element("_CANCEL_").update(visible=True)
        else:
            self.__window.Element("_CANCEL_").update(visible=False)
            
        self.handler()

    def handler(self):
        while True:
            event, values = self.__window.read()
            #print('message_popup:', event)
            
            if event in ('_OK_', '\r'):
                self.__ok = True
                break
            
            if event in ('Escape:27', '_CANCEL_', '+FOCUS OUT+', sg.WIN_CLOSED):
                self.__ok = False
                break
                
        self.__window.close()

    def get_ok(self):
        return self.__ok
        
    ok = property(get_ok)         


class Keypad():

    def __init__(self, current_value):
        self.__input_value = ''
        self.__current_value = current_value
        self.__location = (100,100)
        self.__kb = Controller()

        
        self.__canvas = KeypadCanvas()
    
        self.__window = sg.Window("Keypad", 
                        self.__canvas.layout,
                        keep_on_top = True, 
                        no_titlebar = True,                         
                        return_keyboard_events = False, 
                        modal=True, 
                        icon='images/favicon.ico',
                        finalize=True
                    )
        self.__ui = KeypadUi(self.__window)
        self.__ui.pad_input = current_value
        self.__ui.focus_pad_input()
        

        self.handler()
        
    def handler(self):
        while True:
            event, values = self.__window.read()
            print('keypad_popup=', event, values)
            
            if event in (sg.WIN_CLOSED, 'Escape:27', 'Escape', 'Exit', 'close'):
                break

            if event.isalnum() and not event in ('back', 'point', 'hyphen'):
                inp_val = self.__ui.pad_input

                sel_val = None
                try:
                    sel_val = self.__window['_PAD_INPUT_'].Widget.selection_get()
                except sg.tk.TclError:
                    sel_val = None
                if sel_val:
                    inp_val = event[0]
                    self.__kb.press(Key.right)
                    self.__kb.release(Key.right)                    
                else:
                    inp_val += event[0]
                self.__ui.pad_input = inp_val
                
            if event == 'back':
                self.__kb.press(Key.backspace)
                self.__kb.release(Key.backspace)

            if event == 'point':
                inp_val = self.__ui.pad_input
                inp_val += '.'
                self.__ui.pad_input = inp_val
                
            if event == 'hyphen':
                inp_val = self.__ui.pad_input
                inp_val += '-'
                self.__ui.pad_input = inp_val

            if event == '_PAD_OK_':
                self.__input_value = self.__ui.pad_input
                break
                
        self.__window.close()    
        
    def set_input_value(self, input_value):
        self.__input_value = input_value

    def get_input_value(self):
        return self.__input_value
   
    input_value = property(get_input_value, set_input_value)         


class ItemList:
    def __init__(self, filter):    
        self.__item_code = ''

        self.__db_conn = DbConn()

        db_item_table = DbTable(self.__db_conn, 'tabItem')
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
            self.__ui.selling_price = db_item_row.selling_price
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

        db_customer_table = DbTable(self.__db_conn, 'tabCustomer')
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
                        size=(700,360), 
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
        tabCustomer.customer_type \
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
            print('customer_list=', event, prev_event)
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