import PySimpleGUI as sg
import os
import subprocess
import datetime
import json
import sys
import platform
import pdfkit
import webbrowser
from pynput.keyboard import Key, Controller
from estimate_entry_ui import MainWindow, UiTitlePane, UiHeaderPane, UiSearchPane, UiDetailPane, UiActionPane, UiSummaryPane, UiKeypadPane, \
                             ChangeQtyPopup, UiChangeQtyPopup, ItemNamePopup, UiItemNamePopup,\
                             PaymentPopup, UiPaymentPopup
from alignpos_db import ConnAlignPos, DbTable, DbQuery, Customer, Item, Estimate, EstimateItem

######
def initialize_title_pane():
    ui_title_pane.user_id = 'XXX'
    ui_title_pane.terminal_id = '101'
    ui_title_pane.current_date = '2021/06/13'


def initialize_header_pane():
    ui_header_pane.estimate_number = ''
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
    ui_summary_pane.estimate_amount = 0.00


def initialize_action_pane(context):
    ui_window.Element('F1').update(text='New\nF1')    
    ui_window.Element('F2').update(text='Specs\nF2')
    ui_window.Element('F3').update(text='Quantity\nF3')
    ui_window.Element('F4').update(text='Weight\nF4')
    ui_window.Element('F5').update(text='Price\nF5')
    ui_window.Element('F6').update(text='Save\nF6')
    ui_window.Element('F7').update(text='Delete\nF7')
    ui_window.Element('F8').update(text='Payment\nF8')
    ui_window.Element('F9').update(text='Print\nF9')
       

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
    tax_amount = float(ui_detail_pane.selling_amount) * float(ui_detail_pane.tax_rate) / 100
    ui_detail_pane.tax_amount = round(tax_amount, 2)
    ui_detail_pane.net_amount = float(ui_detail_pane.selling_amount) + float(ui_detail_pane.tax_amount)
    
    ui_detail_pane.add_item_line()    


def move_db_estimate_item_to_ui_detail_pane(db_estimate_item_row):
    ui_detail_pane.item_code = db_estimate_item_row.item
    
    db_item_row = db_item_table.get_row(db_estimate_item_row.item)
    if db_item_row:
        ui_detail_pane.barcode = db_item_row.barcode
        ui_detail_pane.item_name = db_item_row.item_name
        ui_detail_pane.uom = db_item_row.uom
        ui_detail_pane.selling_price = db_item_row.selling_price

    ui_detail_pane.qty = db_estimate_item_row.qty
    ui_detail_pane.cgst_tax_rate = db_estimate_item_row.cgst_tax_rate
    ui_detail_pane.sgst_tax_rate = db_estimate_item_row.sgst_tax_rate
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
        ui_detail_pane.item_line_to_elements(line_items)
        total_amount += float(ui_detail_pane.selling_amount)
        total_tax_amount += float(ui_detail_pane.tax_amount)
        net_amount += float(ui_detail_pane.net_amount)
        cgst_rate = float(ui_detail_pane.cgst_tax_rate)
        sgst_rate = float(ui_detail_pane.sgst_tax_rate)
        cgst_amount = float(ui_detail_pane.selling_amount) * cgst_rate / 100
        sgst_amount = float(ui_detail_pane.selling_amount) * sgst_rate / 100       
        total_cgst_amount += cgst_amount
        total_sgst_amount += sgst_amount
        line_items += 1

    ui_summary_pane.line_items = line_items
    ui_summary_pane.total_amount = total_amount
    ui_summary_pane.total_tax_amount = total_tax_amount
    ui_summary_pane.net_amount = net_amount
    ui_summary_pane.total_cgst_amount = total_cgst_amount
    ui_summary_pane.total_sgst_amount = total_sgst_amount
    estimate_actual_amount = net_amount - float(ui_summary_pane.discount_amount)
    estimate_rounded_amount = round(estimate_actual_amount, 0)
    ui_summary_pane.estimate_amount = estimate_rounded_amount
    ui_summary_pane.roundoff_amount = estimate_rounded_amount - estimate_actual_amount    


def save_estimate():
    if not len(ui_detail_pane.items_list) > 0:
        return    

    if ui_header_pane.estimate_number == '':
        insert_estimate()
    else:
        update_estimate()


def insert_estimate():
    if len(ui_detail_pane.items_list) == 0:
        return

    db_query = DbQuery(db_conn, 'SELECT nextval("ESTIMATE_NUMBER")')
    for db_row in db_query.result:
        ui_header_pane.estimate_number = db_row[0]

    customer_number = walk_in_customer
    db_customer_row = db_customer_table.get_row(customer_number)
    if db_customer_row:
        ui_header_pane.mobile_number = db_customer_row.mobile_number
        ui_header_pane.customer_number = db_customer_row.name
        ui_header_pane.customer_name = db_customer_row.customer_name
        ui_header_pane.customer_address = db_customer_row.address

    db_estimate_row = db_estimate_table.new_row()

    db_estimate_row.name = ui_header_pane.estimate_number
    db_estimate_row.customer = customer_number
    db_estimate_row.posting_date = ui_title_pane.current_date    
    db_estimate_row.total_amount = ui_summary_pane.total_amount
    db_estimate_row.net_amount = ui_summary_pane.net_amount
    db_estimate_row.estimate_amount = ui_summary_pane.estimate_amount
    db_estimate_row.cgst_tax_amount = ui_summary_pane.total_cgst_amount
    db_estimate_row.sgst_tax_amount = ui_summary_pane.total_sgst_amount
    db_estimate_row.terminal_id = ui_title_pane.terminal_id  

    db_estimate_table.create_row(db_estimate_row)
   
    for idx in range(len(ui_detail_pane.items_list)): 
        ui_detail_pane.item_line_to_elements(idx)
        
        db_estimate_item_row = db_estimate_item_table.new_row()
        
        db_estimate_item_row.name = ui_header_pane.estimate_number + f"{idx:04d}"
        db_estimate_item_row.parent = ui_header_pane.estimate_number
        db_estimate_item_row.item = ui_detail_pane.item_code
        db_estimate_item_row.qty = ui_detail_pane.qty
        db_estimate_item_row.standard_selling_price = ui_detail_pane.selling_price
        db_estimate_item_row.applied_selling_price = ui_detail_pane.selling_price
        db_estimate_item_row.cgst_tax_rate = ui_detail_pane.cgst_tax_rate
        db_estimate_item_row.sgst_tax_rate = ui_detail_pane.sgst_tax_rate
      
        db_estimate_item_table.create_row(db_estimate_item_row)

    db_session.commit()
    

def update_estimate():
    db_estimate_row = db_estimate_table.get_row(ui_header_pane.estimate_number)

    if not db_estimate_row:
        return
    db_estimate_row.customer = ui_header_pane.customer_number
    db_estimate_row.total_amount = ui_summary_pane.total_amount
    db_estimate_row.net_amount = ui_summary_pane.net_amount
    db_estimate_row.estimate_amount = ui_summary_pane.estimate_amount
    db_estimate_row.cgst_tax_amount = ui_summary_pane.total_cgst_amount
    db_estimate_row.sgst_tax_amount = ui_summary_pane.total_sgst_amount
    db_estimate_row.terminal_id = ui_title_pane.terminal_id  

    filter = "parent='{}'"
    db_estimate_item_cursor = db_estimate_item_table.list(filter.format(ui_header_pane.estimate_number))
    for db_estimate_item_row in db_estimate_item_cursor:
        db_estimate_item_table.delete_row(db_estimate_item_row)

    db_session.flush()
    
    for idx in range(len(ui_detail_pane.items_list)): 
        ui_detail_pane.item_line_to_elements(idx)
        
        db_estimate_item_row = db_estimate_item_table.new_row()
        
        db_estimate_item_row.name = ui_header_pane.estimate_number + f"{idx:04d}"
        db_estimate_item_row.parent = ui_header_pane.estimate_number
        db_estimate_item_row.item = ui_detail_pane.item_code
        db_estimate_item_row.qty = ui_detail_pane.qty
        db_estimate_item_row.standard_selling_price = ui_detail_pane.selling_price
        db_estimate_item_row.applied_selling_price = ui_detail_pane.selling_price
        db_estimate_item_row.cgst_tax_rate = ui_detail_pane.cgst_tax_rate
        db_estimate_item_row.sgst_tax_rate = ui_detail_pane.sgst_tax_rate
      
        db_estimate_item_table.create_row(db_estimate_item_row)

    db_session.commit()


def delete_estimate():
    if not ui_header_pane.estimate_number or ui_header_pane.estimate_number == '':
        return

    filter = "parent='{}'"
    db_estimate_item_cursor = db_estimate_item_table.list(filter.format(ui_header_pane.estimate_number))
    for db_estimate_item_row in db_estimate_item_cursor:
        print(db_estimate_item_row.name)
        db_estimate_item_table.delete_row(db_estimate_item_row)

    db_session.flush()
    
    db_estimate_row = db_estimate_table.get_row(ui_header_pane.estimate_number)
    if db_estimate_row:
        db_estimate_table.delete_row(db_estimate_row)
    
    db_session.commit()
    

def clear_estimate():
    initialize_header_pane()
    initialize_search_pane()    
    initialize_detail_pane()
    initialize_summary_pane()
    

def show_estimate(db_estimate_row):
    if not db_estimate_row:
        return
        
    ui_header_pane.estimate_number = db_estimate_row.name

    customer_number = db_estimate_row.customer
    db_customer_row = db_customer_table.get_row(customer_number)
    if db_customer_row:
        ui_header_pane.mobile_number = db_customer_row.mobile_number
        ui_header_pane.customer_number = db_customer_row.name
        ui_header_pane.customer_name = db_customer_row.customer_name
        ui_header_pane.customer_address = db_customer_row.address

    ui_detail_pane.item_line = []
    filter = "parent='{}'"
    db_estimate_item_cursor = db_estimate_item_table.list(filter.format(ui_header_pane.estimate_number))    
    for db_estimate_item_row in db_estimate_item_cursor:
        move_db_estimate_item_to_ui_detail_pane(db_estimate_item_row)
    sum_item_list()
    if (db_estimate_row.discount_amount):
        ui_summary_pane.discount_amount = db_estimate_row.discount_amount
    else:
        ui_summary_pane.discount_amount = 0.00       
    ui_summary_pane.estimate_amount = db_estimate_row.estimate_amount
    

def goto_first_estimate():
    db_estimate_row = db_estimate_table.first('')
    if db_estimate_row:
        clear_estimate()    
        show_estimate(db_estimate_row)


def goto_previous_estimate():
    if ui_header_pane.estimate_number:
        name = ui_header_pane.estimate_number
        filter = "name < '{}'"
        db_estimate_row = db_estimate_table.last(filter.format(name))
        if db_estimate_row:
            clear_estimate()    
            show_estimate(db_estimate_row)


def goto_next_estimate():
    if ui_header_pane.estimate_number:
        name = ui_header_pane.estimate_number
        filter = "name > '{}'"
        db_estimate_row = db_estimate_table.first(filter.format(name))
        if db_estimate_row:
            clear_estimate()    
            show_estimate(db_estimate_row)


def goto_last_estimate():
    db_estimate_row = db_estimate_table.last('')
    if db_estimate_row:
        clear_estimate()    
        show_estimate(db_estimate_row)


    
######
# Popup window for Change Quantity
def open_change_qty_popup(row_item):
    ui_detail_pane.item_line_to_elements(row_item)
    
    change_qty_popup = ChangeQtyPopup()
    
    ui_popup = sg.Window("Change Quantity", 
                    change_qty_popup.layout, 
                    location=(300,250), 
                    size=(530,280), 
                    modal=True, 
                    finalize=True,
                    keep_on_top = True,
                    return_keyboard_events=True
                )

    ui_change_qty_popup = UiChangeQtyPopup(ui_popup)
        
    ui_change_qty_popup.item_name = ui_detail_pane.item_name
    ui_change_qty_popup.existing_qty = ui_detail_pane.qty
    ui_change_qty_popup.new_qty_f = 0.00
    ui_change_qty_popup.focus_new_qty()

    prev_event = '' 
    focus = None
    while True:
        event, values = ui_popup.read()
        print('change_qty_popup=', event)
        
        if ui_popup.FindElementWithFocus():
            focus = ui_popup.FindElementWithFocus().Key
        print('eventc=', event, 'prev=', prev_event, 'focus:', focus)
        
        if event == 'ENTER':        
            kb.press(Key.enter)
            kb.release(Key.enter)
            
        if event == 'TAB':        
            kb.press(Key.tab)
            kb.release(Key.tab)
            
        if event == 'DEL':
            kb.press(Key.delete)
            kb.release(Key.delete)
            
        if event == 'BACKSPACE':
            kb.press(Key.backspace)
            kb.release(Key.backspace)
            
        if event in ('Exit', '_CHANGE_QTY_ESC_', 'Escape:27', sg.WIN_CLOSED):
            break             
            
        if event in ('T1','T2','T3','T4','T5','T6','T7','T8','T9','T0'):
            if focus == '_NEW_QTY_':
                ui_change_qty_popup.append_char('_NEW_QTY_', event[1])
          
        if event == '\t':
            if focus == '_NEW_QTY_':     
                ui_change_qty_popup.new_qty_f = ui_change_qty_popup.new_qty
                ui_change_qty_popup.focus_new_qty()       

        if event in ('_CHANGE_QTY_OK_', 'F12:123', '\r'):
            if not ui_change_qty_popup.new_qty:
                break;
            process_change_qty(ui_change_qty_popup, row_item)
            break

    ui_popup.close() 


def process_change_qty(ui_change_qty_popup, row_item):
    if float(ui_change_qty_popup.new_qty) > 0 and ui_change_qty_popup.new_qty != ui_change_qty_popup.existing_qty:
        ui_detail_pane.qty = ui_change_qty_popup.new_qty
        ui_detail_pane.selling_amount = float(ui_detail_pane.qty) * float(ui_detail_pane.selling_price)
        ui_detail_pane.tax_rate = float(ui_detail_pane.cgst_tax_rate) + float(ui_detail_pane.sgst_tax_rate)
        ui_detail_pane.tax_amount = float(ui_detail_pane.selling_amount) * float(ui_detail_pane.tax_rate) / 100
        ui_detail_pane.net_amount = float(ui_detail_pane.selling_amount) + float(ui_detail_pane.tax_amount)
        ui_detail_pane.update_item_line(row_item)                


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
    
    #ui_payment_popup.focus_cash_amount()
    
    prev_event = ''   
    while True:
        event, values = ui_popup.read()
        print('payment_popup=', event)
        
        if event in ('\t', 'TAB') and prev_event == '_MOBILE_NUMBER_':
            if not ui_payment_popup.mobile_number == '':
                process_mobile_number(ui_payment_popup)

        if event == '_MOBILE_NUMBER_' and len(ui_payment_popup.mobile_number) > 9:
            process_mobile_number(ui_payment_popup)
           
        if event in ('\t', 'TAB') and prev_event == '_DISCOUNT_AMOUNT_':
            ui_payment_popup.discount_amount = ui_payment_popup.discount_amount       
            ui_payment_popup.discount_amount_hd = ui_payment_popup.discount_amount
            set_payment_popup_elements(ui_payment_popup)
                       
        if event in ("Exit", '_PAYMENT_ESC_', 'Escape:27') or event == sg.WIN_CLOSED:
            ui_popup.close()
            break
            
        if event == "_PAYMENT_OK_" or event == "F12:123":
            set_payment_popup_elements(ui_payment_popup)
            move_payment_popup_to_summary_pane(ui_payment_popup)
            ui_popup.close()
            print_estimate()
            break
                            
        prev_event = event
            
    #ui_popup.close() 


def process_mobile_number(ui_payment_popup):    
    filter = "mobile_number='{}'"
    db_customer_row = db_customer_table.first(filter.format(ui_payment_popup.mobile_number))
    if db_customer_row:
        print(db_customer_row.customer_name)
        ui_payment_popup.customer_number = db_customer_row.name
        ui_payment_popup.customer_name = db_customer_row.customer_name
        ui_payment_popup.customer_address = db_customer_row.address
        ui_payment_popup.mobile_number_header = db_customer_row.mobile_number
        ui_payment_popup.customer_name_header = db_customer_row.customer_name
        ui_header_pane.mobile_number = db_customer_row.mobile_number
        ui_header_pane.customer_number = db_customer_row.name
        ui_header_pane.mobile_number = db_customer_row.mobile_number
        ui_header_pane.customer_name = db_customer_row.customer_name
        ui_header_pane.customer_address = db_customer_row.address

def initialize_payment_popup_elements(ui_payment_popup):
    ui_payment_popup.mobile_number = ui_header_pane.mobile_number
    ui_payment_popup.customer_name = ui_header_pane.customer_name
    ui_payment_popup.mobile_number_header = ui_header_pane.mobile_number
    ui_payment_popup.customer_name_header = ui_header_pane.customer_name
    ui_payment_popup.customer_number = ui_header_pane.customer_number
    ui_payment_popup.customer_address = ui_header_pane.customer_address
    ui_payment_popup.net_amount = ui_summary_pane.net_amount
    ui_payment_popup.discount_amount = 0
    estimate_actual_amount = float(ui_payment_popup.net_amount) - float(ui_payment_popup.discount_amount)
    estimate_rounded_amount = round(estimate_actual_amount, 0)
    ui_payment_popup.estimate_amount = estimate_rounded_amount
    ui_payment_popup.roundoff_adjustment = estimate_rounded_amount - estimate_actual_amount


def set_payment_popup_elements(ui_payment_popup):
    if not ui_payment_popup.discount_amount or ui_payment_popup.discount_amount == '':
       ui_payment_popup.discount_amount = 0
 
    ui_summary_pane.discount_amount = float(ui_payment_popup.discount_amount)
 
    estimate_actual_amount = float(ui_payment_popup.net_amount) - float(ui_payment_popup.discount_amount)
    estimate_rounded_amount = round(estimate_actual_amount, 0)
    ui_payment_popup.estimate_amount = estimate_rounded_amount
    ui_payment_popup.roundoff_adjustment = estimate_rounded_amount - estimate_actual_amount


def move_payment_popup_to_summary_pane(ui_payment_popup):
    ui_summary_pane.discount_amount = float(ui_payment_popup.discount_amount)
    ui_summary_pane.estimate_amount = float(ui_payment_popup.estimate_amount)
    ui_summary_pane.roundoff_amount = float(ui_payment_popup.roundoff_adjustment)

    
######
# Popup window for selecting Item
def open_item_name_popup(filter, lin, col):
    db_item_cursor = db_item_table.list(filter)
    if not db_item_cursor:
        return
        
    item_name_popup = ItemNamePopup()
    ui_popup = sg.Window("Item Name", 
                    item_name_popup.layout, 
                    location=(lin,col), 
                    size=(348,129), 
                    modal=False, 
                    finalize=True,
                    return_keyboard_events=True, 
                    no_titlebar = True, 
                    element_padding=(0,0), 
                    background_color = 'White', 
                    keep_on_top = True,                    
                    margins=(0,0)
                )
    ui_popup.bind('<FocusIn>', '+FOCUS IN+')
    ui_popup.bind('<FocusOut>', '+FOCUS OUT+')
    
    ui_item_name_popup = UiItemNamePopup(ui_popup)
    ui_item_name_popup.focus_item_list

    ui_item_name_popup.item_list = []
    for db_item_row in db_item_cursor:
        ui_item_name_popup.item_code = db_item_row.item_code
        ui_item_name_popup.item_name = db_item_row.item_name
        ui_item_name_popup.add_item_line()
    ui_item_name_popup.idx = 0

    prev_event = ''    
    while True:
        event, values = ui_popup.read()
        print('item_name_popup=', event)
        if event == 'Down:40':
            ui_item_name_popup.next_item_line()
        if event == 'Up:38':
            ui_item_name_popup.prev_item_line()            
        if event in ("Exit", '_ITEM_NAME_ESC_', 'Escape:27', '+FOCUS OUT+') or event == sg.WIN_CLOSED:
            break        
        if event == '\r':
            sel_item_code =  values['_ITEM_NAME_LIST_'][0][0]
            process_item_name(sel_item_code)
            break
        prev_event = event
    ui_popup.close()


######
# Print Estimate into PDF file
def print_estimate():
    config = pdfkit.configuration(wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    options = {
        'page-height': '120mm',
        'page-width': '60mm',
        'margin-top': '3mm',
        'margin-bottom': '3mm',
        'margin-right': '3mm',
        'margin-left': '3mm',
        'enable-local-file-access': None,
        'quiet': None
    } 

    print_str = """
                <table style="width:100%">
                    <tr>
                        <td>
                            <img src="c:\\python-tkinter\\al-fareeda-logo.png" alt="al-fareeda" width="100" height="48">
                        </td>
                        <td>
                            &nbsp
                        </td>
                        <td padding: 10px;>
                            <p style="font-size:9px; font-family:Courier; text-align:left">
                                13/2947,<br>
                                Pattinamkathaan&nbspbus&nbspstop,<br>
                                Ramanathapuram, Tamil&nbspNadu<br>                        
                                GSTIN: 33ABMFA2300A12E<br>
                            </p>
                        </td>
                    </tr>
                </table>                       
                <p style="font-size:18px; font-weight: bold; font-family:Courier; text-align:center">
                    Estimate
                </p>            
            """    

    print_str += """
            <p  style="font-size:14px; font-weight: bold; font-family:Courier">Estimate No: {}<br>
                Date: {}<br>
            </p>            
            """.format( ui_header_pane.estimate_number, 
                        ui_title_pane.current_date
                )    

    print_str += """
            <p style="font-size:12px; font-family:Courier; margin: 0px;">
                Code&nbspItem&nbspName&nbsp&nbsp&nbsp&nbsp&nbspQty&nbsp&nbsp&nbsp&nbspAmount
            </p>
            <hr style="width:95%;text-align:left;margin-left:0">
        """
        
    for idx in range(len(ui_detail_pane.items_list)): 
        ui_detail_pane.item_line_to_elements(idx)        
        print_str += """
            <p style="font-size:12px; font-family:Courier; margin: 0px;";>
                {:^4s}&nbsp{:^10s}&nbsp&nbsp{}&nbsp&nbsp{}
            </p>
            """.format( ui_detail_pane.item_code[5:], 
                        ui_detail_pane.item_name[0:10].ljust(10, ' ').replace(' ', ''),
                        str(ui_detail_pane.qty).rjust(5,'*').replace('*', '&nbsp'), 
                        str(ui_detail_pane.net_amount).rjust(8,'*').replace('*', '&nbsp')
                )
 
    print_str += """
        <hr style="width:95%;text-align:left;margin-left:0">
        """
 
    print_str += """
        <p style="font-size:12px; font-family:Courier; margin: 0px;">
            &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{}<br>
        </p>
        <hr style="width:95%;text-align:left;margin-left:0">
        <p style="font-size:12px; font-family:Courier; margin: 0px;">
            &nbsp&nbsp&nbsp&nbsp&nbspCost&nbsp&nbsp&nbsp&nbsp:&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{}<br>
            &nbsp&nbsp&nbsp&nbsp&nbspCGS&nbspTax&nbsp:&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{}<br>
            &nbsp&nbsp&nbsp&nbsp&nbspSGS&nbspTax&nbsp:&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{}<br>
        </p>
        <hr style="width:95%;text-align:left;margin-left:0">
        <p style="font-size:12px; font-family:Courier; margin: 0px;">                    
            &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{}<br><br>
            &nbspDiscount&nbsp&nbsp&nbsp&nbsp:&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{}<br>
            &nbspRoundoff&nbsp&nbsp&nbsp&nbsp:&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp{}<br>                    
        </p>
        <hr style="width:95%;text-align:left;margin-left:0">
        """.format(str(ui_summary_pane.net_amount).rjust(12,'*').replace('*', '&nbsp'), 
                    str(ui_summary_pane.total_amount).rjust(12,'*').replace('*', '&nbsp'), 
                    str(ui_summary_pane.total_cgst_amount).rjust(12,'*').replace('*', '&nbsp'), 
                    str(ui_summary_pane.total_sgst_amount).rjust(12,'*').replace('*', '&nbsp'),
                    str(ui_summary_pane.net_amount).rjust(12,'*').replace('*', '&nbsp'),                            
                    str(ui_summary_pane.discount_amount).rjust(12,'*').replace('*', '&nbsp'),                            
                    str(ui_summary_pane.roundoff_amount).rjust(12,'*').replace('*', '&nbsp')                           
            )
    print_str += """
        <p style="font-size:15px; font-family:Courier; font-weight: bold">
            Net&nbspAmt&nbsp&nbsp&nbsp:&nbsp&nbsp&nbsp&nbsp{}
        </p>
        """.format(ui_summary_pane.estimate_amount.rjust(10,'*').replace('*', '&nbsp'))
    
    try:    
        pdfkit.from_string(print_str, 'micro.pdf', options=options)   
        os.startfile('micro.pdf')
    except:
        pass

    
######
# Popup windows for message
def popup_message(type, message):
    ui_message_layout = [
        [sg.T(message)],
        [sg.B(key='_OK_', button_text='Ok - F12'), 
         sg.B(key='_CANCEL_', button_text='Cancel - Esc', visible=True)]
    ]
    ui_popup =  sg.Window('Confirm', 
                    layout=ui_message_layout, 
                    keep_on_top = True, 
                    return_keyboard_events = True, 
                    modal=False, 
                    finalize=True
                )

    ui_popup.bind('<FocusIn>', '+FOCUS IN+')
    ui_popup.bind('<FocusOut>', '+FOCUS OUT+')
    
    ui_popup["_OK_"].Widget.config(takefocus=0) 
    ui_popup["_CANCEL_"].Widget.config(takefocus=0) 

    if type == 'OK':
        ui_popup.Element("_CANCEL_").update(visible=False)
    else:
        ui_popup.Element("_CANCEL_").update(visible=True)
    
    while True:
        event, values = ui_popup.read()
        print('message_popup:', event)
        if event in ('Escape:27', '_OK_', '_CANCEL_', 'F12:123', 'F12', '\r', '+FOCUS OUT+'):
            break
        if event == sg.WIN_CLOSED:
            return 'Cancel'
    ui_popup.close()
    if event in ('Escape:27', '_CANCEL_', '+FOCUS OUT+'):
        return 'Cancel'
    else:
        return 'Ok'


######
# Download details from ERPNext
def execute_download_process():
    pid = subprocess.Popen(["python", "download_customers.py"])
    pid = subprocess.Popen(["python", "download_items.py"])
    pid = subprocess.Popen(["python", "download_exchange_adjustments.py"])


######
# Upload details to ERPNext
def execute_upload_process():
    print('To be implemented')


def process_weight(idx):
    ui_detail_pane.item_line_to_elements(idx)
    if ui_detail_pane.uom == 'Kg':            
        ui_detail_pane.qty = 0.35
        ui_detail_pane.selling_amount = float(ui_detail_pane.qty) * float(ui_detail_pane.selling_price)
        ui_detail_pane.tax_rate = float(ui_detail_pane.cgst_tax_rate) + float(ui_detail_pane.sgst_tax_rate)
        ui_detail_pane.tax_amount = float(ui_detail_pane.selling_amount) * float(ui_detail_pane.tax_rate) / 100
        ui_detail_pane.net_amount = float(ui_detail_pane.selling_amount) + float(ui_detail_pane.tax_amount)
        ui_detail_pane.update_item_line(idx)
        sum_item_list()
    else:
        sg.popup('Not applicable to this UOM', keep_on_top = True)                

    
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
db_estimate_table = DbTable(db_conn, Estimate)
db_estimate_item_table = DbTable(db_conn, EstimateItem)

execute_download_process()

w, h = sg.Window.get_screen_size()
main_window = MainWindow()
ui_window = sg.Window('Estimate Entry', 
                main_window.layout, 
                background_color='White',
                font='Helvetica 11', 
                finalize=True, 
                location=(0,0), 
                size=(w,h), 
                keep_on_top=False, 
                resizable=False,
                return_keyboard_events=True, 
                use_default_focus=False
         )
#ui_window.maximize()

ui_title_pane = UiTitlePane(ui_window)
ui_header_pane = UiHeaderPane(ui_window)
ui_search_pane = UiSearchPane(ui_window)
ui_detail_pane = UiDetailPane(ui_window)
ui_action_pane = UiActionPane(ui_window)
ui_summary_pane = UiSummaryPane(ui_window)
ui_keypad_pane = UiKeypadPane(ui_window)

kb = Controller()


######
# Main function
def main():
    
    initialize_title_pane()
    initialize_header_pane()
    initialize_search_pane()
    initialize_action_pane('ESTIMATE')

    ui_window['_BARCODE_'].bind('<FocusIn>', '+CLICK+')
    ui_window['_ITEM_NAME_'].bind('<FocusIn>', '+CLICK+')
    
    goto_last_estimate()
    
    prev_event = '' 
    focus = None    
    while True:
        event, values = ui_window.read()
        if ui_window.FindElementWithFocus():
            focus = ui_window.FindElementWithFocus().Key
        print('window=', event, 'prev=', prev_event, 'focus=', focus)

        if event == sg.WIN_CLOSED:
            ui_window.close()
            break

        if event == 'Escape:27':
            ui_window.close()
            break

        if event == 'ENTER':        
            kb.press(Key.enter)
            kb.release(Key.enter)
            
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

        if event == '+CLICK+':
            initialize_action_pane('ESTIMATE')
        else:
            initialize_action_pane('ITEM')        
        
        if focus == '_ITEMS_LIST_':
            if len(ui_detail_pane.items_list) > 0:
                initialize_action_pane('ITEM')
            else:
                ui_search_pane.focus_barcode()        
        else:
            initialize_action_pane('ESTIMATE')
            ui_detail_pane.items_list = ui_detail_pane.items_list

        if event in ('F1:112', 'F1'):
            save_estimate()
            clear_estimate()
            execute_download_process()
            ui_search_pane.focus_barcode()

        if event in ('F2:113', 'F2'):
            if prev_event in ('_ITEMS_LIST_', '_ITEM_NAME_'):
                sg.popup('Specs feature not yet implemented', keep_on_top = True)                
                ui_detail_pane.focus_items_list()                
            else:
                ui_search_pane.focus_barcode()
              
        if event in ('F3:114', 'F3'):
            if prev_event in ('_ITEMS_LIST_', '_ITEM_NAME_'):
                idx = values['_ITEMS_LIST_'][0]
                open_change_qty_popup(idx)
                sum_item_list()
                ui_detail_pane.focus_items_list_row(idx)   
            else:
                sg.popup('Select an item', keep_on_top = True)                
                ui_search_pane.focus_barcode()
            
        if event in ('F4:115', 'F4'):
            idx = values['_ITEMS_LIST_'][0]
            process_weight(idx)
            ui_search_pane.focus_barcode()

        if event in ('F5:116', 'F5'):
            if prev_event in ('_ITEMS_LIST_', '_ITEM_NAME_'):
                sg.popup('Weight feature not yet implemented', keep_on_top = True)                
                ui_detail_pane.focus_items_list()                
            else:
                ui_search_pane.focus_barcode()

        if event in ('F6:117', 'F6'):
            if len(ui_detail_pane.items_list) > 0:
                save_estimate()
                sg.popup('Estimate Entry Saved', keep_on_top = True)                
                ui_search_pane.focus_barcode()

        if event in ('F7:118', 'F7'):
            if len(ui_detail_pane.items_list) > 0:
                confirm_delete = popup_message('OK_CANCEL', 'Estimate Entry will be deleted')
                if confirm_delete == 'Ok':       
                    delete_estimate()
                    clear_estimate()
                    goto_previous_estimate()
                    ui_search_pane.focus_barcode()

        if event in ('F8:119', 'F8'):
            save_estimate()
            if not ui_header_pane.estimate_number == '':
                open_payment_popup()
                execute_upload_process()                 
                ui_search_pane.focus_barcode()

        if event in ('F9:120', 'F9'):
            print_estimate()
            ui_search_pane.focus_barcode()
                  
        if event in ('Delete:46', 'Delete'):        
            if prev_event == '_ITEMS_LIST_':
                idx = values['_ITEMS_LIST_'][0]
                ui_detail_pane.delete_item_line(idx)
                sum_item_list()
                if len(ui_detail_pane.items_list) == idx:
                    idx -= 1
                if idx > -1:
                    ui_detail_pane.focus_items_list_row(idx)
           
        if event in ('F11:122', 'F11', '_ADDON_'):
            filter = "upper(item_code) like upper('ITEM-9%')"
            open_item_name_popup(filter, 535, 202)
            initialize_search_pane()            

        if event in ('T1','T2','T3','T4','T5','T6','T7','T8','T9','T0') and focus == '_BARCODE_':
            inp_val = ui_search_pane.barcode
            inp_val += event[1]
            ui_search_pane.barcode = inp_val
            if (ui_search_pane.barcode[0].isnumeric() and len(ui_search_pane.barcode) > 12) or \
               (ui_search_pane.barcode[0] == 'I' and len(ui_search_pane.barcode) > 8) or \
               (ui_search_pane.barcode[0] == 'E' and len(ui_search_pane.barcode) > 8):
                process_barcode(ui_search_pane.barcode)
                initialize_search_pane()
                
        if event in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0') and focus == '_BARCODE_':
            if ui_search_pane.barcode:
                if (ui_search_pane.barcode[0].isnumeric() and len(ui_search_pane.barcode) > 12) or \
                   (ui_search_pane.barcode[0] == 'I' and len(ui_search_pane.barcode) > 8) or \
                   (ui_search_pane.barcode[0] == 'E' and len(ui_search_pane.barcode) > 8):
                    process_barcode(ui_search_pane.barcode)
                    initialize_search_pane()

        if event == 'v:86' and focus == '_BARCODE_':
            process_barcode(ui_search_pane.barcode)
            initialize_search_pane()
            
        if event.isalnum() and focus == '_ITEM_NAME_':
            if len(ui_search_pane.item_name) > 2:
                filter = "upper(item_name) like upper('%{}%')".format(ui_search_pane.item_name)
                open_item_name_popup(filter, 385, 202)
                initialize_search_pane()
                for idx in range(2):
                    kb.press(Key.tab)
                    kb.release(Key.tab)
                for idx in range(len(ui_detail_pane.items_list)-1):
                    kb.press(Key.down)
                    kb.release(Key.down)
            
        if event in ('Prior:33', '_BEGIN_'):
            goto_first_estimate()
            
        if event in ('Left:37', '_PREVIOUS_'):
            goto_previous_estimate()
            
        if event in ('Right:39', '_NEXT_'):
            goto_next_estimate()
            
        if event in ('Next:34', '_END_'):
            goto_last_estimate()
        
        if event in ('\t') and prev_event == '_ITEM_NAME_':
            ui_detail_pane.focus_items_list()
        
        if event not in ('\t', 'Up:38', 'Down:40', 'UP', 'DOWN', 'DEL', 'Delete:46', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
            prev_event = event

    ui_window.close()


######
if __name__ == "__main__":
    main()
