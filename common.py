import PySimpleGUI as sg
import json
from pynput.keyboard import Key, Controller

from alignpos_db import DbConn, DbTable, DbQuery
from common_layout import SigninCanvas, ConfirmMessageCanvas, ItemLookupCanvas, KeypadCanvas, ItemListCanvas
from common_ui import SigninUi, ItemLookupUi, KeypadUi, ItemListUi

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
                self.__ui.signin_user_id = 'admin'
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
        db_query = DbQuery(self.__db_conn, 'select name, DECODE(passwd, "secret") as passwd from tabUser where name = "{}"'.format(self.__ui.signin_user_id))
        if  db_query.result:
            for db_row in db_query.result:
                print('passwd:', db_row[0], self.__ui.signin_passwd, db_row[1].decode("utf-8"))
                if self.__ui.signin_passwd == db_row[1].decode("utf-8"):
                    return True
                else:
                    ConfirmMessage('OK', 'Password mismatch')
                    self.__ui.focus_signin_passwd()
                    return False                
        else:
            ConfirmMessage('OK', 'Invalid User')
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

    
class ConfirmMessage():
    
    def __init__(self, type, message):
        self.__canvas = ConfirmMessageCanvas()

        self.__window = sg.Window("Confirm", 
                        self.__canvas.layout,
                        keep_on_top = True, 
                        return_keyboard_events = True, 
                        modal=True, 
                        finalize=True
                    )

        self.__window.bind('<FocusIn>', '+FOCUS IN+')
        self.__window.bind('<FocusOut>', '+FOCUS OUT+')

        self.__window.Element("_MESSAGE_").update(value=message)       
        self.__window["_OK_"].Widget.config(takefocus=0) 
        self.__window["_CANCEL_"].Widget.config(takefocus=0)

        self.__type = type
        self.__message = message
        self.__ok = False

        if self.__type == 'OK':
            self.__window.Element("_CANCEL_").update(visible=False)
        else:
            self.__window.Element("_CANCEL_").update(visible=True)
            
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

    
class ItemLookup():

    def __init__(self, filter, lin, col):       
        self.__item_code = None
        self.__canvas = ItemLookupCanvas()
        self.__window = sg.Window("Item Name",
                        self.__canvas.layout,
                        location=(lin,col), 
                        size=(348,129), 
                        modal=True, 
                        finalize=True,
                        return_keyboard_events=True, 
                        no_titlebar = True, 
                        element_padding=(0,0), 
                        background_color = 'White',
                        border_depth= 1,
                        keep_on_top = True,                    
                        margins=(0,0)
                    )
        self.__window.bind('<FocusIn>', '+FOCUS IN+')
        self.__window.bind('<FocusOut>', '+FOCUS OUT+')    
    
        self.__ui = ItemLookupUi(self.__window)
        
        self.__db_conn = DbConn()
        db_item_table = DbTable(self.__db_conn, 'tabItem')
        db_item_cursor = db_item_table.list(filter)

        if (len(db_item_cursor) == 0):
            self.__window.close()           
            return
        
        self.__ui.item_list = []
        for db_item_row in db_item_cursor:
            self.__ui.item_code = db_item_row.item_code
            self.__ui.item_name = db_item_row.item_name
            self.__ui.add_item_line()

        self.__ui.idx = 0
        self.__ui.focus_item_list()

        self.handler()

    def handler(self):
        prev_event = ''    
        while True:
            event, values = self.__window.read()
            print('item_name_popup=', event, prev_event, values)
            if event == 'Down:40':
                self.__ui.next_item_line()
            if event == 'Up:38':
                self.__ui.prev_item_line()            
            if event in ("Exit", '_ITEM_NAME_ESC_', 'Escape:27', '+FOCUS OUT+') or event == sg.WIN_CLOSED:
                break        
            if event in ('\r'):
                if values['_ITEM_NAME_LIST_']:
                    self.__item_code =  values['_ITEM_NAME_LIST_'][0][0]
                    break
            if event in ('_ITEM_NAME_LIST_') and prev_event in ('_ITEM_NAME_LIST_'):
                self.__item_code =  values['_ITEM_NAME_LIST_'][0][0]
                break
            prev_event = event
            
        self.__db_conn.close()           
        self.__window.close()    
      
    def get_item_code(self):
        return self.__item_code
    
    item_code = property(get_item_code)         


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
            sg.popup('Item(s) not found', keep_on_top = True)
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
            print('item_list=', event, prev_event, values)
                
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