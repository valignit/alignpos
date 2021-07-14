import PySimpleGUI as sg
import json
import datetime


with open('./alignpos.json') as file_config:
  config = json.load(file_config)


###
# Main Window Layout

sg.theme(config["ui_theme"])
w, h = sg.Window.get_screen_size()
lw = w*78/100
rw = w*22/100

pad_button:  dict = {
                    'size':(4, 2), 
                    'font':('Calibri 11 bold'), 
                    'button_color': (config["ui_pad_button_color"])
                }

nav_button:  dict = {
                    'size':(5, 2), 
                    'font':('Calibri 11 bold'), 
                    'button_color': (config["ui_nav_button_color"])
                }

nav_button_wide:  dict = {
                    'size':(13, 2), 
                    'font':('Calibri 11 bold'), 
                    'button_color': (config["ui_nav_button_color"])
                }
                
action_button:  dict = {
                    'size':(11, 1), 
                    'font':('Calibri 12 bold'), 
                    'button_color': (config["ui_function_button_color"]),
                    'disabled_button_color': ('gray99', 'gray99'),
                    'use_ttk_buttons': True
                }

summary_text:  dict = {           
                    'font':("Helvetica 11"),
                    'size':(10,1)                        
                }
                
summary_text_bold:  dict = {           
                    'font':("Helvetica 13 bold"),
                    'text_color': "blue",
                    'size':(10,1)                        
                }
summary_input:  dict = {           
                    'readonly':True, 
                    'justification':'right', 
                    'disabled_readonly_text_color':(config["ui_readonly_text_color"]), 
                    'disabled_readonly_background_color':(config["ui_readonly_background_color"]), 
                    'default_text':'0.00' , 
                    'font':("Helvetica", 10),
                    'size':(11,1)                        
                }

summary_input_bold:  dict = {           
                    'readonly':True, 
                    'justification':'right', 
                    'disabled_readonly_text_color':"white", 
                    'disabled_readonly_background_color':"blue", 
                    'default_text':'0.00' , 
                    'font':("Helvetica 14 bold"),
                    'size':(8,1)                        
                }

header_text:  dict = {           
                    'font':("Helvetica 12"),
                    'size':(9,1),
                    'justification': 'right'
                }    

header_input:  dict = {           
                    'readonly':True, 
                    'justification':'right', 
                    'disabled_readonly_text_color':(config["ui_readonly_text_color"]), 
                    'disabled_readonly_background_color':(config["ui_readonly_background_color"]), 
                    'default_text':'0.00' , 
                    'font':("Helvetica", 11),
                    'size':(11,1)                        
                }

search_text:  dict = {           
                    'font':("Helvetica 12"),
                    'size':(9,1),
                    'justification': 'right'
                }    

search_input:  dict = {           
                    'readonly':True, 
                    'justification':'right', 
                    'disabled_readonly_text_color':(config["ui_readonly_text_color"]), 
                    'disabled_readonly_background_color':(config["ui_readonly_background_color"]), 
                    'default_text':'0.00' , 
                    'font':("Helvetica", 12),
                    'size':(10,1)                        
                }
                
class MainWindow:
             
    ui_title_pane_layout = [
        [
            sg.Column(
            [
                [
                    sg.Text('Invoice Entry', size=(27,1) ,font=("Helvetica", 18)),
                    sg.Text('User:', **header_text),
                    sg.Input(key='_USER_ID_', **header_input),
                    sg.Text('Terminal:', **header_text),
                    sg.Input(key='_TERMINAL_ID_', **header_input),
                    sg.Text('Date:', **header_text),
                    sg.Input(key='_CURRENT_DATE_', **header_input)
                ]
            ])
        ]
    ]

    ui_header_pane_layout = [
        [
            sg.Column(
            [
                [
                    sg.Text('Invoice:', **header_text),
                    sg.Input(key='_INVOICE_NUMBER_', **header_input),
                    sg.Text('Order:', **header_text),
                    sg.Input(key='_REFERENCE_NUMBER_', **header_input),
                    sg.Text('Mobile:', **header_text),
                    sg.Input(key='_MOBILE_NUMBER_', **header_input),
                    sg.Button(key='_FIND_', button_text='FIND\nF10', **nav_button, pad = ((10,10),(0,0))),
                    sg.Button(key='_BEGIN_', button_text='BEGN\nPgUp',**nav_button, pad = ((5,0),(0,0))),
                    sg.Button(key='_PREVIOUS_', button_text='PREV\n←', **nav_button, pad = ((5,0),(0,0))),
                    sg.Button(key='_NEXT_', button_text='NEXT\n→', **nav_button, pad = ((5,0),(0,0))),
                    sg.Button(key='_END_', button_text='END\nPgDn', **nav_button, pad = ((5,0),(0,0))),    
                ]
            ])    
        ]
    ]

    ui_search_pane_layout = [
        [
            sg.Column(
            [
                [
                    sg.Text('Barcode:', **search_text),
                    sg.Input(key='_BARCODE_',
                        background_color='White',
                        font=("Helvetica", 12),
                        size=(15,1), 
                        enable_events = True
                    ),
                    sg.Text('Item Name:', **search_text, pad=((20,0),(0,0))),
                    sg.Input(key='_ITEM_NAME_',
                        background_color='White',
                        font=("Helvetica", 12),
                        size=(38,1), 
                        enable_events = True
                    ),
                    sg.Button('Quick Item-F11', 
                        size=(13, 1), 
                        font='Calibri 11 bold', 
                        key='_QUICK_ITEMS_', 
                        pad = ((152,0),(0,0)),                                           
                        button_color = config["ui_function_button_color"]
                    ),                        
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
                         num_rows=15,
                         display_row_numbers=True,
                         col_widths=[10, 13, 23, 5, 5, 8, 10, 8, 10, 10]
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
                    sg.Button(key='F1',  button_text='\nF1', **action_button),
                    sg.Button(key='F2',  button_text='\nF2', **action_button),
                    sg.Button(key='F3',  button_text='\nF3', **action_button),
                    sg.Button(key='F4',  button_text='\nF4', **action_button),
                    sg.Button(key='F5',  button_text='\nF5', **action_button),
                    sg.Button(key='F6',  button_text='\nF6', **action_button),
                    sg.Button(key='F7',  button_text='\nF7', **action_button),
                    sg.Button(key='F8',  button_text='\nF8', **action_button),
                    sg.Button(key='ESC', button_text='Exit\nEsc', **action_button),
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
            ], vertical_alignment = 'top', pad=(45,0), background_color = 'white')
        ]
    ]
    
    ui_summary_pane_layout = [
        [
            sg.Column(
            [
                [
                    sg.Text('Line Items:', **summary_text),
                    sg.Input(key='_LINE_ITEMS_', **summary_input)          
                ],
                [
                    sg.Text('Total Amount:', **summary_text),
                    sg.Input(key='_TOTAL_AMOUNT_', **summary_input),
                ],
                [
                    sg.Text('Tax:', **summary_text),
                    sg.Input(key='_TOTAL_TAX_AMOUNT_', **summary_input),
                ],
                [
                    sg.Text('Net Amount:', **summary_text),
                    sg.Input(key='_NET_AMOUNT_', **summary_input),
                ],
                [
                    sg.Text('Discount:', **summary_text),
                    sg.Input(key='_DISCOUNT_AMOUNT_', **summary_input),
                ],
                [
                    sg.Text('Roundoff:', **summary_text),
                    sg.Input(key='_ROUNDOFF_AMOUNT_', **summary_input),
                ],
                [
                    sg.Text('Invoiced:', **summary_text_bold, pad=((5,0),(5,0))),
                    sg.Input(key='_INVOICE_AMOUNT_', **summary_input_bold, pad=((0,0),(0,0))),
                ],
                [
                    sg.Text('Paid:', **summary_text_bold ,pad=((5,0),(5,0))),
                    sg.Input(key='_PAID_AMOUNT_', **summary_input_bold, pad=((0,0),(7,0)))
                ]            
                
            ], vertical_alignment = 'top', pad = (18,0))           
        ]
    ]        

    ui_keypad_pane_layout = [
        [
            sg.Column(
            [
                [
                    sg.Button(key='UP', button_text='↑', **pad_button),
                    sg.Button(key='T7', button_text='7', **pad_button),
                    sg.Button(key='T8', button_text='8', **pad_button),
                    sg.Button(key='T9', button_text='9', **pad_button),                    
                ],
                [
                    sg.Button(key='DOWN', button_text='↓', **pad_button),
                    sg.Button(key='T4', button_text='4', **pad_button),
                    sg.Button(key='T5', button_text='5', **pad_button),
                    sg.Button(key='T6', button_text='6', **pad_button),                    
                ],
                [
                    sg.Button(key='RIGHT', button_text='→', **pad_button),
                    sg.Button(key='T1', button_text='1', **pad_button),
                    sg.Button(key='T2', button_text='2', **pad_button),
                    sg.Button(key='T3', button_text='3', **pad_button),                    
                    
                ],
                [
                    sg.Button(key='LEFT', button_text='←', **pad_button),
                    sg.Button(key='T0', button_text='0', **pad_button),
                    sg.Button('ENT', size=(10, 2), font='Calibri 11 bold', key='ENTER', button_color = config["ui_pad_button_color"]),
                ],            
                [
                    sg.Button(key='BACKSPACE', button_text='\u232B', size=(4, 2), font='Calibri 11 bold', button_color = config["ui_pad_button_color"]),
                    sg.Button(key='FULL_STOP', button_text='.', **pad_button),                    
                    sg.Button(key='DEL', button_text='DEL', **pad_button),                    
                    sg.Button(key='TAB', button_text='TAB', **pad_button),                    
                ],            
            ], vertical_alignment = 'top', pad = (9,0))    
        ]
    ]        

    ui_logo_pane_layout = [
        [
            sg.Column(
            [
                [
                    sg.Image(filename = 'alignpos_logo.PNG', background_color = 'white')
                ]
            ], vertical_alignment = 'top', pad = (45,5), background_color = 'white')    
        ]
    ] 
    
    ui_left_panes_layout = [
        [
            sg.Column(ui_title_pane_layout, size = (lw, h*7/100), vertical_alignment = 'top', pad = ((0,5),(5,5)))     
        ],
        [
            sg.Column(ui_header_pane_layout, size = (lw,h*8/100), vertical_alignment = 'top', pad = ((0,5),(5,5)))     
        ],
        [
            sg.Column(ui_search_pane_layout, size = (lw,h*6/100), vertical_alignment = 'top', pad = ((0,5),(5,5)))     
        ],
        [
            sg.Column(ui_detail_pane_layout, size = (lw,h*57/100), vertical_alignment = 'top', pad = ((0,5),(5,5)))     
        ],
        [
            sg.Column(ui_action_pane_layout, size = (lw,h*9/100), vertical_alignment = 'top', pad = ((0,5),(5,5)))     
        ]         
    ]

    ui_right_panes_layout = [
        [
            sg.Column(ui_company_pane_layout, size = (rw,h*10/100), vertical_alignment = 'top', pad = ((0,5),(5,5)), background_color='White')     
        ],
        [
            sg.Column(ui_summary_pane_layout, size = (rw,h*33/100), vertical_alignment = 'top', pad = ((0,5),(5,5)), background_color=None)     
        ],
        [
            sg.Column(ui_keypad_pane_layout, size = (rw,h*39/100), vertical_alignment = 'top', pad = ((0,5),(5,5)), background_color=None)     
        ],
        [
            sg.Column(ui_logo_pane_layout, size = (rw,h*5/100), vertical_alignment = 'top', pad = ((0,5),(5,5)), background_color='White')     
        ]        
    ]

    layout = [
        [
            sg.Column(ui_left_panes_layout, size = (lw,h), vertical_alignment = 'top', pad = None, background_color='White'),
            sg.Column(ui_right_panes_layout, size = (rw,h), vertical_alignment = 'top', pad = None, background_color='White')   
        ]      
    ]


###
# Main Window - Title Pane Interface
class UiTitlePane:

    def __init__(self, window):
        self.__window = window
        self.__user_id = ''
        self.__terminal_id = ''
        self.__current_date = datetime.datetime(1900, 1, 1)
        
        self.__window['_USER_ID_'].Widget.config(takefocus=0)
        self.__window['_TERMINAL_ID_'].Widget.config(takefocus=0)
        self.__window['_CURRENT_DATE_'].Widget.config(takefocus=0)
                
    def set_user_id(self, user_id):
        self.__user_id = user_id
        self.__window.Element('_USER_ID_').update(value = self.__user_id)
        
    def get_user_id(self):
        self.__user_id = self.__window.Element('_USER_ID_').get()
        return self.__user_id
        
    def set_terminal_id(self, terminal_id):
        self.__terminal_id = terminal_id
        self.__window.Element('_TERMINAL_ID_').update(value = self.__terminal_id)        
        
    def get_terminal_id(self):
        self.__terminal_id = self.__window.Element('_TERMINAL_ID_').get()    
        return self.__terminal_id
        
    def set_current_date(self, current_date):
        self.__current_date = current_date
        self.__window.Element('_CURRENT_DATE_').update(value = self.__current_date)        
        
    def get_current_date(self):
        self.__current_date = self.__window.Element('_CURRENT_DATE_').get()        
        return self.__current_date
               
    user_id = property(get_user_id, set_user_id) 
    terminal_id = property(get_terminal_id, set_terminal_id)
    current_date = property(get_current_date, set_current_date)


###
# Main Window - Header Pane Interface
class UiHeaderPane:

    def __init__(self, window):
        self.__window = window
        self.__reference_number = str('')
        self.__invoice_number = str('')
        self.__mobile_number = str('')
        self.__customer_number = str('')
        self.__customer_name = str('')
        self.__customer_address = str('')
        
        self.__window['_REFERENCE_NUMBER_'].Widget.config(takefocus=0)
        self.__window['_INVOICE_NUMBER_'].Widget.config(takefocus=0)
        self.__window['_MOBILE_NUMBER_'].Widget.config(takefocus=0)
        self.__window['_FIND_'].Widget.config(takefocus=0)
        self.__window['_BEGIN_'].Widget.config(takefocus=0)
        self.__window['_PREVIOUS_'].Widget.config(takefocus=0)
        self.__window['_NEXT_'].Widget.config(takefocus=0)
        self.__window['_END_'].Widget.config(takefocus=0)


    def set_reference_number(self, reference_number):
        self.__reference_number = reference_number
        self.__window.Element('_REFERENCE_NUMBER_').update(value = self.__reference_number)
        
    def get_reference_number(self):
        self.__reference_number = self.__window.Element('_REFERENCE_NUMBER_').get()        
        return self.__reference_number
        
    def set_invoice_number(self, invoice_number):
        self.__invoice_number = invoice_number
        self.__window.Element('_INVOICE_NUMBER_').update(value = self.__invoice_number)
        
    def get_invoice_number(self):
        self.__invoice_number = self.__window.Element('_INVOICE_NUMBER_').get()        
        return self.__invoice_number
        
    def set_mobile_number(self, mobile_number):
        self.__mobile_number = mobile_number
        self.__window.Element('_MOBILE_NUMBER_').update(value = self.__mobile_number)
        
    def get_mobile_number(self):
        self.__mobile_number = self.__window.Element('_MOBILE_NUMBER_').get()        
        return self.__mobile_number

    def set_customer_number(self, customer_number):
        self.__customer_number = customer_number
        
    def get_customer_number(self):
        return self.__customer_number

    def set_customer_name(self, customer_name):
        self.__customer_name = customer_name
        
    def get_customer_name(self):
        return self.__customer_name

    def set_customer_address(self, customer_address):
        self.__customer_address = customer_address
        
    def get_customer_address(self):
        return self.__customer_address


    reference_number = property(get_reference_number, set_reference_number) 
    invoice_number = property(get_invoice_number, set_invoice_number) 
    mobile_number = property(get_mobile_number, set_mobile_number) 
    customer_number = property(get_customer_number, set_customer_number) 
    customer_name = property(get_customer_name, set_customer_name) 
    customer_address = property(get_customer_address, set_customer_address) 
        

###
# Main Window - Search Pane Interface
class UiSearchPane:

    def __init__(self, window):
        self.__window = window
        self.__barcode = str('')
        self.__item_name = str('')
        self.__window['_QUICK_ITEMS_'].Widget.config(takefocus=0)
        
    def set_barcode(self, barcode):
        self.__barcode = barcode
        self.__window.Element('_BARCODE_').update(value = self.__barcode)
        
    def get_barcode(self):
        self.__barcode = self.__window.Element('_BARCODE_').get()        
        return self.__barcode

    def set_item_name(self, item_name):
        self.__item_name = item_name
        self.__window.Element('_ITEM_NAME_').update(value = self.__item_name)
        
    def get_item_name(self):
        self.__item_name = self.__window.Element('_ITEM_NAME_').get()        
        return self.__item_name

    def focus_barcode(self):
        self.__window.Element('_BARCODE_').SetFocus() 

    def focus_item_name(self):
        self.__window.Element('_ITEM_NAME_').SetFocus() 
        
    barcode = property(get_barcode, set_barcode) 
    item_name = property(get_item_name, set_item_name) 


###
# Main Window - Detail Pane Interface
class UiDetailPane:

    def __init__(self, window):
        self.__window = window
        self.__items_list = []
        self.__item_code = str('')
        self.__barcode = str('')
        self.__item_name = str('')
        self.__uom = str('')
        self.__qty = float(0.0)
        self.__selling_price = float(0.00)
        self.__selling_amount = float(0.00)
        self.__tax_rate = float(0.00)
        self.__tax_amount = float(0.00)
        self.__net_amount = float(0.00)
        self.__cgst_tax_rate = float(0.00)
        self.__sgst_tax_rate = float(0.00)
        self.__item_line = []       
        
    def set_items_list(self, items_list):
        self.__items_list = items_list
        self.__window.Element('_ITEMS_LIST_').update(values = self.__items_list)
        
    def get_items_list(self):
        self.__items_list = self.__window.Element('_ITEMS_LIST_').get()
        return self.__items_list
              
    def set_item_code(self, item_code):
        self.__item_code = item_code
        
    def get_item_code(self):
        return self.__item_code

    def set_barcode(self, barcode):
        self.__barcode = barcode
        
    def get_barcode(self):
        return self.__barcode

    def set_item_name(self, item_name):
        self.__item_name = item_name
        
    def get_item_name(self):
        return self.__item_name

    def set_uom(self, uom):
        self.__uom = uom
        
    def get_uom(self):
        return self.__uom

    def set_qty(self, qty):
        self.__qty = qty
        
    def get_qty(self):
        return self.__qty

    def set_selling_price(self, selling_price):
        self.__selling_price = selling_price
        
    def get_selling_price(self):
        return self.__selling_price

    def set_selling_amount(self, selling_amount):
        self.__selling_amount = selling_amount
        
    def get_selling_amount(self):
        return self.__selling_amount

    def set_tax_rate(self, tax_rate):
        self.__tax_rate = tax_rate
        
    def get_tax_rate(self):
        return self.__tax_rate

    def set_tax_amount(self, tax_amount):
        self.__tax_amount = tax_amount
        
    def get_tax_amount(self):
        return self.__tax_amount

    def set_net_amount(self, net_amount):
        self.__net_amount = net_amount
        
    def get_net_amount(self):
        return self.__net_amount

    def set_cgst_tax_rate(self, cgst_tax_rate):
        self.__cgst_tax_rate = cgst_tax_rate
        
    def get_cgst_tax_rate(self):
        return self.__cgst_tax_rate

    def set_sgst_tax_rate(self, sgst_tax_rate):
        self.__sgst_tax_rate = sgst_tax_rate
        
    def get_sgst_tax_rate(self):
        return self.__sgst_tax_rate       
                            
    def clear_ui_items_list(self):
        self.__ui_items_list.clear()
        self.__window.Element('_ui_items_list_').update(values = self.__ui_items_list)

    def elements_to_item_line(self):
        self.__item_line.append(self.__item_code)
        self.__item_line.append(self.__barcode)        
        self.__item_line.append(self.__item_name)        
        self.__item_line.append(self.__uom)        
        self.__item_line.append("{:.2f}".format(float(self.__qty)))      
        self.__item_line.append("{:.2f}".format(float(self.__selling_price)))        
        self.__item_line.append("{:.2f}".format(float(self.__selling_amount)))       
        self.__item_line.append("{:.2f}".format(float(self.__tax_rate)))     
        self.__item_line.append("{:.2f}".format(float(self.__tax_amount)))       
        self.__item_line.append("{:.2f}".format(float(self.__net_amount)))    
        self.__item_line.append("{:.2f}".format(float(self.__cgst_tax_rate)))       
        self.__item_line.append("{:.2f}".format(float(self.__sgst_tax_rate)))
       
    def item_line_to_elements(self, idx):
        self.__item_line = self.__items_list[idx]
        self.__item_code = self.__item_line[0]
        self.__barcode = self.__item_line[1]
        self.__item_name = self.__item_line[2]
        self.__uom = self.__item_line[3]
        self.__qty = self.__item_line[4]
        self.__selling_price = self.__item_line[5]
        self.__selling_amount = self.__item_line[6]
        self.__tax_rate = self.__item_line[7]
        self.__tax_amount = self.__item_line[8]
        self.__net_amount = self.__item_line[9]
        self.__cgst_tax_rate = self.__item_line[10]
        self.__sgst_tax_rate = self.__item_line[11]

    def add_item_line(self):
        self.__item_line = []
        self.elements_to_item_line()    
        self.__items_list.append(self.__item_line)
        self.__window.Element('_ITEMS_LIST_').update(values = self.__items_list)

    def update_item_line(self, idx):
        self.__item_line = []
        self.elements_to_item_line()
        print(self.__item_line)
        self.__items_list[idx] = self.__item_line
        self.__window.Element('_ITEMS_LIST_').update(values = self.__items_list)

    def delete_item_line(self, idx):
        self.__items_list.pop(idx)
        self.__window.Element('_ITEMS_LIST_').update(values = self.__items_list)

    def focus_items_list(self):
        self.__window['_ITEMS_LIST_'].Widget.config(takefocus=1)
        if len(self.__items_list) > 0:        
            table_row = self.__window['_ITEMS_LIST_'].Widget.get_children()[0]
            self.__window['_ITEMS_LIST_'].Widget.selection_set(table_row)  # move selection
            self.__window['_ITEMS_LIST_'].Widget.focus(table_row)  # move focus
            self.__window['_ITEMS_LIST_'].Widget.see(table_row)  # scroll to show i

    def focus_items_list_row(self, row):
        self.__window['_ITEMS_LIST_'].Widget.config(takefocus=1)        
        table_row = self.__window['_ITEMS_LIST_'].Widget.get_children()[row]
        self.__window['_ITEMS_LIST_'].Widget.selection_set(table_row)  # move selection
        self.__window['_ITEMS_LIST_'].Widget.focus(table_row)  # move focus
        self.__window['_ITEMS_LIST_'].Widget.see(table_row)  # scroll to show i
        
    items_list = property(get_items_list, set_items_list)
    item_code = property(get_item_code, set_item_code)
    barcode = property(get_barcode, set_barcode)
    item_name = property(get_item_name, set_item_name)
    uom = property(get_uom, set_uom)
    qty = property(get_qty, set_qty)
    selling_price = property(get_selling_price, set_selling_price)
    selling_amount = property(get_selling_amount, set_selling_amount)
    tax_rate = property(get_tax_rate, set_tax_rate)
    tax_amount = property(get_tax_amount, set_tax_amount)
    net_amount = property(get_net_amount, set_net_amount)
    cgst_tax_rate = property(get_cgst_tax_rate, set_cgst_tax_rate)
    sgst_tax_rate = property(get_sgst_tax_rate, set_sgst_tax_rate)


###
# Main Window - Action Pane Interface
class UiActionPane:

    def __init__(self, window):
        self.__window = window
    
        self.__window['F1'].Widget.config(takefocus=0)
        self.__window['F2'].Widget.config(takefocus=0)
        self.__window['F3'].Widget.config(takefocus=0)
        self.__window['F4'].Widget.config(takefocus=0)
        self.__window['F5'].Widget.config(takefocus=0)        
        self.__window['F6'].Widget.config(takefocus=0)        
        self.__window['F7'].Widget.config(takefocus=0)        
        self.__window['F8'].Widget.config(takefocus=0)        
        self.__window['ESC'].Widget.config(takefocus=0)    


###
# Main Window - Sumary Pane Interface
class UiSummaryPane:

    def __init__(self, window):
        self.__window = window
        self.__line_items = 0
        self.__total_amount = float(0.00)
        self.__total_tax_amount = float(0.00)
        self.__total_cgst_amount = float(0.00)
        self.__total_sgst_amount = float(0.00)
        self.__net_amount = float(0.00)
        self.__discount_amount = float(0.00)
        self.__roundoff_amount = float(0.00)
        self.__invoice_amount = float(0.00)
        self.__paid_amount = float(0.00)
        self.__cash_amount = float(0.00)
        self.__card_amount = float(0.00)
        self.__card_reference = ""
        self.__cash_return = float(0.00)
        self.__exchange_voucher = ""
        self.__exchange_adjustment = float(0.00)
        self.__redeem_points = int(0)
        self.__redeem_adjustment = float(0.00)

        self.__window['_LINE_ITEMS_'].Widget.config(takefocus=0)
        self.__window['_TOTAL_AMOUNT_'].Widget.config(takefocus=0)
        self.__window['_TOTAL_TAX_AMOUNT_'].Widget.config(takefocus=0)
        self.__window['_NET_AMOUNT_'].Widget.config(takefocus=0)
        self.__window['_DISCOUNT_AMOUNT_'].Widget.config(takefocus=0)
        self.__window['_ROUNDOFF_AMOUNT_'].Widget.config(takefocus=0)
        self.__window['_INVOICE_AMOUNT_'].Widget.config(takefocus=0)
        self.__window['_PAID_AMOUNT_'].Widget.config(takefocus=0)

    def set_line_items(self, line_items):
        self.__line_items = line_items
        self.__window.Element('_LINE_ITEMS_').update(value = self.__line_items)
        
    def get_line_items(self):
        self.__line_items = self.__window.Element('_LINE_ITEMS_').get()        
        return self.__line_items
        
    def set_total_amount(self, total_amount):
        self.__total_amount = total_amount
        self.__window.Element('_TOTAL_AMOUNT_').update(value = "{:.2f}".format(self.__total_amount))
        
    def get_total_amount(self):
        self.__total_amount = self.__window.Element('_TOTAL_AMOUNT_').get()        
        return self.__total_amount

    def set_total_tax_amount(self, total_tax_amount):
        self.__total_tax_amount = total_tax_amount
        self.__window.Element('_TOTAL_TAX_AMOUNT_').update(value = "{:.2f}".format(self.__total_tax_amount))
        
    def get_total_tax_amount(self):
        self.__total_tax_amount = self.__window.Element('_TOTAL_TAX_AMOUNT_').get()        
        return self.__total_tax_amount

    def set_total_cgst_amount(self, total_cgst_amount):
        self.__total_cgst_amount = "{:.2f}".format(total_cgst_amount)
        
    def get_total_cgst_amount(self):
        return self.__total_cgst_amount

    def set_total_sgst_amount(self, total_sgst_amount):
        self.__total_sgst_amount = "{:.2f}".format(total_sgst_amount)
        
    def get_total_sgst_amount(self):
        return self.__total_sgst_amount

    def set_net_amount(self, total_net_amount):
        self.__net_amount = total_net_amount
        self.__window.Element('_NET_AMOUNT_').update(value = "{:.2f}".format(self.__net_amount))
        
    def get_net_amount(self):
        self.__net_amount = self.__window.Element('_NET_AMOUNT_').get()        
        return self.__net_amount

    def set_discount_amount(self, discount_amount):
        self.__discount_amount = discount_amount
        self.__window.Element('_DISCOUNT_AMOUNT_').update(value = "{:.2f}".format(self.__discount_amount))
        
    def get_discount_amount(self):
        self.__discount_amount = self.__window.Element('_DISCOUNT_AMOUNT_').get()        
        return self.__discount_amount

    def set_roundoff_amount(self, roundoff_amount):
        self.__roundoff_amount = roundoff_amount
        self.__window.Element('_ROUNDOFF_AMOUNT_').update(value = "{:.2f}".format(self.__roundoff_amount))
        
    def get_roundoff_amount(self):
        self.__roundoff_amount = self.__window.Element('_ROUNDOFF_AMOUNT_').get()        
        return self.__roundoff_amount

    def set_invoice_amount(self, invoice_amount):
        self.__invoice_amount = invoice_amount
        print('here5', self.__invoice_amount)
        self.__window.Element('_INVOICE_AMOUNT_').update(value = "{:.2f}".format(self.__invoice_amount))
        
    def get_invoice_amount(self):
        self.__invoice_amount = self.__window.Element('_INVOICE_AMOUNT_').get()        
        return self.__invoice_amount

    def set_paid_amount(self, paid_amount):
        self.__paid_amount = paid_amount
        self.__window.Element('_PAID_AMOUNT_').update(value = "{:.2f}".format(float(self.__paid_amount)))
        
    def get_paid_amount(self):
        self.__paid_amount = self.__window.Element('_PAID_AMOUNT_').get()        
        return self.__paid_amount
        
    def set_redeem_points(self, redeem_points):
        self.__redeem_points = redeem_points

    def set_redeem_adjustment(self, redeem_adjustment):
        self.__redeem_adjustment = redeem_adjustment

    def set_exchange_voucher(self, exchange_voucher):
        self.__exchange_voucher = exchange_voucher

    def set_exchange_adjustment(self, exchange_adjustment):
        self.__exchange_adjustment = exchange_adjustment

    def set_cash_amount(self, cash_amount):
        self.__cash_amount = cash_amount

    def set_card_amount(self, card_amount):
        self.__card_amount = card_amount

    def set_card_reference(self, card_reference):
        self.__card_reference = card_reference

    def set_cash_return(self, cash_return):
        self.__cash_return = cash_return        

    def get_cash_amount(self):
        return self.__cash_amount

    def get_card_amount(self):
        return self.__card_amount

    def get_card_reference(self):
        return self.__card_reference

    def get_cash_return(self):
        return self.__cash_return

    def get_exchange_voucher(self):
        return self.__exchange_voucher

    def get_exchange_adjustment(self):
        return self.__exchange_adjustment

    def get_redeem_points(self):
        return self.__redeem_points

    def get_redeem_adjustment(self):
        return self.__redeem_adjustment
        
    line_items = property(get_line_items, set_line_items)
    total_amount = property(get_total_amount, set_total_amount)
    total_tax_amount = property(get_total_tax_amount, set_total_tax_amount)
    total_cgst_amount = property(get_total_cgst_amount, set_total_cgst_amount)
    total_sgst_amount = property(get_total_sgst_amount, set_total_sgst_amount)
    net_amount = property(get_net_amount, set_net_amount)
    discount_amount = property(get_discount_amount, set_discount_amount)
    roundoff_amount = property(get_roundoff_amount, set_roundoff_amount)
    invoice_amount = property(get_invoice_amount, set_invoice_amount)
    paid_amount = property(get_paid_amount, set_paid_amount)
    redeem_points = property(get_redeem_points, set_redeem_points)
    redeem_adjustment = property(get_redeem_adjustment, set_redeem_adjustment)
    exchange_voucher = property(get_exchange_voucher, set_exchange_voucher)
    exchange_adjustment = property(get_exchange_adjustment, set_exchange_adjustment)
    cash_amount = property(get_cash_amount, set_cash_amount)
    card_amount = property(get_card_amount, set_card_amount)
    card_reference = property(get_card_reference, set_card_reference)
    cash_return = property(get_cash_return, set_cash_return)



###
# Main Window - Keypad Pane Interface
class UiKeypadPane:

    def __init__(self, window):
        self.__window = window
    
        self.__window['T1'].Widget.config(takefocus=0)     
        self.__window['T2'].Widget.config(takefocus=0)
        self.__window['T3'].Widget.config(takefocus=0)
        self.__window['T4'].Widget.config(takefocus=0)
        self.__window['T5'].Widget.config(takefocus=0)
        self.__window['T6'].Widget.config(takefocus=0)
        self.__window['T7'].Widget.config(takefocus=0)
        self.__window['T8'].Widget.config(takefocus=0)
        self.__window['T9'].Widget.config(takefocus=0)
        self.__window['T0'].Widget.config(takefocus=0)
        self.__window['UP'].Widget.config(takefocus=0)     
        self.__window['DOWN'].Widget.config(takefocus=0)     
        self.__window['LEFT'].Widget.config(takefocus=0)
        self.__window['RIGHT'].Widget.config(takefocus=0)
        self.__window['ENTER'].Widget.config(takefocus=0)
        self.__window['BACKSPACE'].Widget.config(takefocus=0)
        self.__window['FULL_STOP'].Widget.config(takefocus=0)
        self.__window['TAB'].Widget.config(takefocus=0)
        self.__window['DEL'].Widget.config(takefocus=0)

###
# Change Quantity Popup Layout  
class ChangeQtyPopup:
    
    def __init__(self):
        left_pane_layout = [
            [sg.Text('', key='_ITEM_NAME_', size=(25,2),  font=("Helvetica Bold", 14))],
            [sg.Text('Existing Quantity:', size=(15,1),  font=("Helvetica", 11)),     
             sg.Input(key='_EXISTING_QTY_',
                readonly=True, 
                background_color=config["ui_readonly_background_color"], 
                disabled_readonly_text_color=config["ui_readonly_text_color"],
                font=("Helvetica", 11),
                size=(15,1),
                justification = 'right'
            )],
            [sg.Text('New Quantity:', size=(15,1),  font=("Helvetica", 11), pad=((5,5),(10,10))),             
             sg.Input(key='_NEW_QTY_',
                readonly=False, 
                focus=True, 
                background_color='white',
                font=("Helvetica", 11),
                size=(15,1), 
                enable_events=True,
                justification = 'right'
            )],
            [sg.HorizontalSeparator(color = 'grey99', pad = ((0,0),(90,10)))],                        
            [sg.Button('Ok-F12', 
                size=(8, 1), 
                font='Calibri 12 bold', 
                key='_CHANGE_QTY_OK_'), 
             sg.Button('Exit-Esc', 
                size=(8, 1), 
                font='Calibri 12 bold', 
                key='_CHANGE_QTY_ESC_'), 
            ]           
        ]
        
        right_pane_layout = [
            [
                sg.Button(key='UP', button_text='↑', **pad_button),
                sg.Button(key='T7', button_text='7', **pad_button),
                sg.Button(key='T8', button_text='8', **pad_button),
                sg.Button(key='T9', button_text='9', **pad_button),                    
            ],
            [
                sg.Button(key='DOWN', button_text='↓', **pad_button),
                sg.Button(key='T4', button_text='4', **pad_button),
                sg.Button(key='T5', button_text='5', **pad_button),
                sg.Button(key='T6', button_text='6', **pad_button),                    
            ],
            [
                sg.Button(key='RIGHT', button_text='→', **pad_button),
                sg.Button(key='T1', button_text='1', **pad_button),
                sg.Button(key='T2', button_text='2', **pad_button),
                sg.Button(key='T3', button_text='3', **pad_button),                    
                
            ],
            [
                sg.Button(key='LEFT', button_text='←', **pad_button),
                sg.Button(key='T0', button_text='0', **pad_button),
                sg.Button('ENT', size=(10, 2), font='Calibri 11 bold', key='ENTER', button_color = config["ui_pad_button_color"]),
            ],            
            [
                sg.Button(key='BACKSPACE', button_text='\u232B', size=(4, 2), font='Calibri 11 bold', button_color = config["ui_pad_button_color"]),
                sg.Button(key='FULL_STOP', button_text='.', **pad_button),                    
                sg.Button(key='DEL', button_text='DEL', **pad_button),                    
                sg.Button(key='TAB', button_text='TAB', **pad_button),                    
            ],            
        
        ]

        self.__layout = [
            [
                sg.Column(left_pane_layout, vertical_alignment = 'top', pad = None),
                sg.Column(right_pane_layout, vertical_alignment = 'center', pad = None)
            ]
        ]

    def get_layout(self):
        return self.__layout
    
    layout = property(get_layout)         

    
###
# Change Quantity Popup Interface  
class UiChangeQtyPopup:

    def __init__(self, popup):
        self.__popup = popup
        self.__item_name = ''
        self.__existing_qty = float(0.00)
        self.__new_qty = float(0.00)

        self.__popup['_EXISTING_QTY_'].Widget.config(takefocus=0)
        self.__popup['T1'].Widget.config(takefocus=0)     
        self.__popup['T2'].Widget.config(takefocus=0)
        self.__popup['T3'].Widget.config(takefocus=0)
        self.__popup['T4'].Widget.config(takefocus=0)
        self.__popup['T5'].Widget.config(takefocus=0)
        self.__popup['T6'].Widget.config(takefocus=0)
        self.__popup['T7'].Widget.config(takefocus=0)
        self.__popup['T8'].Widget.config(takefocus=0)
        self.__popup['T9'].Widget.config(takefocus=0)
        self.__popup['T0'].Widget.config(takefocus=0)
        self.__popup['UP'].Widget.config(takefocus=0)     
        self.__popup['DOWN'].Widget.config(takefocus=0)     
        self.__popup['LEFT'].Widget.config(takefocus=0)
        self.__popup['RIGHT'].Widget.config(takefocus=0)
        self.__popup['ENTER'].Widget.config(takefocus=0)
        self.__popup['BACKSPACE'].Widget.config(takefocus=0)
        self.__popup['FULL_STOP'].Widget.config(takefocus=0)
        self.__popup['TAB'].Widget.config(takefocus=0)
        self.__popup['DEL'].Widget.config(takefocus=0)
        self.__popup["_CHANGE_QTY_OK_"].Widget.config(takefocus=0) 
        self.__popup["_CHANGE_QTY_ESC_"].Widget.config(takefocus=0) 
        

    def set_item_name(self, item_name):
        self.__item_name = item_name
        self.__popup.Element('_ITEM_NAME_').update(value = self.__item_name)
        
    def get_item_name(self):
        return self.__item_name
        
    def set_existing_qty(self, existing_qty):
        self.__existing_qty = existing_qty
        self.__popup.Element('_EXISTING_QTY_').update(value = self.__existing_qty)
        
    def get_existing_qty(self):
        self.__existing_qty = self.__popup.Element('_EXISTING_QTY_').get()        
        return self.__existing_qty

    def set_new_qty(self, new_qty):
        self.__new_qty = new_qty
        self.__popup.Element('_NEW_QTY_').update(value = self.__new_qty)
        
    def set_new_qty_f(self, new_qty):
        self.__new_qty = new_qty
        self.__popup.Element('_NEW_QTY_').update(value = "{:.2f}".format(float(self.__new_qty)))
        
    def get_new_qty(self):
        self.__new_qty = self.__popup.Element('_NEW_QTY_').get()        
        return self.__new_qty

    def focus_existing_qty(self):
        self.__popup.Element('_EXISTING_QTY_').SetFocus() 

    def focus_new_qty(self):
        self.__popup.Element('_NEW_QTY_').SetFocus() 
        self.__popup.Element('_NEW_QTY_').update(select=True)        

    def append_char(self, key, char):
        if self.__popup[key].Widget.select_present():
            self.__new_qty = ''
            self.__popup.Element(key).update(value = self.__new_qty)
        
        self.__new_qty = self.__popup.Element('_NEW_QTY_').get()        
        self.__new_qty = str(self.__new_qty) + char
        self.__popup.Element(key).update(value = self.__new_qty)

    item_name = property(get_item_name, set_item_name)     
    existing_qty = property(get_existing_qty, set_existing_qty) 
    new_qty = property(get_new_qty, set_new_qty) 
    new_qty_f = property(get_new_qty, set_new_qty_f) 


###
# Payment Popup Layout  
class PaymentPopup:
    

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
                    disabled_readonly_text_color=config["ui_readonly_text_color"], 
                    disabled_readonly_background_color=config["ui_readonly_background_color"],                     
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
                    disabled_readonly_text_color=config["ui_readonly_text_color"], 
                    disabled_readonly_background_color=config["ui_readonly_background_color"],                     
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
                    disabled_readonly_text_color=config["ui_readonly_text_color"], 
                    disabled_readonly_background_color=config["ui_readonly_background_color"],                     
                    font=("Helvetica", 11),
                    size=(15,1),
                    justification = 'right'
                )
            ],
            [
                sg.Text('Discount Amount:', size=(17,1),  font=("Helvetica", 11)),             
                sg.Input(key='_DISCOUNT_AMOUNT_HD_',
                    readonly=True, 
                    disabled_readonly_text_color=config["ui_readonly_text_color"], 
                    disabled_readonly_background_color=config["ui_readonly_background_color"],                     
                    font=("Helvetica", 11),size=(15,1),
                    justification = 'right'
                )
            ],
            [
                sg.Text('Roundoff Adjustment:', size=(17,1),  font=("Helvetica", 11)),             
                sg.Input(key='_ROUNDOFF_ADJUSTMENT_',
                    readonly=True, 
                    disabled_readonly_text_color=config["ui_readonly_text_color"], 
                    disabled_readonly_background_color=config["ui_readonly_background_color"],                     
                    font=("Helvetica", 11),size=(15,1),
                    justification = 'right'
                )
            ],
            [
                sg.Text('Invoice Amount:', size=(15,1), font=("Helvetica 12 bold"), text_color='Blue'),             
                sg.Input(key='_INVOICE_AMOUNT_',
                    readonly=True, 
                    disabled_readonly_text_color=config["ui_readonly_text_color"], 
                    disabled_readonly_background_color=config["ui_readonly_background_color"],                     
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
                    disabled_readonly_text_color=config["ui_readonly_text_color"], 
                    disabled_readonly_background_color=config["ui_readonly_background_color"],                     
                    font=("Helvetica", 11),
                    size=(15,1),
                    justification = 'right'
                )
            ],
            [
                sg.Text('Exchange Adjustment:', size=(17,1),  font=("Helvetica", 11)),     
                sg.Input(key='_EXCHANGE_ADJUSTMENT_HD_',
                    readonly=True, 
                    disabled_readonly_text_color=config["ui_readonly_text_color"], 
                    disabled_readonly_background_color=config["ui_readonly_background_color"],                     
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
                    disabled_readonly_text_color="Blue", 
                    disabled_readonly_background_color=config["ui_readonly_background_color"],                     
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
                    disabled_readonly_text_color="Blue", 
                    disabled_readonly_background_color=config["ui_readonly_background_color"],                     
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
                    disabled_readonly_text_color=config["ui_readonly_text_color"], 
                    disabled_readonly_background_color=config["ui_readonly_background_color"],                     
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
                    disabled_readonly_text_color=config["ui_readonly_text_color"], 
                    disabled_readonly_background_color=config["ui_readonly_background_color"],                     
                    font=("Helvetica", 11),
                    size=(5,1),
                    justification = 'right'
                ),
                sg.Input(key='_AVAILABLE_BALANCE_',
                    readonly=True, 
                    disabled_readonly_text_color=config["ui_readonly_text_color"], 
                    disabled_readonly_background_color=config["ui_readonly_background_color"],                     
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
                    disabled_readonly_text_color=config["ui_readonly_text_color"], 
                    disabled_readonly_background_color=config["ui_readonly_background_color"],                     
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
                    disabled_readonly_text_color=config["ui_readonly_text_color"], 
                    disabled_readonly_background_color=config["ui_readonly_background_color"],                     
                    justification = 'left',
                    pad=((5,0),(10,5))            
                ),    
                sg.Input(key='_CUSTOMER_NAME_HEADER_',
                    readonly=True, 
                    font=("Helvetica", 11),
                    size=(34,1),
                    disabled_readonly_text_color=config["ui_readonly_text_color"], 
                    disabled_readonly_background_color=config["ui_readonly_background_color"],                     
                    justification = 'left', 
                    pad=((5,0),(10,5))
                )
            ],
            [
                sg.Text('Balance:', size=(7,1), font=("Helvetica 12 bold"), text_color='Blue', pad=((10,0),(0,10))),         
                sg.Input(key='_BALANCE_AMOUNT_',
                    readonly=True,
                    disabled_readonly_text_color="Blue", 
                    disabled_readonly_background_color=config["ui_readonly_background_color"],                     
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
                    selected_background_color=config["ui_pad_button_color"] ,           
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
# Change Quantity Popup Interface  
class UiPaymentPopup:

	def __init__(self, popup):
		self.__popup = popup
		self.__mobile_number = '0000000000'
		self.__customer_name = 'Walk-in Customer'
		self.__customer_address = ""
		self.__net_amount = float(0.00)
		self.__discount_amount_hd = float(0.00)
		self.__roundoff_adjustment = float(0.00)
		self.__invoice_amount = float(0.00)
		self.__redeem_adjustment_hd = float(0.00)
		self.__exchange_adjustment_hd = float(0.00)
		self.__cash_amount = float(0.00)
		self.__card_amount = float(0.00)
		self.__card_reference = ""
		self.__cash_return = float(0.00)
		self.__exchange_voucher = ['None']
		self.__exchange_adjustment = float(0.00)
		self.__discount_amount = float(0.00)
		self.__discount_pin = ""
		self.__available_points = int(0)
		self.__available_balance = float(0.00)
		self.__redeem_points = int(0)
		self.__redeem_adjustment = float(0.00)
		self.__redeem_pin = ""
		self.__mobile_number_header = ""
		self.__customer_name_header = ""
		self.__balance_amount = float(0.00)
		self.__total_received_amount = float(0.00)
        
		#set initial elements
		self.__popup.Element("_MOBILE_NUMBER_").update(value = self.__mobile_number)
		self.__popup.Element("_CUSTOMER_NAME_").update(value = self.__customer_name)
		self.__popup.Element("_CUSTOMER_ADDRESS_").update(value = self.__customer_address)
		self.__popup.Element("_NET_AMOUNT_").update(value = "{:.2f}".format(self.__net_amount))
		self.__popup.Element("_DISCOUNT_AMOUNT_HD_").update(value = "{:.2f}".format(self.__discount_amount_hd))
		self.__popup.Element("_ROUNDOFF_ADJUSTMENT_").update(value = "{:.2f}".format(self.__roundoff_adjustment))
		self.__popup.Element("_INVOICE_AMOUNT_").update(value = "{:.2f}".format(self.__invoice_amount))
		self.__popup.Element("_REDEEM_ADJUSTMENT_HD_").update(value = "{:.2f}".format(self.__redeem_adjustment_hd))
		self.__popup.Element("_EXCHANGE_ADJUSTMENT_HD_").update(value = "{:.2f}".format(self.__exchange_adjustment_hd))
		self.__popup.Element("_CASH_AMOUNT_").update(value = "{:.2f}".format(self.__cash_amount))
		self.__popup.Element("_CARD_AMOUNT_").update(value = "{:.2f}".format(self.__card_amount))
		self.__popup.Element("_CARD_REFERENCE_").update(value = self.__card_reference)
		self.__popup.Element("_CASH_RETURN_").update(value = "{:.2f}".format(self.__cash_return))
		self.__popup.Element("_TOTAL_RECEIVED_AMOUNT_").update(value = "{:.2f}".format(self.__total_received_amount))
		self.__popup.Element("_EXCHANGE_VOUCHER_").update(value = self.__exchange_voucher)
		self.__popup.Element("_EXCHANGE_ADJUSTMENT_").update(value = "{:.2f}".format(self.__exchange_adjustment))
		self.__popup.Element("_DISCOUNT_AMOUNT_").update(value = "{:.2f}".format(self.__discount_amount))
		self.__popup.Element("_DISCOUNT_PIN_").update(value = self.__discount_pin)
		self.__popup.Element("_AVAILABLE_POINTS_").update(value = self.__available_points)
		self.__popup.Element("_AVAILABLE_BALANCE_").update(value = "{:.2f}".format(self.__available_balance))
		self.__popup.Element("_REDEEM_POINTS_").update(value = self.__redeem_points)
		self.__popup.Element("_REDEEM_ADJUSTMENT_").update(value = "{:.2f}".format(self.__redeem_adjustment))
		self.__popup.Element("_REDEEM_PIN_").update(value = self.__redeem_pin)
		self.__popup.Element("_MOBILE_NUMBER_HEADER_").update(value = self.__mobile_number_header)
		self.__popup.Element("_CUSTOMER_NAME_HEADER_").update(value = self.__customer_name_header)
		self.__popup.Element("_BALANCE_AMOUNT_").update(value = "{:.2f}".format(self.__balance_amount))

		#avoid focus
		self.__popup["_CUSTOMER_NAME_"].Widget.config(takefocus=0) 
		self.__popup["_CUSTOMER_ADDRESS_"].Widget.config(takefocus=0) 
		self.__popup["_NET_AMOUNT_"].Widget.config(takefocus=0) 
		self.__popup["_DISCOUNT_AMOUNT_HD_"].Widget.config(takefocus=0) 
		self.__popup["_ROUNDOFF_ADJUSTMENT_"].Widget.config(takefocus=0) 
		self.__popup["_INVOICE_AMOUNT_"].Widget.config(takefocus=0) 
		self.__popup["_REDEEM_ADJUSTMENT_HD_"].Widget.config(takefocus=0) 
		self.__popup["_EXCHANGE_ADJUSTMENT_HD_"].Widget.config(takefocus=0) 
		self.__popup["_CASH_RETURN_"].Widget.config(takefocus=0) 
		self.__popup["_EXCHANGE_ADJUSTMENT_"].Widget.config(takefocus=0) 
		self.__popup["_AVAILABLE_POINTS_"].Widget.config(takefocus=0) 
		self.__popup["_AVAILABLE_BALANCE_"].Widget.config(takefocus=0) 
		self.__popup["_REDEEM_ADJUSTMENT_"].Widget.config(takefocus=0) 
		self.__popup["_MOBILE_NUMBER_HEADER_"].Widget.config(takefocus=0) 
		self.__popup["_CUSTOMER_NAME_HEADER_"].Widget.config(takefocus=0) 
		self.__popup["_BALANCE_AMOUNT_"].Widget.config(takefocus=0) 
		self.__popup["_TOTAL_RECEIVED_AMOUNT_"].Widget.config(takefocus=0) 
		self.__popup["_PAYMENT_OK_"].Widget.config(takefocus=0) 
		self.__popup["_PAYMENT_ESC_"].Widget.config(takefocus=0) 

	#setters
	def set_mobile_number(self, mobile_number):
		self.__mobile_number = mobile_number
		self.__popup.Element("_MOBILE_NUMBER_").update(value = self.__mobile_number)

	def set_customer_name(self, customer_name):
		self.__customer_name = customer_name
		self.__popup.Element("_CUSTOMER_NAME_").update(value = self.__customer_name)

	def set_customer_address(self, customer_address):
		self.__customer_address = customer_address
		self.__popup.Element("_CUSTOMER_ADDRESS_").update(value = self.__customer_address)

	def set_net_amount(self, net_amount):
		self.__net_amount = net_amount
		self.__popup.Element("_NET_AMOUNT_").update(value = "{:.2f}".format(float(self.__net_amount)))

	def set_discount_amount_hd(self, discount_amount_hd):
		self.__discount_amount_hd = discount_amount_hd
		self.__popup.Element("_DISCOUNT_AMOUNT_HD_").update(value = "{:.2f}".format(float(self.__discount_amount_hd)))

	def set_roundoff_adjustment(self, roundoff_adjustment):
		self.__roundoff_adjustment = roundoff_adjustment
		self.__popup.Element("_ROUNDOFF_ADJUSTMENT_").update(value = "{:.2f}".format(float(self.__roundoff_adjustment)))

	def set_invoice_amount(self, invoice_amount):
		self.__invoice_amount = invoice_amount
		self.__popup.Element("_INVOICE_AMOUNT_").update(value = "{:.2f}".format(float(self.__invoice_amount)))

	def set_redeem_adjustment_hd(self, redeem_adjustment_hd):
		self.__redeem_adjustment_hd = redeem_adjustment_hd
		self.__popup.Element("_REDEEM_ADJUSTMENT_HD_").update(value = "{:.2f}".format(float(self.__redeem_adjustment_hd)))

	def set_exchange_adjustment_hd(self, exchange_adjustment_hd):
		self.__exchange_adjustment_hd = exchange_adjustment_hd
		self.__popup.Element("_EXCHANGE_ADJUSTMENT_HD_").update(value = "{:.2f}".format(float(self.__exchange_adjustment_hd)))

	def set_cash_amount(self, cash_amount):
		self.__cash_amount = cash_amount
		self.__popup.Element("_CASH_AMOUNT_").update(value = "{:.2f}".format(float(self.__cash_amount)))

	def set_card_amount(self, card_amount):
		self.__card_amount = card_amount
		self.__popup.Element("_CARD_AMOUNT_").update(value = "{:.2f}".format(float(self.__card_amount)))

	def set_card_reference(self, card_reference):
		self.__card_reference = card_reference
		self.__popup.Element("_CARD_REFERENCE_").update(value = self.__card_reference)

	def set_cash_return(self, cash_return):
		self.__cash_return = cash_return
		self.__popup.Element("_CASH_RETURN_").update(value = "{:.2f}".format(float(self.__cash_return)))

	def set_exchange_voucher(self, exchange_voucher):
		self.__exchange_voucher = exchange_voucher
		self.__popup.Element("_EXCHANGE_VOUCHER_").update(values = self.__exchange_voucher)

	def set_exchange_adjustment(self, exchange_adjustment):
		self.__exchange_adjustment = exchange_adjustment
		self.__popup.Element("_EXCHANGE_ADJUSTMENT_").update(value = "{:.2f}".format(float(self.__exchange_adjustment)))

	def set_discount_amount(self, discount_amount):
		self.__discount_amount = discount_amount
		self.__popup.Element("_DISCOUNT_AMOUNT_").update(value = "{:.2f}".format(float(self.__discount_amount)))

	def set_discount_pin(self, discount_pin):
		self.__discount_pin = discount_pin
		self.__popup.Element("_DISCOUNT_PIN_").update(value = self.__discount_pin)

	def set_available_points(self, available_points):
		self.__available_points = available_points
		self.__popup.Element("_AVAILABLE_POINTS_").update(value = self.__available_points)

	def set_available_balance(self, available_balance):
		self.__available_balance = available_balance
		self.__popup.Element("_AVAILABLE_BALANCE_").update(value = "{:.2f}".format(float(self.__available_balance)))

	def set_redeem_points(self, redeem_points):
		self.__redeem_points = redeem_points
		self.__popup.Element("_REDEEM_POINTS_").update(value = self.__redeem_points)

	def set_redeem_adjustment(self, redeem_adjustment):
		self.__redeem_adjustment = redeem_adjustment
		self.__popup.Element("_REDEEM_ADJUSTMENT_").update(value = "{:.2f}".format(float(self.__redeem_adjustment)))

	def set_redeem_pin(self, redeem_pin):
		self.__redeem_pin = redeem_pin
		self.__popup.Element("_REDEEM_PIN_").update(value = self.__redeem_pin)

	def set_mobile_number_header(self, mobile_number_header):
		self.__mobile_number_header = mobile_number_header
		self.__popup.Element("_MOBILE_NUMBER_HEADER_").update(value = self.__mobile_number_header)

	def set_customer_name_header(self, customer_name_header):
		self.__customer_name_header = customer_name_header
		self.__popup.Element("_CUSTOMER_NAME_HEADER_").update(value = self.__customer_name_header)

	def set_balance_amount(self, balance_amount):
		self.__balance_amount = balance_amount
		self.__popup.Element("_BALANCE_AMOUNT_").update(value = "{:.2f}".format(float(self.__balance_amount)))

	def set_total_received_amount(self, total_received_amount):
		self.__total_received_amount = total_received_amount
		self.__popup.Element("_TOTAL_RECEIVED_AMOUNT_").update(value = "{:.2f}".format(float(self.__total_received_amount)))

	#getters
	def get_mobile_number(self):
		self.__mobile_number = self.__popup.Element("_MOBILE_NUMBER_").get()
		return self.__mobile_number

	def get_customer_name(self):
		self.__customer_name = self.__popup.Element("_CUSTOMER_NAME_").get()
		return self.__customer_name

	def get_customer_address(self):
		self.__customer_address = self.__popup.Element("_CUSTOMER_ADDRESS_").get()
		return self.__customer_address

	def get_net_amount(self):
		self.__net_amount = self.__popup.Element("_NET_AMOUNT_").get()
		return self.__net_amount

	def get_discount_amount_hd(self):
		self.__discount_amount_hd = self.__popup.Element("_DISCOUNT_AMOUNT_HD_").get()
		return self.__discount_amount_hd

	def get_roundoff_adjustment(self):
		self.__roundoff_adjustment = self.__popup.Element("_ROUNDOFF_ADJUSTMENT_").get()
		return self.__roundoff_adjustment

	def get_invoice_amount(self):
		self.__invoice_amount = self.__popup.Element("_INVOICE_AMOUNT_").get()
		return self.__invoice_amount

	def get_redeem_adjustment_hd(self):
		self.__redeem_adjustment_hd = self.__popup.Element("_REDEEM_ADJUSTMENT_HD_").get()
		return self.__redeem_adjustment_hd

	def get_exchange_adjustment_hd(self):
		self.__exchange_adjustment_hd = self.__popup.Element("_EXCHANGE_ADJUSTMENT_HD_").get()
		return self.__exchange_adjustment_hd

	def get_cash_amount(self):
		self.__cash_amount = self.__popup.Element("_CASH_AMOUNT_").get()
		return self.__cash_amount

	def get_card_amount(self):
		self.__card_amount = self.__popup.Element("_CARD_AMOUNT_").get()
		return self.__card_amount

	def get_card_reference(self):
		self.__card_reference = self.__popup.Element("_CARD_REFERENCE_").get()
		return self.__card_reference

	def get_cash_return(self):
		self.__cash_return = self.__popup.Element("_CASH_RETURN_").get()
		return self.__cash_return

	def get_exchange_voucher(self):
		self.__exchange_voucher = self.__popup.Element("_EXCHANGE_VOUCHER_").get()
		return self.__exchange_voucher

	def get_exchange_adjustment(self):
		self.__exchange_adjustment = self.__popup.Element("_EXCHANGE_ADJUSTMENT_").get()
		return self.__exchange_adjustment

	def get_discount_amount(self):
		self.__discount_amount = self.__popup.Element("_DISCOUNT_AMOUNT_").get()
		return self.__discount_amount

	def get_discount_pin(self):
		self.__discount_pin = self.__popup.Element("_DISCOUNT_PIN_").get()
		return self.__discount_pin

	def get_available_points(self):
		self.__available_points = self.__popup.Element("_AVAILABLE_POINTS_").get()
		return self.__available_points

	def get_available_balance(self):
		self.__available_adjustment = self.__popup.Element("_AVAILABLE_BALANCE_").get()
		return self.__available_adjustment

	def get_redeem_points(self):
		self.__redeem_points = self.__popup.Element("_REDEEM_POINTS_").get()
		return self.__redeem_points

	def get_redeem_adjustment(self):
		self.__redeem_adjustment = self.__popup.Element("_REDEEM_ADJUSTMENT_").get()
		return self.__redeem_adjustment

	def get_redeem_pin(self):
		self.__redeem_pin = self.__popup.Element("_REDEEM_PIN_").get()
		return self.__redeem_pin

	def get_mobile_number_header(self):
		self.__mobile_number_header = self.__popup.Element("_MOBILE_NUMBER_HEADER_").get()
		return self.__mobile_number_header

	def get_customer_name_header(self):
		self.__customer_name_header = self.__popup.Element("_CUSTOMER_NAME_HEADER_").get()
		return self.__customer_name_header

	def get_balance_amount(self):
		self.__balance_amount = self.__popup.Element("_BALANCE_AMOUNT_").get()
		return self.__balance_amount

	def get_total_received_amount(self):
		self.__total_received_amount = self.__popup.Element("_TOTAL_RECEIVED_AMOUNT_").get()
		return self.__total_received_amount

	#utilities
	def focus_mobile_number(self):
		self.__popup.Element('_MOBILE_NUMBER_').SetFocus() 
		self.__popup.Element('_MOBILE_NUMBER_').update(select=True)        

	def focus_cash_amount(self):
		self.__popup.Element('_CASH_AMOUNT_').SetFocus()
		self.__popup.Element('_CASH_AMOUNT_').update(select=True)        
    
	def focus_card_reference(self):
		self.__popup.Element('_CARD_REFERENCE_').SetFocus()
		self.__popup.Element('_CARD_REFERENCE_').update(select=True)        

	#property
	mobile_number = property(get_mobile_number, set_mobile_number)
	customer_name = property(get_customer_name, set_customer_name)
	customer_address = property(get_customer_address, set_customer_address)
	net_amount = property(get_net_amount, set_net_amount)
	discount_amount_hd = property(get_discount_amount_hd, set_discount_amount_hd)
	roundoff_adjustment = property(get_roundoff_adjustment, set_roundoff_adjustment)
	invoice_amount = property(get_invoice_amount, set_invoice_amount)
	redeem_adjustment_hd = property(get_redeem_adjustment_hd, set_redeem_adjustment_hd)
	exchange_adjustment_hd = property(get_exchange_adjustment_hd, set_exchange_adjustment_hd)
	cash_amount = property(get_cash_amount, set_cash_amount)
	card_amount = property(get_card_amount, set_card_amount)
	card_reference = property(get_card_reference, set_card_reference)
	cash_return = property(get_cash_return, set_cash_return)
	exchange_voucher = property(get_exchange_voucher, set_exchange_voucher)
	exchange_adjustment = property(get_exchange_adjustment, set_exchange_adjustment)
	discount_amount = property(get_discount_amount, set_discount_amount)
	discount_pin = property(get_discount_pin, set_discount_pin)
	available_points = property(get_available_points, set_available_points)
	available_balance = property(get_available_balance, set_available_balance)
	redeem_points = property(get_redeem_points, set_redeem_points)
	redeem_adjustment = property(get_redeem_adjustment, set_redeem_adjustment)
	redeem_pin = property(get_redeem_pin, set_redeem_pin)
	mobile_number_header = property(get_mobile_number_header, set_mobile_number_header)
	customer_name_header = property(get_customer_name_header, set_customer_name_header)
	balance_amount = property(get_balance_amount, set_balance_amount)
	total_received_amount = property(get_total_received_amount, set_total_received_amount)


###
# Item Name Popup Layout  
class ItemNamePopup:
    
    def __init__(self):
        self.__layout = [
            [sg.Listbox(values=[], 
                key='_ITEM_NAME_LIST_', 
                size=(60,6),  font=("Helvetica Bold", 11), 
                select_mode='LISTBOX_SELECT_MODE_SINGLE', 
                enable_events=True, 
                bind_return_key=True)
            ]
        ]

    def get_layout(self):
        return self.__layout
    
    layout = property(get_layout)         

    
###
# Item Name Popup Interface
class UiItemNamePopup:

    def __init__(self, popup):
        self.__popup = popup
        self.__item_code = ''
        self.__item_name = ''       
        self.__item_list = []
        self.__item_line = []
        self.__idx = 0

    def set_item_code(self, item_code):
        self.__item_code = item_code
        
    def get_item_code(self):
        return self.__item_code

    def set_item_name(self, item_name):
        self.__item_name = item_name
        
    def get_item_name(self):
        return self.__item_name

    def set_item_list(self, item_list):
        self.__item_list = item_list
        self.__popup.Element('_ITEM_NAME_LIST_').update(values = self.__item_list, set_to_index=self.__idx)
        
    def get_item_list(self):
        return self.__item_list
        
    def get_item_line(self):
        return self.__popup.Element('_ITEM_NAME_LIST_').get()

    def set_item_line(self, item_line):
        self.__item_line = item_line

    def elements_to_item_line(self):
        self.__item_line.append(self.__item_code)
        self.__item_line.append(self.__item_name)        
       
    def item_line_to_elements(self, idx):
        self.__item_line = self.__items_list[idx]
        self.__item_code = self.__item_line[0]
        self.__item_name = self.__item_line[1]
        
    def add_item_line(self):
        self.__item_line = []
        self.elements_to_item_line()    
        self.__item_list.append(self.__item_line)
        self.__popup.Element('_ITEM_NAME_LIST_').update(values = self.__item_list)

    def prev_item_line(self):
        idx = self.__idx
        if idx > 0:
            idx = idx - 1
            self.__idx = idx
            self.__popup.Element('_ITEM_NAME_LIST_').update(set_to_index=self.__idx)
            
    def next_item_line(self):
        idx = self.__idx
        if idx < len(self.__item_list) - 1:
            idx = idx + 1
            self.__idx = idx
            self.__popup.Element('_ITEM_NAME_LIST_').update(set_to_index=self.__idx)
                   
    def focus_item_list(self):
        self.__popup.Element('_ITEM_NAME_LIST_').SetFocus()
        
    def get_item_idx(self):
        return self.__idx
        
    def set_item_idx(self, idx):
        self.__idx = idx
        self.__popup.Element('_ITEM_NAME_LIST_').update(set_to_index=self.__idx)       
        
    item_list = property(get_item_list, set_item_list)     
    item_code = property(get_item_code, set_item_code)
    item_name = property(get_item_name, set_item_name)
    item_line = property(get_item_line, set_item_line)
    idx = property(get_item_idx, set_item_idx)



###
if __name__ == "__main__":
    print('***Not an executable module, please call the main script')
