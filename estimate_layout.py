import PySimpleGUI as sg
from common_layout import ElementStyle as ap_style


###
# Estimate Layout               
class EstimateLayout:
    def __init__(self, config, w, h):
        sg.theme(config["ui_theme"])
        lw = w*78/100
        rw = w*25/100                
        lh = h
        rh = h

        menu_def = [
                ['&File', ['&New', '&Delete', '&Save', 'S&ubmit', '&Print', 'E&xit']],      
                ['&Edit', ['&Specs', '&Quantity', '&Weight', '&Price', '&Addon', '&Bundle' ]],      
                ['&View', ['&First', '&Previous', '&Next',  '&Last']],      
                ['&Help', '&About'], 
        ]
        
        ui_header_pane_layout = [
            [
                sg.Text('Estimate', **ap_style.page_title, pad=((0,0),(0,3))),
                sg.Text('', **ap_style.page_title, pad=((0,0),(0,3)), key='_ESTIMATE_NUMBER_'),
                sg.Text('', **ap_style.page_title, pad=((0,350),(0,3)), key='_MOBILE_NUMBER_'),
                sg.Button(key='_BEGIN_', button_text='BEGN\nPgUp',**ap_style.nav_button, pad = ((0,5),(0,0))),
                sg.Button(key='_PREVIOUS_', button_text='PREV\n←', **ap_style.nav_button, pad = ((3,5),(0,0))),
                sg.Button(key='_NEXT_', button_text='NEXT\n→', **ap_style.nav_button, pad = ((3,5),(0,0))),
                sg.Button(key='_END_', button_text='END\nPgDn', **ap_style.nav_button, pad = ((3,3),(0,0))),                    
            ]
        ]

        ui_search_pane_layout = [
            [
                sg.Text('Barcode:', **ap_style.search_text),
                sg.Input(key='_BARCODE_', size=(15,1), **ap_style.search_input),
                sg.Text('Item Name:', **ap_style.search_text, pad=((20,0),(0,0))),
                sg.Input(key='_ITEM_NAME_', size=(38,1), **ap_style.search_input),
                sg.Button(key='_ADDON_', button_text='Addon-F11', **ap_style.search_button, pad = ((100,0),(0,0))),
                sg.Button(key='_BUNDLE_', button_text='Bundle-F12', **ap_style.search_button, pad = ((5,3),(0,0)))                       
            ]
        ]

        ui_detail_pane_layout = [
            [
                sg.Table(values=[], key='_ITEMS_LIST_', enable_events=True,
                     headings= ['Item code', 'Barcode', 'Item Name', 'Unit', 'Qty', 'Price', 'Amount', 'Tax Rate', 'Tax', 'Net'],
                     font=(("Helvetica", 11)),
                     auto_size_columns=False,
                     justification='right',
                     row_height=25,
                     alternating_row_color='MistyRose2',
                     num_rows=18,
                     display_row_numbers=True,
                     col_widths=[10, 13, 24, 5, 5, 8, 9, 8, 10, 10],
                )            
            ]        
        ]

        ui_action_pane_layout = [
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
                sg.Button(key='ESC', button_text='Exit\nEsc', **ap_style.exit_button, pad=((65,0),(0,0))),
            ]               
        ]

        ui_footer_pane_layout = [
            [
                sg.Text('USER:', **ap_style.footer_text),
                sg.Input(key='_USER_ID_', **ap_style.footer_input),
                sg.Text('COUNTER:', **ap_style.footer_text),
                sg.Input(key='_TERMINAL_ID_', **ap_style.footer_input),
                sg.Text('DATE:', **ap_style.footer_text),
                sg.Input(key='_CURRENT_DATE_', **ap_style.footer_input)
            ]
        ]

        ui_top_pane_layout = [
            [
                sg.Image(filename = 'al_fareeda_logo.PNG', background_color = 'white', pad = ((55,55),(0,0)))
            ],
        ]

        ui_summary_pane_layout = [
            [
                sg.Text('Line Items:', **ap_style.summary_text, pad = ((5,5),(10,5))),
                sg.Input(key='_LINE_ITEMS_', **ap_style.summary_input, pad = ((5,5),(10,5)))          
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
                sg.Text('Estimate:', **ap_style.summary_text_bold, pad=((5,0),(10,10))),
                sg.Input(key='_ESTIMATE_AMOUNT_', **ap_style.summary_input_bold, pad=((0,0),(10,10))),
            ]                
        ]        
        
        ui_keypad_pane_layout = [
            [
                sg.Button(key='UP', button_text='↑', **ap_style.pad_button, pad = ((6,3),(6,3))),
                sg.Button(key='T7', button_text='7', **ap_style.pad_button, pad = ((3,3),(6,3))),
                sg.Button(key='T8', button_text='8', **ap_style.pad_button, pad = ((3,3),(6,3))),
                sg.Button(key='T9', button_text='9', **ap_style.pad_button, pad = ((3,6),(6,3))),                    
            ],
            [
                sg.Button(key='DOWN', button_text='↓', **ap_style.pad_button, pad = ((6,3),(3,3))),
                sg.Button(key='T4', button_text='4', **ap_style.pad_button, pad = ((3,3),(3,3))),
                sg.Button(key='T5', button_text='5', **ap_style.pad_button, pad = ((3,3),(3,3))),
                sg.Button(key='T6', button_text='6', **ap_style.pad_button, pad = ((3,6),(3,3))),                    
            ],
            [
                sg.Button(key='RIGHT', button_text='→', **ap_style.pad_button, pad = ((6,3),(3,3))),
                sg.Button(key='T1', button_text='1', **ap_style.pad_button, pad = ((3,3),(3,3))),
                sg.Button(key='T2', button_text='2', **ap_style.pad_button, pad = ((3,3),(3,3))),
                sg.Button(key='T3', button_text='3', **ap_style.pad_button, pad = ((3,6),(3,3))),                    
                
            ],
            [
                sg.Button(key='LEFT', button_text='←', **ap_style.pad_button, pad = ((6,3),(3,3))),
                sg.Button(key='T0', button_text='0', **ap_style.pad_button, pad = ((3,3),(3,3))),
                sg.Button(key='ENTER',button_text='ENTER', **ap_style.pad_button_wide, pad = ((3,6),(3,3))),
            ],            
            [
                sg.Button(key='BACKSPACE', button_text='\u232B', **ap_style.pad_button, pad = ((6,3),(3,6))),
                sg.Button(key='FULL_STOP', button_text='.', **ap_style.pad_button, pad = ((3,3),(3,6))),                    
                sg.Button(key='DEL', button_text='DEL', **ap_style.pad_button, pad = ((3,3),(3,6))),                    
                sg.Button(key='TAB', button_text='TAB', **ap_style.pad_button, pad = ((3,3),(3,6))),                    
            ],            
        ]

        ui_bottom_pane_layout = [
            [
                sg.Image(filename = 'alignpos_logo.PNG', background_color = 'white', pad = ((52,53),(0,0))),
            ]
        ]
        
        ui_temp_layout = [
            [
                sg.Graph(canvas_size=(300, 400), graph_bottom_left=(0,0), graph_top_right=(400, 400), background_color = None, key='graph')
            ],      
        ]
        
        ui_left_panes_layout = [
            [
                sg.Frame('',
                    ui_header_pane_layout, 
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((5,0),(5,0)),
                )     
            ],
            [
                sg.Frame('',
                    ui_search_pane_layout,
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((5,0),(7,5)),
                )     
            ],
            [
                sg.Frame('',
                    ui_detail_pane_layout,
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((5,0),(0,0)),
                )     
            ],
            [
                sg.Frame('',
                    ui_action_pane_layout,
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((5,0),(0,0)),
                )     
            ],
            [
                sg.Frame('',
                    ui_footer_pane_layout, 
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((5,0),(5,0)),
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
                    pad = ((15,0),(2,0)),
                )     
            ],
            [
                sg.HorizontalSeparator(color = 'white', pad = ((0,0),(0,3))),
            ],
            [
                sg.Frame('',
                    ui_keypad_pane_layout, 
                    background_color = 'white',
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((23,0),(0,0)),
                )     
            ],
            [
                sg.HorizontalSeparator(color = 'white', pad = ((0,0),(5,10))),
            ],
            [
                sg.Frame('',
                    ui_bottom_pane_layout, 
                    background_color = 'white',
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((0,0),(13,0)),
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
                    #pad = ((0,0),(0,0)), 
                ),
                sg.Column(
                    ui_right_panes_layout,
                    key='_RIGHT_PANES_',
                    background_color='White',
                    size=(rw,rh), 
                    justification = 'Center',
                    vertical_alignment = 'top', 
                    #pad = ((0,0),(0,0)), 
                )   
            ]      
        ]


    def get_layout(self):
        return self.__layout

    layout = property(get_layout) 


###
if __name__ == "__main__":
    print('***Not an executable module, please call the main script')
