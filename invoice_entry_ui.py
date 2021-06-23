import PySimpleGUI as sg
import json
import datetime


with open('./alignpos.json') as file_config:
  config = json.load(file_config)


###
# Main Window Layout
class MainWindow:
             
    sg.theme(config["ui_theme"])

    ui_title_pane_layout = [
        [
            sg.Column(
            [
                [
                    sg.Text('Invoice Entry', size=(36,1) ,font=("Helvetica", 18)),
                    sg.Text('User:', font=("Helvetica", 10)),
                    sg.Input(key='_USER_ID_', font=("Helvetica", 10),size=(15,1),readonly=True, disabled_readonly_text_color=config["ui_readonly_text_color"], disabled_readonly_background_color=config["ui_readonly_background_color"]),
                    sg.Text('Terminal:',font=("Helvetica", 10)),
                    sg.Input(key='_TERMINAL_ID_', font=("Helvetica", 10),size=(4,1),readonly=True, disabled_readonly_text_color=config["ui_readonly_text_color"], disabled_readonly_background_color=config["ui_readonly_background_color"]),
                    sg.Text('Date:',font=("Helvetica", 10)),
                    sg.Input(key='_CURRENT_DATE_', font=("Helvetica", 10),size=(10,1),readonly=True, disabled_readonly_text_color=config["ui_readonly_text_color"], disabled_readonly_background_color=config["ui_readonly_background_color"]),
                ]
            ])
        ]
    ]

    ui_header_pane_layout = [
        [
            sg.Column(
            [
                [
                    sg.Text('Invoice No:', size=(8,1),  font=("Helvetica", 12)),
                    sg.Input(key='_INVOICE_NUMBER_',readonly=True, disabled_readonly_text_color=config["ui_readonly_text_color"], disabled_readonly_background_color=config["ui_readonly_background_color"] ,default_text='' ,font=("Helvetica", 12),size=(10,1)),
                    sg.Text('Reference No:', size=(8,1),  font=("Helvetica", 12)),
                    sg.Input(key='_REFERENCE_NUMBER_',readonly=True, disabled_readonly_text_color=config["ui_readonly_text_color"], disabled_readonly_background_color=config["ui_readonly_background_color"] ,default_text='' ,font=("Helvetica", 12),size=(10,1)),
                    sg.Text('Mobile No:', size=(8,1),  font=("Helvetica", 12)),
                    sg.Input(key='_MOBILE_NUMBER_',readonly=True, disabled_readonly_text_color=config["ui_readonly_text_color"], disabled_readonly_background_color=config["ui_readonly_background_color"] ,default_text='' ,font=("Helvetica", 12),size=(15,1)),
                    sg.Input(key='_PAYMENT_STATUS_',readonly=True, disabled_readonly_text_color=config["ui_readonly_text_color"], disabled_readonly_background_color='gray95' ,default_text='' ,font=("Helvetica", 16), border_width = 0, size=(9,1)),
                    sg.Button('BEGN\nHome', size=(5, 2), font='Calibri 11 bold', key='_BEGIN_', button_color = config["ui_pad_button_color"]),
                    sg.Button('PREV\nPgUp', size=(5, 2), font='Calibri 11 bold', key='_PREVIOUS_', button_color = config["ui_pad_button_color"]),
                    sg.Button('NEXT\nPgDn', size=(5, 2), font='Calibri 11 bold', key='_NEXT_', button_color = config["ui_pad_button_color"]),    
                    sg.Button('END\nEnd', size=(5, 2), font='Calibri 11 bold', key='_END_', button_color = config["ui_pad_button_color"]),    
                ]
            ])    
        ]
    ]

    ui_search_pane_layout = [
        [
            sg.Column(
            [
                [
                    sg.Text('Barcode:', size=(8,1),  font=("Helvetica", 12)),
                    sg.Input(key='_BARCODE_',background_color='White',font=("Helvetica", 12),size=(15,1), enable_events = True),
                    sg.Text('Item Name:', size=(9,1), font=("Helvetica", 12), justification='right'),
                    sg.Input(key='_ITEM_NAME_',background_color='White',font=("Helvetica", 12),size=(25,1), enable_events = True),
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
                         alternating_row_color='lightsteelBlue1',
                         num_rows=12,
                         display_row_numbers=True,
                         col_widths=[10, 13, 20, 5, 5, 8, 10, 8, 10, 10]
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
                    sg.Button('Help\nF1', size=(13, 2), font='Helvetica 11 bold', key='F1', button_color = config["ui_function_button_color"], tooltip=config["ui_f1_tooltip"]),
                    sg.Button('Delete Item\nF2', size=(13, 2), font='Helvetica 11 bold', key='F2', button_color = config["ui_function_button_color"]),
                    sg.Button('Change Quantity\nF3', size=(13, 2), font='Helvetica 11 bold', key='F3', button_color = config["ui_function_button_color"]),
                    sg.Button('Change Price\nF4', size=(13, 2), font='Helvetica 11 bold', key='F4', button_color = config["ui_function_button_color"]),
                    sg.Button('Get Weight\nF5', size=(13, 2), font='Helvetica 11 bold', key='F5', button_color = config["ui_function_button_color"]),
                    sg.Button('Carry Bag\nF6', size=(13, 2), font='Helvetica 11 bold', key='F6', button_color = config["ui_function_button_color"])
                ],
                [
                    sg.Button('New Invoice\nF7', size=(13, 2), font='Helvetica 11 bold', key='F7', button_color = config["ui_function_button_color"]),
                    sg.Button('Delete Invoice\nF8', size=(13, 2), font='Helvetica 11 bold', key='F8', button_color = config["ui_function_button_color"]),
                    sg.Button('List Invoices\nF9', size=(13, 2), font='Helvetica 11 bold', key='F9', button_color = config["ui_function_button_color"]),
                    sg.Button('Print Invoice\nF10', size=(13, 2), font='Helvetica 11 bold', key='F10', button_color = config["ui_function_button_color"]),
                    sg.Button('Cash Position\nF11', size=(13, 2), font='Helvetica 11 bold', key='F11', button_color = config["ui_function_button_color"]),
                    sg.Button('Payment\nF12', size=(13, 2), font='Helvetica 11 bold', key='F12', button_color = config["ui_function_button_color"]),
                    sg.Button('Exit\nEsc', size=(13, 2), font='Helvetica 11 bold', key='ESC', button_color = config["ui_function_button_color"])
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
            ], vertical_alignment = 'top', pad=(45,5), background_color = 'white')
        ]
    ]
    
    ui_summary_pane_layout = [
        [
            sg.Column(
            [
                [
                    sg.Text('Line Items:',  font=("Helvetica", 10) , justification="right", size=(10,1)),
                    sg.Input(key='_LINE_ITEMS_', readonly=True, justification="right", disabled_readonly_text_color=config["ui_readonly_text_color"], disabled_readonly_background_color=config["ui_readonly_background_color"], default_text='0' ,font=("Helvetica", 10), size=(10,1))          
                ],
                [
                    sg.Text('Total Qty:',  font=("Helvetica", 10),justification="right", size=(10,1)),
                    sg.Input(key='_TOTAL_QTY_', readonly=True, justification="right", disabled_readonly_text_color=config["ui_readonly_text_color"], disabled_readonly_background_color=config["ui_readonly_background_color"], default_text='0.00' ,font=("Helvetica", 10), size=(10,1))
                ],
                [
                    sg.Text('Total Amount:',  font=("Helvetica", 10),justification="right", size=(10,1)),
                    sg.Input(key='_TOTAL_AMOUNT_', readonly=True, justification="right", disabled_readonly_text_color=config["ui_readonly_text_color"], disabled_readonly_background_color=config["ui_readonly_background_color"], default_text='0.00' ,font=("Helvetica", 10),size=(10,1)),
                ],
                [
                    sg.Text('CGST:', font=("Helvetica", 10),justification="right",size=(10,1), visible=False),
                    sg.Input(key='_TOTAL_CGST_AMOUNT_', readonly=True, justification="right", disabled_readonly_text_color=config["ui_readonly_text_color"], disabled_readonly_background_color=config["ui_readonly_background_color"], default_text='0.00' , font=("Helvetica", 10), size=(10,1), visible=False),
                ],
                [
                    sg.Text('SGST:', font=("Helvetica", 10),justification="right",size=(10,1), visible=False),
                    sg.Input(key='_TOTAL_SGST_AMOUNT_', readonly=True, justification="right", disabled_readonly_text_color=config["ui_readonly_text_color"], disabled_readonly_background_color=config["ui_readonly_background_color"], default_text='0.00' , font=("Helvetica", 10), size=(10,1), visible=False),
                ],
                [
                    sg.Text('Tax:', font=("Helvetica", 10),justification="right",size=(10,1)),
                    sg.Input(key='_TOTAL_TAX_AMOUNT_', readonly=True, justification="right", disabled_readonly_text_color=config["ui_readonly_text_color"], disabled_readonly_background_color=config["ui_readonly_background_color"], default_text='0.00' , font=("Helvetica", 10), size=(10,1)),
                ],
                [
                    sg.Text('Net Amount:', font=("Helvetica", 10),justification="right",size=(10,1)),
                    sg.Input(key='_NET_AMOUNT_', readonly=True, justification="right", disabled_readonly_text_color=config["ui_readonly_text_color"], disabled_readonly_background_color=config["ui_readonly_background_color"], default_text='0.00' , font=("Helvetica", 10), size=(10,1)),
                ],
                [
                    sg.Text('Discount:', font=("Helvetica", 10),justification="right",size=(10,1)),
                    sg.Input(key='_DISCOUNT_AMOUNT_', readonly=True, justification="right", disabled_readonly_text_color=config["ui_readonly_text_color"], disabled_readonly_background_color=config["ui_readonly_background_color"], default_text='0.00' , font=("Helvetica", 10), size=(10,1)),
                ],
                [
                    sg.Text('Invoice Amt:', font=("Helvetica", 10),justification="right",size=(10,1)),
                    sg.Input(key='_INVOICE_AMOUNT_', readonly=True, justification="right", disabled_readonly_text_color=config["ui_readonly_text_color"], disabled_readonly_background_color=config["ui_readonly_background_color"], default_text='0.00' ,font=("Helvetica", 10),size=(10,1)),
                ],
                [
                    sg.Text('Paid Amt:', font=("Helvetica", 10),justification="right",size=(10,1)),
                    sg.Input(key='_PAID_AMOUNT_', readonly=True, justification="right", disabled_readonly_text_color=config["ui_readonly_text_color"], disabled_readonly_background_color=config["ui_readonly_background_color"], default_text='0.00' , font=("Helvetica", 10), size=(10,1))
                ]            
                
            ], vertical_alignment = 'top', pad = (18,0))           
        ]
    ]        

    ui_keypad_pane_layout = [
        [
            sg.Column(
            [
                [
                    sg.Button('↑', size=(4, 2), font='Calibri 11 bold', key='UP', button_color = config["ui_pad_button_color"]),
                    sg.Button('7', size=(4, 2), font='Calibri 11 bold', key='T7', button_color = config["ui_pad_button_color"]),
                    sg.Button('8', size=(4, 2), font='Calibri 11 bold', key='T8', button_color = config["ui_pad_button_color"]),
                    sg.Button('9', size=(4, 2), font='Calibri 11 bold', key='T9', button_color = config["ui_pad_button_color"]),                
                    
                ],
                [
                    sg.Button('↓', size=(4, 2), font='Calibri 11 bold', key='DOWN', button_color = config["ui_pad_button_color"]),
                    sg.Button('4', size=(4, 2), font='Calibri 11 bold', key='T4', button_color = config["ui_pad_button_color"]),
                    sg.Button('5', size=(4, 2), font='Calibri 11 bold', key='T5', button_color = config["ui_pad_button_color"]),
                    sg.Button('6', size=(4, 2), font='Calibri 11 bold', key='T6', button_color = config["ui_pad_button_color"]),                  
                ],
                [
                    sg.Button('→', size=(4, 2), font='Calibri 11 bold', key='RIGHT', button_color = config["ui_pad_button_color"]),
                    sg.Button('1', size=(4, 2), font='Calibri 11 bold', key='T1', button_color = config["ui_pad_button_color"]),
                    sg.Button('2', size=(4, 2), font='Calibri 11 bold', key='T2', button_color = config["ui_pad_button_color"]),
                    sg.Button('3', size=(4, 2), font='Calibri 11 bold', key='T3', button_color = config["ui_pad_button_color"]),                
                    
                ],
                [
                    sg.Button('←', size=(4, 2), font='Calibri 11 bold', key='LEFT', button_color = config["ui_pad_button_color"]),
                    sg.Button('0', size=(4, 2), font='Calibri 11 bold', key='T0', button_color = config["ui_pad_button_color"]),
                    sg.Button('ENT', size=(10, 2), font='Calibri 11 bold', key='ENTER', button_color = config["ui_pad_button_color"]),
                ],            
                [
                    sg.Button('\u232B', size=(4, 2), font='Calibri 11 bold', key='BACKSPACE', button_color = config["ui_pad_button_color"]),
                    sg.Button('.', size=(4, 2), font='Calibri 11 bold', key='FULL_STOP', button_color = config["ui_pad_button_color"]),
                    sg.Button('TAB', size=(10, 2), font='Calibri 11 bold', key='TAB', button_color = config["ui_pad_button_color"]),
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
            sg.Column(ui_title_pane_layout, size = (990,42), vertical_alignment = 'top', pad = None)     
        ],
        [
            sg.Column(ui_header_pane_layout, size = (990,60), vertical_alignment = 'top', pad = None)     
        ],
        [
            sg.Column(ui_search_pane_layout, size = (990,38), vertical_alignment = 'top', pad = None)     
        ],
        [
            sg.Column(ui_detail_pane_layout, size = (990,338), vertical_alignment = 'top', pad = None)     
        ],
        [
            sg.Column(ui_action_pane_layout, size = (990,120), vertical_alignment = 'top', pad = None)     
        ]         
    ]

    ui_right_panes_layout = [
        [
            sg.Column(ui_company_pane_layout, size = (530,75), vertical_alignment = 'top', pad = ((0,0),(0,0)), background_color='White')     
        ],
        [
            sg.Column(ui_summary_pane_layout, size = (530,230), vertical_alignment = 'top', pad = ((3,0),(10,0)), background_color=None)     
        ],
        [
            sg.Column(ui_keypad_pane_layout, size = (530,270), vertical_alignment = 'top', pad = ((12,12),(0,0)), background_color=None)     
        ],
        [
            sg.Column(ui_logo_pane_layout, size = (530,40), vertical_alignment = 'top', pad = ((0,0),(10,0)), background_color='White')     
        ]        
    ]

    layout = [
        [
            sg.Column(ui_left_panes_layout, size = (990,700), vertical_alignment = 'top', pad = (0,0), background_color='White'),
            sg.Column(ui_right_panes_layout, size = (530,700), vertical_alignment = 'top', pad = None, background_color=None)   
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
        self.__payment_status = str('')
        
        self.__window['_REFERENCE_NUMBER_'].Widget.config(takefocus=0)
        self.__window['_INVOICE_NUMBER_'].Widget.config(takefocus=0)
        self.__window['_MOBILE_NUMBER_'].Widget.config(takefocus=0)
        self.__window['_PAYMENT_STATUS_'].Widget.config(takefocus=0)
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

    def set_payment_status(self, payment_status):
        self.__payment_status = payment_status
        self.__window.Element('_PAYMENT_STATUS_').update(value = self.__payment_status)
        
    def get_payment_status(self):
        self.__payment_status = self.__window.Element('_PAYMENT_STATUS_').get()        
        return self.__payment_status

    reference_number = property(get_reference_number, set_reference_number) 
    invoice_number = property(get_invoice_number, set_invoice_number) 
    mobile_number = property(get_mobile_number, set_mobile_number) 
    payment_status = property(get_payment_status, set_payment_status) 
        

###
# Main Window - Search Pane Interface
class UiSearchPane:

    def __init__(self, window):
        self.__window = window
        self.__barcode = str('')
        self.__item_name = str('')
        
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
        self.__window['F9'].Widget.config(takefocus=0)
        self.__window['F10'].Widget.config(takefocus=0)
        self.__window['F11'].Widget.config(takefocus=0)
        self.__window['F12'].Widget.config(takefocus=0)
        self.__window['ESC'].Widget.config(takefocus=0)    


###
# Main Window - Sumary Pane Interface
class UiSummaryPane:

    def __init__(self, window):
        self.__window = window
        self.__line_items = 0
        self.__total_qty = float(0.00)
        self.__total_amount = float(0.00)
        self.__total_tax_amount = float(0.00)
        self.__total_cgst_amount = float(0.00)
        self.__total_sgst_amount = float(0.00)
        self.__net_amount = float(0.00)
        self.__discount_amount = float(0.00)
        self.__invoice_amount = float(0.00)
        self.__paid_amount = float(0.00)

        self.__window['_LINE_ITEMS_'].Widget.config(takefocus=0)
        self.__window['_TOTAL_QTY_'].Widget.config(takefocus=0)
        self.__window['_TOTAL_AMOUNT_'].Widget.config(takefocus=0)
        self.__window['_TOTAL_TAX_AMOUNT_'].Widget.config(takefocus=0)
        self.__window['_TOTAL_CGST_AMOUNT_'].Widget.config(takefocus=0)
        self.__window['_TOTAL_SGST_AMOUNT_'].Widget.config(takefocus=0)
        self.__window['_NET_AMOUNT_'].Widget.config(takefocus=0)
        self.__window['_DISCOUNT_AMOUNT_'].Widget.config(takefocus=0)
        self.__window['_INVOICE_AMOUNT_'].Widget.config(takefocus=0)
        self.__window['_PAID_AMOUNT_'].Widget.config(takefocus=0)

    def set_line_items(self, line_items):
        self.__line_items = line_items
        self.__window.Element('_LINE_ITEMS_').update(value = self.__line_items)
        
    def get_line_items(self):
        self.__line_items = self.__window.Element('_LINE_ITEMS_').get()        
        return self.__line_items
        
    def set_total_qty(self, total_qty):
        self.__total_qty = total_qty
        self.__window.Element('_TOTAL_QTY_').update(value = self.__total_qty)
        
    def get_total_qty(self):
        self.__total_qty = self.__window.Element('_TOTAL_QTY_').get()        
        return self.__total_qty

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
        self.__total_cgst_amount = total_cgst_amount
        self.__window.Element('_TOTAL_CGST_AMOUNT_').update(value = "{:.2f}".format(self.__total_cgst_amount))
        
    def get_total_cgst_amount(self):
        self.__total_cgst_amount = self.__window.Element('_TOTAL_CGST_AMOUNT_').get()        
        return self.__total_cgst_amount

    def set_total_sgst_amount(self, total_sgst_amount):
        self.__total_sgst_amount = total_sgst_amount
        self.__window.Element('_TOTAL_SGST_AMOUNT_').update(value = "{:.2f}".format(self.__total_sgst_amount))
        
    def get_total_sgst_amount(self):
        self.__total_sgst_amount = self.__window.Element('_TOTAL_SGST_AMOUNT_').get()        
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

    def set_invoice_amount(self, invoice_amount):
        self.__invoice_amount = invoice_amount
        self.__window.Element('_INVOICE_AMOUNT_').update(value = "{:.2f}".format(self.__invoice_amount))
        
    def get_invoice_amount(self):
        self.__invoice_amount = self.__window.Element('_INVOICE_AMOUNT_').get()        
        return self.__invoice_amount

    def set_paid_amount(self, paid_amount):
        self.__paid_amount = paid_amount
        self.__window.Element('_PAID_AMOUNT_').update(value = "{:.2f}".format(self.__paid_amount))
        
    def get_paid_amount(self):
        self.__paid_amount = self.__window.Element('_PAID_AMOUNT_').get()        
        return self.__paid_amount

    line_items = property(get_line_items, set_line_items)
    total_qty = property(get_total_qty, set_total_qty)
    total_amount = property(get_total_amount, set_total_amount)
    total_tax_amount = property(get_total_tax_amount, set_total_tax_amount)
    total_cgst_amount = property(get_total_cgst_amount, set_total_cgst_amount)
    total_sgst_amount = property(get_total_sgst_amount, set_total_sgst_amount)
    net_amount = property(get_net_amount, set_net_amount)
    discount_amount = property(get_discount_amount, set_discount_amount)
    invoice_amount = property(get_invoice_amount, set_invoice_amount)
    paid_amount = property(get_paid_amount, set_paid_amount)


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

###
# Change Quantity Popup Layout  
class ChangeQtyPopup:
    
    def __init__(self):
        self.__layout = [
            [sg.Text('', key='_ITEM_NAME_', size=(30,2),  font=("Helvetica Bold", 12))],
            [sg.Text('Existing Quantity:', size=(15,1),  font=("Helvetica", 11)),     
             sg.Input(key='_EXISTING_QTY_',readonly=True, background_color=config["ui_readonly_background_color"], disabled_readonly_text_color=config["ui_readonly_text_color"],font=("Helvetica", 11),size=(15,1))],
            [sg.Text('New Quantity:', size=(15,1),  font=("Helvetica", 11)),             
             sg.Input(key='_NEW_QTY_',readonly=False, focus=True, background_color='white',font=("Helvetica", 11),size=(15,1), enable_events=True)],
            [sg.Text('')],
            [sg.Button('Ok-F12', size=(8, 1), font='Calibri 12 bold', key='_CHANGE_QTY_OK_', button_color = config["ui_pad_button_color"]),
             sg.Button('Exit-Esc', size=(8, 1), font='Calibri 12 bold', key='_CHANGE_QTY_ESC_', button_color = config["ui_pad_button_color"])]           
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
        
    def get_new_qty(self):
        self.__new_qty = self.__popup.Element('_NEW_QTY_').get()        
        return self.__new_qty

    def focus_existing_qty(self):
        self.__popup.Element('_EXISTING_QTY_').SetFocus() 

    def focus_new_qty(self):
        self.__popup.Element('_NEW_QTY_').SetFocus() 

    item_name = property(get_item_name, set_item_name)     
    existing_qty = property(get_existing_qty, set_existing_qty) 
    new_qty = property(get_new_qty, set_new_qty) 


###
if __name__ == "__main__":
    print('***Not an executable module, please call the main script')
