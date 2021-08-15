import PySimpleGUI as sg

from common_layout import ElementStyle as ap_style


###
# Invoice Layout               
class InvoiceCanvas:
    def __init__(self, fav_item_codes_list, fav_item_names_list, fast_item_codes_list, fast_item_names_list):
   
        w, h = sg.Window.get_screen_size()        
        lw = w*78/100
        rw = w*25/100                
        lh = h
        rh = h
        background_color='LightCyan',

        menu_def = [
                ['&File', ['New', 'Delete', 'Save', 'Submit', 'Print', '---', 'Exit']],      
                ['&Edit', ['Specs', 'Quantity', 'Weight', 'Price', '---', 'Add', 'Less', '---', 'Addon', 'Bundle' ]],      
                ['&View', ['First', 'Previous', 'Next',  'Last']],      
                ['&Help', 'About'], 
        ]
        
        ui_header_pane_layout = [
            [
                sg.Text('BILL', **ap_style.page_title, pad=((0,0),(0,3)), background_color=background_color),
                sg.Text('', **ap_style.page_title, pad=((0,0),(0,3)), key='_BILL_NUMBER_', background_color=background_color),
                sg.Text('', **ap_style.page_title, pad=((0,264),(0,3)), key='_MOBILE_NUMBER_', background_color=background_color),
                sg.Button(key='_FIND_', button_text='FIND\nF10',**ap_style.action_button, pad = ((0,7),(0,0))),
                sg.Button(key='_BEGIN_', button_text='BEGN\nHome',**ap_style.nav_button, pad = ((3,5),(0,0))),
                sg.Button(key='_PREVIOUS_', button_text='PREV\n←', **ap_style.nav_button, pad = ((3,5),(0,0))),
                sg.Button(key='_NEXT_', button_text='NEXT\n→', **ap_style.nav_button, pad = ((3,5),(0,0))),
                sg.Button(key='_END_', button_text='END\nEnd', **ap_style.nav_button, pad = ((3,3),(0,0))),                    
            ]
        ]

        ui_search_pane_layout = [
            [
                sg.Text('Barcode:', **ap_style.search_text, background_color=background_color),
                sg.Input(key='_BARCODE_', size=(15,1), **ap_style.search_input),
                sg.Button(key='_KEYPAD1_', button_text='⌨', **ap_style.pad_button_small, pad = ((0,0),(0,0))),                
                sg.Text('Item Name:', **ap_style.search_text, pad=((25,0),(0,0)), background_color=background_color),
                sg.Input(key='_SEARCH_NAME_', size=(35,1), **ap_style.search_input),
                sg.Button(key='_KEYPAD2_', button_text='⌨', **ap_style.pad_button_small, pad = ((0,0),(0,0))), 
                sg.Text('Item Group:', **ap_style.search_text, background_color=background_color),
                sg.Combo([''], key='_ITEM_GROUP_',default_value = 'None'),                
            ]
        ]

        ui_favorite_pane_layout = [
            [
                sg.Column(
                    [ 
                        [
                            sg.Button(fav_item_codes_list[fav_count] + ' (Alt-' + str(fav_count) + ')', 
                                key='FAV_'+fav_item_codes_list[fav_count], 
                                **ap_style.fav_button, 
                                pad=((0,0),(0,0)),
                            ) for fav_count, fav_item_name in enumerate(fav_item_names_list, start=0)
                        ] 
                    ],
                    size=(958,105), background_color=background_color,
                )
            ]
        ]

        ui_detail_pane_layout = [
            [
                sg.Table(values=[], key='_ITEMS_LIST_', enable_events=True,
                     headings= ['Item code', 'Barcode', 'Item Name', 'Unit', 'Qty', 'Price', 'Amount', 'Tax Rate', 'Tax', 'Net'],
                     font=(("Helvetica", 11)),
                     auto_size_columns=False,
                     justification='right',
                     row_height=24,
                     alternating_row_color='LightSkyBlue1',
                     num_rows=14,
                     display_row_numbers=True,
                     right_click_menu=["that",["Specs","Quantity","Weight", "Price", "---", "Add", "Less", "---", "Delete"]],
                     bind_return_key=True,
                     col_widths=[10, 13, 24, 5, 5, 8, 9, 8, 10, 10],
                )            
            ],
        ]

        ui_action_pane_layout = [
            [
                sg.Button(key='F1',  button_text='\nF1', **ap_style.action_button, pad=((3,5),(5,0))),
                sg.Button(key='F2',  button_text='\nF2', **ap_style.action_button, pad=((0,5),(5,0))),
                sg.Button(key='F3',  button_text='\nF3', **ap_style.action_button, pad=((0,5),(5,0))),
                sg.Button(key='F4',  button_text='\nF4', **ap_style.action_button, pad=((0,5),(5,0))),
                sg.Button(key='F5',  button_text='\nF5', **ap_style.action_button, pad=((0,25),(5,0))),
                sg.Button(key='F6',  button_text='\nF6', **ap_style.action_button_small, pad=((0,5),(5,0))),
                sg.Button(key='F7',  button_text='\nF7', **ap_style.action_button_small, pad=((0,5),(5,0))),
                sg.Button(key='F8',  button_text='\nF8', **ap_style.action_button_small, pad=((0,5),(5,0))),
                sg.Button(key='F9',  button_text='\nF9', **ap_style.action_button_small, pad=((0,5),(5,0))),
                sg.Button(key='+',  button_text='\n+', **ap_style.action_button_small, pad=((20,5),(5,0))),
                sg.Button(key='-',  button_text='\n-', **ap_style.action_button_small, pad=((0,5),(5,0))),
                sg.Button(key='ESC', button_text='Exit\nEsc', **ap_style.exit_button, pad=((20,0),(5,0))),
            ]               
        ]

        ui_footer_pane_layout = [
            [
                sg.Text('USER:', **ap_style.footer_text, background_color=background_color),
                sg.Input(key='_USER_ID_', **ap_style.footer_input),
                sg.Text('COUNTER:', **ap_style.footer_text, background_color=background_color),
                sg.Input(key='_TERMINAL_ID_', **ap_style.footer_input),
                sg.Text('DATE:', **ap_style.footer_text, background_color=background_color),
                sg.Input(key='_CURRENT_DATE_', **ap_style.footer_input)
            ]
        ]

        ui_top_pane_layout = [
            [
                sg.Image(filename = 'images/al_fareeda_logo.PNG', background_color = 'white', pad = ((55,55),(0,0)))
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
                sg.Text('Billed:', **ap_style.summary_text_bold, pad=((5,0),(10,0))),
                sg.Input(key='_INVOICE_AMOUNT_', **ap_style.summary_input_bold, pad=((0,0),(10,10))),
            ],
            [
                sg.Text('Paid:', **ap_style.summary_text_bold ,pad=((5,0),(5,0))),
                sg.Input(key='_PAID_AMOUNT_', **ap_style.summary_input_bold, pad=((0,0),(0,10)))
            ]            
        ]        
        
        ui_tools_pane_layout = [
            [
                sg.Button('ADDON  (Alt-A)', key='Addon', **ap_style.search_button_wide)
            ],
            [
                sg.Button('BUNDLE  (Alt-B)', key='Bundle', **ap_style.search_button_wide)
            ],
        ]

        ui_fast_pane_layout = [
            [sg.Button(fast_item + '  (Alt-' + chr(count + 73) + ')', key='FAST_'+fast_item_codes_list[count], **ap_style.search_button_wide)] for count, fast_item in enumerate(fast_item_names_list, start=0)
        ]
        
        ui_bottom_pane_layout = [
            [
                sg.Image(filename = 'images/alignpos_logo.PNG', background_color = 'white', pad = ((52,53),(0,0))),
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
                    background_color=background_color,
                )     
            ],
            [
                sg.Frame('',
                    ui_favorite_pane_layout,
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((2,0),(0,0)),
                    background_color=background_color,
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
                    pad = ((5,0),(5,0)),
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
                    pad = ((15,0),(2,0)),
                )     
            ],
            [
                sg.HorizontalSeparator(color = 'white', pad = ((0,0),(3,3))),
            ],
            [
                sg.Frame('',
                    ui_tools_pane_layout, 
                    background_color = 'grey90',
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((4,0),(2,9)),
                )     
            ],
            [sg.Text('Fast moving:', **ap_style.summary_text_bold, pad=((5,0),(10,0)))],                              
            [
                sg.Frame('',
                    ui_fast_pane_layout, 
                    background_color = 'grey90',
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((4,0),(2,20)),
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
                    background_color=background_color,
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


class InvoiceListCanvas:
    def __init__(self):
    
        invoice_list_layout = [
            [
                sg.Text('Invoice No:', size=(15,1),  font=("Helvetica", 11)),     
                sg.Input(key='_INVOICE_NUMBER_SEARCH_',
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
                sg.Button('Search-F11', **ap_style.search_button_short, key='_INVOICE_LIST_SEARCH_', pad=((100,0),(0,0))),                                
            ],
        
            [
                sg.Table(values=[], key='_INVOICES_LIST_', enable_events=True,
                     headings= ['Invoice-No', 'Mobile-No', 'Items', 'Total-Amt', 'Tax', 'Net-Amt', 'Discount', 'Roundoff', 'Invoice-Amt'],
                     font=(("Helvetica", 11)),
                     auto_size_columns=False,
                     justification='right',
                     row_height=25,
                     alternating_row_color='MistyRose2',
                     num_rows=10,
                     display_row_numbers=False,
                     bind_return_key = True,
                     col_widths=[10, 12, 5, 9, 9, 9, 9, 9, 12],
                     pad=((5,0),(5,5))
                )            
            ],
            [
                sg.Button('Ok-F12', **ap_style.search_button_short, key='_INVOICE_LIST_OK_'),                
                sg.Button('Exit-Esc', **ap_style.search_button_short, key='_INVOICE_LIST_ESC_'), 
            ]             
        ]
        
        self.__layout = [
            [
                sg.Column(invoice_list_layout, vertical_alignment = 'top', pad = ((0,0),(0,0))),
            ]
        ]

    def get_layout(self):
        return self.__layout
    
    layout = property(get_layout)         


###
if __name__ == "__main__":
    print('***Not an executable module, please call the main script')
