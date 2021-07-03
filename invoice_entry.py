import PySimpleGUI as sg
import datetime
import json
import sys
import platform
from pynput.keyboard import Key, Controller
from invoice_entry_ui import MainWindow, UiTitlePane, UiHeaderPane, UiSearchPane, UiDetailPane, UiActionPane, UiSummaryPane, UiKeypadPane, \
                             ChangeQtyPopup, UiChangeQtyPopup, ItemNamePopup, UiItemNamePopup,\
                             PaymentPopup, UiPaymentPopup
from alignpos_db import ConnAlignPos, DbTable, DbQuery, Customer, Item, Invoice, InvoiceItem, Estimate, EstimateItem


######
def initialize_title_pane():
    ui_title_pane.user_id = 'XXX'
    ui_title_pane.terminal_id = '101'
    ui_title_pane.current_date = '2021/06/13'


def initialize_header_pane():
    ui_header_pane.reference_number = ''
    ui_header_pane.invoice_number = ''
    ui_header_pane.payment_status = ''
    ui_header_pane.mobile_number = '0000000000'
    ui_header_pane.customer_number = ''
    ui_header_pane.customer_name = ''
    ui_header_pane.customer_address = ''

    
def initialize_search_pane():
    ui_search_pane.barcode = ''
    ui_search_pane.item_name = ''
    ui_search_pane.item_name = ''
    ui_search_pane.focus_barcode()


def initialize_detail_pane():
    ui_detail_pane.items_list = []
    ui_detail_pane.item_code = str('')
    ui_detail_pane.barcode = str('')
    ui_detail_pane.item_name = str('')
    ui_detail_pane.uom = str('')
    ui_detail_pane.qty = float(0.0)
    ui_detail_pane.selling_price = float(0.00)
    ui_detail_pane.selling_amount = float(0.00)
    ui_detail_pane.tax_rate = float(0.00)
    ui_detail_pane.tax_amount = float(0.00)
    ui_detail_pane.net_amount = float(0.00)
    ui_detail_pane.cgst_tax_rate = float(0.00)
    ui_detail_pane.sgst_tax_rate = float(0.00)
    ui_detail_pane.item_line = [] 


def initialize_summary_pane():
    ui_summary_pane.line_items = 0
    ui_summary_pane.total_amount = 0.00
    ui_summary_pane.total_tax_amount = 0.00
    ui_summary_pane.net_amount = 0.00
    ui_summary_pane.total_cgst_amount = 0.00
    ui_summary_pane.total_sgst_amount = 0.00
    ui_summary_pane.total_tax_amount = 0.00
    ui_summary_pane.discount_amount = 0.00          
    ui_summary_pane.roundoff_amount = 0.00          
    ui_summary_pane.invoice_amount = 0.00
    ui_summary_pane.paid_amount = 0.00


def initialize_action_pane(context):
    if context == 'INVOICE':
        ui_window.Element('F1').update(text='New Invoice\nF1')
        ui_window.Element('F2').update(text='Save Invoice\nF2')
        ui_window.Element('F3').update(text='Payment\nF3')
        ui_window.Element('F4').update(text='Print Invoice\nF4', button_color = config["ui_function_button_color"], disabled = False)
        ui_window.Element('F5').update(text='Delete Invoice\nF5')
    else:
        ui_window.Element('F1').update(text='Item Addon\nF1')
        ui_window.Element('F2').update(text='Change Quantity\nF2')
        ui_window.Element('F3').update(text='Change Price\nF3')
        ui_window.Element('F4').update(text='', button_color='gray99', disabled = True)
        ui_window.Element('F5').update(text='Delete Item\nF5')
       

def move_db_item_to_ui_detail_pane(db_item_row):
    ui_detail_pane.item_code = db_item_row.name
    ui_detail_pane.barcode = db_item_row.barcode
    ui_detail_pane.item_name = db_item_row.item_name
    ui_detail_pane.uom = db_item_row.uom
    ui_detail_pane.qty = 1
    ui_detail_pane.selling_price = db_item_row.selling_price
    ui_detail_pane.cgst_tax_rate = db_item_row.cgst_tax_rate
    ui_detail_pane.sgst_tax_rate = db_item_row.sgst_tax_rate
    ui_detail_pane.selling_amount = float(ui_detail_pane.qty) * float(ui_detail_pane.selling_price)
    ui_detail_pane.tax_rate = float(ui_detail_pane.cgst_tax_rate) + float(ui_detail_pane.sgst_tax_rate)
    ui_detail_pane.tax_amount = float(ui_detail_pane.selling_amount) * float(ui_detail_pane.tax_rate) / 100
    ui_detail_pane.net_amount = float(ui_detail_pane.selling_amount) + float(ui_detail_pane.tax_amount)
    
    ui_detail_pane.add_item_line()    


def move_db_invoice_item_to_ui_detail_pane(db_invoice_item_row):
    ui_detail_pane.item_code = db_invoice_item_row.item
    
    db_item_row = db_item_table.get_row(db_invoice_item_row.item)
    if db_item_row:
        ui_detail_pane.barcode = db_item_row.barcode
        ui_detail_pane.item_name = db_item_row.item_name
        ui_detail_pane.uom = db_item_row.uom
        ui_detail_pane.selling_price = db_item_row.selling_price

    ui_detail_pane.qty = db_invoice_item_row.qty
    ui_detail_pane.cgst_tax_rate = db_invoice_item_row.cgst_tax_rate
    ui_detail_pane.sgst_tax_rate = db_invoice_item_row.sgst_tax_rate
    ui_detail_pane.selling_amount = float(ui_detail_pane.qty) * float(ui_detail_pane.selling_price)
    ui_detail_pane.tax_rate = float(ui_detail_pane.cgst_tax_rate) + float(ui_detail_pane.sgst_tax_rate)
    ui_detail_pane.tax_amount = float(ui_detail_pane.selling_amount) * float(ui_detail_pane.tax_rate) / 100
    ui_detail_pane.net_amount = float(ui_detail_pane.selling_amount) + float(ui_detail_pane.tax_amount)
    
    ui_detail_pane.add_item_line()    
    
    
def process_carry_bag():
    filter = "item_code='{}'"
    db_item_row = db_item_table.first(filter.format(carry_bag_item))
    move_db_item_to_ui_detail_pane(db_item_row)
    sum_item_list()


def process_barcode(barcode):
    if not barcode:
        return
    if not ui_header_pane.invoice_number == '':
        return
    
    print('here ', len(ui_search_pane.barcode), ' ', ui_search_pane.barcode[0])
       
    if (ui_search_pane.barcode[0].isnumeric() and len(ui_search_pane.barcode) > 12):
        filter = "barcode='{}'"
        db_item_row = db_item_table.first(filter.format(barcode))
        if db_item_row:
            move_db_item_to_ui_detail_pane(db_item_row)       
    elif (ui_search_pane.barcode[0] == 'I' and len(ui_search_pane.barcode) > 8):
        filter = "item_code='{}'"   
        db_item_row = db_item_table.first(filter.format(barcode))
        if db_item_row:
            move_db_item_to_ui_detail_pane(db_item_row)
    elif (ui_search_pane.barcode[0] == 'E' and len(ui_search_pane.barcode) > 7):
        filter = "parent='{}'"   
        db_estimate_item_cursor = db_estimate_item_table.list(filter.format(barcode))
        for db_estimate_item_row in db_estimate_item_cursor:
            print(db_estimate_item_row.name)
            move_db_invoice_item_to_ui_detail_pane(db_estimate_item_row)
    else:
        return
        
    sum_item_list()


def process_item_name(item_code):
    filter = "item_code='{}'"   
    
    db_item_row = db_item_table.first(filter.format(item_code))
    if db_item_row:
        move_db_item_to_ui_detail_pane(db_item_row)
        sum_item_list()  

        
def sum_item_list():
    line_items = 0
    total_amount = 0.00
    total_tax_amount = 0.00
    total_cgst_amount = 0.00
    total_sgst_amount = 0.00
    net_amount = 0.00
   
    for item_line in ui_detail_pane.items_list:
        line_items += 1
        total_amount += float(item_line[6])
        total_tax_amount += float(item_line[8])
        net_amount += float(item_line[9])
        total_cgst_amount += float(item_line[10])
        total_sgst_amount += float(item_line[11])

    ui_summary_pane.line_items = line_items
    ui_summary_pane.total_amount = total_amount
    ui_summary_pane.total_tax_amount = total_tax_amount
    ui_summary_pane.net_amount = net_amount
    ui_summary_pane.total_cgst_amount = total_cgst_amount
    ui_summary_pane.total_sgst_amount = total_sgst_amount
    invoice_actual_amount = net_amount - float(ui_summary_pane.discount_amount)
    invoice_rounded_amount = round(invoice_actual_amount, 0)
    ui_summary_pane.invoice_amount = invoice_rounded_amount
    ui_summary_pane.roundoff_amount = invoice_rounded_amount - invoice_actual_amount    


def save_invoice():
    if ui_header_pane.invoice_number != '':
        return
    if not len(ui_detail_pane.items_list) > 0:
        return    

    if ui_header_pane.reference_number == '':
        insert_invoice()
    else:
        update_invoice()


def insert_invoice():
    print('insert')
    if len(ui_detail_pane.items_list) == 0:
        return

    db_query = DbQuery(db_conn, 'SELECT nextval("REFERENCE_NUMBER")')
    for db_row in db_query.result:
        ui_header_pane.reference_number = db_row[0]

    customer_number = walk_in_customer
    db_customer_row = db_customer_table.get_row(customer_number)
    if db_customer_row:
        ui_header_pane.mobile_number = db_customer_row.mobile_number
        ui_header_pane.customer_number = db_customer_row.name
        ui_header_pane.customer_name = db_customer_row.customer_name
        ui_header_pane.customer_address = db_customer_row.address

    db_invoice_row = db_invoice_table.new_row()

    db_invoice_row.name = ui_header_pane.reference_number
    db_invoice_row.customer = customer_number
    db_invoice_row.posting_date = ui_title_pane.current_date    
    db_invoice_row.total_amount = ui_summary_pane.total_amount
    db_invoice_row.net_amount = ui_summary_pane.net_amount
    db_invoice_row.invoice_amount = ui_summary_pane.invoice_amount
    db_invoice_row.cgst_tax_amount = ui_summary_pane.total_cgst_amount
    db_invoice_row.sgst_tax_amount = ui_summary_pane.total_sgst_amount
    db_invoice_row.paid_amount = ui_summary_pane.paid_amount   
    db_invoice_row.terminal_id = ui_title_pane.terminal_id  

    db_invoice_table.create_row(db_invoice_row)
   
    for idx in range(len(ui_detail_pane.items_list)): 
        ui_detail_pane.item_line_to_elements(idx)
        
        db_invoice_item_row = db_invoice_item_table.new_row()
        
        db_invoice_item_row.name = ui_header_pane.reference_number + f"{idx:04d}"
        db_invoice_item_row.parent = ui_header_pane.reference_number
        db_invoice_item_row.item = ui_detail_pane.item_code
        db_invoice_item_row.qty = ui_detail_pane.qty
        db_invoice_item_row.standard_selling_price = ui_detail_pane.selling_price
        db_invoice_item_row.applied_selling_price = ui_detail_pane.selling_price
        db_invoice_item_row.cgst_tax_rate = ui_detail_pane.cgst_tax_rate
        db_invoice_item_row.sgst_tax_rate = ui_detail_pane.sgst_tax_rate
      
        db_invoice_item_table.create_row(db_invoice_item_row)

    db_session.commit()
    

def update_invoice():
    print('update')

    db_invoice_row = db_invoice_table.get_row(ui_header_pane.reference_number)

    if not db_invoice_row:
        return

    db_invoice_row.customer = ui_header_pane.customer_number
    db_invoice_row.total_amount = ui_summary_pane.total_amount
    db_invoice_row.net_amount = ui_summary_pane.net_amount
    db_invoice_row.invoice_amount = ui_summary_pane.invoice_amount
    db_invoice_row.cgst_tax_amount = ui_summary_pane.total_cgst_amount
    db_invoice_row.sgst_tax_amount = ui_summary_pane.total_sgst_amount
    db_invoice_row.paid_amount = ui_summary_pane.paid_amount   
    db_invoice_row.terminal_id = ui_title_pane.terminal_id  

    filter = "parent='{}'"
    db_invoice_item_cursor = db_invoice_item_table.list(filter.format(ui_header_pane.reference_number))
    for db_invoice_item_row in db_invoice_item_cursor:
        db_invoice_item_table.delete_row(db_invoice_item_row)

    db_session.flush()
    
    for idx in range(len(ui_detail_pane.items_list)): 
        ui_detail_pane.item_line_to_elements(idx)
        
        db_invoice_item_row = db_invoice_item_table.new_row()
        
        db_invoice_item_row.name = ui_header_pane.reference_number + f"{idx:04d}"
        db_invoice_item_row.parent = ui_header_pane.reference_number
        db_invoice_item_row.item = ui_detail_pane.item_code
        db_invoice_item_row.qty = ui_detail_pane.qty
        db_invoice_item_row.standard_selling_price = ui_detail_pane.selling_price
        db_invoice_item_row.applied_selling_price = ui_detail_pane.selling_price
        db_invoice_item_row.cgst_tax_rate = ui_detail_pane.cgst_tax_rate
        db_invoice_item_row.sgst_tax_rate = ui_detail_pane.sgst_tax_rate
      
        db_invoice_item_table.create_row(db_invoice_item_row)

    db_session.commit()


def delete_invoice():
    print('delete1')
    if not ui_header_pane.reference_number or ui_header_pane.reference_number == '':
        return

    filter = "parent='{}'"
    db_invoice_item_cursor = db_invoice_item_table.list(filter.format(ui_header_pane.reference_number))
    for db_invoice_item_row in db_invoice_item_cursor:
        print(db_invoice_item_row.name)
        db_invoice_item_table.delete_row(db_invoice_item_row)

    db_session.flush()
    
    db_invoice_row = db_invoice_table.get_row(ui_header_pane.reference_number)
    if db_invoice_row:
        db_invoice_table.delete_row(db_invoice_row)
    
    db_session.commit()
    

def clear_invoice():
    print('clear')
    initialize_header_pane()
    initialize_search_pane()    
    initialize_detail_pane()
    initialize_summary_pane()
    

def show_invoice(db_invoice_row):
    if not db_invoice_row:
        return
        
    ui_header_pane.reference_number = db_invoice_row.name
    ui_header_pane.invoice_number = db_invoice_row.invoice_number

    customer_number = db_invoice_row.customer
    db_customer_row = db_customer_table.get_row(customer_number)
    if db_customer_row:
        ui_header_pane.mobile_number = db_customer_row.mobile_number
        ui_header_pane.customer_number = db_customer_row.name
        ui_header_pane.customer_name = db_customer_row.customer_name
        ui_header_pane.customer_address = db_customer_row.address

    ui_detail_pane.item_line = []
    filter = "parent='{}'"
    db_invoice_item_cursor = db_invoice_item_table.list(filter.format(ui_header_pane.reference_number))    
    for db_invoice_item_row in db_invoice_item_cursor:
        move_db_invoice_item_to_ui_detail_pane(db_invoice_item_row)
    sum_item_list()
    if (db_invoice_row.discount_amount):
        ui_summary_pane.discount_amount = db_invoice_row.discount_amount
    else:
        ui_summary_pane.discount_amount = 0.00       
    ui_summary_pane.invoice_amount = db_invoice_row.invoice_amount
    ui_summary_pane.paid_amount = db_invoice_row.paid_amount
    

def goto_first_invoice():
    db_invoice_row = db_invoice_table.first('')
    if db_invoice_row:
        clear_invoice()    
        show_invoice(db_invoice_row)


def goto_previous_invoice():
    if ui_header_pane.reference_number:
        name = ui_header_pane.reference_number
        filter = "name < '{}'"
        db_invoice_row = db_invoice_table.last(filter.format(name))
        if db_invoice_row:
            clear_invoice()    
            show_invoice(db_invoice_row)


def goto_next_invoice():
    if ui_header_pane.reference_number:
        name = ui_header_pane.reference_number
        filter = "name > '{}'"
        db_invoice_row = db_invoice_table.first(filter.format(name))
        if db_invoice_row:
            clear_invoice()    
            show_invoice(db_invoice_row)


def goto_last_invoice():
    db_invoice_row = db_invoice_table.last('')
    if db_invoice_row:
        clear_invoice()    
        show_invoice(db_invoice_row)


    
######
# Popup window for Change Quantity
def open_change_qty_popup(row_item):

    ui_detail_pane.item_line_to_elements(row_item)
    
    change_qty_popup = ChangeQtyPopup()
    
    ui_popup = sg.Window("Change Quantity", 
                    change_qty_popup.layout, 
                    location=(300,250), 
                    size=(350,185), 
                    modal=True, 
                    finalize=True,
                    keep_on_top = True,
                    return_keyboard_events=True
                )

    ui_change_qty_popup = UiChangeQtyPopup(ui_popup)
    
    ui_change_qty_popup.item_name = ui_detail_pane.item_name
    ui_change_qty_popup.existing_qty = ui_detail_pane.qty
    ui_change_qty_popup.new_qty = ''
    
    while True:
        event, values = ui_popup.read()
        print('eventc=', event)
        if event in ("Exit", '_CHANGE_QTY_ESC_', 'Escape:27') or event == sg.WIN_CLOSED:
            break        
        if event == "_CHANGE_QTY_OK_" or event == "F12:123" or event == '\r':
            print('here')
            if not ui_change_qty_popup.new_qty:
                break;
            if float(ui_change_qty_popup.new_qty) > 0 and ui_change_qty_popup.new_qty != ui_change_qty_popup.existing_qty:
                ui_detail_pane.qty = ui_change_qty_popup.new_qty
                ui_detail_pane.selling_amount = float(ui_detail_pane.qty) * float(ui_detail_pane.selling_price)
                ui_detail_pane.tax_rate = float(ui_detail_pane.cgst_tax_rate) + float(ui_detail_pane.sgst_tax_rate)
                ui_detail_pane.tax_amount = float(ui_detail_pane.selling_amount) * float(ui_detail_pane.tax_rate) / 100
                ui_detail_pane.net_amount = float(ui_detail_pane.selling_amount) + float(ui_detail_pane.tax_amount)
                ui_detail_pane.update_item_line(row_item)                
            break
            
    ui_popup.close() 


######
# Popup window for Payment
def open_payment_popup():
    payment_popup = PaymentPopup()
    
    ui_popup = sg.Window("Payment", 
                    payment_popup.layout,
                    location=(400,40), 
                    size=(500,510), 
                    modal=True, 
                    finalize=True,
                    keep_on_top = True,
                    return_keyboard_events=True
                )

    ui_payment_popup = UiPaymentPopup(ui_popup)

    initialize_payment_popup_elements(ui_payment_popup)
    
    #ui_payment_popup.focus_mobile_number()
    
    prev_event = ''   
    while True:
        event, values = ui_popup.read()
        print('eventp=', event)
        
        if event in ('\t', 'TAB') and prev_event == '_MOBILE_NUMBER_':
            if not ui_payment_popup.mobile_number == '':
                process_mobile_number(ui_payment_popup)

        if event == '_MOBILE_NUMBER_' and len(ui_payment_popup.mobile_number) > 9:
                process_mobile_number(ui_payment_popup)
           
        if event in ('\t', 'TAB') and prev_event == '_CASH_AMOUNT_':
            set_payment_popup_elements(ui_payment_popup)
            
        if event in ('\t', 'TAB') and prev_event == '_CARD_AMOUNT_':
            set_payment_popup_elements(ui_payment_popup)
            
        if event in ("Exit", '_PAYMENT_ESC_', 'Escape:27') or event == sg.WIN_CLOSED:
            break
            
        if event == "_PAYMENT_OK_" or event == "F12:123" or event == '\r':
            set_payment_popup_elements(ui_payment_popup)
            if float(ui_payment_popup.balance_amount) == 0:
                if float(ui_payment_popup.card_amount) > 0 and ui_payment_popup.card_reference == '':
                    sg.popup('Enter Card Reference',keep_on_top = True)            
                else:
                    break
            else:
                sg.popup('Settle Balance amount',keep_on_top = True)
                ui_payment_popup.focus_cash_amount()
                            
        prev_event = event
            
    ui_popup.close() 


def process_mobile_number(ui_payment_popup):    
    filter = "mobile_number='{}'"
    db_customer_row = db_customer_table.first(filter.format(ui_payment_popup.mobile_number))
    if db_customer_row:
        print(db_customer_row.customer_name)
        ui_payment_popup.customer_number = db_customer_row.name
        ui_payment_popup.customer_name = db_customer_row.customer_name
        ui_payment_popup.customer_address = db_customer_row.address
        ui_payment_popup.loyalty_points = db_customer_row.loyalty_points
        ui_payment_popup.loyalty_balance = db_customer_row.loyalty_points *  0.10     
        ui_header_pane.mobile_number = db_customer_row.mobile_number
        ui_header_pane.customer_number = db_customer_row.name
        ui_header_pane.mobile_number = db_customer_row.mobile_number
        ui_header_pane.customer_name = db_customer_row.customer_name
        ui_header_pane.customer_address = db_customer_row.address


def initialize_payment_popup_elements(ui_payment_popup):
    ui_payment_popup.mobile_number = ui_header_pane.mobile_number
    ui_payment_popup.customer_name = ui_header_pane.customer_name
    ui_payment_popup.customer_number = ui_header_pane.customer_number
    ui_payment_popup.customer_address = ui_header_pane.customer_address
    ui_payment_popup.net_amount = ui_summary_pane.net_amount
    ui_payment_popup.discount_amount = ui_summary_pane.discount_amount
    invoice_actual_amount = float(ui_payment_popup.net_amount) - float(ui_payment_popup.discount_amount)
    invoice_rounded_amount = round(invoice_actual_amount, 0)
    ui_payment_popup.invoice_amount = invoice_rounded_amount
    ui_payment_popup.roundoff_adjustment = invoice_rounded_amount - invoice_actual_amount
    ui_payment_popup.cash_amount = invoice_rounded_amount
    ui_payment_popup.total_received_amount =    float(ui_payment_popup.cash_amount) +\
                                                float(ui_payment_popup.card_amount)


def set_payment_popup_elements(ui_payment_popup):
    ui_payment_popup.total_received_amount = float(ui_payment_popup.cash_amount) + \
                            float(ui_payment_popup.card_amount) + \
                            float(ui_payment_popup.exchange_adjustment) + \
                            float(ui_payment_popup.redeem_adjustment)
    ui_payment_popup.cash_return = 0.00
    if float(ui_payment_popup.total_received_amount) > float(ui_payment_popup.invoice_amount):
        ui_payment_popup.cash_return = min(float(ui_payment_popup.total_received_amount) - float(ui_payment_popup.invoice_amount),\
                                                float(ui_payment_popup.cash_amount))
        print('here1:',ui_payment_popup.cash_return)    
    ui_payment_popup.balance_amount =   float(ui_payment_popup.total_received_amount) - \
                                        float(ui_payment_popup.invoice_amount) - \
                                        float(ui_payment_popup.cash_return)   


def process_payment():
    db_invoice_row = db_invoice_table.get_row(ui_header_pane.reference_number)

    if not db_invoice_row:
        return

    ui_summary_pane.discount_amount = 0.00          
    ui_summary_pane.invoice_amount = round(float(ui_summary_pane.net_amount), 0)
    ui_summary_pane.paid_amount = ui_summary_pane.invoice_amount
    db_invoice_row.discount_amount = ui_summary_pane.discount_amount
    db_invoice_row.invoice_amount = ui_summary_pane.invoice_amount
    db_invoice_row.paid_amount = ui_summary_pane.paid_amount   
    db_query = DbQuery(db_conn, 'SELECT nextval("INVOICE_NUMBER")')
    for db_row in db_query.result:
        ui_header_pane.invoice_number = db_row[0]
    db_invoice_row.invoice_number = ui_header_pane.invoice_number
    db_invoice_table.update_row(db_invoice_row)
    db_session.commit()
    
    
######
# Popup window for selecting Item
def open_item_name_popup(item_name):
    if not item_name:
        return

    if not len(ui_search_pane.item_name) > 2:
        return

    filter = "upper(item_name) like upper('%{}%')"       
    db_item_cursor = db_item_table.list(filter.format(item_name))
    if not db_item_cursor:
        return
        
    item_name_popup = ItemNamePopup()
    
    ui_popup = sg.Window("Item Name", 
                    item_name_popup.layout, 
                    location=(457,184), 
                    size=(350,130), 
                    modal=True, 
                    finalize=True,
                    return_keyboard_events=True, 
                    no_titlebar = True, 
                    element_padding=(0,0), 
                    background_color = 'White', 
                    keep_on_top = True,                    
                    margins=(0,0)
                )

    ui_item_name_popup = UiItemNamePopup(ui_popup)
    ui_item_name_popup.focus_item_list

    ui_item_name_popup.item_list = []
    for db_item_row in db_item_cursor:
        #print(db_item_row.item_code, db_item_row.item_name)
        ui_item_name_popup.item_code = db_item_row.item_code
        ui_item_name_popup.item_name = db_item_row.item_name
        ui_item_name_popup.add_item_line()
    ui_item_name_popup.idx = 0

    prev_event = ''    
    while True:
        event, values = ui_popup.read()
        print('eventn=', event)
        if event == 'Down:40':
            ui_item_name_popup.next_item_line()
        if event == 'Up:38':
            ui_item_name_popup.prev_item_line()            
        if event in ("Exit", '_ITEM_NAME_ESC_', 'Escape:27') or event == sg.WIN_CLOSED:
            break        
        if event == '\r':
            sel_item_code =  values['_ITEM_NAME_LIST_'][0][0]
            process_item_name(sel_item_code)
            break
        prev_event = event
        
    ui_popup.close() 

######
# Popup window for message
def open_message_popup(message):
        
    ui_popup = sg.Window(   'Confirm', 
                            [
                                [sg.Text(message)],      
                                [sg.Button('Ok - F12', key='_MESSAGE_OK_'), 
                                 sg.Button('Cancel - Esc', key='_MESSAGE_CANCEL_')
                                ]
                            ], 
                            keep_on_top=True, 
                            modal=True, 
                            return_keyboard_events=True
                        )    
    
    retval = ''
    while True:
        event, values = ui_popup.read()
        print (event, values)
        if event in ('_MESSAGE_OK_', 'F12:123'):
            retval = 'Ok'
            break
        elif event in ('_MESSAGE_CANCEL_', 'Escape:27'):
            retval = 'Cancel'
            break
    ui_popup.close()
    return retval

    
######
# Global variables
with open('./alignpos.json') as file_config:
  config = json.load(file_config)

walk_in_customer = config["walk_in_customer"]
carry_bag_item = config["carry_bag_item"]

db_conn = ConnAlignPos()
db_session = db_conn.session

db_customer_table = DbTable(db_conn, Customer)
db_item_table = DbTable(db_conn, Item)
db_invoice_table = DbTable(db_conn, Invoice)
db_invoice_item_table = DbTable(db_conn, InvoiceItem)
db_estimate_table = DbTable(db_conn, Estimate)
db_estimate_item_table = DbTable(db_conn, EstimateItem)

main_window = MainWindow()
ui_window = sg.Window('Invoice Entry', 
                main_window.layout, 
                background_color='White',
                font='Helvetica 11', 
                finalize=True, 
                location=(0,0), 
                size=(1600,800), 
                keep_on_top=False, 
                resizable=True,
                return_keyboard_events=True, 
                use_default_focus=False
         )

ui_title_pane = UiTitlePane(ui_window)
ui_header_pane = UiHeaderPane(ui_window)
ui_search_pane = UiSearchPane(ui_window)
ui_detail_pane = UiDetailPane(ui_window)
ui_action_pane = UiActionPane(ui_window)
ui_summary_pane = UiSummaryPane(ui_window)
ui_keypad_pane = UiKeypadPane(ui_window)


######
# Main function
def main():
    
    initialize_title_pane()
    initialize_header_pane()
    initialize_search_pane()
    initialize_action_pane('INVOICE')

    kb = Controller()

    prev_event = ''
      
    while True:
        event, values = ui_window.read()
        print('eventm=', event, 'prev=', prev_event)
        if event == sg.WIN_CLOSED:
            ui_window.close()
            break
            
        if event == 'Escape:27':
            ui_window.close()
            break
            
        if event == 'ESC':
            kb.press(Key.esc)
            kb.release(Key.esc)
            
        if event == 'TAB':        
            kb.press(Key.tab)
            kb.release(Key.tab)
            
        if event == 'DEL':
            kb.press(Key.delete)
            kb.release(Key.delete)
            
        if event == 'UP':        
            kb.press(Key.up)
            kb.release(Key.up)
            
        if event == 'DOWN':
            kb.press(Key.down)
            kb.release(Key.down)
            
        if event == 'RIGHT':
            kb.press(Key.right)
            kb.release(Key.right)
            
        if event == 'LEFT':
            kb.press(Key.left)
            kb.release(Key.left)
            
        if event == 'BACKSPACE':
            kb.press(Key.backspace)
            kb.release(Key.backspace)

        if ui_window.FindElementWithFocus().Key == '_ITEMS_LIST_':
            if len(ui_detail_pane.items_list) > 0:
                initialize_action_pane('ITEM')
            else:
                ui_search_pane.focus_barcode()        
        else:
            initialize_action_pane('INVOICE')
            ui_detail_pane.items_list = ui_detail_pane.items_list

        if event in ('F1:112', 'F1'):
            if prev_event == '_ITEMS_LIST_':
                ui_detail_pane.focus_items_list()                
            else:
                save_invoice()
                clear_invoice()
                ui_search_pane.focus_barcode()

        if event in ('F2:113', 'F2'):
            if prev_event in ('_ITEMS_LIST_', '_ITEM_NAME_'):
                idx = values['_ITEMS_LIST_'][0]
                open_change_qty_popup(idx)
                sum_item_list()
                ui_detail_pane.focus_items_list()                
            else:
                save_invoice()
                ui_search_pane.focus_barcode()

        if event in ('F3:114', 'F3'):
            if prev_event in ('_ITEMS_LIST_', '_ITEM_NAME_'):
                idx = values['_ITEMS_LIST_'][0]
                open_change_qty_popup(idx)
                sum_item_list()
                ui_detail_pane.focus_items_list()                
            else:
                if ui_header_pane.invoice_number == '':
                    save_invoice()
                    if not ui_header_pane.reference_number == '':
                        open_payment_popup()
                ui_search_pane.focus_barcode()

        if event in ('F4:115', 'F4'):
            if prev_event == '_ITEMS_LIST_':
                ui_detail_pane.focus_items_list()                
            else:
                ui_search_pane.focus_barcode()

        if event in ('F5:116', 'F5', 'Delete:46', 'Delete'):
            if prev_event == '_ITEMS_LIST_':
                if ui_header_pane.invoice_number == '':
                    idx = values['_ITEMS_LIST_'][0]
                    ui_detail_pane.delete_item_line(idx)
                    sum_item_list()
                if len(ui_detail_pane.items_list) == idx:
                    idx -= 1
                if idx > -1:
                    ui_detail_pane.focus_items_list_row(idx)
                else:
                    delete_invoice()
                    clear_invoice()
                    initialize_action_pane('INVOICE')        
                    ui_search_pane.focus_barcode()     
            else:
                if len(ui_detail_pane.items_list) > 0 and ui_header_pane.invoice_number == '':
                    confirm_delete = open_message_popup('Invoice will be Deleted')
                    if confirm_delete == 'Ok':       
                        delete_invoice()
                        clear_invoice()
                ui_search_pane.focus_barcode()
            
        if event in ('F12:123', 'F12', '_QUICK_ITEMS_'):
            process_carry_bag()
            ui_search_pane.focus_barcode()

        if event in ('T1','T2','T3','T4','T5','T6','T7','T8','T9','T0') and ui_window.FindElementWithFocus().Key == '_BARCODE_':
            inp_val = ui_search_pane.barcode
            inp_val += event[1]
            ui_search_pane.barcode = inp_val
            if (ui_search_pane.barcode[0].isnumeric() and len(ui_search_pane.barcode) > 12) or \
               (ui_search_pane.barcode[0] == 'I' and len(ui_search_pane.barcode) > 8) or \
               (ui_search_pane.barcode[0] == 'E' and len(ui_search_pane.barcode) > 7):
                process_barcode(ui_search_pane.barcode)
                initialize_search_pane()
                
        if event in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0') and ui_window.FindElementWithFocus().Key == '_BARCODE_':
            if (ui_search_pane.barcode[0].isnumeric() and len(ui_search_pane.barcode) > 12) or \
               (ui_search_pane.barcode[0] == 'I' and len(ui_search_pane.barcode) > 8) or \
               (ui_search_pane.barcode[0] == 'E' and len(ui_search_pane.barcode) > 7):
                process_barcode(ui_search_pane.barcode)
                initialize_search_pane()

        if event == 'v:86' and ui_window.FindElementWithFocus().Key == '_BARCODE_':
            process_barcode(ui_search_pane.barcode)
            initialize_search_pane()
            
        if event.isalnum() and ui_window.FindElementWithFocus().Key == '_ITEM_NAME_':
            if len(ui_search_pane.item_name) > 2:
                open_item_name_popup(ui_search_pane.item_name)
                initialize_search_pane()            
            
        if event in ('Prior:33', '_BEGIN_'):
            #save_invoice()
            goto_first_invoice()
            
        if event in ('Left:37', '_PREVIOUS_'):
            #save_invoice()
            goto_previous_invoice()
            
        if event in ('Right:39', '_NEXT_'):
            #save_invoice()
            goto_next_invoice()
            
        if event in ('Next:34', '_END_'):
            #save_invoice()
            goto_last_invoice()
        
        if event in ('\t', 'TAB') and prev_event == '_ITEM_NAME_':
            ui_detail_pane.focus_items_list()
        
        if event not in ('\t', 'Up:38', 'Down:40', 'UP', 'DOWN', 'DEL', 'Delete:46', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
            prev_event = event

    ui_window.close()


######
if __name__ == "__main__":
    main()