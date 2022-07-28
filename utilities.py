import PySimpleGUI as sg
from pynput.keyboard import Key, Controller
from utilities_layout import MessageCanvas, KeypadCanvas
from utilities_ui import KeypadUi


class Message():
    
    def __init__(self, type, message):
        self.__type = type
        self.__message = message
        
        self.__canvas = MessageCanvas(type)
        self.__window = sg.Window(self.__canvas.title, 
                        self.__canvas.layout,
                        keep_on_top = True, 
                        return_keyboard_events = True, 
                        modal=True, 
                        icon='c:/alignpos/images/favicon.ico',
                        background_color = 'White',
                        finalize=True,
                        text_justification = self.__canvas.justification,
                        element_justification = self.__canvas.justification
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
                        finalize=True,
                        background_color = 'grey90'
                    )
        self.__ui = KeypadUi(self.__window)
        self.__ui.pad_input = current_value
        self.__ui.focus_pad_input()
        
        self.handler()
        
    def handler(self):
        while True:
            event, values = self.__window.read()
            #print('keypad_popup=', event, values)
            
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

        