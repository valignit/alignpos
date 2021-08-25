import datetime


class EstimateUi:

    def __init__(self, window):
    
        self.__window = window

        ###
        # Initialize Header Pane
        self.__estimate_number = str('')
        self.__mobile_number = str('')
        self.__customer_number = str('')
        self.__customer_name = str('')
        self.__customer_address = str('')
        
        # Initialize Search Pane
        self.__barcode = str('')
        self.__search_name = str('') 
        self.__search_item_group = str('') 
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
        self.__estimate_amount = float(0.00)

        ###
        # Unfocus Header Pane        
        self.__window['_ESTIMATE_NUMBER_'].Widget.config(takefocus=0)
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
        self.__window['_ESTIMATE_AMOUNT_'].Widget.config(takefocus=0)

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
    def set_estimate_number(self, estimate_number):
        self.__estimate_number = estimate_number
        self.__window.Element('_ESTIMATE_NUMBER_').update(value = self.__estimate_number)
        
    def get_estimate_number(self):
        self.__estimate_number = self.__window.Element('_ESTIMATE_NUMBER_').get()        
        return self.__estimate_number
        
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

    def set_estimate_amount(self, estimate_amount):
        self.__estimate_amount = estimate_amount
        self.__window.Element('_ESTIMATE_AMOUNT_').update(value = "{:.2f}".format(self.__estimate_amount))
        
    def get_estimate_amount(self):
        self.__estimate_amount = self.__window.Element('_ESTIMATE_AMOUNT_').get()        
        return self.__estimate_amount


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
    estimate_number = property(get_estimate_number, set_estimate_number) 
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
    estimate_amount = property(get_estimate_amount, set_estimate_amount)
        

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


class EstimateListUi:
    def __init__(self, window):
        self.__window = window

        self.__estimates_list = []
        self.__estimate_line = []
        self.__estimate_idx = 0
        self.__estimate_number = ''
        self.__estimate_number_search = ''
        self.__mobile_number = ''
        self.__mobile_number_search = ''
        self.__line_items = 0
        self.__total_amount = float(0.00)
        self.__total_tax_amount = float(0.00)
        self.__net_amount = float(0.00)
        self.__discount_amount = float(0.00)
        self.__roundoff_amount = float(0.00)
        self.__estimate_amount = float(0.00)
        
        self.__window["_ESTIMATE_LIST_OK_"].Widget.config(takefocus=0)
        self.__window["_ESTIMATE_LIST_ESC_"].Widget.config(takefocus=0)
        self.__window["_ESTIMATE_LIST_SEARCH_"].Widget.config(takefocus=0)
       
    # Setters and Getters
    def set_estimates_list(self, estimates_list):
        self.__estimates_list = estimates_list
        self.__window.Element('_ESTIMATES_LIST_').update(values = self.__estimates_list)
        
    def get_estimates_list(self):
        self.__estimates_list = self.__window.Element('_ESTIMATES_LIST_').get()
        return self.__estimates_list
              
    def set_estimate_line(self, estimate_line):
        self.__estimate_line = estimate_line
        
    def get_estimate_line(self):
        self.__estimate_line = self.__estimates_list[self.__item_idx]
        return self.__estimate_line
    
    def set_estimate_number_search(self, estimate_number_search):
        self.__estimate_number_search = estimate_number_search
        self.__window.Element('_ESTIMATE_NUMBER_SEARCH_').update(value = self.__estimate_number_search)
        
    def get_estimate_number_search(self):
        self.__estimate_number_search = self.__window.Element('_ESTIMATE_NUMBER_SEARCH_').get()        
        return self.__estimate_number_search
        
    def set_mobile_number_search(self, mobile_number_search):
        self.__mobile_number_search = mobile_number_search
        self.__window.Element('_MOBILE_NUMBER_SEARCH_').update(value = self.__mobile_number_search)
        
    def get_mobile_number_search(self):
        self.__mobile_number_search = self.__window.Element('_MOBILE_NUMBER_SEARCH_').get()        
        return self.__mobile_number_search
        
    def set_estimate_number(self, estimate_number):
        self.__estimate_number = estimate_number
        
    def get_estimate_number(self):
        return self.__estimate_number
        
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

    def set_estimate_amount(self, estimate_amount):
        self.__estimate_amount = estimate_amount
        
    def get_estimate_amount(self):
        return self.__estimate_amount

    def set_estimate_idx(self, estimate_idx):
        self.__estimate_idx = estimate_idx
        
    def get_estimate_idx(self):
        return self.__estimate_idx  

    # Focus        
    def focus_estimates_list(self):
        self.__window['_ESTIMATES_LIST_'].Widget.config(takefocus=1)
        self.__window.Element('_ESTIMATES_LIST_').set_focus(force = True)        
        if len(self.__estimates_list) > 0:        
            table_row = self.__window['_ESTIMATES_LIST_'].Widget.get_children()[0]
            self.__window['_ESTIMATES_LIST_'].Widget.selection_set(table_row)  # move selection
            self.__window['_ESTIMATES_LIST_'].Widget.focus(table_row)  # move focus
            self.__window['_ESTIMATES_LIST_'].Widget.see(table_row)  # scroll to show i

    def focus_estimates_list_row(self, idx):
        self.__window['_ESTIMATES_LIST_'].Widget.config(takefocus=1)
        self.__window.Element('_ESTIMATES_LIST_').set_focus(force = True)
        table_row = self.__window['_ESTIMATES_LIST_'].Widget.get_children()[idx]
        self.__window['_ESTIMATES_LIST_'].Widget.selection_set(table_row)  # move selection
        self.__window['_ESTIMATES_LIST_'].Widget.focus(table_row)  # move focus
        self.__window['_ESTIMATES_LIST_'].Widget.see(table_row)  # scroll to show i
    
    def clear_estimates_list(self):
        self.__estimates_list.clear()
        self.__window.Element('_ESTIMATES_LIST_').update(values = self.__estimates_list)

    def elements_to_estimate_line(self):
        self.__estimate_line.append(self.__estimate_number)
        self.__estimate_line.append(self.__mobile_number)        
        self.__estimate_line.append(self.__line_items)        
        self.__estimate_line.append("{:.2f}".format(float(self.__total_amount)))      
        self.__estimate_line.append("{:.2f}".format(float(self.__total_tax_amount)))       
        self.__estimate_line.append("{:.2f}".format(float(self.__net_amount)))    
        self.__estimate_line.append("{:.2f}".format(float(self.__discount_amount)))       
        self.__estimate_line.append("{:.2f}".format(float(self.__roundoff_amount)))
        self.__estimate_line.append("{:.2f}".format(float(self.__estimate_amount)))
       
    def estimate_line_to_elements(self, idx):
        self.__estimate_line = self.__estimates_list[idx]
        self.__estimate_number = self.__estimate_line[0]
        self.__mobile_number = self.__estimate_line[1]
        self.__line_items = self.__estimate_line[2]
        self.__total_amount = self.__estimate_line[3]
        self.__total_tax_amount = self.__estimate_line[4]
        self.__net_amount = self.__estimate_line[5]
        self.__discount_amount = self.__estimate_line[6]
        self.__roundoff_amount = self.__estimate_line[7]
        self.__estimate_amount = self.__estimate_line[8]

    def add_estimate_line(self):
        self.__estimate_line = []
        self.elements_to_estimate_line()    
        self.__estimates_list.append(self.__estimate_line)
        self.__window.Element('_ESTIMATES_LIST_').update(values = self.__estimates_list)

    # Properties   
    estimates_list = property(get_estimates_list, set_estimates_list)
    estimate_line = property(get_estimate_line, set_estimate_line)
    estimate_idx = property(get_estimate_idx, set_estimate_idx)
    estimate_number_search = property(get_estimate_number_search, set_estimate_number_search)
    mobile_number_search = property(get_mobile_number_search, set_mobile_number_search)
    estimate_number = property(get_estimate_number, set_estimate_number)
    mobile_number = property(get_mobile_number, set_mobile_number)
    line_items = property(get_line_items, set_line_items)
    total_amount = property(get_total_amount, set_total_amount)
    total_tax_amount = property(get_total_tax_amount, set_total_tax_amount)
    net_amount = property(get_net_amount, set_net_amount)
    discount_amount = property(get_discount_amount, set_discount_amount)
    roundoff_amount = property(get_roundoff_amount, set_roundoff_amount)
    estimate_amount = property(get_estimate_amount, set_estimate_amount)

