import datetime


class InvoiceUi:

    def __init__(self, window):
    
        self.__window = window

        ###
        # Initialize Header Pane
        self.__invoice_number = str('')
        self.__mobile_number = str('')
        self.__customer_number = str('')
        self.__customer_name = str('')
        self.__customer_address = str('')
        
        # Initialize Search Pane
        self.__barcode = str('')
        self.__search_name = str('') 
        self.__item_group = str('') 
        self.__item_groups_list = ['']
        
        # Initialize Detail Pane
        self.__items_list = []
        self.__item_line = []
        self.__item_idx = 0
        self.__item_code = str('')
        self.__item_barcode = str('')
        self.__item_name = str('')
        self.__uom = str('')
        self.__qty = float(0.0)
        self.__selling_price = float(0.00)
        self.__selling_amount = float(0.00)
        self.__tax_rate = float(0.00)
        self.__tax_amount = float(0.00)
        self.__item_net_amount = float(0.00)
        self.__cgst_tax_rate = float(0.00)
        self.__sgst_tax_rate = float(0.00)
        
        # Initialize Footer Pane
        self.__user_id = ''
        self.__terminal_id = ''
        self.__current_date = datetime.datetime(1900, 1, 1)
        
        # Initialize Summary Pane
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

        ###
        # Unfocus Header Pane        
        self.__window['_INVOICE_NUMBER_'].Widget.config(takefocus=0)
        self.__window['_FIND_'].Widget.config(takefocus=0)
        self.__window['_BEGIN_'].Widget.config(takefocus=0)
        self.__window['_PREVIOUS_'].Widget.config(takefocus=0)
        self.__window['_NEXT_'].Widget.config(takefocus=0)
        self.__window['_END_'].Widget.config(takefocus=0)
        self.__window['_MOBILE_NUMBER_'].Widget.config(takefocus=0)

        ###
        # Unfocus Search Pane        
        self.__window['_KEYPAD1_'].Widget.config(takefocus=0)
        self.__window['_KEYPAD2_'].Widget.config(takefocus=0)

        # Unfocus Summary Pane
        self.__window['_LINE_ITEMS_'].Widget.config(takefocus=0)
        self.__window['_TOTAL_AMOUNT_'].Widget.config(takefocus=0)
        self.__window['_TOTAL_TAX_AMOUNT_'].Widget.config(takefocus=0)
        self.__window['_NET_AMOUNT_'].Widget.config(takefocus=0)
        self.__window['_DISCOUNT_AMOUNT_'].Widget.config(takefocus=0)
        self.__window['_ROUNDOFF_AMOUNT_'].Widget.config(takefocus=0)
        self.__window['_INVOICE_AMOUNT_'].Widget.config(takefocus=0)
        self.__window['_PAID_AMOUNT_'].Widget.config(takefocus=0)

        # Unfocus Tools Pane        
        self.__window['Addon'].Widget.config(takefocus=0)
        self.__window['Bundle'].Widget.config(takefocus=0)

        # Unfocus Action Pane
        self.__window['F1'].Widget.config(takefocus=0)
        self.__window['F2'].Widget.config(takefocus=0)
        self.__window['F3'].Widget.config(takefocus=0)
        self.__window['F4'].Widget.config(takefocus=0)
        self.__window['F5'].Widget.config(takefocus=0)        
        self.__window['F6'].Widget.config(takefocus=0)        
        self.__window['F7'].Widget.config(takefocus=0)        
        self.__window['F8'].Widget.config(takefocus=0)        
        self.__window['F9'].Widget.config(takefocus=0)        
        self.__window['ESC'].Widget.config(takefocus=0)    
        self.__window['+'].Widget.config(takefocus=0)    
        self.__window['-'].Widget.config(takefocus=0)    

        # Unfocus Footer Pane
        self.__window['_USER_ID_'].Widget.config(takefocus=0)
        self.__window['_TERMINAL_ID_'].Widget.config(takefocus=0)
        self.__window['_CURRENT_DATE_'].Widget.config(takefocus=0)
        

    ###
    # Setters and Getters for Header Pane 
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


    # Setters and Getters for Search Pane    
    def set_barcode(self, barcode):
        self.__barcode = barcode
        self.__window.Element('_BARCODE_').update(value = self.__barcode)
        
    def get_barcode(self):
        self.__barcode = self.__window.Element('_BARCODE_').get()        
        return self.__barcode

    def set_search_name(self, search_name):
        self.__search_name = search_name
        self.__window.Element('_SEARCH_NAME_').update(value = self.__search_name)
        
    def get_search_name(self):
        self.__search_name = self.__window.Element('_SEARCH_NAME_').get()        
        return self.__search_name

    def set_item_group(self, item_group):
        self.__item_group = item_group
        self.__window.Element('_ITEM_GROUP_').update(values = self.__item_group_list)
        
    def get_item_group(self):
        self.__item_group = self.__window.Element('_ITEM_GROUP_').get()        
        return self.__item_group

    def set_item_groups_list(self, item_groups_list):
        self.__item_groups_list = item_groups_list
        self.__window.Element('_ITEM_GROUP_').update(values = self.__item_groups_list)
        
    def get_item_groups_list(self):
        return self.__item_groups_list


    # Setters and Getters for Detail Pane    
    def set_items_list(self, items_list):
        self.__items_list = items_list
        self.__window.Element('_ITEMS_LIST_').update(values = self.__items_list)
        
    def get_items_list(self):
        self.__items_list = self.__window.Element('_ITEMS_LIST_').get()
        return self.__items_list
              
    def set_item_line(self, item_line):
        self.__item_line = item_line
        
    def get_item_line(self):
        self.__item_line = self.__items_list[self.__item_idx]
        return self.__item_line
              
    def set_item_code(self, item_code):
        self.__item_code = item_code
        
    def get_item_code(self):
        return self.__item_code

    def set_item_barcode(self, item_barcode):
        self.__item_barcode = item_barcode
        
    def get_item_barcode(self):
        return self.__item_barcode

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

    def set_item_net_amount(self, item_net_amount):
        self.__item_net_amount = item_net_amount
        
    def get_item_net_amount(self):
        return self.__item_net_amount

    def set_cgst_tax_rate(self, cgst_tax_rate):
        self.__cgst_tax_rate = cgst_tax_rate
        
    def get_cgst_tax_rate(self):
        return self.__cgst_tax_rate

    def set_sgst_tax_rate(self, sgst_tax_rate):
        self.__sgst_tax_rate = sgst_tax_rate
        
    def get_sgst_tax_rate(self):
        return self.__sgst_tax_rate       

    def set_item_idx(self, item_idx):
        self.__item_idx = item_idx
        
    def get_item_idx(self):
        return self.__item_idx  

    # Setters and Getters for Footer Pane    
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
               

    # Setters and Getters for Summary Pane    
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


    ###
    # Focus Search Pane        
    def focus_barcode(self):
        self.__window.Element('_BARCODE_').SetFocus() 

    def focus_item_name(self):
        self.__window.Element('_SEARCH_NAME_').SetFocus() 
                                   
    def focus_item_group(self):
        self.__window.Element('_ITEM_GROUP_').SetFocus() 

    def focus_item_group_line(self, idx):
        self.__window.Element('_ITEM_GROUP_').update(set_to_index = idx)


    # Focus Detail Pane
    def unfocus_items_list(self):
        self.__window.Element('_ITEMS_LIST_').update(select_rows=[])

    def focus_items_list(self):
        self.__window['_ITEMS_LIST_'].Widget.config(takefocus=1)
        self.__window.Element('_ITEMS_LIST_').set_focus(force = True)                
        if len(self.__items_list) > 0:        
            table_row = self.__window['_ITEMS_LIST_'].Widget.get_children()[0]
            self.__window['_ITEMS_LIST_'].Widget.selection_set(table_row)  # move selection
            self.__window['_ITEMS_LIST_'].Widget.focus(table_row)  # move focus
            self.__window['_ITEMS_LIST_'].Widget.see(table_row)  # scroll to show i

    def focus_items_list_row(self, idx):
        self.__window['_ITEMS_LIST_'].Widget.config(takefocus=1)        
        self.__window.Element('_ITEMS_LIST_').set_focus(force = True)                
        table_row = self.__window['_ITEMS_LIST_'].Widget.get_children()[idx]
        self.__window['_ITEMS_LIST_'].Widget.selection_set(table_row)  # move selection
        self.__window['_ITEMS_LIST_'].Widget.focus(table_row)  # move focus
        self.__window['_ITEMS_LIST_'].Widget.see(table_row)  # scroll to show i

    def focus_items_list_last(self):
        idx = len(self.__items_list) - 1
        self.__window['_ITEMS_LIST_'].Widget.config(takefocus=1)        
        self.__window.Element('_ITEMS_LIST_').set_focus(force = True)                
        table_row = self.__window['_ITEMS_LIST_'].Widget.get_children()[idx]
        self.__window['_ITEMS_LIST_'].Widget.selection_set(table_row)  # move selection
        self.__window['_ITEMS_LIST_'].Widget.focus(table_row)  # move focus
        self.__window['_ITEMS_LIST_'].Widget.see(table_row)  # scroll to show i

    ###
    # Specific to Detail Pane        
    def clear_ui_items_list(self):
        self.__ui_items_list.clear()
        self.__window.Element('_ITEMS_LIST_').update(values = self.__ui_items_list)

    def elements_to_item_line(self):
        self.__item_line.append(self.__item_code)
        self.__item_line.append(self.__item_barcode)        
        self.__item_line.append(self.__item_name)        
        self.__item_line.append(self.__uom)        
        self.__item_line.append("{:.2f}".format(float(self.__qty)))      
        self.__item_line.append("{:.2f}".format(float(self.__selling_price)))        
        self.__item_line.append("{:.2f}".format(float(self.__selling_amount)))       
        self.__item_line.append("{:.2f}".format(float(self.__tax_rate)))     
        self.__item_line.append("{:.2f}".format(float(self.__tax_amount)))       
        self.__item_line.append("{:.2f}".format(float(self.__item_net_amount)))    
        self.__item_line.append("{:.2f}".format(float(self.__cgst_tax_rate)))       
        self.__item_line.append("{:.2f}".format(float(self.__sgst_tax_rate)))
       
    def item_line_to_elements(self, idx):
        self.__item_line = self.__items_list[idx]
        self.__item_code = self.__item_line[0]
        self.__item_barcode = self.__item_line[1]
        self.__item_name = self.__item_line[2]
        self.__uom = self.__item_line[3]
        self.__qty = self.__item_line[4]
        self.__selling_price = self.__item_line[5]
        self.__selling_amount = self.__item_line[6]
        self.__tax_rate = self.__item_line[7]
        self.__tax_amount = self.__item_line[8]
        self.__item_net_amount = self.__item_line[9]
        self.__cgst_tax_rate = self.__item_line[10]
        self.__sgst_tax_rate = self.__item_line[11]

    def add_item_line(self):
        self.__item_line = []
        self.elements_to_item_line()    
        self.__items_list.append(self.__item_line)
        self.__window.Element('_ITEMS_LIST_').update(values = self.__items_list)

    def fetch_item_line(self, idx):
        self.item_line_to_elements(idx)
        return self.__item_line

    def update_item_line(self, idx):
        self.__item_line = []
        self.elements_to_item_line()
        print('ui:', self.__item_line)
        self.__items_list[idx] = self.__item_line
        self.__window.Element('_ITEMS_LIST_').update(values = self.__items_list)

    def delete_item_line(self, idx):
        self.__items_list.pop(idx)
        self.__window.Element('_ITEMS_LIST_').update(values = self.__items_list)      

    
    ###
    def unfocus_fast_pane(self, fast_item_codes_list):
        for item_code in fast_item_codes_list:
            self.__window['FAST_'+item_code].Widget.config(takefocus=0)

    def unfocus_favorite_pane(self, fav_moving_item_codes_list):
        for item_code in fav_moving_item_codes_list:
            self.__window['FAV_'+item_code].Widget.config(takefocus=0)

    def unfocus_tools_pane(self):            
        self.__window['Addon'].Widget.config(takefocus=0)
        self.__window['Bundle'].Widget.config(takefocus=0)


    ###
    # Properties for Header Pane
    invoice_number = property(get_invoice_number, set_invoice_number) 
    mobile_number = property(get_mobile_number, set_mobile_number) 
    customer_number = property(get_customer_number, set_customer_number) 
    customer_name = property(get_customer_name, set_customer_name) 
    customer_address = property(get_customer_address, set_customer_address) 

    # Properties for Search Pane
    barcode = property(get_barcode, set_barcode) 
    search_name = property(get_search_name, set_search_name) 
    item_group = property(get_item_group, set_item_group) 
    item_groups_list = property(get_item_groups_list, set_item_groups_list) 
    
    # Properties for Detail Pane    
    items_list = property(get_items_list, set_items_list)
    item_line = property(get_item_line, set_item_line)
    item_idx = property(get_item_idx, set_item_idx)
    item_code = property(get_item_code, set_item_code)
    item_barcode = property(get_item_barcode, set_item_barcode)
    item_name = property(get_item_name, set_item_name)
    uom = property(get_uom, set_uom)
    qty = property(get_qty, set_qty)
    selling_price = property(get_selling_price, set_selling_price)
    selling_amount = property(get_selling_amount, set_selling_amount)
    tax_rate = property(get_tax_rate, set_tax_rate)
    tax_amount = property(get_tax_amount, set_tax_amount)
    item_net_amount = property(get_item_net_amount, set_item_net_amount)
    cgst_tax_rate = property(get_cgst_tax_rate, set_cgst_tax_rate)
    sgst_tax_rate = property(get_sgst_tax_rate, set_sgst_tax_rate)
    
    # Properties for Footer Pane    
    user_id = property(get_user_id, set_user_id) 
    terminal_id = property(get_terminal_id, set_terminal_id)
    current_date = property(get_current_date, set_current_date)
    
    # Properties for Summary Pane    
    line_items = property(get_line_items, set_line_items)
    total_amount = property(get_total_amount, set_total_amount)
    total_tax_amount = property(get_total_tax_amount, set_total_tax_amount)
    total_cgst_amount = property(get_total_cgst_amount, set_total_cgst_amount)
    total_sgst_amount = property(get_total_sgst_amount, set_total_sgst_amount)
    net_amount = property(get_net_amount, set_net_amount)
    discount_amount = property(get_discount_amount, set_discount_amount)
    roundoff_amount = property(get_roundoff_amount, set_roundoff_amount)
    invoice_amount = property(get_invoice_amount, set_invoice_amount)
    paid_amount = property(get_invoice_amount, set_invoice_amount)
        

class ChangeQtyUi:
    def __init__(self, popup):
        self.__popup = popup
        self.__item_name = ''
        self.__existing_qty = float(0.00)
        self.__new_qty = float(0.00)

        self.__popup["_EXISTING_QTY_"].Widget.config(takefocus=0)
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


class InvoiceListUi:
    def __init__(self, window):
        self.__window = window

        self.__invoices_list = []
        self.__invoice_line = []
        self.__invoice_idx = 0
        self.__bill_number = ''
        self.__bill_number_search = ''
        self.__mobile_number = ''
        self.__mobile_number_search = ''
        self.__line_items = 0
        self.__total_amount = float(0.00)
        self.__total_tax_amount = float(0.00)
        self.__net_amount = float(0.00)
        self.__discount_amount = float(0.00)
        self.__roundoff_amount = float(0.00)
        self.__invoice_amount = float(0.00)
        
        self.__window["_INVOICE_LIST_OK_"].Widget.config(takefocus=0)
        self.__window["_INVOICE_LIST_ESC_"].Widget.config(takefocus=0)
        self.__window["_INVOICE_LIST_SEARCH_"].Widget.config(takefocus=0)
       
    # Setters and Getters
    def set_invoices_list(self, invoices_list):
        self.__invoices_list = invoices_list
        self.__window.Element('_INVOICES_LIST_').update(values = self.__invoices_list)
        
    def get_invoices_list(self):
        self.__invoices_list = self.__window.Element('_INVOICES_LIST_').get()
        return self.__invoices_list
              
    def set_invoice_line(self, invoice_line):
        self.__invoice_line = invoice_line
        
    def get_invoice_line(self):
        self.__invoice_line = self.__invoices_list[self.__item_idx]
        return self.__invoice_line
    
    def set_invoice_number_search(self, invoice_number_search):
        self.__invoice_number_search = invoice_number_search
        self.__window.Element('_INVOICE_NUMBER_SEARCH_').update(value = self.__invoice_number_search)
        
    def get_invoice_number_search(self):
        self.__invoice_number_search = self.__window.Element('_INVOICE_NUMBER_SEARCH_').get()        
        return self.__invoice_number_search
        
    def set_mobile_number_search(self, mobile_number_search):
        self.__mobile_number_search = mobile_number_search
        self.__window.Element('_MOBILE_NUMBER_SEARCH_').update(value = self.__mobile_number_search)
        
    def get_mobile_number_search(self):
        self.__mobile_number_search = self.__window.Element('_MOBILE_NUMBER_SEARCH_').get()        
        return self.__mobile_number_search
        
    def set_invoice_number(self, invoice_number):
        self.__invoice_number = invoice_number
        
    def get_invoice_number(self):
        return self.__invoice_number
        
    def set_mobile_number(self, mobile_number):
        self.__mobile_number = mobile_number
        
    def get_mobile_number(self):
        return self.__mobile_number
        
    def set_line_items(self, line_items):
        self.__line_items = line_items
        
    def get_line_items(self):
        return self.__line_items
        
    def set_total_amount(self, total_amount):
        self.__total_amount = total_amount
        
    def get_total_amount(self):
        return self.__total_amount

    def set_total_tax_amount(self, total_tax_amount):
        self.__total_tax_amount = total_tax_amount
        
    def get_total_tax_amount(self):
        return self.__total_tax_amount

    def set_net_amount(self, total_net_amount):
        self.__net_amount = total_net_amount
        
    def get_net_amount(self):
        return self.__net_amount

    def set_discount_amount(self, discount_amount):
        self.__discount_amount = discount_amount
        
    def get_discount_amount(self):
        return self.__discount_amount

    def set_roundoff_amount(self, roundoff_amount):
        self.__roundoff_amount = roundoff_amount
        
    def get_roundoff_amount(self):
        return self.__roundoff_amount

    def set_invoice_amount(self, invoice_amount):
        self.__invoice_amount = invoice_amount
        
    def get_invoice_amount(self):
        return self.__invoice_amount

    def set_invoice_idx(self, invoice_idx):
        self.__invoice_idx = invoice_idx
        
    def get_invoice_idx(self):
        return self.__invoice_idx  

    # Focus        
    def focus_invoices_list(self):
        self.__window['_INVOICES_LIST_'].Widget.config(takefocus=1)
        self.__window.Element('_INVOICES_LIST_').set_focus(force = True)        
        if len(self.__invoices_list) > 0:        
            table_row = self.__window['_INVOICES_LIST_'].Widget.get_children()[0]
            self.__window['_INVOICES_LIST_'].Widget.selection_set(table_row)  # move selection
            self.__window['_INVOICES_LIST_'].Widget.focus(table_row)  # move focus
            self.__window['_INVOICES_LIST_'].Widget.see(table_row)  # scroll to show i

    def focus_invoices_list_row(self, idx):
        self.__window['_INVOICES_LIST_'].Widget.config(takefocus=1)
        self.__window.Element('_INVOICES_LIST_').set_focus(force = True)
        table_row = self.__window['_INVOICES_LIST_'].Widget.get_children()[idx]
        self.__window['_INVOICES_LIST_'].Widget.selection_set(table_row)  # move selection
        self.__window['_INVOICES_LIST_'].Widget.focus(table_row)  # move focus
        self.__window['_INVOICES_LIST_'].Widget.see(table_row)  # scroll to show i
    
    def clear_ui_invoices_list(self):
        self.__ui_invoice_list.clear()
        self.__window.Element('_INVOICES_LIST_').update(values = self.__ui_invoice_list)

    def elements_to_invoice_line(self):
        self.__invoice_line.append(self.__invoice_number)
        self.__invoice_line.append(self.__mobile_number)        
        self.__invoice_line.append(self.__line_items)        
        self.__invoice_line.append("{:.2f}".format(float(self.__total_amount)))      
        self.__invoice_line.append("{:.2f}".format(float(self.__total_tax_amount)))       
        self.__invoice_line.append("{:.2f}".format(float(self.__net_amount)))    
        self.__invoice_line.append("{:.2f}".format(float(self.__discount_amount)))       
        self.__invoice_line.append("{:.2f}".format(float(self.__roundoff_amount)))
        self.__invoice_line.append("{:.2f}".format(float(self.__invoice_amount)))
       
    def invoice_line_to_elements(self, idx):
        self.__invoice_line = self.__invoices_list[idx]
        self.__invoice_number = self.__invoice_line[0]
        self.__mobile_number = self.__invoice_line[1]
        self.__line_items = self.__invoice_line[2]
        self.__total_amount = self.__invoice_line[3]
        self.__total_tax_amount = self.__invoice_line[4]
        self.__net_amount = self.__invoice_line[5]
        self.__discount_amount = self.__invoice_line[6]
        self.__roundoff_amount = self.__invoice_line[7]
        self.__invoice_amount = self.__invoice_line[8]

    def add_invoice_line(self):
        self.__invoice_line = []
        self.elements_to_invoice_line()    
        self.__invoices_list.append(self.__invoice_line)
        self.__window.Element('_INVOICES_LIST_').update(values = self.__invoices_list)

    # Properties   
    invoices_list = property(get_invoices_list, set_invoices_list)
    invoice_line = property(get_invoice_line, set_invoice_line)
    invoice_idx = property(get_invoice_idx, set_invoice_idx)
    invoice_number_search = property(get_invoice_number_search, set_invoice_number_search)
    mobile_number_search = property(get_mobile_number_search, set_mobile_number_search)
    invoice_number = property(get_invoice_number, set_invoice_number)
    mobile_number = property(get_mobile_number, set_mobile_number)
    line_items = property(get_line_items, set_line_items)
    total_amount = property(get_total_amount, set_total_amount)
    total_tax_amount = property(get_total_tax_amount, set_total_tax_amount)
    net_amount = property(get_net_amount, set_net_amount)
    discount_amount = property(get_discount_amount, set_discount_amount)
    roundoff_amount = property(get_roundoff_amount, set_roundoff_amount)
    invoice_amount = property(get_invoice_amount, set_invoice_amount)


class PaymentUi:

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
