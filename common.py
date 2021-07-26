import PySimpleGUI as sg
from pynput.keyboard import Key, Controller

from alignpos_db import DbConn, DbTable, DbQuery

from common_layout import ConfirmMessageCanvas, ItemLookupCanvas, KeypadCanvas
from common_ui import ItemLookupUi, KeypadUi

 
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

        self.handler()

    def handler(self):
        if self.__type == 'OK':
            self.__window.Element("_CANCEL_").update(visible=False)
        else:
            self.__window.Element("_CANCEL_").update(visible=True)

        while True:
            event, values = self.__window.read()
            #print('message_popup:', event)
            
            if event in ('_OK_', 'F12:123', 'F12', '\r'):
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

    def __init__(self, current_val):
        self.__input_value = ''
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
        self.__ui.pad_input = current_val 
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
