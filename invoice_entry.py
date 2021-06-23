import PySimpleGUI as sg
import datetime
import json
import sys
import platform
from pynput.keyboard import Key, Controller
from invoice_entry_ui import MainWindow, UiTitlePane, UiHeaderPane, UiSearchPane, UiDetailPane, UiActionPane, UiSummaryPane, UiKeypadPane, ChangeQtyPopup, UiChangeQtyPopup
from alignpos_db import ConnAlignPos, DbTable, DbQuery, Customer, Item, Invoice, InvoiceItem


######
def initialize_title_pane():
    ui_title_pane.user_id = 'XXX'
    ui_title_pane.terminal_id = '101'
    ui_title_pane.current_date = '2021/06/13'


def initialize_header_pane():
    ui_header_pane.reference_number = ''
    ui_header_pane.invoice_number = ''
    ui_header_pane.payment_status = ''
    ui_header_pane.mobile_number = ''

    
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


def db_item_to_ui_item_line(db_item_row):
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


def db_invoice_item_to_ui_item_line(db_invoice_item_row):
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
    db_item_to_ui_item_line(db_item_row)
    sum_item_list()


def process_barcode(barcode):
    if not barcode:
        return
        
    filter = "barcode='{}'"
    db_item_row = db_item_table.first(filter.format(barcode))    
    db_item_to_ui_item_line(db_item_row)
    sum_item_list()


def sum_item_list():
    line_items = 0
    total_qty = 0.00
    total_amount = 0.00
    total_tax_amount = 0.00
    total_cgst_amount = 0.00
    total_sgst_amount = 0.00
    net_amount = 0.00
   
    for item_line in ui_detail_pane.items_list:
        line_items += 1
        total_qty += float(item_line[4])
        total_amount += float(item_line[6])
        total_tax_amount += float(item_line[8])
        net_amount += float(item_line[9])
        total_cgst_amount += float(item_line[10])
        total_sgst_amount += float(item_line[11])

    ui_summary_pane.line_items = line_items
    ui_summary_pane.total_qty = total_qty
    ui_summary_pane.total_amount = total_amount
    ui_summary_pane.total_tax_amount = total_tax_amount
    ui_summary_pane.net_amount = net_amount
    ui_summary_pane.total_cgst_amount = total_cgst_amount
    ui_summary_pane.total_sgst_amount = total_sgst_amount


def save_invoice():
    if ui_header_pane.invoice_number != '':
        return
    if ui_header_pane.reference_number == '' and len(ui_detail_pane.items_list) > 0:
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
    
    db_invoice_row = db_invoice_table.get_row(ui_header_pane.reference_number)
    if db_invoice_row:
        db_invoice_table.delete_row(db_invoice_row)
    
    db_session.commit()
    

def clear_invoice():
    print('clear')
    initialize_header_pane()
    initialize_search_pane()    
    initialize_detail_pane()
    

def show_invoice(db_invoice_row):
    if not db_invoice_row:
        return
        
    ui_header_pane.reference_number = db_invoice_row.name
    ui_header_pane.invoice_number = db_invoice_row.invoice_number

    customer_number = db_invoice_row.customer
    db_customer_row = db_customer_table.get_row(customer_number)
    if db_customer_row:
        ui_header_pane.mobile_number = db_customer_row.mobile_number

    ui_detail_pane.item_line = []
    filter = "parent='{}'"
    db_invoice_item_cursor = db_invoice_item_table.list(filter.format(ui_header_pane.reference_number))    
    for db_invoice_item_row in db_invoice_item_cursor:
        db_invoice_item_to_ui_item_line(db_invoice_item_row)
    sum_item_list()


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
    
    ui_popup = sg.Window("Change Quantity", change_qty_popup.layout, location=(300,250), size=(350,180), modal=True, finalize=True,return_keyboard_events=True)

    ui_change_qty_popup = UiChangeQtyPopup(ui_popup)
    
    ui_change_qty_popup.item_name = ui_detail_pane.item_name
    ui_change_qty_popup.existing_qty = ui_detail_pane.qty
    ui_change_qty_popup.new_qty = ''
    
    while True:
        event, values = ui_popup.read()
        print('eventc=', event)
        
        if event in ("Exit", '_CHANGE_QTY_ESC_', 'Escape:27') or event == sg.WIN_CLOSED:
            break        
        if event == "_CHANGE_QTY_OK_" or event == "F12:123":
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

main_window = MainWindow()
ui_window = sg.Window('Invoice Entry', main_window.layout, background_color='White',
                   font='Helvetica 11', finalize=True, location=(0,0), size=(1600,800), keep_on_top=False, resizable=True,return_keyboard_events=True, use_default_focus=False
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
            
        if event in ('F2:113', 'F2') and prev_event == '_ITEMS_LIST_':
            if ui_header_pane.invoice_number == '':
                idx = values['_ITEMS_LIST_'][0]
                ui_detail_pane.delete_item_line(idx)
                ui_detail_pane.focus_items_list()
                sum_item_list()

        if event in ('F3:114', 'F3') and prev_event == '_ITEMS_LIST_':
            idx = values['_ITEMS_LIST_'][0]
            open_change_qty_popup(idx)
            sum_item_list()

        if event in ('F6:117', 'F6'):
            process_carry_bag()
            
        if event in ('F7:118', 'F7'):
            save_invoice()
            clear_invoice()
            ui_search_pane.focus_barcode()

        if event in ('F8:119', 'F8'):
            if ui_header_pane.invoice_number == '':
                confirm_delete = sg.popup_ok_cancel('Invoice will be Deleted',keep_on_top = True)
                if confirm_delete == 'OK':       
                    delete_invoice()
                    clear_invoice()
                    ui_search_pane.focus_barcode()

        if event in ('T1','T2','T3','T4','T5','T6','T7','T8','T9','T0') and ui_window.FindElementWithFocus().Key == '_BARCODE_':
            inp_val = ui_search_pane.barcode
            inp_val += event[1]
            ui_search_pane.barcode = inp_val
            if len(ui_search_pane.barcode) > 12:
                print('here0')            
                process_barcode(ui_search_pane.barcode)
                initialize_search_pane()
                
        if event in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0') and ui_window.FindElementWithFocus().Key == '_BARCODE_':
            if len(pane_search.barcode) > 12:
                print('here1:', len(pane_search.barcode))
                process_barcode(ui_search_pane.barcode)
                initialize_search_pane()

        if event == 'v:86' and ui_window.FindElementWithFocus().Key == '_BARCODE_':
            process_barcode(ui_search_pane.barcode)
            initialize_search_pane()
            
        if event in ('Home:36', '_BEGIN_'):
            save_invoice()
            goto_first_invoice()
            
        if event in ('Prior:33', '_PREVIOUS_'):
            save_invoice()
            goto_previous_invoice()
            
        if event in ('Next:34', '_NEXT_'):
            save_invoice()
            goto_next_invoice()
            
        if event in ('End:35', '_END_'):
            save_invoice()
            goto_last_invoice()
            
        if event in ('\t', 'TAB') and prev_event == '_ITEM_NAME_':
            ui_detail_pane.focus_items_list()

        if event not in ('\t', 'Up:38', 'Down:40', 'UP', 'DOWN', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
            prev_event = event

    ui_window.close()


######
if __name__ == "__main__":
    main()
