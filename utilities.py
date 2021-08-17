import os
import PySimpleGUI as sg
import json
from pynput.keyboard import Key, Controller
from utilities_layout import MessageCanvas, KeypadCanvas
from utilities_ui import KeypadUi


class Config():

    def __init__(self):
        self.__application_path = os.environ['ALIGNPOS_PATH']
        with open(self.__application_path + '/app_config.json') as file_config:
          config = json.load(file_config)

        self.__terminal_id = config["terminal_id"]
        self.__ws_host = config["ws_host"]
        self.__ws_user = config["ws_user"]
        self.__ws_passwd = config["ws_passwd"]
        self.__db_host = config["db_host"]
        self.__db_port = config["db_port"]
        self.__db_database = config["db_database"]
        self.__db_user = config["db_user"]
        self.__db_passwd = config["db_passwd"]
        self.__kv_database = config["kv_database"]
        self.__log_folder_path = config["log_folder_path"]

    def get_application_path(self):
        return(self.__application_path)
    
    def get_terminal_id(self):
        return(self.__terminal_id)
    
    def get_ws_host(self):
        return(self.__ws_host)
       
    def get_ws_user(self):
        return(self.__ws_user)
       
    def get_ws_passwd(self):
        return(self.__ws_passwd)
       
    def get_db_host(self):
        return(self.__db_host)
       
    def get_db_port(self):
        return(self.__db_port)
       
    def get_db_database(self):
        return(self.__db_database)
       
    def get_db_user(self):
        return(self.__db_user)
       
    def get_db_passwd(self):
        return(self.__db_passwd)
       
    def get_kv_database(self):
        return(self.__kv_database)
       
    def get_log_folder_path(self):
        return(self.__log_folder_path)

    application_path = property(get_application_path)         
    terminal_id = property(get_terminal_id)         
    ws_host = property(get_ws_host)         
    ws_user = property(get_ws_user)         
    ws_passwd = property(get_ws_passwd)         
    db_host = property(get_db_host)         
    db_port = property(get_db_port)         
    db_database = property(get_db_database)         
    db_user = property(get_db_user)         
    db_passwd = property(get_db_passwd)         
    kv_database = property(get_kv_database)         
    log_folder_path = property(get_log_folder_path)         
               

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
                        icon='c:/alignpos/images/favicon.ico',
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

        
