from estimate_ui import UiTitlePane, UiHeaderPane, UiSearchPane, UiDetailPane, UiActionPane, UiSummaryPane
from alignpos_db import DbConn, DbTable, DbQuery

class Estimate:
    
    db_conn = None
    ui_window = None
    ui_title_pane = None
    ui_header_pane = None
    ui_search_pane = None
    ui_detail_pane = None
    ui_summary_pane = None
    ui_action_pane = None
    db_customer_table = None
    db_estimate_table = None
    db_estimate_item_table = None
    
    
    def __init__(self, ui_window, db_conn):
        self.db_conn = db_conn
        self.ui_window = ui_window
        self.ui_title_pane = UiTitlePane(ui_window)
        self.ui_header_pane = UiHeaderPane(ui_window)
        self.ui_search_pane = UiSearchPane(ui_window)
        self.ui_detail_pane = UiDetailPane(ui_window)
        self.ui_summary_pane = UiSummaryPane(ui_window)
        self.ui_action_pane = UiActionPane(ui_window)
        self.db_customer_table = DbTable(db_conn, 'tabCustomer')
        self.db_estimate_table = DbTable(db_conn, 'tabEstimate')
        self.db_estimate_item_table = DbTable(db_conn, 'tabEstimate_Item')
        

    def initialize_title_pane(self):
        self.ui_title_pane.user_id = 'XXX'
        self.ui_title_pane.terminal_id = '101'
        self.ui_title_pane.current_date = '2021/06/13'

        
    def initialize_header_pane(self):
        self.ui_header_pane.estimate_number = ''
        self.ui_header_pane.payment_status = ''
        self.ui_header_pane.mobile_number = '0000000000'
        self.ui_header_pane.customer_number = ''
        self.ui_header_pane.customer_name = ''
        self.ui_header_pane.customer_address = ''

        
    def initialize_search_pane(self):
        self.ui_search_pane.barcode = ''
        self.ui_search_pane.item_name = ''
        self.ui_search_pane.item_name = ''
        self.ui_search_pane.focus_barcode()


    def initialize_detail_pane(self):
        self.ui_detail_pane.items_list = []
        self.ui_detail_pane.item_code = str('')
        self.ui_detail_pane.barcode = str('')
        self.ui_detail_pane.item_name = str('')
        self.ui_detail_pane.uom = str('')
        self.ui_detail_pane.qty = float(0.0)
        self.ui_detail_pane.selling_price = float(0.00)
        self.ui_detail_pane.selling_amount = float(0.00)
        self.ui_detail_pane.tax_rate = float(0.00)
        self.ui_detail_pane.tax_amount = float(0.00)
        self.ui_detail_pane.net_amount = float(0.00)
        self.ui_detail_pane.cgst_tax_rate = float(0.00)
        self.ui_detail_pane.sgst_tax_rate = float(0.00)
        self.ui_detail_pane.item_line = [] 


    def initialize_summary_pane(self):
        self.ui_summary_pane.line_items = 0
        self.ui_summary_pane.total_amount = 0.00
        self.ui_summary_pane.total_tax_amount = 0.00
        self.ui_summary_pane.net_amount = 0.00
        self.ui_summary_pane.total_cgst_amount = 0.00
        self.ui_summary_pane.total_sgst_amount = 0.00
        self.ui_summary_pane.total_tax_amount = 0.00
        self.ui_summary_pane.discount_amount = 0.00          
        self.ui_summary_pane.roundoff_amount = 0.00          
        self.ui_summary_pane.estimate_amount = 0.00


    def initialize_action_pane(self):
        self.ui_window.Element('F1').update(text='New\nF1')    
        self.ui_window.Element('F2').update(text='Specs\nF2')
        self.ui_window.Element('F3').update(text='Quantity\nF3')
        self.ui_window.Element('F4').update(text='Weight\nF4')
        self.ui_window.Element('F5').update(text='Price\nF5')
        self.ui_window.Element('F6').update(text='Save\nF6')
        self.ui_window.Element('F7').update(text='Delete\nF7')
        self.ui_window.Element('F8').update(text='Submit\nF8')
        self.ui_window.Element('F9').update(text='Print\nF9')


    def clear_estimate(self):
        self.initialize_header_pane()
        self.initialize_search_pane()    
        self.initialize_detail_pane()
        self.initialize_summary_pane()
    
    
    def goto_last_estimate(self):
        db_estimate_row = self.db_estimate_table.last('')
        if db_estimate_row:
            self.clear_estimate()
            self.show_estimate(db_estimate_row)


    def show_estimate(self, self.db_estimate_row):
        if not db_estimate_row:
            return
            
        self.ui_header_pane.estimate_number = db_estimate_row.name

        customer_number = db_estimate_row.customer
        db_customer_row = self.db_customer_table.get_row(customer_number)
        if db_customer_row:
            self.ui_header_pane.mobile_number = db_customer_row.mobile_number
            self.ui_header_pane.customer_number = db_customer_row.name
            self.ui_header_pane.customer_name = db_customer_row.customer_name
            self.ui_header_pane.customer_address = db_customer_row.address

        self.ui_detail_pane.item_line = []
        filter = "parent='{}'"
        db_estimate_item_cursor = self.db_estimate_item_table.list(filter.format(ui_header_pane.estimate_number))    
        for db_estimate_item_row in db_estimate_item_cursor:
            move_db_estimate_item_to_ui_detail_pane(db_estimate_item_row)
        sum_item_list()
        if (db_estimate_row.discount_amount):
            self.ui_summary_pane.discount_amount = db_estimate_row.discount_amount
        else:
            self.ui_summary_pane.discount_amount = 0.00       
        self.ui_summary_pane.estimate_amount = db_estimate_row.estimate_amount