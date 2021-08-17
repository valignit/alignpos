import datetime


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


