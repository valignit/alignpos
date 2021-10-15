import PySimpleGUI as sg
from config import Config
from db_nosql import KvDatabase
from styles import ElementStyle
from config import Config


class CashCanvas:
    def __init__(self, denomination_list):

        config = Config()

        w, h = sg.Window.get_screen_size()
        #w = w - 60
        #h = h - 60
        lw = w*73/100
        rw = w*65/100                
        lh = h
        rh = h

        title = 'CASH'
        background_color='DarkSeaGreen1'
        readonly = True
        
        menu_def = [
                ['&File', ['Receipt', 'Payment', '---', 'Exit']],      
                ['&Edit', ['Denom']],      
                ['&Help', 'About']
        ]
        right_click_menu=["that",["Denom"]]          

        ui_header_pane_layout = [
            [
                sg.Text(title, **ElementStyle.page_title, pad=((0,0),(0,3)), background_color=background_color),
            ]
        ]

        ui_search_pane_layout = [
            [
                sg.Text('Trn. Type:', size=(12,1),  font=("Helvetica", 11), background_color=background_color),
                sg.Combo(['', 'Payment', 'Receipt'], key='_TRANSACTION_TYPE_SEARCH_',default_value = '',                
                    font=("Helvetica", 11),
                    size=(15,1),
                ),
                sg.Text('Trn. Context:', size=(12,1),  font=("Helvetica", 11), background_color=background_color),     
                sg.Combo(['', 'Invoice', 'Drawer', 'Change'], key='_TRANSACTION_CONTEXT_SEARCH_',default_value = '',                
                    font=("Helvetica", 11),
                    size=(15,1),
                ),
                sg.Button('Search-F11', **ElementStyle.search_button_short, key='_CASH_LIST_SEARCH_', pad=((35,0),(0,0))),                                
            ]
        ]
        
        ui_detail_pane_layout = [
            [
                sg.Table(values=[], 
                     key='_CASH_LIST_', 
                     enable_events=True,
                     headings= ['SNo.', 'Type', 'Context', 'Reference', 'Date', 'Receipt', 'Payment'],
                     font=("Helvetica", 11),
                     auto_size_columns=False,
                     justification='right',
                     row_height=25,
                     right_click_menu=right_click_menu,
                     alternating_row_color='DarkSeaGreen3',
                     num_rows=17,
                     display_row_numbers=False,
                     bind_return_key = True,
                     col_widths=[15, 10, 10, 15, 20, 12, 12],
                     pad=((5,0),(5,5))
                )            
            ]
        ]
        
        ui_action_pane_layout = [        
            [
                sg.Button('Receipt\nF1', **ElementStyle.action_button, key='_CASH_LIST_RECEIPT_'),                
                sg.Button('Payment\nF2', **ElementStyle.action_button, key='_CASH_LIST_PAYMENT_'),                
                sg.Button('Change\nF3', **ElementStyle.action_button, key='_CASH_LIST_CHANGE_'),                
                sg.Button('Denom\nF4', **ElementStyle.action_button, key='_CASH_LIST_DENOMINATION_', pad=((40,0),(0,0))),                
                sg.Button('Exit\nEsc', **ElementStyle.action_button, key='_CASH_LIST_ESC_', pad=((375,0),(0,0))), 
            ]             
        ]

        ui_footer_pane_layout = [
            [
                sg.Text('USER:', **ElementStyle.footer_text, background_color=background_color),
                sg.Input(key='_USER_ID_', **ElementStyle.footer_input),
                sg.Text('COUNTER:', **ElementStyle.footer_text, background_color=background_color),
                sg.Input(key='_TERMINAL_ID_', **ElementStyle.footer_input),
                sg.Text('BRANCH:', **ElementStyle.footer_text, background_color=background_color),
                sg.Input(key='_BRANCH_ID_', **ElementStyle.footer_input),
                sg.Text('DATE:', **ElementStyle.footer_text, background_color=background_color),
                sg.Input(key='_CURRENT_DATE_', **ElementStyle.footer_input)
            ]
        ]

        ui_top_pane_layout = [
            [
                sg.Image(filename = config.application_path + '/images/client_logo.PNG', background_color = 'white', pad = ((85,55),(0,0)))
            ],
        ]

        ui_summary_pane_layout = [
            [sg.Text(denomination_list[i], size=(12,1), font=("Helvetica", 11)), sg.Input(key=denomination_list[i]+'_count', size=(5,1), **ElementStyle.search_input_ar, readonly = readonly), sg.Input(key=denomination_list[i]+'_amount', size=(10,1), **ElementStyle.search_input_ar, readonly=True)] for i in range(len(denomination_list))  
        ]

        ui_total_pane_layout = [
            [
                sg.Text('Received:', **ElementStyle.summary_text, pad = ((5,15),(15,5))),
                sg.Input(key='_RECEIVED_AMOUNT_', **ElementStyle.summary_input, pad = ((5,5),(15,5))),         
            ],
            [
                sg.Text('Paid:', **ElementStyle.summary_text, pad = ((5,15),(5,5))),
                sg.Input(key='_PAID_AMOUNT_', **ElementStyle.summary_input),
            ],
            [
                sg.Text('Balance:', **ElementStyle.summary_text_bold),
                sg.Input(key='_BALANCE_AMOUNT_', **ElementStyle.summary_input_bold),
            ],
        ]

        ui_bottom_pane_layout = [
            [
                sg.Image(filename = config.application_path + '/images/application_logo.PNG', background_color = 'white', pad = ((72,53),(0,0))),
            ]
        ]

        ui_left_panes_layout = [
            [
                sg.Frame('',
                    ui_header_pane_layout, 
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((5,0),(5,0)),
                    background_color=background_color,
                )     
            ],
            [
                sg.Frame('',
                    ui_search_pane_layout,
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((5,0),(7,5)),
                    background_color=background_color
                )     
            ],
            [
                sg.Frame('',
                    ui_detail_pane_layout,
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((5,0),(0,0)),
                    background_color=background_color,
                )     
            ],
            [
                sg.Frame('',
                    ui_action_pane_layout,
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((5,0),(0,0)),
                    background_color=background_color,
                )     
            ],
            [
                sg.Frame('',
                    ui_footer_pane_layout, 
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((5,0),(10,0)),
                    background_color=background_color,
                )     
            ],
        ]

        ui_right_panes_layout = [
            [
                sg.Frame('',
                    ui_top_pane_layout, 
                    background_color = 'white',
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((0,0),(10,0)),
                )     
            ],
            [
                sg.HorizontalSeparator(color = 'white', pad = ((0,0),(7,0))),
            ],
            [
                sg.Frame('',
                    ui_summary_pane_layout, 
                    background_color = 'white',
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((15,0),(15,10)),
                )     
            ],
            [
                sg.HorizontalSeparator(color = 'white', pad = ((0,0),(7,0))),
            ],
            [
                sg.Frame('',
                    ui_total_pane_layout, 
                    background_color = 'white',
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((15,0),(5,10)),
                )     
            ],
            [
                sg.HorizontalSeparator(color = 'white', pad = ((0,0),(20,3))),
            ],
           [
                sg.Frame('',
                    ui_bottom_pane_layout, 
                    background_color = 'white',
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((0,0),(10,0)),
                )     
            ],
        ]

        
        self.__layout = [
            [
                sg.Menu(menu_def, tearoff=False, font=(("Helvetica", 10))),
                sg.Column(
                    ui_left_panes_layout,
                    key='_LEFT_PANES_',
                    size=(lw,lh),
                    justification = 'Left',
                    vertical_alignment = 'top', 
                    background_color=background_color,
                ),
                sg.Column(
                    ui_right_panes_layout,
                    key='_RIGHT_PANES_',
                    background_color='White',
                    size=(rw,rh),
                    justification = 'Center',
                    vertical_alignment = 'top', 
                )   
            ]      
        ]


    def get_layout(self):
        return self.__layout
    
    layout = property(get_layout)         


class DrawerTrnCanvas:
    def __init__(self, transaction_type):
    
        drawer_trn_layout = [
            [
                sg.Text(transaction_type, key='_TRANSACTION_TYPE_', size=(25,2),  font=("Helvetica Bold", 14))
            ],
            [
                sg.Text(transaction_type + ' Amount:', size=(15,1), font=("Helvetica", 11), pad=((5,5),(10,10))),             
                sg.Input(key='_TRANSACTION_AMOUNT_',
                    readonly=False, 
                    focus=True, 
                    background_color='white',
                    font=("Helvetica", 11),
                    size=(15,1), 
                    enable_events=True,
                    justification = 'right'
                ),
                sg.Button(key='_KEYPAD_', button_text='⌨', **ElementStyle.pad_button_small, pad = ((0,10),(0,0))),                
                sg.Button('$', key='_CASH_DENOMINATION_', **ElementStyle.pad_button_small, pad = ((0,10),(0,0)))                
            ],
            [
                sg.Text('User Id:', size=(15,1), font=("Helvetica", 11), pad=((5,5),(5,10))),
                sg.Input(key='_SUPERVISOR_USER_ID_', size=(15,1), font=("Helvetica", 11), pad=((5,5),(5,10)))          
            ], 
            [
                sg.Text('Password:', size=(15,1), font=("Helvetica", 11), pad=((5,5),(5,0))),
                sg.Input(key='_SUPERVISOR_PASSWD_', size=(15,1), font=("Helvetica", 11), password_char='*', pad=((5,5),(5,0)))          
            ], 
            [
                sg.HorizontalSeparator(color = 'grey99', pad = ((0,0),(20,10)))
            ],                        
            [
                sg.Button('Ok-F12', **ElementStyle.search_button_short, key='_DRAWER_TRN_OK_', pad = ((10,10),(0,15))), 
                sg.Button('Exit-Esc', **ElementStyle.search_button_short, key='_DRAWER_TRN_ESC_', pad = ((0,0),(0,15))), 
            ]           
        ]
        
        self.__layout = [
            [
                sg.Column(drawer_trn_layout, key='_DRAWER_TRN_', vertical_alignment = 'top'),
            ]
        ]

    def get_layout(self):
        return self.__layout
    
    layout = property(get_layout)         


class DrawerChangeCanvas:
    def __init__(self):
    
        drawer_exchange_layout = [
            [
                sg.Text('Cash Change', size=(25,2),  font=("Helvetica Bold", 14))
            ],
            [
                sg.Text('REC      PAY', font=("Helvetica 9 bold"), pad=((328,0),(0,0))),             
            ],
            [
                sg.Text('Amount:', size=(15,1), font=("Helvetica", 11), pad=((5,5),(10,10))),             
                sg.Input(key='_CHANGE_AMOUNT_',
                    readonly=False, 
                    focus=True, 
                    background_color='white',
                    font=("Helvetica", 11),
                    size=(15,1), 
                    enable_events=True,
                    justification = 'right'
                ),
                sg.Button(key='_KEYPAD_', button_text='⌨', **ElementStyle.pad_button_small, pad = ((0,10),(0,0))),                
                sg.Button('$', key='_FROM_DENOMINATION_', **ElementStyle.pad_button_small, pad = ((0,10),(0,0))),                
                sg.Button('$', key='_TO_DENOMINATION_', **ElementStyle.pad_button_small, pad = ((0,10),(0,0)))                
            ],
            [
                sg.HorizontalSeparator(color = 'grey99', pad = ((0,0),(20,10)))
            ],                        
            [
                sg.Button('Ok-F12', **ElementStyle.search_button_short, key='_DRAWER_CHANGE_OK_', pad = ((10,10),(0,15))), 
                sg.Button('Exit-Esc', **ElementStyle.search_button_short, key='_DRAWER_CHANGE_ESC_', pad = ((0,0),(0,15))), 
            ]           
        ]
        
        self.__layout = [
            [
                sg.Column(drawer_exchange_layout, key='_DRAWER_CHANGE_', vertical_alignment = 'top'),
            ]
        ]

    def get_layout(self):
        return self.__layout
    
    layout = property(get_layout)         



 
