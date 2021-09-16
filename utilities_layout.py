import PySimpleGUI as sg
from config import Config
from styles import ElementStyle


class MessageCanvas:

    def __init__(self, type):
        config = Config()
        self.__language = config.language
        
        switcher = {
            'INFO': 'Information',
            'OPT': 'Option',
            'STOP': 'Error',
            'WARN': 'Warning',
        }
        self.__title_en = switcher.get(type)

        switcher = {
            'INFO': 'معلومة',
            'OPT': 'خيار',
            'STOP': 'خطأ',
            'WARN': 'تحذير',
        }
        self.__title_ar = switcher.get(type)
        
 
        self.__layout_en = [
            [
                sg.Image(filename = 'c:/alignpos/images/' + type + '.PNG', size=(25,25), pad = ((10,10),(0,5)))
            ],
            [
                sg.T(key='_MESSAGE_',size=(30,1), background_color = 'White', pad = ((10,10),(5,15)))
            ], 
            [
                sg.B(key='_OK_', button_text='Ok - Ent', pad = ((10,10),(5,5))), 
                sg.B(key='_CANCEL_', button_text='Cancel - Esc', visible=True, pad = ((10,10),(5,5)))
            ]
        ]

        self.__layout_ar = [
            [
                sg.Image(filename = 'c:/alignpos/images/' + type + '.PNG', size=(25,25), pad = ((10,10),(0,5)))
            ],
            [
                sg.T(key='_MESSAGE_',size=(30,1), background_color = 'White', pad = ((10,10),(5,15)),justification = 'right',),
            ], 
            [
                sg.B(key='_CANCEL_', button_text='Esc-يلغي', visible=True, pad = ((10,10),(5,5))),
                sg.B(key='_OK_', button_text='Ent-نعم', pad = ((10,10),(5,5)))
            ]
        ]

    def get_layout(self):
        if self.__language == 'ar': 
            return self.__layout_ar
        else:
            return self.__layout_en
    
    def get_title(self):
        if self.__language == 'ar': 
            return self.__title_ar
        else:
            return self.__title_en
    
    def get_justification(self):
        if self.__language == 'ar': 
            return 'right'
        else:
            return 'left'

    layout = property(get_layout)      
    title = property(get_title)      
    justification = property(get_justification)      


class KeypadCanvas:
    
    def __init__(self):
        self.font=('Arial', 16)
        numberRow = '1234567890'
        topRow = 'QWERTYUIOP'
        midRow = 'ASDFGHJKL'
        bottomRow = 'ZXCVBNM'
        
        self.__layout = [
            [
                sg.Input(key='_PAD_INPUT_', size=(44,1), **ElementStyle.search_input, pad=((0,14),(0,0))),
                sg.Button(key='_PAD_OK_', button_text='Ok', **ElementStyle.search_button),
                sg.Button(key='close', button_text='Cancel', **ElementStyle.search_button)
            ],
            [
                sg.Button(c, key=c, **ElementStyle.pad_button) for c in numberRow
            ] + 
            [
                sg.Button('⌫', key='back', **ElementStyle.pad_button),
            ],
            [
                sg.Text(' ' * 4)] + [sg.Button(c, key=c, **ElementStyle.pad_button) for c in
                               topRow] + [sg.Stretch()
            ],
            [
                sg.Text(' ' * 11)] + [sg.Button(c, key=c, **ElementStyle.pad_button) for c in
                                midRow] + [sg.Stretch()
            ],
            [
                sg.Text(' ' * 18)
            ] + 
            [
                sg.Button(c, key=c, **ElementStyle.pad_button) for c in
                                bottomRow
            ] + 
            [
                sg.Button('.', key='point', **ElementStyle.pad_button),
                sg.Button('-', key='hyphen', **ElementStyle.pad_button)
            ] + 
            [sg.Stretch()]
        ]

    def get_layout(self):
        return self.__layout
    
    layout = property(get_layout)
