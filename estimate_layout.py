import PySimpleGUI as sg

from common_layout import ElementStyle as ap_style


###
# Estimate Layout               
class EstimateCanvas:
    def __init__(self, fav_items_list):
   
        w, h = sg.Window.get_screen_size()        
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
                sg.Text('', **ap_style.page_title, pad=((0,300),(0,3)), key='_MOBILE_NUMBER_'),
                sg.Button(key='_FIND_', button_text='FIND\nF10',**ap_style.nav_button, pad = ((0,5),(0,0))),
                sg.Button(key='_BEGIN_', button_text='BEGN\nPgUp',**ap_style.nav_button, pad = ((3,5),(0,0))),
                sg.Button(key='_PREVIOUS_', button_text='PREV\n←', **ap_style.nav_button, pad = ((3,5),(0,0))),
                sg.Button(key='_NEXT_', button_text='NEXT\n→', **ap_style.nav_button, pad = ((3,5),(0,0))),
                sg.Button(key='_END_', button_text='END\nPgDn', **ap_style.nav_button, pad = ((3,3),(0,0))),                    
            ]
        ]

        ui_search_pane_layout = [
            [
                sg.Text('Barcode:', **ap_style.search_text),
                sg.Input(key='_BARCODE_', size=(15,1), **ap_style.search_input),
                sg.Button(key='_KEYPAD1_', button_text='⌨', **ap_style.pad_button_small, pad = ((0,0),(0,0))),                
                sg.Text('Item Name:', **ap_style.search_text, pad=((25,0),(0,0))),
                sg.Input(key='_SEARCH_NAME_', size=(35,1), **ap_style.search_input),
                sg.Button(key='_KEYPAD2_', button_text='⌨', **ap_style.pad_button_small, pad = ((0,0),(0,0))), 
                sg.Text('Item Group:', **ap_style.search_text),
                sg.Combo([''], key='_ITEM_GROUP_',default_value = 'None'),                
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
            ],
        ]        
        
        ui_favorite1_pane_layout = [
            [
                sg.Button('ADDON', key='_ADDON_', **ap_style.search_button_wide)
            ],
            [
                sg.Button('BUNDLE', key='_BUNDLE_', **ap_style.search_button_wide)
            ]
        ]

        ui_favorite2_pane_layout = [
            [sg.Button(fav_item, key=fav_item.upper(), **ap_style.search_button_wide)] for fav_item in fav_items_list
        ]
        
        ui_bottom_pane_layout = [
            [
                sg.Image(filename = 'alignpos_logo.PNG', background_color = 'white', pad = ((52,53),(0,0))),
            ]
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
                sg.HorizontalSeparator(color = 'white', pad = ((0,0),(3,3))),
            ],
            [
                sg.Frame('',
                    ui_favorite1_pane_layout, 
                    background_color = 'grey90',
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((4,0),(2,9)),
                )     
            ],
            [
                sg.Frame('',
                    ui_favorite2_pane_layout, 
                    background_color = 'grey90',
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((4,0),(2,3)),
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


class ChangeQtyCanvas:
    def __init__(self):
    
        change_qty_layout = [
            [
                sg.Text('', key='_ITEM_NAME_', size=(25,2),  font=("Helvetica Bold", 14))
            ],
            [
                sg.Text('Existing Quantity:', size=(15,1),  font=("Helvetica", 11)),     
                sg.Input(key='_EXISTING_QTY_',
                    readonly=True, 
                    font=("Helvetica", 11),
                    size=(15,1),
                    justification = 'right'
                )
            ],
            [
                sg.Text('New Quantity:', size=(15,1),  font=("Helvetica", 11), pad=((5,5),(10,10))),             
                sg.Input(key='_NEW_QTY_',
                    readonly=False, 
                    focus=True, 
                    background_color='white',
                    font=("Helvetica", 11),
                    size=(15,1), 
                    enable_events=True,
                    justification = 'right'
                ),
                sg.Button(key='_KEYPAD_', button_text='⌨', **ap_style.pad_button_small, pad = ((0,0),(0,0))),                
            ],
            [
                sg.HorizontalSeparator(color = 'grey99', pad = ((0,0),(20,10)))
            ],                        
            [
                sg.Button('Ok-F12', **ap_style.search_button_short, key='_CHANGE_QTY_OK_'), 
                sg.Button('Exit-Esc', **ap_style.search_button_short, key='_CHANGE_QTY_ESC_'), 
            ]           
        ]
        
        self.__layout = [
            [
                sg.Column(change_qty_layout, vertical_alignment = 'top', pad = None),
            ]
        ]

    def get_layout(self):
        return self.__layout
    
    layout = property(get_layout)         


class EstimateListCanvas:
    def __init__(self):
    
        estimate_list_layout = [
            [
                sg.Text('Estimate No:', size=(15,1),  font=("Helvetica", 11)),     
                sg.Input(key='_ESTIMATE_NUMBER_SEARCH_',
                    font=("Helvetica", 11),
                    size=(15,1),
                    justification = 'right'
                ),
                sg.Text('Mobile No:', size=(15,1),  font=("Helvetica", 11)),     
                sg.Input(key='_MOBILE_NUMBER_SEARCH_',
                    font=("Helvetica", 11),
                    size=(15,1),
                    justification = 'right'
                ),
                sg.Button('Search-F11', **ap_style.search_button_short, key='_ESTIMATE_LIST_SEARCH_', pad=((100,0),(0,0))),                                
            ],
        
            [
                sg.Table(values=[], key='_ESTIMATES_LIST_', enable_events=True,
                     headings= ['Estimate-No', 'Mobile-No', 'Items', 'Total-Amt', 'Tax', 'Net-Amt', 'Discount', 'Roundoff', 'Estimate-Amt'],
                     font=(("Helvetica", 11)),
                     auto_size_columns=False,
                     justification='right',
                     row_height=25,
                     alternating_row_color='MistyRose2',
                     num_rows=10,
                     display_row_numbers=False,
                     col_widths=[10, 12, 5, 9, 9, 9, 9, 9, 12],
                     pad=((5,0),(5,5))
                )            
            ],
            [
                sg.Button('Ok-F12', **ap_style.search_button_short, key='_ESTIMATE_LIST_OK_'),                
                sg.Button('Exit-Esc', **ap_style.search_button_short, key='_ESTIMATE_LIST_ESC_'), 
            ]             
        ]
        
        self.__layout = [
            [
                sg.Column(estimate_list_layout, vertical_alignment = 'top', pad = ((0,0),(0,0))),
            ]
        ]

    def get_layout(self):
        return self.__layout
    
    layout = property(get_layout)         


###
if __name__ == "__main__":
    print('***Not an executable module, please call the main script')
