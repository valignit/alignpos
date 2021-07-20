import PySimpleGUI as sg
from common_layout import ElementStyle as ap_style


###
# Estimate Layout               
class EstimateLayout:
    def __init__(self, config, w, h):
        sg.theme(config["ui_theme"])
        lw = w*78/100
        rw = w*22/100                
        lh = h
        rh = h
        
        menu_def = [
                ['&File', ['&New', '&Delete', '&Save', 'S&ubmit', '&Print', 'E&xit']],      
                ['&Edit', ['&Specs', '&Quantity', '&Weight',  '&Price']],      
                ['&Help', '&About'], 
        ]

        ui_title_pane_layout = [
            [
                sg.Column(
                [
                    [
                        sg.Image(filename = 'alignpos_logo.PNG', background_color = 'white'),
                        sg.Text('ESTIMATE', **ap_style.page_title, pad=((40,20),(0,0))),
                        sg.Text('USER:', **ap_style.title_text),
                        sg.Input(key='_USER_ID_', **ap_style.title_input),
                        sg.Text('COUNTER:', **ap_style.title_text),
                        sg.Input(key='_TERMINAL_ID_', **ap_style.title_input),
                        sg.Text('DATE:', **ap_style.title_text),
                        sg.Input(key='_CURRENT_DATE_', **ap_style.title_input)
                    ]
                ], background_color = 'white')
            ]
        ]

        ui_header_pane_layout = [
            [
                sg.Column(
                [
                    [
                        sg.Text('Estimate:', **ap_style.header_text),
                        sg.Input(key='_ESTIMATE_NUMBER_', **ap_style.header_input),
                        sg.Text('Mobile:', **ap_style.header_text, pad=((70,0),(0,0))),
                        sg.Input(key='_MOBILE_NUMBER_', **ap_style.header_input),
                        sg.Button(key='_BEGIN_', button_text='BEGN\nPgUp',**ap_style.nav_button, pad = ((285,0),(0,0))),
                        sg.Button(key='_PREVIOUS_', button_text='PREV\n←', **ap_style.nav_button, pad = ((10,0),(0,0))),
                        sg.Button(key='_NEXT_', button_text='NEXT\n→', **ap_style.nav_button, pad = ((10,0),(0,0))),
                        sg.Button(key='_END_', button_text='END\nPgDn', **ap_style.nav_button, pad = ((10,0),(0,0))),    
                    ]
                ])    
            ]
        ]

        ui_search_pane_layout = [
            [
                sg.Column(
                [
                    [
                        sg.Text('Barcode:', **ap_style.search_text),
                        sg.Input(key='_BARCODE_', size=(15,1), **ap_style.search_input),
                        sg.Text('Item Name:', **ap_style.search_text, pad=((20,0),(0,0))),
                        sg.Input(key='_ITEM_NAME_', size=(38,1), **ap_style.search_input),
                        sg.Button(key='_ADDON_', button_text='Addon-F11', **ap_style.search_button, pad = ((8,0),(0,0))),
                        sg.Button(key='_BUNDLE_', button_text='Bundle-F12', **ap_style.search_button, pad = ((10,0),(0,0)))                       
                    ]
                ])   
            ]
        ]
    
        ui_detail_pane_layout = [
            [
                sg.Column(
                [
                    [
                        sg.Table(values=[], key='_ITEMS_LIST_', enable_events=True,
                             headings= ['Item code', 'Barcode', 'Item Name', 'Unit', 'Qty', 'Price', 'Amount', 'Tax Rate', 'Tax', 'Net'],
                             font=(("Helvetica", 11)),
                             auto_size_columns=False,
                             justification='right',
                             row_height=25,
                             alternating_row_color='MistyRose2',
                             num_rows=13,
                             display_row_numbers=True,
                             col_widths=[10, 13, 21, 5, 5, 8, 9, 8, 10, 10],
                        )            
                    ]        
                ])    
            ]
        ]

        ui_action_pane_layout = [
            [
                sg.Column(
                [
                    [
                        sg.Button(key='F1',  button_text='\nF1', **ap_style.action_button),
                        sg.Button(key='F2',  button_text='\nF2', **ap_style.action_button),
                        sg.Button(key='F3',  button_text='\nF3', **ap_style.action_button),
                        sg.Button(key='F4',  button_text='\nF4', **ap_style.action_button),
                        sg.Button(key='F5',  button_text='\nF5', **ap_style.action_button),
                        sg.Button(key='F6',  button_text='\nF6', **ap_style.action_button),
                        sg.Button(key='F7',  button_text='\nF7', **ap_style.action_button),
                        sg.Button(key='F8',  button_text='\nF8', **ap_style.action_button),
                        sg.Button(key='F9',  button_text='\nF9', **ap_style.action_button),
                        sg.Button(key='ESC', button_text='Exit\nEsc', **ap_style.exit_button, pad=((55,0),(0,0))),
                    ]               
                ])    
            ]
        ]

        ui_company_pane_layout = [
            [
                sg.Column(
                [
                    [
                        sg.Image(filename = 'al_fareeda_logo.PNG', background_color = 'white')
                    ]
                ], vertical_alignment = 'top', pad=(38,0), background_color = 'white')
            ]
        ]

        ui_summary_pane_layout = [
            [
                sg.Column(
                [
                    [
                        sg.Text('Line Items:', **ap_style.summary_text),
                        sg.Input(key='_LINE_ITEMS_', **ap_style.summary_input)          
                    ],
                    [
                        sg.Text('Total Amount:', **ap_style.summary_text),
                        sg.Input(key='_TOTAL_AMOUNT_', **ap_style.summary_input),
                    ],
                    [
                        sg.Text('Tax:', **ap_style.summary_text),
                        sg.Input(key='_TOTAL_TAX_AMOUNT_', **ap_style.summary_input),
                    ],
                    [
                        sg.Text('Net Amount:', **ap_style.summary_text),
                        sg.Input(key='_NET_AMOUNT_', **ap_style.summary_input),
                    ],
                    [
                        sg.Text('Discount:', **ap_style.summary_text),
                        sg.Input(key='_DISCOUNT_AMOUNT_', **ap_style.summary_input),
                    ],
                    [
                        sg.Text('Roundoff:', **ap_style.summary_text),
                        sg.Input(key='_ROUNDOFF_AMOUNT_', **ap_style.summary_input),
                    ],
                    [
                        sg.Text('Estimate:', **ap_style.summary_text_bold, pad=((5,0),(15,0))),
                        sg.Input(key='_ESTIMATE_AMOUNT_', **ap_style.summary_input_bold, pad=((0,0),(12,0))),
                    ]                
                ], vertical_alignment = 'top', pad = ((5,0),(5,0)))           
            ]
        ]        

        ui_keypad_pane_layout = [
            [
                sg.Column(
                [
                    [
                        sg.Button(key='UP', button_text='↑', **ap_style.pad_button),
                        sg.Button(key='T7', button_text='7', **ap_style.pad_button),
                        sg.Button(key='T8', button_text='8', **ap_style.pad_button),
                        sg.Button(key='T9', button_text='9', **ap_style.pad_button),                    
                    ],
                    [
                        sg.Button(key='DOWN', button_text='↓', **ap_style.pad_button),
                        sg.Button(key='T4', button_text='4', **ap_style.pad_button),
                        sg.Button(key='T5', button_text='5', **ap_style.pad_button),
                        sg.Button(key='T6', button_text='6', **ap_style.pad_button),                    
                    ],
                    [
                        sg.Button(key='RIGHT', button_text='→', **ap_style.pad_button),
                        sg.Button(key='T1', button_text='1', **ap_style.pad_button),
                        sg.Button(key='T2', button_text='2', **ap_style.pad_button),
                        sg.Button(key='T3', button_text='3', **ap_style.pad_button),                    
                        
                    ],
                    [
                        sg.Button(key='LEFT', button_text='←', **ap_style.pad_button),
                        sg.Button(key='T0', button_text='0', **ap_style.pad_button),
                        sg.Button(key='ENTER',button_text='ENTER', **ap_style.pad_button_wide),
                    ],            
                    [
                        sg.Button(key='BACKSPACE', button_text='\u232B', **ap_style.pad_button),
                        sg.Button(key='FULL_STOP', button_text='.', **ap_style.pad_button),                    
                        sg.Button(key='DEL', button_text='DEL', **ap_style.pad_button),                    
                        sg.Button(key='TAB', button_text='TAB', **ap_style.pad_button),                    
                    ],            
                ], vertical_alignment = 'top', pad = ((6,0),(4,0)))    
            ]
        ]

        ui_left_panes_layout = [
            [
                sg.Column(ui_title_pane_layout, 
                    size=(lw*97.5/100,lh*5.5/100),
                    vertical_alignment = 'top',
                    pad = ((10,10),(0,0)),
                    background_color = 'white'
                )     
            ],
            [
                sg.Column(ui_header_pane_layout, 
                    size=(lw*97.5/100,lh*8/100),
                    vertical_alignment = 'top',
                    pad = ((10,10),(10,0))
                )     
            ],
            [
                sg.Column(ui_search_pane_layout, 
                    size=(lw*97.5/100,lh*5.5/100),
                    vertical_alignment = 'top',
                    pad = ((10,10),(10,0))
                )     
            ],
            [
                sg.Column(ui_detail_pane_layout, 
                    size=(lw*97.5/100,lh*51/100),
                    vertical_alignment = 'top',
                    pad = ((10,10),(10,0)),
                )     
            ],
            [
                sg.Column(ui_action_pane_layout, 
                    size=(lw*97.5/100,lh*9/100),
                    vertical_alignment = 'top',
                    pad = ((10,10),(10,0))
                )     
            ],
        ]

        ui_right_panes_layout = [
            [
                sg.Column(ui_company_pane_layout, 
                    size=(rw*77/100,rh*10/100),
                    vertical_alignment = 'top',
                    pad = ((10,10),(10,0)), 
                    background_color = 'white'
                )     
            ],
            [
                sg.Column(ui_summary_pane_layout, 
                    size=(rw*77/100,rh*31/100),
                    vertical_alignment = 'top',
                    pad = ((10,10),(10,0))
                )     
            ],
            [
                sg.Column(ui_keypad_pane_layout, 
                    size=(rw*77/100,rh*39.5/100),
                    vertical_alignment = 'top',
                    pad = ((10,10),(10,0))
                )     
            ],
        ]

        self.__layout = [
            [
                sg.Menu(menu_def, tearoff=False, font=(("Helvetica", 10))),
                sg.Column(ui_left_panes_layout,
                    background_color = 'white',
                    size=(lw,lh), 
                    vertical_alignment = 'top', 
                    pad = None, 
                ),
                sg.Column(ui_right_panes_layout,
                    background_color = 'white',
                    size=(rw,rh), 
                    vertical_alignment = 'top', 
                    pad = None
                )   
            ]      
        ]


    def get_layout(self):
        return self.__layout

    layout = property(get_layout) 


###
if __name__ == "__main__":
    print('***Not an executable module, please call the main script')
