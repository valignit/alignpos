import PySimpleGUI as sg

from styles import ElementStyle as ap_style
from utilities import Config


###
# Invoice Layout               
class InvoiceCanvas:
    def __init__(self, type, fav_item_codes_list, fav_item_names_list, fast_item_codes_list, fast_item_names_list):

        title = type.upper() + ' INVOICE'
        
        config = Config()
        
        w, h = sg.Window.get_screen_size()        
        lw = w*78/100
        rw = w*25/100                
        lh = h
        rh = h
        
        if type == 'draft':
            background_color='PaleTurquoise1'
            alternating_row_color = 'LightSkyBlue1'
            item_rows = 13
            bottom_pane_top = 16
            print_left_pad = 0
            exit_left_pad = 20          
        else:
            background_color='LemonChiffon'
            alternating_row_color = 'Khaki'        
            item_rows = 19
            bottom_pane_top = 24
            print_left_pad = 4
            exit_left_pad = 775         

        if type == 'draft':
            menu_def = [
                    ['&File', ['New', 'Delete', 'Save', 'Submit', 'Print', '---', 'Exit']],      
                    ['&Edit', ['Specs', 'Quantity', 'Weight', 'Discount', '---', 'Add', 'Less', '---', 'Addon', 'Bundle' ]],      
                    ['&View', ['First', 'Previous', 'Next',  'Last']],      
                    ['&Help', 'About']
            ]
            right_click_menu=["that",["Specs","Quantity","Weight", "Discount", "---", "Add", "Less", "---", "Delete"]]          
        else:
            menu_def = [
                    ['&File', ['Print', '---', 'Exit']],      
                    ['&View', ['First', 'Previous', 'Next',  'Last']],      
                    ['&Help', 'About'], 
            ]
            right_click_menu=["that",[]]   
        
        ui_header_pane_layout = [
            [
                sg.Text(title, **ap_style.page_title, pad=((0,0),(0,3)), background_color=background_color),
                sg.Text('', **ap_style.page_title, pad=((0,0),(0,3)), key='_DRAFT_INVOICE_NUMBER_', background_color=background_color,visible=(eval("type=='draft'"))),
                sg.Text('', **ap_style.page_title, pad=((0,0),(0,3)), key='_TAX_INVOICE_NUMBER_', background_color=background_color,visible=(eval("type=='tax'"))),
                sg.Text('', **ap_style.page_title, pad=((0,67),(0,3)), key='_MOBILE_NUMBER_', background_color=background_color),
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
                sg.Combo([''], key='_SEARCH_ITEM_GROUP_',default_value = 'None'),                
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
                     headings= ['Item code', 'Barcode', 'Item Name', 'Unit', 'Qty', 'Price', 'Disc', 'Amount', 'Tax Rate', 'Tax', 'Net'],
                     font=(("Helvetica", 11)),
                     auto_size_columns=False,
                     justification='right',
                     row_height=24,
                     alternating_row_color= alternating_row_color,
                     num_rows=item_rows,
                     display_row_numbers=True,
                     right_click_menu=right_click_menu,
                     bind_return_key=True,
                     col_widths=[9, 13, 24, 5, 5, 7, 8, 7, 8, 7, 9],
                )            
            ],
        ]

        ui_action_pane_layout = [
            [
                sg.Button(key='F1',  button_text='\nF1', **ap_style.action_button, pad=((3,5),(5,0)),visible=(eval("type=='draft'"))),
                sg.Button(key='F2',  button_text='\nF2', **ap_style.action_button, pad=((0,5),(5,0)),visible=(eval("type=='draft'"))),
                sg.Button(key='F3',  button_text='\nF3', **ap_style.action_button, pad=((0,5),(5,0)),visible=(eval("type=='draft'"))),
                sg.Button(key='F4',  button_text='\nF4', **ap_style.action_button, pad=((0,5),(5,0)),visible=(eval("type=='draft'"))),
                sg.Button(key='F5',  button_text='\nF5', **ap_style.action_button, pad=((print_left_pad,25),(5,0))),
                sg.Button(key='F6',  button_text='\nF6', **ap_style.action_button_small, pad=((0,5),(5,0)),visible=(eval("type=='draft'"))),
                sg.Button(key='F7',  button_text='\nF7', **ap_style.action_button_small, pad=((0,5),(5,0)),visible=(eval("type=='draft'"))),
                sg.Button(key='F8',  button_text='\nF8', **ap_style.action_button_small, pad=((0,5),(5,0)),visible=(eval("type=='draft'"))),
                sg.Button(key='F9',  button_text='\nF9', **ap_style.action_button_small, pad=((0,5),(5,0)),visible=(eval("type=='draft'"))),
                sg.Button(key='+',  button_text='\n+', **ap_style.action_button_small, pad=((20,5),(5,0)),visible=(eval("type=='draft'"))),
                sg.Button(key='-',  button_text='\n-', **ap_style.action_button_small, pad=((0,5),(5,0)),visible=(eval("type=='draft'"))),
                sg.Button(key='ESC', button_text='Exit\nEsc', **ap_style.exit_button, pad=((exit_left_pad,0),(5,0))),
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
                sg.Image(filename = config.application_path + '/images/client_logo.PNG', background_color = 'white', pad = ((55,55),(0,0)))
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
                sg.Text('CGST:', **ap_style.summary_text),
                sg.Input(key='_TOTAL_CGST_AMOUNT_', **ap_style.summary_input),
            ],
            [
                sg.Text('SGST:', **ap_style.summary_text),
                sg.Input(key='_TOTAL_SGST_AMOUNT_', **ap_style.summary_input),
            ],
            [
                sg.Text('Tax:', **ap_style.summary_text, visible=False),
                sg.Input(key='_TOTAL_TAX_AMOUNT_', **ap_style.summary_input, visible=False),
            ],
            [
                sg.Text('Net Amount:', **ap_style.summary_text_bold, pad=((5,0),(5,0))),
                sg.Input(key='_NET_AMOUNT_', **ap_style.summary_input_bold, pad=((0,0),(5,7))),
            ],
            [
                sg.Text('Discount:', **ap_style.summary_text, visible=(eval("type=='tax'"))),
                sg.Input(key='_DISCOUNT_AMOUNT_', **ap_style.summary_input, visible=(eval("type=='tax'"))),
            ],
            [
                sg.Text('Roundoff:', **ap_style.summary_text),
                sg.Input(key='_ROUNDOFF_AMOUNT_', **ap_style.summary_input),
            ],
            [
                sg.Text('Invoiced:', **ap_style.summary_text_bold, pad=((5,0),(5,0))),
                sg.Input(key='_INVOICE_AMOUNT_', **ap_style.summary_input_bold, pad=((0,0),(5,7))),
            ],
            [
                sg.Text('Cash:', **ap_style.summary_text, visible=(eval("type=='tax'"))),
                sg.Input(key='_CASH_AMOUNT_', **ap_style.summary_input, visible=(eval("type=='tax'"))),
            ],
            [
                sg.Text('Card:', **ap_style.summary_text, visible=(eval("type=='tax'"))),
                sg.Input(key='_CARD_AMOUNT_', **ap_style.summary_input, visible=(eval("type=='tax'"))),
            ],
            [
                sg.Text('Exchange:', **ap_style.summary_text, visible=(eval("type=='tax'"))),
                sg.Input(key='_EXCHANGE_AMOUNT_', **ap_style.summary_input, visible=(eval("type=='tax'"))),
            ],
            [
                sg.Text('Redeem:', **ap_style.summary_text, visible=(eval("type=='tax'"))),
                sg.Input(key='_REDEEMED_AMOUNT_', **ap_style.summary_input, visible=(eval("type=='tax'"))),
            ],
            [
                sg.Text('Received:', **ap_style.summary_text_bold ,pad=((5,0),(10,0)), visible=(eval("type=='tax'"))),
                sg.Input(key='_PAID_AMOUNT_', **ap_style.summary_input_bold, pad=((0,0),(10,10)), visible=(eval("type=='tax'")))
            ],          
            [
                sg.Text('Returned:', **ap_style.summary_text_bold,pad=((5,0),(10,0)), visible=(eval("type=='tax'"))),
                sg.Input(key='_CASH_RETURN_', **ap_style.summary_input_bold, pad=((0,0),(5,10)), visible=(eval("type=='tax'"))),
            ],
        ]        
        
        ui_tools_pane_layout = [
            [
                sg.Button('ADDON  (Alt-A)', key='Addon', **ap_style.search_button_wide,visible=(eval("type=='draft'")))
            ],
            [
                sg.Button('BUNDLE  (Alt-B)', key='Bundle', **ap_style.search_button_wide,visible=(eval("type=='draft'")))
            ],
        ]

        ui_fast_pane_layout = [
            [sg.Button(fast_item + '  (Alt-' + chr(count + 73) + ')', key='FAST_'+fast_item_codes_list[count], **ap_style.search_button_wide)] for count, fast_item in enumerate(fast_item_names_list, start=0)
        ]
        
        ui_bottom_pane_layout = [
            [
                sg.Image(filename = config.application_path + '/images/application_logo.PNG', background_color = 'white', pad = ((52,53),(0,0))),
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
                    background_color=background_color, visible=(eval("type=='draft'"))
                )     
            ],
            [
                sg.Frame('',
                    ui_favorite_pane_layout,
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((2,0),(0,0)),
                    background_color=background_color, visible=(eval("type=='draft'"))
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
            [
                sg.Frame('',
                    ui_fast_pane_layout, 
                    background_color = 'grey90',
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((4,0),(20,10)),
                )     
            ],            
            [
                sg.HorizontalSeparator(color = 'white', pad = ((0,0),(bottom_pane_top,10))),
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


class DiscountCanvas:
    def __init__(self):
    
        discount_layout = [
            [
                sg.Text('', key='_ITEM_NAME_', size=(25,2),  font=("Helvetica Bold", 14))
            ],
            [
                sg.Text('Selling Price:', size=(15,1),  font=("Helvetica", 11)),     
                sg.Input(key='_SELLING_PRICE_',
                    readonly=True, 
                    font=("Helvetica", 11),
                    size=(15,1),
                    justification = 'right'
                )
            ],
            [
                sg.Text('Discount:', size=(15,1),  font=("Helvetica", 11), pad=((5,5),(10,10))),             
                sg.Input(key='_ITEM_DISCOUNT_AMOUNT_',
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
                sg.Button('Ok-F12', **ap_style.search_button_short, key='_DISCOUNT_OK_'), 
                sg.Button('Exit-Esc', **ap_style.search_button_short, key='_DISCOUNT_ESC_'), 
            ]           
        ]
        
        self.__layout = [
            [
                sg.Column(discount_layout, vertical_alignment = 'top', pad = None),
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
                     col_widths=[15, 12, 5, 9, 9, 9, 9, 9, 12],
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
class PaymentCanvas:
    def __init__(self):
    
        ui_customer_tab_layout = [
            [
                sg.Text('', font=("Helvetica", 5)),
            ],
            [
                sg.Text('Mobile No.:', size=(12,1),  font=("Helvetica", 11)),     
                sg.Input(key='_MOBILE_NUMBER_',
                    background_color='white',
                    font=("Helvetica", 11),size=(15,1),
                    enable_events=True,                                
                    justification = 'left'
                )
            ],
            [
                sg.Text('Name:', size=(12,1),  font=("Helvetica", 11)),     
                sg.Input(key='_CUSTOMER_NAME_',
                    readonly=True, 
                    font=("Helvetica", 11),
                    size=(30,1),
                    justification = 'left'
                )
            ],
            [
                sg.Text('Address:', size=(12,1),  font=("Helvetica", 11)),         
            ],
            [
                sg.Input(key='_CUSTOMER_ADDRESS_',
                    readonly=True, 
                    font=("Helvetica", 11),
                    size=(45,1),
                    justification = 'left'
                )
            ]
        ]

        ui_receive_tab_layout = [
            [
                sg.Text('', font=("Helvetica", 5)),
            ],
            [
                sg.Text('Net Amount:', size=(17,1),  font=("Helvetica", 11)),     
                sg.Input(key='_NET_AMOUNT_',
                    readonly=True, 
                    font=("Helvetica", 11),
                    size=(15,1),
                    justification = 'right'
                )
            ],
            [
                sg.Text('Discount Amount:', size=(17,1),  font=("Helvetica", 11)),             
                sg.Input(key='_DISCOUNT_AMOUNT_HD_',
                    readonly=True, 
                    font=("Helvetica", 11),size=(15,1),
                    justification = 'right'
                )
            ],
            [
                sg.Text('Roundoff Adjustment:', size=(17,1),  font=("Helvetica", 11)),             
                sg.Input(key='_ROUNDOFF_ADJUSTMENT_',
                    readonly=True, 
                    font=("Helvetica", 11),size=(15,1),
                    justification = 'right'
                )
            ],
            [
                sg.Text('Invoice Amount:', size=(15,1), font=("Helvetica 12 bold"), text_color='Blue'),             
                sg.Input(key='_INVOICE_AMOUNT_',
                    readonly=True, 
                    size=(11,1),                
                    font=("Helvetica 14 bold"),
                    pad = ((8,0),(0,0)),                
                    justification = 'right'
                )
            ],
            [sg.HorizontalSeparator(color = 'grey99', pad = ((0,0),(15,15)))],            
            [
                sg.Text('Redeem Adjustment:', size=(17,1),  font=("Helvetica", 11)),     
                sg.Input(key='_REDEEM_ADJUSTMENT_HD_',
                    readonly=True, 
                    font=("Helvetica", 11),
                    size=(15,1),
                    justification = 'right'
                )
            ],
            [
                sg.Text('Exchange Adjustment:', size=(17,1),  font=("Helvetica", 11)),     
                sg.Input(key='_EXCHANGE_ADJUSTMENT_HD_',
                    readonly=True, 
                    font=("Helvetica", 11),
                    size=(15,1),
                    justification = 'right'
                )
            ],
            [
                sg.Text('Cash Amount:', size=(17,1),  font=("Helvetica", 11)),     
                sg.Input(key='_CASH_AMOUNT_',
                    focus=True, 
                    background_color='white',
                    font=("Helvetica", 11),size=(15,1),
                    enable_events=True,                                
                    justification = 'right'
                ),
            ],
            [
                sg.Text('Card Amount:', size=(17,1),  font=("Helvetica", 11)),     
                sg.Input(key='_CARD_AMOUNT_',
                    background_color='white',
                    font=("Helvetica", 11),size=(15,1),
                    enable_events=True,                                
                    justification = 'right'
                ), 
                sg.Text('Ref:', font=("Helvetica", 11)),                         
                sg.Input(key='_CARD_REFERENCE_',
                    background_color='white',
                    font=("Helvetica", 11),size=(15,1),
                    enable_events=True,                                
                    justification = 'left',
                    pad=((0,20),(0,0))
                ),        
            ],
            [
                sg.Text('Total Received :', size=(15,1), font=("Helvetica 12 bold"), text_color='Blue', pad = ((6,0),(5,5))),             
                sg.Input(key='_TOTAL_RECEIVED_AMOUNT_',
                    readonly=True, 
                     size=(11,1),                
                    font=("Helvetica 14 bold"),
                    pad = ((12,0),(0,0)),                
                    justification = 'right'
                )
            ],            
            [
                sg.Text('Cash Return:', size=(15,1), font=("Helvetica 12 bold"), text_color='Blue', pad = ((6,0),(0,15))),             
                sg.Input(key='_CASH_RETURN_',
                    readonly=True, 
                    size=(11,1),                
                    font=("Helvetica 14 bold"),
                    pad = ((12,0),(0,15)),                
                    justification = 'right'
                )
            ],
        ]

        ui_exchange_tab_layout = [
            [
                sg.Text('', font=("Helvetica", 5)),
            ],
            [
                sg.Text('Voucher:', size=(10,1),  font=("Helvetica", 11)),     
                sg.Combo(key='_EXCHANGE_VOUCHER_',
                    values=['None'],
                    default_value='None',
                    background_color='white',
                    font=("Helvetica", 11),size=(20,2),
                    enable_events=True,                                
                )
            ],
            [
                sg.Text('Adjustment:', size=(10,1),  font=("Helvetica", 11)),     
                sg.Input(key='_EXCHANGE_ADJUSTMENT_',
                    readonly=True, 
                    font=("Helvetica", 11),
                    size=(15,1),
                    justification = 'right'
                )
            ],
        ]

        ui_discount_tab_layout = [
            [
                sg.Text('', font=("Helvetica", 5)),
            ],
            [
                sg.Text('Discount:', size=(10,1),  font=("Helvetica", 11)),     
                sg.Input(key='_DISCOUNT_AMOUNT_',
                    background_color='white',
                    font=("Helvetica", 11),size=(15,1),
                    enable_events=True,                                
                    justification = 'right'
                )
            ],
            [
                sg.Text('PIN:', size=(10,1),  font=("Helvetica", 11)),     
                sg.Input(key='_DISCOUNT_PIN_',
                    background_color='white',
                    font=("Helvetica", 11),size=(5,1),
                    enable_events=True,                                
                    justification = 'left'
                )
            ],
        ]

        ui_redeem_tab_layout = [
            [
                sg.Text('', font=("Helvetica", 5)),
            ],
            [
                sg.Text('Available Points:', size=(15,1),  font=("Helvetica", 11)),     
                sg.Input(key='_AVAILABLE_POINTS_',
                    readonly=True, 
                    font=("Helvetica", 11),
                    size=(5,1),
                    justification = 'right'
                ),
                sg.Input(key='_AVAILABLE_BALANCE_',
                    readonly=True, 
                    font=("Helvetica", 11),
                    size=(15,1),
                    justification = 'right'
                )        
            ],
            [
                sg.Text('Redeem Points:', size=(15,1),  font=("Helvetica", 11)),     
                sg.Input(key='_REDEEM_POINTS_',
                    background_color='white',
                    font=("Helvetica", 11),size=(5,1),
                    enable_events=True,                                
                    justification = 'right'
                ),
                sg.Input(key='_REDEEM_ADJUSTMENT_',
                    readonly=True, 
                     font=("Helvetica", 11),
                    size=(15,1),
                    justification = 'right'
                )        
            ],
            [
                sg.Text('PIN:', size=(15,1),  font=("Helvetica", 11)),     
                sg.Input(key='_REDEEM_PIN_',
                    background_color='white',
                    font=("Helvetica", 11),size=(5,1),
                    enable_events=True,                                
                    justification = 'left'
                )
            ],
        ]
    
        self.__layout = [
            [
                sg.Text('Customer:', size=(8,1),  font=("Helvetica", 11), pad=((10,0),(10,5))),     
                sg.Input(key='_MOBILE_NUMBER_HEADER_',
                    readonly=True, 
                    font=("Helvetica", 11),
                    size=(12,1),
                    justification = 'left',
                    pad=((5,0),(10,5))            
                ),    
                sg.Input(key='_CUSTOMER_NAME_HEADER_',
                    readonly=True, 
                    font=("Helvetica", 11),
                    size=(34,1),
                    justification = 'left', 
                    pad=((5,0),(10,5))
                )
            ],
            [
                sg.Text('Balance:', size=(7,1), font=("Helvetica 12 bold"), text_color='Blue', pad=((10,0),(0,10))),         
                sg.Input(key='_BALANCE_AMOUNT_',
                    readonly=True,
                    font=("Helvetica 14 bold"),
                    size=(12,1),
                    justification = 'right',
                    pad=((7,0),(0,10)),            
                ),    
            
            ],
            [
                sg.TabGroup(
                    [
                        [
                            sg.Tab('Receive-F1', ui_receive_tab_layout, key='_RECEIVE_TAB_'),
                            sg.Tab('Exchange-F2', ui_exchange_tab_layout, key='_EXCHANGE_TAB_'),
                            sg.Tab('Redeem-F3', ui_redeem_tab_layout, key='_REDEEM_TAB_'),
                            sg.Tab('Discount-F4', ui_discount_tab_layout, key='_DISCOUNT_TAB_'),
                            sg.Tab('Customer-F5', ui_customer_tab_layout, key='_CUSTOMER_TAB_'),
                        ]
                    ],
                    key='-group2-', 
                    title_color='grey32',
                    font=("Helvetica 11"),
                    selected_title_color='white',
                    tab_location='topleft'
                ),
            ],
            [
                sg.Button('Ok-F12', 
                    size=(8, 1), 
                    font='Calibri 12 bold', 
                    key='_PAYMENT_OK_',
                    pad = ((5,0),(10,10)),                            
                ),

                sg.Button('Exit-Esc', 
                    size=(8, 1), 
                    font='Calibri 12 bold', 
                    key='_PAYMENT_ESC_', 
                    pad = ((15,0),(10,10)),                            
                )
            ]                   
        ]

    def get_layout(self):
        return self.__layout
    
    layout = property(get_layout)         



###
if __name__ == "__main__":
    print('***Not an executable module, please call the main script')
