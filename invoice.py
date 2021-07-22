from alignpos_db import DbConn, DbTable, DbQuery
from invoice_ui import UiHeaderPane, UiSearchPane, UiDetailPane, UiActionPane, UiFooterPane, UiSummaryPane, UiKeypadPane


class Invoice():
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
    db_invoice_table = None
    db_invoice_item_table = None

    
    def __init__(invoice, db_conn, ui_window):
        invoice.db_conn = db_conn
        invoice.ui_window = ui_window
        
        invoice.ui_header_pane = UiHeaderPane(ui_window)
        invoice.ui_search_pane = UiSearchPane(ui_window)
        invoice.ui_detail_pane = UiDetailPane(ui_window)
        invoice.ui_action_pane = UiActionPane(ui_window)
        invoice.ui_footer_pane = UiFooterPane(ui_window)
        invoice.ui_summary_pane = UiSummaryPane(ui_window)
        invoice.ui_keypad_pane = UiKeypadPane(ui_window)
        
        invoice.db_customer_table = DbTable(db_conn, 'tabCustomer')
        invoice.db_item_table = DbTable(db_conn, 'tabItem')
        invoice.db_invoice_table = DbTable(db_conn, 'tabInvoice')
        invoice.db_invoice_item_table = DbTable(db_conn, 'tabInvoice_Item')

    
    def initialize_ui_header_pane(invoice):
        invoice.ui_header_pane.invoice_number = ''
        invoice.ui_header_pane.payment_status = ''
        invoice.ui_header_pane.mobile_number = '0000000000'
        invoice.ui_header_pane.customer_number = ''
        invoice.ui_header_pane.customer_name = ''
        invoice.ui_header_pane.customer_address = ''
 
 
    def initialize_ui_search_pane(invoice):
        invoice.ui_search_pane.barcode = ''
        invoice.ui_search_pane.item_name = ''


    def initialize_ui_detail_pane(invoice):
        invoice.ui_detail_pane.items_list = []
        invoice.ui_detail_pane.item_code = str('')
        invoice.ui_detail_pane.barcode = str('')
        invoice.ui_detail_pane.item_name = str('')
        invoice.ui_detail_pane.uom = str('')
        invoice.ui_detail_pane.qty = float(0.0)
        invoice.ui_detail_pane.selling_price = float(0.00)
        invoice.ui_detail_pane.selling_amount = float(0.00)
        invoice.ui_detail_pane.tax_rate = float(0.00)
        invoice.ui_detail_pane.tax_amount = float(0.00)
        invoice.ui_detail_pane.net_amount = float(0.00)
        invoice.ui_detail_pane.cgst_tax_rate = float(0.00)
        invoice.ui_detail_pane.sgst_tax_rate = float(0.00)
        invoice.ui_detail_pane.item_line = [] 


    def initialize_ui_action_pane(invoice):
        invoice.ui_window.Element('F1').update(text='New\nF1')    
        invoice.ui_window.Element('F2').update(text='Specs\nF2')
        invoice.ui_window.Element('F3').update(text='Quantity\nF3')
        invoice.ui_window.Element('F4').update(text='Weight\nF4')
        invoice.ui_window.Element('F5').update(text='Price\nF5')
        invoice.ui_window.Element('F6').update(text='Save\nF6')
        invoice.ui_window.Element('F7').update(text='Delete\nF7')
        invoice.ui_window.Element('F8').update(text='Submit\nF8')
        invoice.ui_window.Element('F9').update(text='Print\nF9')


    def initialize_ui_footer_pane(invoice):
        invoice.ui_footer_pane.user_id = 'XXX'
        invoice.ui_footer_pane.terminal_id = '101'
        invoice.ui_footer_pane.current_date = '2021/06/13'


    def initialize_ui_summary_pane(invoice):
        invoice.ui_summary_pane.line_items = 0
        invoice.ui_summary_pane.total_amount = 0.00
        invoice.ui_summary_pane.total_tax_amount = 0.00
        invoice.ui_summary_pane.net_amount = 0.00
        invoice.ui_summary_pane.total_cgst_amount = 0.00
        invoice.ui_summary_pane.total_sgst_amount = 0.00
        invoice.ui_summary_pane.total_tax_amount = 0.00
        invoice.ui_summary_pane.discount_amount = 0.00          
        invoice.ui_summary_pane.roundoff_amount = 0.00          
        invoice.ui_summary_pane.invoice_amount = 0.00


    def initialize_ui(invoice):
        invoice.initialize_ui_header_pane()
        invoice.initialize_ui_search_pane()
        invoice.initialize_ui_detail_pane()
        invoice.initialize_ui_action_pane()
        invoice.initialize_ui_footer_pane()
        invoice.initialize_ui_summary_pane()


    def clear_ui(invoice):
        invoice.initialize_ui_header_pane()
        invoice.initialize_ui_search_pane()    
        invoice.initialize_ui_detail_pane()
        invoice.initialize_ui_summary_pane()
    
    
    def goto_last_row(invoice):
        db_invoice_row = invoice.db_invoice_table.last('')
        if db_invoice_row:
            invoice.clear_ui()
            invoice.show_ui(db_invoice_row)


    def show_ui(invoice, db_invoice_row):
        if not db_invoice_row:
            return
            
        invoice.ui_header_pane.invoice_number = db_invoice_row.name

        customer_number = db_invoice_row.customer
        db_customer_row = invoice.db_customer_table.get_row(customer_number)
        if db_customer_row:
            invoice.ui_header_pane.mobile_number = db_customer_row.mobile_number
            invoice.ui_header_pane.customer_number = db_customer_row.name
            invoice.ui_header_pane.customer_name = db_customer_row.customer_name
            invoice.ui_header_pane.customer_address = db_customer_row.address

        invoice.ui_detail_pane.item_line = []
        filter = "parent='{}'"
        db_invoice_item_cursor = invoice.db_invoice_item_table.list(filter.format(invoice.ui_header_pane.invoice_number))    
        for db_invoice_item_row in db_invoice_item_cursor:
            invoice.move_db_invoice_item_to_ui_detail_pane(db_invoice_item_row)
        invoice.sum_item_list()
        if (db_invoice_row.discount_amount):
            invoice.ui_summary_pane.discount_amount = db_invoice_row.discount_amount
        else:
            invoice.ui_summary_pane.discount_amount = 0.00       
        invoice.ui_summary_pane.invoice_amount = db_invoice_row.invoice_amount


    def move_db_item_to_ui_detail_pane(invoice, db_item_row):
        invoice.ui_detail_pane.item_code = db_item_row.name
        invoice.ui_detail_pane.barcode = db_item_row.barcode
        invoice.ui_detail_pane.item_name = db_item_row.item_name
        invoice.ui_detail_pane.uom = db_item_row.uom
        invoice.ui_detail_pane.qty = 1
        invoice.ui_detail_pane.selling_price = db_item_row.selling_price
        invoice.ui_detail_pane.cgst_tax_rate = db_item_row.cgst_tax_rate
        invoice.ui_detail_pane.sgst_tax_rate = db_item_row.sgst_tax_rate
        invoice.ui_detail_pane.selling_amount = float(invoice.ui_detail_pane.qty) * float(invoice.ui_detail_pane.selling_price)
        invoice.ui_detail_pane.tax_rate = float(invoice.ui_detail_pane.cgst_tax_rate) + float(invoice.ui_detail_pane.sgst_tax_rate)
        invoice.tax_amount = float(invoice.ui_detail_pane.selling_amount) * float(invoice.ui_detail_pane.tax_rate) / 100
        invoice.ui_detail_pane.tax_amount = round(tax_amount, 2)
        invoice.ui_detail_pane.net_amount = float(invoice.ui_detail_pane.selling_amount) + float(invoice.ui_detail_pane.tax_amount)
        
        invoice.ui_detail_pane.add_item_line()    

 
    def move_db_invoice_item_to_ui_detail_pane(invoice, db_invoice_item_row):
        invoice.ui_detail_pane.item_code = db_invoice_item_row.item
        
        db_item_row = invoice.db_item_table.get_row(db_invoice_item_row.item)
        if db_item_row:
            invoice.ui_detail_pane.barcode = db_item_row.barcode
            invoice.ui_detail_pane.item_name = db_item_row.item_name
            invoice.ui_detail_pane.uom = db_item_row.uom
            invoice.ui_detail_pane.selling_price = db_item_row.selling_price

        invoice.ui_detail_pane.qty = db_invoice_item_row.qty
        invoice.ui_detail_pane.cgst_tax_rate = db_invoice_item_row.cgst_tax_rate
        invoice.ui_detail_pane.sgst_tax_rate = db_invoice_item_row.sgst_tax_rate
        invoice.ui_detail_pane.selling_amount = float(invoice.ui_detail_pane.qty) * float(invoice.ui_detail_pane.selling_price)
        invoice.ui_detail_pane.tax_rate = float(invoice.ui_detail_pane.cgst_tax_rate) + float(invoice.ui_detail_pane.sgst_tax_rate)
        invoice.ui_detail_pane.tax_amount = float(invoice.ui_detail_pane.selling_amount) * float(invoice.ui_detail_pane.tax_rate) / 100
        invoice.ui_detail_pane.net_amount = float(invoice.ui_detail_pane.selling_amount) + float(invoice.ui_detail_pane.tax_amount)
        
        invoice.ui_detail_pane.add_item_line()    


    def sum_item_list(invoice):
        line_items = 0
        total_amount = 0.00
        total_tax_amount = 0.00
        total_cgst_amount = 0.00
        total_sgst_amount = 0.00
        net_amount = 0.00
       
        for item_line in invoice.ui_detail_pane.items_list:
            invoice.ui_detail_pane.item_line_to_elements(line_items)
            total_amount += float(invoice.ui_detail_pane.selling_amount)
            total_tax_amount += float(invoice.ui_detail_pane.tax_amount)
            net_amount += float(invoice.ui_detail_pane.net_amount)
            cgst_rate = float(invoice.ui_detail_pane.cgst_tax_rate)
            sgst_rate = float(invoice.ui_detail_pane.sgst_tax_rate)
            cgst_amount = float(invoice.ui_detail_pane.selling_amount) * cgst_rate / 100
            sgst_amount = float(invoice.ui_detail_pane.selling_amount) * sgst_rate / 100       
            total_cgst_amount += cgst_amount
            total_sgst_amount += sgst_amount
            line_items += 1

        invoice.ui_summary_pane.line_items = line_items
        invoice.ui_summary_pane.total_amount = total_amount
        invoice.ui_summary_pane.total_tax_amount = total_tax_amount
        invoice.ui_summary_pane.net_amount = net_amount
        invoice.ui_summary_pane.total_cgst_amount = total_cgst_amount
        invoice.ui_summary_pane.total_sgst_amount = total_sgst_amount
        invoice_actual_amount = net_amount - float(invoice.ui_summary_pane.discount_amount)
        invoice_rounded_amount = round(invoice_actual_amount, 0)
        invoice.ui_summary_pane.invoice_amount = invoice_rounded_amount
        invoice.ui_summary_pane.roundoff_amount = invoice_rounded_amount - invoice_actual_amount    
       