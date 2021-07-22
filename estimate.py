from alignpos_db import DbConn, DbTable, DbQuery
from estimate_ui import UiHeaderPane, UiSearchPane, UiDetailPane, UiActionPane, UiFooterPane, UiSummaryPane, UiKeypadPane


class Estimate():
    db_conn = None
    ui_window = None
    
    ui_header_pane = None
    ui_search_pane = None
    ui_detail_pane = None
    ui_action_pane = None
    ui_footer_pane = None
    ui_summary_pane = None
    
    db_customer_table = None
    db_item_table = None
    db_estimate_table = None
    db_estimate_item_table = None

    
    def __init__(estimate, db_conn, ui_window):
        estimate.db_conn = db_conn
        estimate.ui_window = ui_window
        
        estimate.ui_header_pane = UiHeaderPane(ui_window)
        estimate.ui_search_pane = UiSearchPane(ui_window)
        estimate.ui_detail_pane = UiDetailPane(ui_window)
        estimate.ui_action_pane = UiActionPane(ui_window)
        estimate.ui_footer_pane = UiFooterPane(ui_window)
        estimate.ui_summary_pane = UiSummaryPane(ui_window)
        estimate.ui_keypad_pane = UiKeypadPane(ui_window)
        
        estimate.db_customer_table = DbTable(db_conn, 'tabCustomer')
        estimate.db_item_table = DbTable(db_conn, 'tabItem')
        estimate.db_estimate_table = DbTable(db_conn, 'tabEstimate')
        estimate.db_estimate_item_table = DbTable(db_conn, 'tabEstimate_Item')

    
    def initialize_ui_header_pane(estimate):
        estimate.ui_header_pane.estimate_number = ''
        estimate.ui_header_pane.payment_status = ''
        estimate.ui_header_pane.mobile_number = '0000000000'
        estimate.ui_header_pane.customer_number = ''
        estimate.ui_header_pane.customer_name = ''
        estimate.ui_header_pane.customer_address = ''
 
 
    def initialize_ui_search_pane(estimate):
        estimate.ui_search_pane.barcode = ''
        estimate.ui_search_pane.item_name = ''


    def initialize_ui_detail_pane(estimate):
        estimate.ui_detail_pane.items_list = []
        estimate.ui_detail_pane.item_code = str('')
        estimate.ui_detail_pane.barcode = str('')
        estimate.ui_detail_pane.item_name = str('')
        estimate.ui_detail_pane.uom = str('')
        estimate.ui_detail_pane.qty = float(0.0)
        estimate.ui_detail_pane.selling_price = float(0.00)
        estimate.ui_detail_pane.selling_amount = float(0.00)
        estimate.ui_detail_pane.tax_rate = float(0.00)
        estimate.ui_detail_pane.tax_amount = float(0.00)
        estimate.ui_detail_pane.net_amount = float(0.00)
        estimate.ui_detail_pane.cgst_tax_rate = float(0.00)
        estimate.ui_detail_pane.sgst_tax_rate = float(0.00)
        estimate.ui_detail_pane.item_line = [] 


    def initialize_ui_action_pane(estimate):
        estimate.ui_window.Element('F1').update(text='New\nF1')    
        estimate.ui_window.Element('F2').update(text='Specs\nF2')
        estimate.ui_window.Element('F3').update(text='Quantity\nF3')
        estimate.ui_window.Element('F4').update(text='Weight\nF4')
        estimate.ui_window.Element('F5').update(text='Price\nF5')
        estimate.ui_window.Element('F6').update(text='Save\nF6')
        estimate.ui_window.Element('F7').update(text='Delete\nF7')
        estimate.ui_window.Element('F8').update(text='Submit\nF8')
        estimate.ui_window.Element('F9').update(text='Print\nF9')


    def initialize_ui_footer_pane(estimate):
        estimate.ui_footer_pane.user_id = 'XXX'
        estimate.ui_footer_pane.terminal_id = '101'
        estimate.ui_footer_pane.current_date = '2021/06/13'


    def initialize_ui_summary_pane(estimate):
        estimate.ui_summary_pane.line_items = 0
        estimate.ui_summary_pane.total_amount = 0.00
        estimate.ui_summary_pane.total_tax_amount = 0.00
        estimate.ui_summary_pane.net_amount = 0.00
        estimate.ui_summary_pane.total_cgst_amount = 0.00
        estimate.ui_summary_pane.total_sgst_amount = 0.00
        estimate.ui_summary_pane.total_tax_amount = 0.00
        estimate.ui_summary_pane.discount_amount = 0.00          
        estimate.ui_summary_pane.roundoff_amount = 0.00          
        estimate.ui_summary_pane.estimate_amount = 0.00


    def initialize_ui(estimate):
        estimate.initialize_ui_header_pane()
        estimate.initialize_ui_search_pane()
        estimate.initialize_ui_detail_pane()
        estimate.initialize_ui_action_pane()
        estimate.initialize_ui_footer_pane()
        estimate.initialize_ui_summary_pane()


    def clear_ui(estimate):
        estimate.initialize_ui_header_pane()
        estimate.initialize_ui_search_pane()    
        estimate.initialize_ui_detail_pane()
        estimate.initialize_ui_summary_pane()
    
    
    def goto_last_row(estimate):
        db_estimate_row = estimate.db_estimate_table.last('')
        if db_estimate_row:
            estimate.clear_ui()
            estimate.show_ui(db_estimate_row)


    def show_ui(estimate, db_estimate_row):
        if not db_estimate_row:
            return
            
        estimate.ui_header_pane.estimate_number = db_estimate_row.name

        customer_number = db_estimate_row.customer
        db_customer_row = estimate.db_customer_table.get_row(customer_number)
        if db_customer_row:
            estimate.ui_header_pane.mobile_number = db_customer_row.mobile_number
            estimate.ui_header_pane.customer_number = db_customer_row.name
            estimate.ui_header_pane.customer_name = db_customer_row.customer_name
            estimate.ui_header_pane.customer_address = db_customer_row.address

        estimate.ui_detail_pane.item_line = []
        filter = "parent='{}'"
        db_estimate_item_cursor = estimate.db_estimate_item_table.list(filter.format(estimate.ui_header_pane.estimate_number))    
        for db_estimate_item_row in db_estimate_item_cursor:
            estimate.move_db_estimate_item_to_ui_detail_pane(db_estimate_item_row)
        estimate.sum_item_list()
        if (db_estimate_row.discount_amount):
            estimate.ui_summary_pane.discount_amount = db_estimate_row.discount_amount
        else:
            estimate.ui_summary_pane.discount_amount = 0.00       
        estimate.ui_summary_pane.estimate_amount = db_estimate_row.estimate_amount


    def move_db_item_to_ui_detail_pane(estimate, db_item_row):
        estimate.ui_detail_pane.item_code = db_item_row.name
        estimate.ui_detail_pane.barcode = db_item_row.barcode
        estimate.ui_detail_pane.item_name = db_item_row.item_name
        estimate.ui_detail_pane.uom = db_item_row.uom
        estimate.ui_detail_pane.qty = 1
        estimate.ui_detail_pane.selling_price = db_item_row.selling_price
        estimate.ui_detail_pane.cgst_tax_rate = db_item_row.cgst_tax_rate
        estimate.ui_detail_pane.sgst_tax_rate = db_item_row.sgst_tax_rate
        estimate.ui_detail_pane.selling_amount = float(estimate.ui_detail_pane.qty) * float(estimate.ui_detail_pane.selling_price)
        estimate.ui_detail_pane.tax_rate = float(estimate.ui_detail_pane.cgst_tax_rate) + float(estimate.ui_detail_pane.sgst_tax_rate)
        estimate.tax_amount = float(estimate.ui_detail_pane.selling_amount) * float(estimate.ui_detail_pane.tax_rate) / 100
        estimate.ui_detail_pane.tax_amount = round(tax_amount, 2)
        estimate.ui_detail_pane.net_amount = float(estimate.ui_detail_pane.selling_amount) + float(estimate.ui_detail_pane.tax_amount)
        
        estimate.ui_detail_pane.add_item_line()    

 
    def move_db_estimate_item_to_ui_detail_pane(estimate, db_estimate_item_row):
        estimate.ui_detail_pane.item_code = db_estimate_item_row.item
        
        db_item_row = estimate.db_item_table.get_row(db_estimate_item_row.item)
        if db_item_row:
            estimate.ui_detail_pane.barcode = db_item_row.barcode
            estimate.ui_detail_pane.item_name = db_item_row.item_name
            estimate.ui_detail_pane.uom = db_item_row.uom
            estimate.ui_detail_pane.selling_price = db_item_row.selling_price

        estimate.ui_detail_pane.qty = db_estimate_item_row.qty
        estimate.ui_detail_pane.cgst_tax_rate = db_estimate_item_row.cgst_tax_rate
        estimate.ui_detail_pane.sgst_tax_rate = db_estimate_item_row.sgst_tax_rate
        estimate.ui_detail_pane.selling_amount = float(estimate.ui_detail_pane.qty) * float(estimate.ui_detail_pane.selling_price)
        estimate.ui_detail_pane.tax_rate = float(estimate.ui_detail_pane.cgst_tax_rate) + float(estimate.ui_detail_pane.sgst_tax_rate)
        estimate.ui_detail_pane.tax_amount = float(estimate.ui_detail_pane.selling_amount) * float(estimate.ui_detail_pane.tax_rate) / 100
        estimate.ui_detail_pane.net_amount = float(estimate.ui_detail_pane.selling_amount) + float(estimate.ui_detail_pane.tax_amount)
        
        estimate.ui_detail_pane.add_item_line()    


    def sum_item_list(estimate):
        line_items = 0
        total_amount = 0.00
        total_tax_amount = 0.00
        total_cgst_amount = 0.00
        total_sgst_amount = 0.00
        net_amount = 0.00
       
        for item_line in estimate.ui_detail_pane.items_list:
            estimate.ui_detail_pane.item_line_to_elements(line_items)
            total_amount += float(estimate.ui_detail_pane.selling_amount)
            total_tax_amount += float(estimate.ui_detail_pane.tax_amount)
            net_amount += float(estimate.ui_detail_pane.net_amount)
            cgst_rate = float(estimate.ui_detail_pane.cgst_tax_rate)
            sgst_rate = float(estimate.ui_detail_pane.sgst_tax_rate)
            cgst_amount = float(estimate.ui_detail_pane.selling_amount) * cgst_rate / 100
            sgst_amount = float(estimate.ui_detail_pane.selling_amount) * sgst_rate / 100       
            total_cgst_amount += cgst_amount
            total_sgst_amount += sgst_amount
            line_items += 1

        estimate.ui_summary_pane.line_items = line_items
        estimate.ui_summary_pane.total_amount = total_amount
        estimate.ui_summary_pane.total_tax_amount = total_tax_amount
        estimate.ui_summary_pane.net_amount = net_amount
        estimate.ui_summary_pane.total_cgst_amount = total_cgst_amount
        estimate.ui_summary_pane.total_sgst_amount = total_sgst_amount
        estimate_actual_amount = net_amount - float(estimate.ui_summary_pane.discount_amount)
        estimate_rounded_amount = round(estimate_actual_amount, 0)
        estimate.ui_summary_pane.estimate_amount = estimate_rounded_amount
        estimate.ui_summary_pane.roundoff_amount = estimate_rounded_amount - estimate_actual_amount    
       