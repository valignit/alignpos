import PySimpleGUI as sg


###
# Common UI Styles             
class ElementStyle:
    
    page_title:  dict = {           
                        'font':("Calibri 18 bold"),
                        'size':(10,1),
                        'text_color': 'grey30',
                    }

    pad_button_small:  dict = {
                        'size':(3, 1), 
                        'font':('Calibri 12 bold'), 
                        'button_color': ('grey20','grey80'),
                 }

    pad_button:  dict = {
                        'size':(4, 2), 
                        'font':('Calibri 11 bold'), 
                        'button_color': ('grey20','grey80'),
                 }

    pad_button_wide:  dict = {
                        'size':(10, 2), 
                        'font':('Calibri 11 bold'), 
                        'button_color': ('grey20','grey80'),
                      }

    nav_button:  dict = {
                        'size':(5, 1), 
                        'font':('Calibri 11 bold'), 
                        'button_color': ('grey20','grey80'),
                        'use_ttk_buttons': True
                 }

    nav_button_wide:  dict = {
                        'size':(8, 1), 
                        'font':('Calibri 11 bold'), 
                        'button_color': ('grey20','grey80'),
                        'use_ttk_buttons': True
                      }
                    
    action_button:  dict = {
                        'size':(10, 1), 
                        'font':('Calibri 11 bold'), 
                        'button_color': ('grey20', 'grey80'),
                        'use_ttk_buttons': True
                    }

    exit_button:  dict = {
                        'size':(10, 1), 
                        'font':('Calibri 11 bold'), 
                        'button_color': ('grey20', 'grey80'),
                        'use_ttk_buttons': True
                    }

    summary_text:  dict = {           
                        'font':("Helvetica 11"),
                        'size':(10,1)  ,
                        'background_color': 'White'
                    }
                    
    menu_text:  dict = {           
                        'font':('Calibri 16'), 
                        'size':(10,1),
                    }
                    
    menu_button:  dict = {
                        'size':(28, 1), 
                        'font':('Calibri 16'), 
                        'button_color': ('grey20', 'grey80'),
                        'use_ttk_buttons': True
                    }

    summary_text:  dict = {           
                        'font':("Helvetica 11"),
                        'size':(10,1)  ,
                        'background_color': 'White'
                    }
                    
    summary_text_bold:  dict = {           
                        'font':("Helvetica 13 bold"),
                        'text_color': "navyblue",
                        'background_color': 'White',
                        'size':(10,1)                        
                        }
                        
    summary_input:  dict = {           
                        'readonly':True, 
                        'justification':'right', 
                        'disabled_readonly_text_color':'grey32', 
                        'disabled_readonly_background_color':'grey89', 
                        'default_text':'0.00' , 
                        'font':("Helvetica", 10),
                        'size':(11,1)                        
                    }

    summary_input_bold:  dict = {           
                            'readonly':True, 
                            'justification':'right', 
                            'disabled_readonly_text_color':"white", 
                            'disabled_readonly_background_color':"navyblue", 
                            'default_text':'0.00' , 
                            'font':("Helvetica 14 bold"),
                            'size':(8,1)                        
                        }

    title_text:  dict = {           
                        'font':("Helvetica 10"),
                        'size':(9,1),
                        'justification': 'right',
                    }    

    title_input:  dict = {           
                        'readonly':True, 
                        'justification':'right', 
                        'disabled_readonly_text_color':'grey32', 
                        'disabled_readonly_background_color':'grey89', 
                        'font':("Helvetica", 10),
                        'size':(9,1)                        
                    }

    header_text:  dict = {           
                        'font':("Helvetica 12"),
                        'size':(9,1),
                        'justification': 'right'
                    }    

    header_input:  dict = {           
                        'readonly':True, 
                        'justification':'right', 
                        'disabled_readonly_text_color':'grey32', 
                        'disabled_readonly_background_color':'grey89', 
                        'font':("Helvetica", 11),
                        'size':(11,1)                        
                    }

    footer_text:  dict = {           
                        'font':("Helvetica 9"),
                        'size':(9,1),
                        'justification': 'left'
                    }    

    footer_input:  dict = {           
                        'readonly':True, 
                        'justification':'left', 
                        'disabled_readonly_text_color':'grey32', 
                        'disabled_readonly_background_color':'grey89', 
                        'font':("Helvetica", 9),
                        'size':(12,1)                        
                    }

    search_text:  dict = {           
                        'font':("Helvetica 11"),
                        'size':(9,1),
                        'justification': 'left'
                    }    

    search_input:  dict = {           
                        'justification':'left', 
                        'font':("Helvetica", 10),
                        'background_color': 'White',
                        'enable_events':True                    
                    }

    search_button:  dict = {
                        'size':(13, 1), 
                        'font':('Calibri 11 bold'),
                        'button_color':('grey20','chocolate2'),
                        'use_ttk_buttons': True
                    }

    search_button_wide:  dict = {
                        'size':(29, 1), 
                        'font':('Calibri 11 bold'), 
                        'button_color': ('grey20', 'grey80'),
                        'use_ttk_buttons': True
                    }
    search_button_short:  dict = {
                        'size':(12, 1), 
                        'font':('Calibri 11 bold'), 
                        'button_color': ('grey20', 'grey80'),
                        'use_ttk_buttons': True
                    }
    welcome_text:  dict = {           
                        'font':("Calibri 13"),
                        'size':(20,15),
                        'background_color': 'White'
                    }


class SigninCanvas:

    def __init__(self):
        self.__layout = [
            [
                sg.Image(filename = 'alignpos_logo.PNG', background_color = 'white', pad = ((52,53),(0,0))),
            
            ],
            [
                sg.Frame('',
                    [
                        [
                            sg.Text('Counter:', background_color = 'grey90', **ElementStyle.search_text, pad=((10,5),(15,5))),
                            sg.Input(key='_SIGNIN_TERMINAL_ID_', readonly='True', size=(15,1), **ElementStyle.search_input, pad=((10,5),(15,5)))          
                        ], 
                        [
                            sg.Text('User Id:', background_color = 'grey90', **ElementStyle.search_text, pad=((10,5),(15,5))),
                            sg.Input(key='_SIGNIN_USER_ID_', size=(15,1), **ElementStyle.search_input, pad=((10,5),(15,5)))          
                        ], 
                        [
                            sg.Text('Password:', background_color = 'grey90', **ElementStyle.search_text, pad=((10,5),(5,5))),
                            sg.Input(key='_SIGNIN_PASSWD_', size=(15,1), **ElementStyle.search_input, password_char='*', pad=((10,5),(5,5)))          
                        ], 
                        [
                            sg.B(key='_OK_', button_text='Ok - Ent', **ElementStyle.search_button_short, pad=((10,5),(15,10))), 
                            sg.B(key='_CANCEL_', button_text='Cancel - Esc', **ElementStyle.search_button_short, visible=True, pad=((10,12),(15,10)))
                        ]
                    ],
                    background_color = 'grey90',
                    border_width = 0,
                    pad=((7,5),(10,10))
                )
            ]
        ]

    def get_layout(self):
        return self.__layout
    
    layout = property(get_layout)      


class ConfirmMessageCanvas:

    def __init__(self):
        self.__layout = [
            [
                sg.T(key='_MESSAGE_',size=(30,1))
            ], 
            [
                sg.B(key='_OK_', button_text='Ok - Ent'), 
                sg.B(key='_CANCEL_', button_text='Cancel - Esc', visible=True)
            ]
        ]

    def get_layout(self):
        return self.__layout
    
    layout = property(get_layout)      


class ItemLookupCanvas:
    
    def __init__(self):
        self.__layout = [
            [sg.Listbox(values=[], 
                key='_ITEM_NAME_LIST_', 
                size=(60,6),  
                font=("Helvetica Bold", 11), 
                select_mode='LISTBOX_SELECT_MODE_SINGLE', 
                enable_events=True,
                bind_return_key=True)
            ]
        ]

    def get_layout(self):
        return self.__layout
    
    layout = property(get_layout)
    
    
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


class ItemListCanvas:
    def __init__(self):
    
        item_list_layout = [
            [
                sg.Table(values=[], key='_ITEMS_LIST_', enable_events=True,
                     headings= ['Item-code', 'Item-Name', 'Stock', 'Price'],
                     font=(("Helvetica", 11)),
                     auto_size_columns=False,
                     justification='right',
                     row_height=25,
                     alternating_row_color='MistyRose2',
                     num_rows=10,
                     display_row_numbers=False,
                     bind_return_key = True,
                     col_widths=[10, 20, 9, 12],
                     pad=((0,0),(0,5))
                )            
            ],
        ]
        
        self.__layout = [
            [
                sg.Column(item_list_layout, vertical_alignment = 'top', pad = ((0,0),(0,0))),
            ]
        ]

    def get_layout(self):
        return self.__layout
    
    layout = property(get_layout)         
    