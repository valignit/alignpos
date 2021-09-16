import PySimpleGUI as sg
from config import Config
from styles import ElementStyle


class SigninCanvas:

    def __init__(self):
        config = Config()
        self.__language = config.language

        self.__title_en = 'Signin'
        self.__title_ar = 'تسجيل الدخول'
        
        self.__layout_en = [
            [
                sg.Image(filename = config.application_path + '/images/application_logo.PNG', background_color = 'white', pad = ((52,53),(0,0))),
            ],
            [
                sg.Frame('',
                    [
                        [
                            sg.Text('Counter:', background_color = 'grey90', **ElementStyle.search_text, pad=((10,5),(15,5))),
                            sg.Input(key='_SIGNIN_TERMINAL_ID_', readonly='True', size=(15,1), **ElementStyle.search_input, pad=((10,5),(15,5)))          
                        ], 
                        [
                            sg.Text('Branch:', background_color = 'grey90', **ElementStyle.search_text, pad=((10,5),(15,5))),
                            sg.Input(key='_SIGNIN_BRANCH_ID_', readonly='True', size=(15,1), **ElementStyle.search_input, pad=((10,5),(15,5)))          
                        ], 
                        [
                            sg.Text('User Id:', background_color = 'grey90', **ElementStyle.search_text, pad=((10,5),(15,5))),
                            sg.Input(key='_SIGNIN_USER_ID_', size=(15,1), **ElementStyle.search_input, pad=((10,5),(15,5)))          
                        ], 
                        [
                            sg.Text('Password:', background_color = 'grey90', **ElementStyle.search_text, pad=((10,5),(15,5))),
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
        self.__layout_ar = [
            [
                sg.Image(filename = config.application_path + '/images/application_logo.PNG', background_color = 'white', pad = ((52,53),(0,0))),
            
            ],
            [
                sg.Frame('',
                    [
                        [
                            sg.Input(key='_SIGNIN_TERMINAL_ID_', readonly='True', size=(15,1), **ElementStyle.search_input_ar, pad=((10,5),(15,5))),         
                            sg.Text(':رقم المحطة', background_color = 'grey90', **ElementStyle.search_text, pad=((10,5),(15,5))),
                        ], 
                        [
                            sg.Input(key='_SIGNIN_BRANCH_ID_', readonly='True', size=(15,1), **ElementStyle.search_input_ar, pad=((10,5),(15,5))),         
                            sg.Text(':معرف الفرع', background_color = 'grey90', **ElementStyle.search_text, pad=((10,5),(15,5))),
                        ], 
                        [
                            sg.Input(key='_SIGNIN_USER_ID_', size=(15,1), **ElementStyle.search_input_ar, pad=((10,5),(15,5))),         
                            sg.Text(':اسم االمستخدم', background_color = 'grey90', **ElementStyle.search_text, pad=((10,5),(15,5))),
                        ], 
                        [
                            sg.Input(key='_SIGNIN_PASSWD_', size=(15,1), **ElementStyle.search_input_ar, password_char='*', pad=((10,5),(5,5))),         
                            sg.Text(':كلمه السر', background_color = 'grey90', **ElementStyle.search_text, pad=((10,5),(15,5))),
                        ], 
                        [
                            sg.B(key='_CANCEL_', button_text='Esc-يلغي', **ElementStyle.search_button_short, visible=True, pad=((10,12),(15,10))),
                            sg.B(key='_OK_', button_text='Ent-نعم', **ElementStyle.search_button_short, pad=((10,5),(15,10))), 
                        ]
                    ],
                    background_color = 'grey90',
                    border_width = 0,
                    pad=((7,5),(10,10)),
                    element_justification = "right",
                )
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
 

class CustomerListCanvas:
    def __init__(self):
    
        customer_list_layout = [
            [
                sg.Text('Customer No:', size=(12,1),  font=("Helvetica", 11)),     
                sg.Input(key='_CUSTOMER_NUMBER_SEARCH_',
                    font=("Helvetica", 11),
                    size=(15,1),
                    justification = 'right'
                ),
                sg.Text('Mobile No:', size=(12,1),  font=("Helvetica", 11)),     
                sg.Input(key='_MOBILE_NUMBER_SEARCH_',
                    font=("Helvetica", 11),
                    size=(15,1),
                    justification = 'right'
                ),
                sg.Button('Search-F11', **ElementStyle.search_button_short, key='_CUSTOMER_LIST_SEARCH_', pad=((35,0),(0,0))),                                
            ],
            [
                sg.Table(values=[], 
                     key='_CUSTOMERS_LIST_', 
                     enable_events=True,
                     headings= ['Customer-No', 'Mobile-No', 'Name', 'Type', 'Group'],
                     font=("Helvetica", 11),
                     auto_size_columns=False,
                     justification='right',
                     row_height=25,
                     alternating_row_color='MistyRose2',
                     num_rows=10,
                     display_row_numbers=False,
                     bind_return_key = True,
                     col_widths=[12, 12, 30, 15, 15],
                     pad=((5,0),(5,5))
                )            
            ],
            [
                sg.Button('Ok-F12', **ElementStyle.search_button_short, key='_CUSTOMER_LIST_OK_'),                
                sg.Button('Exit-Esc', **ElementStyle.search_button_short, key='_CUSTOMER_LIST_ESC_'), 
            ]             
        ]
        
        self.__layout = [
            [
                sg.Column(customer_list_layout, vertical_alignment = 'top', pad = ((0,0),(0,0))),
            ]
        ]

    def get_layout(self):
        return self.__layout
    
    layout = property(get_layout)         

 