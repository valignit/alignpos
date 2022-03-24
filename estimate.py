import PySimpleGUI as sg
from datetime import datetime
from pynput.keyboard import Key, Controller
import pdfkit
import os
from barcode import Code128
from barcode import Code128
from barcode.writer import ImageWriter

from config import Config
from utilities import Message, Keypad
from db_nosql import KvDatabase
from db_orm import DbConn, DbTable, DbQuery
from estimate_layout import EstimateCanvas, ChangeQtyCanvas, EstimateListCanvas, PaymentCanvas, DiscountCanvas
from estimate_ui import EstimateUi, ChangeQtyUi, EstimateListUi, PaymentUi, DiscountUi
from common import ItemList, CustomerList


class Estimate():

    def __init__(self, menu_opt, user_id, terminal_id, branch_id):
    
        config = Config()
        
        self.__menu_opt = menu_opt
        self.__terminal_id = terminal_id
        self.__branch_id = branch_id
        
        self.__reference_number = None
        w, h = sg.Window.get_screen_size()
        
        self.__kv_settings = KvDatabase('kv_settings')
        self.__kv_strings = KvDatabase('kv_strings')

        self.__tax_included = self.__kv_settings.get('tax_included')
        self.__current_date = self.__kv_settings.get('current_date')
        self.__current_status = self.__kv_settings.get('current_status')
        
        kb = Controller()
        self.__kb = kb
        
        self.__actual_items_list = []
        
        self.__db_conn = DbConn()
        self.__db_session = self.__db_conn.session

        self.__db_customer_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabCustomer)
        self.__db_item_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabItem)
        self.__db_estimate_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabEstimate)
        self.__db_estimate_item_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabEstimate_Item)
        self.__db_estimate_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabEstimate)
        self.__db_estimate_item_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabEstimate_Item)
        self.__db_exchange_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabExchange)   
        
        # Creating Items list to populate dynamic favorite buttons - done before Layout instance is created
        self.__fav_item_codes_list = []
        self.__fast_item_codes_list = []
        self.__fav_item_names_list = []
        self.__fast_item_names_list = []
       
        if self.__menu_opt == 'operation':
            title = 'Estimate'
            self.fill_item_lists()
        else:
            title = 'Estimate History'

        self.__canvas = EstimateCanvas( self.__menu_opt,
                                        self.__fav_item_codes_list,
                                        self.__fav_item_names_list,
                                        self.__fast_item_codes_list,                                  
                                        self.__fast_item_names_list)
        
        self.__window = sg.Window(title, 
                        self.__canvas.layout,
                        font='Helvetica 11', 
                        finalize=True, 
                        location=(-8,0), 
                        size=(w,h-50),
                        keep_on_top=False, 
                        resizable=False,
                        return_keyboard_events=True, 
                        use_default_focus=False,
                        icon='images/favicon.ico',
                        modal=True
                    )

        #self.__window.maximize()
        
        self.__window['_LEFT_PANES_'].Widget.configure(borderwidth=1, relief=sg.DEFAULT_FRAME_RELIEF)
        self.__window['_RIGHT_PANES_'].Widget.configure(borderwidth=1, relief=sg.DEFAULT_FRAME_RELIEF)
        self.__window['_BARCODE_'].bind('<FocusIn>', '+CLICK+')
        self.__window['_SEARCH_NAME_'].bind('<FocusIn>', '+CLICK+')
        self.__window['_SEARCH_ITEM_GROUP_'].bind('<FocusIn>', '+CLICK+')

        self.__ui = EstimateUi(self.__window)
    
        self.initialize_ui()        
        self.__ui.user_id = user_id
        self.__ui.terminal_id = terminal_id    
        self.__ui.branch_id = branch_id    
        #self.__ui.current_date = self.__current_date    
        self.__ui.current_date = datetime.strptime(self.__current_date, "%Y-%m-%d").strftime("%d-%m-%Y")
        
        # Creating Item Groups list to populate search combo
        item_groups_list = ['None']
        db_query = DbQuery(self.__db_conn, 'select distinct(item_group) from tabItem where item_group <> "NULL"')        
        if  db_query.result:
            for db_row in db_query.result:
                item_groups_list.append(db_row[0])

        self.__ui.item_groups_list = item_groups_list
        self.__ui.focus_item_group_line(0)
        self.__ui.unfocus_tools_pane()
        self.__ui.unfocus_fast_pane(self.__fast_item_codes_list)
        self.__ui.unfocus_favorite_pane(self.__fav_item_codes_list)

        ct = 0
        
        # Setting images in Favorite item buttons
        # If there is no image for an item, a default image will be displayed
        for item_code in self.__fav_item_codes_list:
            path = config.application_path + '/images/'
            file = path + item_code + '.png'
            element = 'FAV_' + item_code            
            if os.path.isfile(file):
                self.__window.Element(element).update(image_filename = file)                
            else:
                self.__window.Element(element).update(image_filename = path + 'ITEM-0000.png')              
            self.__window.Element(element).set_tooltip(item_code + '\n' + self.__fav_item_names_list[ct] + '\n' + 'ALT-' + str( ct + 1))
            ct += 1
              
        self.goto_last_row()
        
        self.handler()
        self.__db_conn.close()
        self.__window.close()


    def handler(self):
        event = None
        prev_event = None 
        item_idx = '' 
        focus = None    
        while True:
            if not event == 'Shift_L:16':
                prev_event = event

            event, values = self.__window.read()
            
            if self.__window.FindElementWithFocus():
                focus = self.__window.FindElementWithFocus().Key
                
            #print('---main---', '\nevent=', event, '\nprev=', prev_event, '\nfocus=', focus, '\nval=', values)
            #print('---main---', '\nevent=', event, '\nprev=', prev_event, '\nfocus=', focus)

            if event in (sg.WIN_CLOSED, 'Escape:27', 'Escape', 'Exit'):
                break

            if event == 'ENTER':        
                self.__kb.press(Key.enter)
                self.__kb.release(Key.enter)
                continue
                
            if event == 'ESC':
                self.__kb.press(Key.esc)
                self.__kb.release(Key.esc)
                continue
                
            if event == 'TAB':        
                self.__kb.press(Key.tab)
                self.__kb.release(Key.tab)
                continue
                
            if event == 'DEL':
                self.__kb.press(Key.delete)
                self.__kb.release(Key.delete)
                continue
                
            if event == 'UP':        
                self.__kb.press(Key.up)
                self.__kb.release(Key.up)
                continue
                
            if event == 'DOWN':
                self.__kb.press(Key.down)
                self.__kb.release(Key.down)
                continue
                
            if event == 'RIGHT':
                self.__kb.press(Key.right)
                self.__kb.release(Key.right)
                continue
                
            if event == 'LEFT':
                self.__kb.press(Key.left)
                self.__kb.release(Key.left)
                continue
                
            if event == 'BACKSPACE':
                self.__kb.press(Key.backspace)
                self.__kb.release(Key.backspace)
                continue

            if event in ('Home:36', '_BEGIN_'):            
                if not self.__actual_items_list == self.__ui.items_list:
                    confirm_save = Message('OPT', 'Save current Estimate?')
                    if confirm_save.ok:
                        self.save_estimate()            
                self.goto_first_row()
                continue
                
            if event in ('Left:37', '_PREVIOUS_'):
                if not self.__actual_items_list == self.__ui.items_list:
                    confirm_save = Message('OPT', 'Save current Estimate?')
                    if confirm_save.ok:
                        self.save_estimate()            
                self.goto_previous_row()
                continue
                
            if event in ('Right:39', '_NEXT_'):
                if not self.__actual_items_list == self.__ui.items_list:
                    confirm_save = Message('OPT', 'Save current Estimate?')
                    if confirm_save.ok:
                        self.save_estimate()            
                self.goto_next_row()
                continue

            if event in ('End:35', '_END_'):
                if not self.__actual_items_list == self.__ui.items_list:
                    confirm_save = Message('OPT', 'Save current Estimate?')
                    if confirm_save.ok:
                        self.save_estimate()            
                self.goto_last_row()
                continue

            if self.__menu_opt == 'history' and event not in ('F5:116', 'F5', 'Print', 'F10', 'F10:121', '_FIND_'):
                continue

            if event == '\t':
                if focus == '_ITEMS_LIST_':
                    if len(self.__ui.items_list) > 0:
                        self.__ui.focus_items_list_row(len(self.__ui.items_list)-1)
                continue
             
            if event == '_SEARCH_ITEM_GROUP_+CLICK+':
                selected_group = values['_SEARCH_ITEM_GROUP_']
                if not selected_group == 'None':
                    filter = 'item_group = "{}"'.format(selected_group)
                    item_code = self.item_list(filter)
                    self.process_item_name(item_code)                    
                    self.initialize_search_pane()            
                    self.__ui.focus_item_group_line(0)
                    if self.__ui.items_list:
                        self.__ui.focus_items_list_last()
                continue

            if event in ('+', 'Add') and focus in ('_ITEMS_LIST_', '+'):
                if values['_ITEMS_LIST_']:
                    item_idx = values['_ITEMS_LIST_'][0]
                    self.process_count(item_idx, '+')
                    self.sum_item_list()
                    continue

            if event in ('-', 'Less') and focus in ('_ITEMS_LIST_', '-'):
                if values['_ITEMS_LIST_']:
                    item_idx = values['_ITEMS_LIST_'][0]
                    self.process_count(item_idx, '-')
                    self.sum_item_list()
                    continue

            if event[4:] in self.__fav_item_codes_list:
                item_code = event[4:]
                self.process_item_name(item_code)                    
                self.initialize_search_pane()
                self.__ui.focus_items_list_last()
                continue
                
            if event[5:] in self.__fast_item_codes_list:
                item_code = event[5:]
                self.process_item_name(item_code)                    
                self.initialize_search_pane()
                self.__ui.focus_items_list_last()
                continue

            if prev_event == 'Alt_L:18' and event.upper() in ('I', 'J', 'K', 'L', 'M'):
                item_code = self.__fast_item_codes_list[ord(event.upper()) - 73]
                self.process_item_name(item_code)             
                self.__ui.focus_items_list_last()
                continue
                
            if event == 'Alt_L:18' and prev_event.upper() in ('I', 'J', 'K', 'L', 'M'):
                item_code = self.__fast_item_codes_list[ord(prev_event.upper()) - 73]
                self.process_item_name(item_code)
                self.initialize_search_pane()
                self.__ui.focus_items_list_last()
                continue

            if prev_event == 'Alt_L:18' and event.isnumeric():
                item_code = self.__fav_item_codes_list[int(event)-1]
                self.process_item_name(item_code)             
                self.__ui.focus_items_list_last()
                continue
                
            if event == 'Alt_L:18' and prev_event.isnumeric():
                item_code = self.__fav_item_codes_list[int(prev_event)-1]
                self.process_item_name(item_code)
                self.initialize_search_pane()
                self.__ui.focus_items_list_last()
                continue

            if event == '_KEYPAD1_':        
                result = self.keypad(self.__ui.barcode)
                self.__ui.barcode = result
                self.process_barcode()
                self.initialize_search_pane()
                continue

            if event == '_KEYPAD2_':        
                result = self.keypad(self.__ui.search_name)
                self.__ui.search_name = result
                if len(self.__ui.search_name) > 2:
                    filter = "upper(item_name) like upper('%{}%')".format(self.__ui.search_name)
                    item_code = self.item_list(filter)
                    self.process_item_name(item_code)
                    self.initialize_search_pane()            
                continue
            
            if event in ('F1:112', 'F1', 'New'):
                self.new_estimate()
                self.__ui.focus_items_list()
                continue

            if event in ('F2:113', 'F2', 'Delete:46', 'Delete'):
                if focus == '_ITEMS_LIST_':
                    if values['_ITEMS_LIST_']:
                        confirm_delete = Message('OPT', 'Delete current Item?')
                        if not confirm_delete.ok:
                            continue
                        idx = values['_ITEMS_LIST_'][0]
                        self.delete_item(idx)
                        if len(self.__ui.items_list) == 0: 
                            Message('WARN', 'Empty estimate will be deleted')                        
                            estimate_number = self.__ui.draft_number            
                            self.delete_estimate()
                            self.clear_ui()
                            self.__actual_items_list = []
                            self.__ui.items_list = []                        
                            self.__ui.draft_number = estimate_number
                            self.goto_previous_row()
                            if self.__ui.draft_number == estimate_number:
                                self.__ui.draft_number = ''
                        prev_idx = ''
                        item_idx = ''
                    else:
                        Message('WARN', 'Select an Item')
                        self.__ui.focus_barcode()                                  
                        continue
                elif focus == '_SEARCH_ITEM_GROUP_':
                    self.__ui.focus_item_group_line(0)
                    self.__ui.focus_barcode()                         
                    continue
                else:
                    if not self.__ui.draft_number or self.__ui.draft_number == '':
                        Message('WARN', 'Please save the Estimate')
                        continue
                    confirm_delete = Message('OPT', 'Delete current Estimate?')
                    if not confirm_delete.ok:
                        continue
                    estimate_number = self.__ui.draft_number            
                    self.delete_estimate()
                    self.clear_ui()
                    self.__actual_items_list = []
                    self.__ui.items_list = []                        
                    self.__ui.draft_number = estimate_number
                    self.goto_previous_row()
                    if self.__ui.draft_number == estimate_number:
                        self.__ui.draft_number = ''
                continue
               
            if event in ('F3:114', 'F3', 'Save'):
                if len(self.__ui.items_list) > 0:
                    self.save_estimate()
                    self.__ui.focus_items_list_last()
                continue

            if event in ('F4:115', 'F4', 'Submit'):
                self.payment()
                #self.save_estimate()
                if self.__ui.final_number:               
                    self.print_estimate()
                    self.clear_ui()
                    self.__actual_items_list = []                                
                continue
                
            if event in ('F5:116', 'F5', 'Print'):
                self.print_estimate()
                self.__ui.focus_items_list_last()
                continue

            if event in ('F6:117', 'F6', 'Specs'):
                if focus == '_ITEMS_LIST_' :        
                    if values['_ITEMS_LIST_']:
                        item_idx = values['_ITEMS_LIST_'][0]
                        Message('INFO', 'Feature not yet implemented')
                        prev_idx = ''
                        item_idx = ''
                    else:
                        Message('WARN', 'Select an Item')                                
                else:
                    Message('WARN', 'Select an Item')                
                continue

            if event in ('F7:118', 'F7', 'Quantity'):
                if focus == '_ITEMS_LIST_' :
                    if values['_ITEMS_LIST_']:
                        item_idx = values['_ITEMS_LIST_'][0]
                        new_qty = self.change_qty(self.__ui.items_list[item_idx])
                        self.process_change_qty(new_qty, item_idx)
                        prev_idx = ''
                        item_idx = ''
                    else:
                        Message('WARN', 'Select an Item')                                
                else:
                    Message('WARN', 'Select an Item')                
                continue
                
            if event in ('F8:119', 'F8', 'Weight'):
                if focus == '_ITEMS_LIST_' :
                    if values['_ITEMS_LIST_']:
                        item_idx = values['_ITEMS_LIST_'][0]
                        self.process_weight(item_idx)
                        prev_idx = ''
                        item_idx = ''
                    else:
                        Message('WARN', 'Select an Item')                                
                else:
                    Message('WARN', 'Select an Item')                                
                continue

            if event in ('F9:120', 'F9', 'Discount'):
                if focus == '_ITEMS_LIST_' :
                    if values['_ITEMS_LIST_']:
                        item_idx = values['_ITEMS_LIST_'][0]
                        item_discount_amount = self.discount(self.__ui.items_list[item_idx])                        
                        self.process_discount(item_discount_amount, item_idx)
                        self.sum_item_list()
                        prev_idx = ''
                        item_idx = ''
                    else:
                        Message('WARN', 'Select an Item')                                
                else:
                    Message('WARN', 'Select an Item')                                
                continue

            if event in ('F10', 'F10:121', '_FIND_'):
                if len(self.__ui.items_list) > 0:
                    if not self.__actual_items_list == self.__ui.items_list:                
                        confirm_save = Message('OPT', 'Save current Estimate?')
                        if confirm_save.ok:
                            self.save_estimate()
                estimate_number = self.estimate_list()
                self.goto_this_row(estimate_number)
                continue
            
            if (event == 'Addon') or (event == 'Alt_L:18' and prev_event in ('a', 'A')):
                filter = "upper(item_code) like upper('ITEM-9%')"
                item_code = self.item_list(filter)
                if item_code:
                    self.process_item_name(item_code)
                    self.initialize_search_pane()
                    self.__ui.focus_items_list_last()
                continue
            
            if (event == 'Bundle') or (event == 'Alt_L:18' and prev_event in ('b', 'B')):
                filter = "bundle = 1"
                item_code = self.item_list(filter)
                if item_code:
                    self.process_item_name(item_code)
                    self.initialize_search_pane()
                    self.__ui.focus_items_list_last()
                continue
                       
            if event == 'v:86' and focus == '_BARCODE_':
                self.process_barcode()
                self.initialize_search_pane()
                continue

            if event == 'v:86' and focus == '_ITEMS_LIST_':
                self.process_barcode()
                self.initialize_search_pane()
                continue

            if event == 'v:86' and focus == '_SEARCH_NAME_':
                if len(self.__ui.search_name) > 2:
                    filter = "upper(item_name) like upper('%{}%')".format(self.__ui.search_name)
                    item_code = self.item_list(filter)
                    self.process_item_name(item_code)
                    self.initialize_search_pane()
                    self.__ui.focus_items_list_last()
                continue
                
            if event.isnumeric() and focus == '_BARCODE_':
                if self.__ui.barcode:
                    self.__ui.barcode = self.__ui.barcode.upper()
                    if (self.__ui.barcode[0].isnumeric() and len(self.__ui.barcode) > 12) or \
                       (self.__ui.barcode[0] == 'I' and len(self.__ui.barcode) > 8):
                        self.process_barcode()
                        self.initialize_search_pane()
                continue

            if event.isalnum() and focus == '_SEARCH_NAME_':
                if len(self.__ui.search_name) > 2:
                    filter = "upper(item_name) like upper('%{}%')".format(self.__ui.search_name)
                    item_code = self.item_list(filter)                    
                    self.process_item_name(item_code)
                    self.initialize_search_pane()
                    self.__ui.focus_items_list_last()
                continue
            
            if (event.isnumeric() or event == 'BackSpace:8' or event in ('I', 'T', 'E', 'M', '-', 'i', 't', 'e', 'm')) and focus == '_ITEMS_LIST_':
                if event.isnumeric(): 
                    if prev_event == 'Alt_L:18':
                        continue
                        
                if event == 'BackSpace:8':
                    if len(self.__ui.barcode) > 0:
                        self.__ui.barcode = self.__ui.barcode[:-1]
                    continue

                if event == '-':
                    print('here')
                    if len(self.__ui.barcode) == 4:
                        self.__ui.barcode = self.__ui.barcode + event
                    else:                    
                        if values['_ITEMS_LIST_']:
                            item_idx = values['_ITEMS_LIST_'][0]
                            self.process_count(item_idx, '-')
                            self.sum_item_list()
                    continue                 
                                    
                self.__ui.barcode = self.__ui.barcode + event
                self.__ui.barcode = self.__ui.barcode.upper()
                if (self.__ui.barcode[0].isnumeric() and len(self.__ui.barcode) > 12) or \
                   (self.__ui.barcode[0] == 'I' and len(self.__ui.barcode) > 8):
                    self.process_barcode()
                    self.initialize_search_pane()
                continue
    
    ######
    # Wrapper function for Change Qty
    #      whole line is sent as parameter so that item_name and old_qty also can be used
    def change_qty(self, item_line):
        change_qty = ChangeQty(item_line)
        return(change_qty.new_qty)


    ######
    # Wrapper function for Discount
    #      whole line is sent as parameter so that item_name and selling price also can be used
    def discount(self, item_line):
        discount = Discount(item_line)
        return(discount.item_discount_amount)


    ######
    # Wrapper function for Estimate List
    def estimate_list(self):
        estimate_list = EstimateList(self.__menu_opt, self.__terminal_id, self.__branch_id)
        return estimate_list.estimate_number


    ######
    # Wrapper function for Customer List
    def customer_list(self):
        customer_list = CustomerList()
        return customer_list.customer_number, customer_list.mobile_number


    ######
    # Wrapper function for Item List
    def item_list(self, filter):
        item_list = ItemList(filter)
        return(item_list.item_code)


    ######
    # Wrapper function for Payment
    def payment(self):
        input_param = dict()
        input_param['estimate_number'] = self.__ui.draft_number
        input_param['customer_number'] = self.__ui.customer_number
        input_param['mobile_number'] = self.__ui.mobile_number
        input_param['customer_name'] = self.__ui.customer_name
        input_param['customer_address'] = self.__ui.customer_address        
        input_param['net_amount'] = self.__ui.net_amount        
        payment = Payment(input_param)
        print(payment.output_param)
        if not payment.output_param:
            return
        self.__ui.final_number = payment.output_param['final_number']
        self.__ui.tax_estimate_amount = payment.output_param['estimate_amount']
        self.__ui.discount_amount = payment.output_param['discount_amount']
        self.__ui.roundoff_amount = payment.output_param['roundoff_adjustment']
        return 


    ######
    # Wrapper function for Keypad
    def keypad(self, current_value):
        keypad = Keypad(current_value)
        return(keypad.input_value)


    def fill_item_lists(self):
        max_fav_ct = 9
        max_fast_ct = 3
        fav_ct = 0
        fast_ct = 0
        for key in self.__kv_settings.getall():
            if key[:13] == 'favorite_item':
                fav_ct += 1
                if fav_ct > max_fav_ct:
                    continue
                item_key = 'favorite_item_' + str(fav_ct)
                self.__fav_item_codes_list.append(self.__kv_settings.get(item_key))

            elif key[:16] == 'fast_moving_item':
                fast_ct += 1
                if fast_ct > max_fast_ct:
                    continue
                item_key = 'fast_moving_item_' + str(fast_ct)
                self.__fast_item_codes_list.append(self.__kv_settings.get(item_key))

        for fav_item_code in self.__fav_item_codes_list:
            db_item_row = self.__db_item_table.get_row(fav_item_code)
            if db_item_row:
                self.__fav_item_names_list.append((db_item_row.item_name[:15].replace(' ', '_')).upper())
                
        for fast_item_code in self.__fast_item_codes_list:
            db_item_row = self.__db_item_table.get_row(fast_item_code)
            if db_item_row:
                self.__fast_item_names_list.append((db_item_row.item_name[:15].replace(' ', '_')).upper())

    def initialize_header_pane(self):
        self.__ui.draft_number = ''
        self.__ui.final_number = ''
        self.__ui.payment_status = ''
        walk_in_customer = self.__kv_settings.get('walk_in_customer')  
        db_customer_row = self.__db_customer_table.get_row(walk_in_customer)
        if db_customer_row:        
            self.__ui.mobile_number = db_customer_row.mobile_number
            self.__ui.customer_number = db_customer_row.name
            self.__ui.customer_name = db_customer_row.customer_name
            self.__ui.customer_address = db_customer_row.address
            self.__ui.customer_type = db_customer_row.customer_type
 
    def initialize_search_pane(self):
        self.__ui.barcode = ''
        self.__ui.search_name = ''
        self.__ui.focus_item_group_line(0)

    def initialize_detail_pane(self):
        self.__ui.items_list = []
        self.__ui.item_code = str('')
        self.__ui.barcode = str('')
        self.__ui.item_name = str('')
        self.__ui.item_group = str('')
        self.__ui.uom = str('')
        self.__ui.qty = float(0.0)
        self.__ui.standard_selling_price = float(0.00)
        self.__ui.applied_selling_price = float(0.00)
        self.__ui.item_discount_amount = float(0.00)
        self.__ui.selling_amount = float(0.00)
        self.__ui.tax_rate = float(0.00)
        self.__ui.tax_amount = float(0.00)
        self.__ui.net_amount = float(0.00)
        self.__ui.cgst_tax_rate = float(0.00)
        self.__ui.sgst_tax_rate = float(0.00)
        self.__ui.cgst_tax_amount = float(0.00)
        self.__ui.sgst_tax_amount = float(0.00)
        self.__ui.item_line = [] 

    def initialize_action_pane(self):
        self.__window.Element('F1').update(text='New\nF1')    
        self.__window.Element('F2').update(text='Delete\nF2')
        self.__window.Element('F3').update(text='Save\nF3')
        self.__window.Element('F4').update(text='Submit\nF4')
        self.__window.Element('F5').update(text='Print\nF5')
        self.__window.Element('F6').update(text='Specs\nF6')
        self.__window.Element('F7').update(text='Qty\nF7')
        self.__window.Element('F8').update(text='Weight\nF8')
        self.__window.Element('F9').update(text='Price\nF9')
        self.__window.Element('+').update(text='Add\n+')
        self.__window.Element('-').update(text='Less\n-')
        
    def initialize_footer_pane(self):
        self.__ui.user_id = ''
        self.__ui.terminal_id = ''
        self.__ui.branch_id = ''
        self.__ui.current_date = ''

    def initialize_summary_pane(self):
        self.__ui.line_items = 0
        self.__ui.total_amount = 0.00
        self.__ui.total_tax_amount = 0.00
        self.__ui.net_amount = 0.00
        self.__ui.total_cgst_amount = 0.00
        self.__ui.total_sgst_amount = 0.00
        self.__ui.total_tax_amount = 0.00
        self.__ui.discount_amount = 0.00          
        self.__ui.roundoff_amount = 0.00          
        self.__ui.estimate_amount = 0.00
        self.__ui.cash_amount = 0.00
        self.__ui.card_amount = 0.00
        self.__ui.exchange_amount = 0.00
        self.__ui.redeem_amount = 0.00
        self.__ui.paid_amount = 0.00

    def initialize_ui(self):
        self.initialize_header_pane()
        self.initialize_search_pane()
        self.initialize_detail_pane()
        self.initialize_action_pane()
        self.initialize_footer_pane()
        self.initialize_summary_pane()

    def clear_ui(self):
        self.initialize_header_pane()
        self.initialize_search_pane()    
        self.initialize_detail_pane()
        self.initialize_summary_pane()
    
    def goto_this_row(self, estimate_number):
        if estimate_number:
            if self.__menu_opt == 'operation':
                filter = "name = '{}' and terminal_id = {}"
            else:
                filter = "estimate_number = '{}' and terminal_id = {}"
            
            db_estimate_row = self.__db_estimate_table.first(filter.format(estimate_number, self.__terminal_id))
            if db_estimate_row:
                self.clear_ui()    
                self.show_ui(db_estimate_row)
                self.__ui.focus_items_list_last()                
        else:
            self.goto_last_row()

    def goto_first_row(self):
        if self.__menu_opt == 'operation':
            filter = "estimate_number is null and terminal_id = {}"
        else:
            filter = "estimate_number is not null and terminal_id = {}"
        
        db_estimate_row = self.__db_estimate_table.first(filter.format(self.__terminal_id))
        if db_estimate_row:
            self.clear_ui()    
            self.show_ui(db_estimate_row)
            self.__ui.focus_items_list_last()            

    def goto_previous_row(self): 
        db_estimate_row = None  
        if self.__menu_opt == 'operation':            
            if self.__ui.draft_number:
                name = self.__ui.draft_number
                filter = "name < '{}' and estimate_number is null and terminal_id = {}"
                db_estimate_row = self.__db_estimate_table.last(filter.format(name, self.__terminal_id))            
        else:
            if self.__ui.final_number:
                estimate_number = self.__ui.final_number
                filter = "name < '{}' and estimate_number is not null and terminal_id = {}"
                order = 'estimate_number'
                db_estimate_row = self.__db_estimate_table.last(filter.format(estimate_number, self.__terminal_id), order)
        if db_estimate_row:
                self.clear_ui()    
                self.show_ui(db_estimate_row)
                self.__ui.focus_items_list_last()                


    def goto_next_row(self):
        db_estimate_row = None  
        if self.__menu_opt == 'operation':            
            if self.__ui.draft_number:
                name = self.__ui.draft_number
                filter = "name > '{}' and estimate_number is null and terminal_id = {}"
                db_estimate_row = self.__db_estimate_table.first(filter.format(name, self.__terminal_id))            
        else:
            if self.__ui.final_number:
                estimate_number = self.__ui.final_number
                filter = "name > '{}' and estimate_number is not null and terminal_id = {}"
                order = 'estimate_number'
                db_estimate_row = self.__db_estimate_table.first(filter.format(estimate_number, self.__terminal_id), order)
                
        if db_estimate_row:
                self.clear_ui()    
                self.show_ui(db_estimate_row)
                self.__ui.focus_items_list_last()                
        else:
            self.goto_last_row()

    def goto_last_row(self):
        if self.__menu_opt == 'operation':            
            filter = "estimate_number is null and terminal_id = {}"
        else:
            filter = "estimate_number is not null and terminal_id = {}"
               
        db_estimate_row = self.__db_estimate_table.last(filter.format(self.__terminal_id))
        if db_estimate_row:
            self.clear_ui()
            self.show_ui(db_estimate_row)
            self.__ui.focus_items_list_last()

    def show_ui(self, db_estimate_row):
        if not db_estimate_row:
            return

        self.__reference_number = db_estimate_row.name
        if self.__menu_opt == 'operation':
            self.__ui.draft_number = db_estimate_row.name
        else:
            self.__ui.final_number = db_estimate_row.estimate_number        

        customer_number = db_estimate_row.customer
        db_customer_row = self.__db_customer_table.get_row(customer_number)
        if db_customer_row:
            self.__ui.mobile_number = db_customer_row.mobile_number
            self.__ui.customer_number = db_customer_row.name
            self.__ui.customer_name = db_customer_row.customer_name
            self.__ui.customer_address = db_customer_row.address

        self.__ui.item_line = []
        filter = "parent='{}'"
        db_estimate_item_cursor = self.__db_estimate_item_table.list(filter.format(self.__reference_number))    
        for db_estimate_item_row in db_estimate_item_cursor:
            self.move_db_estimate_item_to_ui_detail_pane(db_estimate_item_row)
        self.sum_item_list()
        if db_estimate_row.discount_amount:
            self.__ui.discount_amount = db_estimate_row.discount_amount
        else:
            self.__ui.discount_amount = 0.00
        if db_estimate_row.estimate_amount:
            self.__ui.estimate_amount = db_estimate_row.estimate_amount
        else:
            self.__ui.estimate_amount = 0.00
       
        self.__actual_items_list = self.__ui.items_list.copy()
    
    def move_db_item_to_ui_detail_pane(self, db_item_row):
        self.__ui.item_code = db_item_row.name
        self.__ui.item_barcode = db_item_row.barcode
        self.__ui.item_name = db_item_row.item_name
        self.__ui.uom = db_item_row.uom
        self.__ui.barcode = db_item_row.barcode
        self.__ui.item_group = db_item_row.item_group
        self.__ui.qty = 1
        self.__ui.cgst_tax_rate = db_item_row.cgst_tax_rate
        self.__ui.sgst_tax_rate = db_item_row.sgst_tax_rate
        self.__ui.tax_rate = float(self.__ui.cgst_tax_rate) + float(self.__ui.sgst_tax_rate)
        self.__ui.item_discount_amount = float(0.00)
        
        if self.__tax_included == 0:
            self.__ui.standard_selling_price = db_item_row.standard_selling_price
            self.__ui.applied_selling_price = float(db_item_row.standard_selling_price) - float(self.__ui.item_discount_amount)
            self.__ui.selling_amount = float(self.__ui.qty) * float(self.__ui.applied_selling_price)
            self.__ui.tax_amount = float(self.__ui.selling_amount) * float(self.__ui.tax_rate) / 100
            self.__ui.item_net_amount = float(self.__ui.selling_amount) + float(self.__ui.tax_amount)            
        else:
            self.__ui.standard_selling_price = db_item_row.standard_selling_price
            self.__ui.item_net_amount = float(db_item_row.standard_selling_price) * float(self.__ui.qty)
            self.__ui.tax_amount = round(float(self.__ui.item_net_amount)*(float(self.__ui.tax_rate)/(100 + float(self.__ui.tax_rate))),2)
            self.__ui.selling_amount = float(self.__ui.item_net_amount) - float(self.__ui.tax_amount)
            self.__ui.applied_selling_price = (float(self.__ui.selling_amount) / float(self.__ui.qty)) - float(self.__ui.item_discount_amount)
        self.__ui.cgst_tax_amount = round((float(self.__ui.selling_amount) * float(self.__ui.cgst_tax_rate) / 100), 2)
        self.__ui.sgst_tax_amount = round((float(self.__ui.selling_amount) * float(self.__ui.sgst_tax_rate) / 100), 2)
            
        self.__ui.add_item_line()    

    def move_db_estimate_item_to_ui_detail_pane(self, db_estimate_item_row):
        self.__ui.item_code = db_estimate_item_row.item
        
        db_item_row = self.__db_item_table.get_row(db_estimate_item_row.item)
        if db_item_row:
            self.__ui.item_barcode = db_item_row.barcode
            self.__ui.item_name = db_item_row.item_name
            self.__ui.uom = db_item_row.uom
            self.__ui.item_group = db_item_row.item_group
            self.__ui.uom = db_item_row.uom

        self.__ui.qty = db_estimate_item_row.qty
        self.__ui.cgst_tax_rate = db_estimate_item_row.cgst_tax_rate
        self.__ui.sgst_tax_rate = db_estimate_item_row.sgst_tax_rate
        self.__ui.tax_rate = float(self.__ui.cgst_tax_rate) + float(self.__ui.sgst_tax_rate)
        self.__ui.item_discount_amount = db_estimate_item_row.item_discount_amount
        self.__ui.standard_selling_price = db_estimate_item_row.standard_selling_price
        self.__ui.applied_selling_price = db_estimate_item_row.applied_selling_price
        self.__ui.selling_amount = db_estimate_item_row.selling_amount
        self.__ui.cgst_tax_amount = db_estimate_item_row.cgst_tax_amount
        self.__ui.sgst_tax_amount = db_estimate_item_row.cgst_tax_amount
        self.__ui.tax_amount = float(self.__ui.cgst_tax_amount) + float(self.__ui.sgst_tax_amount)
        self.__ui.item_net_amount = float(self.__ui.selling_amount) + float(self.__ui.tax_amount)
        
        self.__ui.add_item_line()
   
    def move_db_estimate_item_to_ui_detail_pane(self, db_estimate_item_row):
        self.__ui.item_code = db_estimate_item_row.item
        
        db_item_row = self.__db_item_table.get_row(db_estimate_item_row.item)
        if db_item_row:
            self.__ui.item_barcode = db_item_row.barcode
            self.__ui.item_name = db_item_row.item_name
            self.__ui.uom = db_item_row.uom
            self.__ui.item_group = db_item_row.item_group
            self.__ui.uom = db_item_row.uom

        self.__ui.qty = db_estimate_item_row.qty
        self.__ui.cgst_tax_rate = db_estimate_item_row.cgst_tax_rate
        self.__ui.sgst_tax_rate = db_estimate_item_row.sgst_tax_rate
        self.__ui.tax_rate = float(self.__ui.cgst_tax_rate) + float(self.__ui.sgst_tax_rate)

        self.__ui.qty = db_estimate_item_row.qty
        self.__ui.cgst_tax_rate = db_estimate_item_row.cgst_tax_rate
        self.__ui.sgst_tax_rate = db_estimate_item_row.sgst_tax_rate
        self.__ui.tax_rate = float(self.__ui.cgst_tax_rate) + float(self.__ui.sgst_tax_rate)
        self.__ui.item_discount_amount = db_estimate_item_row.item_discount_amount
        self.__ui.standard_selling_price = db_estimate_item_row.standard_selling_price
        self.__ui.applied_selling_price = db_estimate_item_row.applied_selling_price
        self.__ui.selling_amount = db_estimate_item_row.selling_amount
        self.__ui.cgst_tax_amount = db_estimate_item_row.cgst_tax_amount
        self.__ui.sgst_tax_amount = db_estimate_item_row.cgst_tax_amount
        self.__ui.tax_amount = float(self.__ui.cgst_tax_amount) + float(self.__ui.sgst_tax_amount)
        self.__ui.item_net_amount = float(self.__ui.selling_amount) + float(self.__ui.tax_amount)
        
        self.__ui.add_item_line()    
   
    def sum_item_list(self):
        line_items = 0
        total_selling_amount = 0.00
        total_item_discount_amount = 0.00
        total_tax_amount = 0.00
        total_cgst_amount = 0.00
        total_sgst_amount = 0.00
        total_net_amount = 0.00
       
        for item_line in self.__ui.items_list:
            self.__ui.item_line_to_elements(line_items)
            total_selling_amount += float(self.__ui.selling_amount)
            total_item_discount_amount += (float(self.__ui.qty) * float(self.__ui.item_discount_amount))
            total_cgst_amount += float(self.__ui.cgst_tax_amount)
            total_sgst_amount += float(self.__ui.sgst_tax_amount)
            line_items += 1

        self.__ui.line_items = line_items
        self.__ui.total_amount = total_selling_amount
        self.__ui.total_item_discount_amount = total_item_discount_amount
        self.__ui.total_cgst_amount = total_cgst_amount
        self.__ui.total_sgst_amount = total_sgst_amount
        self.__ui.total_tax_amount = total_cgst_amount + total_sgst_amount
        self.__ui.net_amount = float(self.__ui.total_amount) + float(self.__ui.total_tax_amount)
        self.__ui.estimate_amount = round(float(self.__ui.net_amount),0)
        self.__ui.roundoff_amount =  float(self.__ui.estimate_amount) - float(self.__ui.net_amount)

    def process_change_qty(self, new_qty, item_idx):
        if not new_qty:
            return
            
        if not float(new_qty) > 0:
            return
        self.__ui.fetch_item_line(item_idx)
        self.__ui.qty = new_qty

        self.__ui.selling_amount = float(self.__ui.qty) * float(self.__ui.applied_selling_price) - float(self.__ui.item_discount_amount)
        self.__ui.tax_rate = float(self.__ui.cgst_tax_rate) + float(self.__ui.sgst_tax_rate)
        self.__ui.tax_amount = float(self.__ui.selling_amount) * float(self.__ui.tax_rate) / 100
        self.__ui.cgst_tax_amount = float(self.__ui.selling_amount) * float(self.__ui.cgst_tax_rate) / 100
        self.__ui.sgst_tax_amount = float(self.__ui.selling_amount) * float(self.__ui.sgst_tax_rate) / 100
        self.__ui.item_net_amount = float(self.__ui.selling_amount) + float(self.__ui.tax_amount)
        
        self.__ui.update_item_line(item_idx)
        self.sum_item_list()
        self.__ui.focus_items_list_row(item_idx)
       
    def process_weight(self, idx):
        self.__ui.item_line_to_elements(idx)
        if not self.__ui.uom == 'Kg':
            Message('INFO', 'Not applicable to this UOM')
            return
        self.__ui.qty = 0.35

        self.__ui.selling_amount = float(self.__ui.qty) * float(self.__ui.applied_selling_price) - float(self.__ui.item_discount_amount)
        self.__ui.tax_rate = float(self.__ui.cgst_tax_rate) + float(self.__ui.sgst_tax_rate)
        self.__ui.tax_amount = float(self.__ui.selling_amount) * float(self.__ui.tax_rate) / 100
        self.__ui.cgst_tax_amount = float(self.__ui.selling_amount) * float(self.__ui.cgst_tax_rate) / 100
        self.__ui.sgst_tax_amount = float(self.__ui.selling_amount) * float(self.__ui.sgst_tax_rate) / 100
        self.__ui.item_net_amount = float(self.__ui.selling_amount) + float(self.__ui.tax_amount)

        self.__ui.update_item_line(idx)
        self.sum_item_list()
        self.__ui.focus_items_list_row(idx)       

    def process_discount(self, item_discount_amount, item_idx):
        if not item_discount_amount:
            return
        
        self.__ui.fetch_item_line(item_idx)
        self.__ui.item_discount_amount = item_discount_amount

        self.__ui.selling_amount = float(self.__ui.qty) * float(self.__ui.applied_selling_price) - float(self.__ui.item_discount_amount)
        self.__ui.tax_rate = float(self.__ui.cgst_tax_rate) + float(self.__ui.sgst_tax_rate)
        self.__ui.tax_amount = float(self.__ui.selling_amount) * float(self.__ui.tax_rate) / 100
        self.__ui.cgst_tax_amount = float(self.__ui.selling_amount) * float(self.__ui.cgst_tax_rate) / 100
        self.__ui.sgst_tax_amount = float(self.__ui.selling_amount) * float(self.__ui.sgst_tax_rate) / 100
        self.__ui.item_net_amount = float(self.__ui.selling_amount) + float(self.__ui.tax_amount)
        
        self.__ui.update_item_line(item_idx)
        self.sum_item_list()
        self.__ui.focus_items_list_row(item_idx)

    def process_count(self, idx, operator):
        self.__ui.item_line_to_elements(idx)
        if not self.__ui.uom == 'Nos':
            Message('INFO', 'Not applicable to this UOM')
            return
        qty = float(self.__ui.qty)
        if operator == '+':
            self.__ui.qty = qty + 1
        else:
            if qty > 1:
                print('qty:', qty)
                self.__ui.qty = qty - 1

        self.__ui.selling_amount = float(self.__ui.qty) * float(self.__ui.applied_selling_price) - float(self.__ui.item_discount_amount)
        self.__ui.tax_rate = float(self.__ui.cgst_tax_rate) + float(self.__ui.sgst_tax_rate)
        self.__ui.cgst_tax_amount = round((float(self.__ui.selling_amount) * float(self.__ui.cgst_tax_rate) / 100), 2)
        self.__ui.sgst_tax_amount = round((float(self.__ui.selling_amount) * float(self.__ui.sgst_tax_rate) / 100), 2)
        
        self.__ui.tax_amount = float(self.__ui.cgst_tax_amount) + float(self.__ui.sgst_tax_amount)
        self.__ui.item_net_amount = float(self.__ui.selling_amount) + float(self.__ui.tax_amount)

        self.__ui.update_item_line(idx)
        self.sum_item_list()
        self.__ui.focus_items_list_row(idx)
    
    def process_barcode(self):
        if not self.__ui.barcode:
            return
        
        self.__ui.barcode = self.__ui.barcode.upper()
        if (self.__ui.barcode[0].isnumeric() and len(self.__ui.barcode) > 12):
            filter = "barcode='{}'"
            db_item_row = self.__db_item_table.first(filter.format(self.__ui.barcode))
            if db_item_row:
                self.move_db_item_to_ui_detail_pane(db_item_row)       
        elif (self.__ui.barcode[0] == 'I' and len(self.__ui.barcode) > 8):
            filter = "item_code='{}'"   
            db_item_row = self.__db_item_table.first(filter.format(self.__ui.barcode))
            if db_item_row:
                self.move_db_item_to_ui_detail_pane(db_item_row)
        elif (self.__ui.barcode[0] == 'E' and len(self.__ui.barcode) > 8):
            filter = "parent='{}'"   
            db_estimate_item_cursor = self.__db_estimate_item_table.list(filter.format(self.__ui.barcode))
            for db_estimate_item_row in db_estimate_item_cursor:
                self.move_db_estimate_item_to_ui_detail_pane(db_estimate_item_row)
        else:
            return
        self.sum_item_list()
        self.__ui.focus_items_list_last()

    def process_item_name(self, item_code):
        filter = "item_code='{}'"   
        
        db_item_row = self.__db_item_table.first(filter.format(item_code))
        if db_item_row:
            self.move_db_item_to_ui_detail_pane(db_item_row)
            self.sum_item_list()

    def new_estimate(self):
        if not len(self.__ui.items_list) > 0:
            return

        if not self.__actual_items_list == self.__ui.items_list:
            confirm_save = Message('OPT', 'Save current Estimate?')
            if confirm_save.ok:
                self.save_estimate()
            
        self.clear_ui()

    def save_estimate(self):
        if not len(self.__ui.items_list) > 0:
            return    

        if self.__ui.draft_number == '':
            self.insert_estimate()        
        else:
            self.update_estimate()
        self.__actual_items_list = self.__ui.items_list

    def insert_estimate(self):
        db_query = DbQuery(self.__db_conn, 'SELECT nextval("ESTIMATE_NUMBER")')
        for db_row in db_query.result:
            self.__ui.draft_number = db_row[0]

        customer_number = 'CUST-00000'
        db_customer_row = self.__db_customer_table.get_row(customer_number)
        if db_customer_row:
            self.__ui.mobile_number = db_customer_row.mobile_number
            self.__ui.customer_number = db_customer_row.name
            self.__ui.customer_name = db_customer_row.customer_name
            self.__ui.customer_address = db_customer_row.address

        db_estimate_row = self.__db_estimate_table.new_row()

        db_estimate_row.name = self.__ui.draft_number
        db_estimate_row.customer = customer_number
        #db_estimate_row.posting_date = self.__ui.current_date    
        db_estimate_row.total_amount = self.__ui.total_amount
        db_estimate_row.net_amount = self.__ui.net_amount
        db_estimate_row.estimate_amount = self.__ui.estimate_amount
        db_estimate_row.cgst_tax_amount = self.__ui.total_cgst_amount
        db_estimate_row.sgst_tax_amount = self.__ui.total_sgst_amount
        db_estimate_row.branch_id = self.__ui.branch_id  
        db_estimate_row.terminal_id = self.__ui.terminal_id  

        self.__db_estimate_table.create_row(db_estimate_row)
        
        for idx in range(len(self.__ui.items_list)): 
            self.__ui.item_line_to_elements(idx)

            db_estimate_item_row = self.__db_estimate_item_table.new_row()
            
            db_estimate_item_row.name = self.__ui.draft_number + f"{idx:04d}"
            db_estimate_item_row.parent = self.__ui.draft_number
            db_estimate_item_row.item = self.__ui.item_code
            db_estimate_item_row.item_name = self.__ui.item_name
            db_estimate_item_row.qty = self.__ui.qty
            db_estimate_item_row.standard_selling_price = self.__ui.standard_selling_price
            db_estimate_item_row.applied_selling_price = self.__ui.applied_selling_price
            db_estimate_item_row.item_discount_amount = self.__ui.item_discount_amount
            db_estimate_item_row.selling_amount = self.__ui.selling_amount
            db_estimate_item_row.cgst_tax_rate = self.__ui.cgst_tax_rate
            db_estimate_item_row.sgst_tax_rate = self.__ui.sgst_tax_rate
            db_estimate_item_row.cgst_tax_amount = self.__ui.cgst_tax_amount
            db_estimate_item_row.sgst_tax_amount = self.__ui.sgst_tax_amount
          
            self.__db_estimate_item_table.create_row(db_estimate_item_row)

        self.__db_session.commit()
        
    def update_estimate(self):
        db_estimate_row = self.__db_estimate_table.get_row(self.__ui.draft_number)

        if not db_estimate_row:
            return
        #db_estimate_row.posting_date = self.__ui.current_date    
        db_estimate_row.customer = self.__ui.customer_number
        db_estimate_row.total_amount = self.__ui.total_amount
        db_estimate_row.net_amount = self.__ui.net_amount
        db_estimate_row.estimate_amount = self.__ui.estimate_amount
        db_estimate_row.cgst_tax_amount = self.__ui.total_cgst_amount
        db_estimate_row.sgst_tax_amount = self.__ui.total_sgst_amount
        db_estimate_row.terminal_id = self.__ui.terminal_id  

        filter = "parent='{}'"
        db_estimate_item_cursor = self.__db_estimate_item_table.list(filter.format(self.__ui.draft_number))
        for db_estimate_item_row in db_estimate_item_cursor:
            self.__db_estimate_item_table.delete_row(db_estimate_item_row)

        self.__db_session.flush()
        
        for idx in range(len(self.__ui.items_list)): 
            self.__ui.item_line_to_elements(idx)
            
            db_estimate_item_row = self.__db_estimate_item_table.new_row()
            
            db_estimate_item_row.name = self.__ui.draft_number + f"{idx:04d}"
            db_estimate_item_row.parent = self.__ui.draft_number
            db_estimate_item_row.item = self.__ui.item_code
            db_estimate_item_row.item_name = self.__ui.item_name
            db_estimate_item_row.qty = self.__ui.qty
            db_estimate_item_row.standard_selling_price = self.__ui.standard_selling_price
            db_estimate_item_row.applied_selling_price = self.__ui.applied_selling_price
            db_estimate_item_row.item_discount_amount = self.__ui.item_discount_amount
            db_estimate_item_row.selling_amount = self.__ui.selling_amount
            db_estimate_item_row.cgst_tax_rate = self.__ui.cgst_tax_rate
            db_estimate_item_row.sgst_tax_rate = self.__ui.sgst_tax_rate
            db_estimate_item_row.cgst_tax_amount = self.__ui.cgst_tax_amount
            db_estimate_item_row.sgst_tax_amount = self.__ui.sgst_tax_amount
          
            self.__db_estimate_item_table.create_row(db_estimate_item_row)

        self.__db_session.commit()
    
    def delete_estimate(self):
        filter = "parent='{}'"
        db_estimate_item_cursor = self.__db_estimate_item_table.list(filter.format(self.__ui.draft_number))
        for db_estimate_item_row in db_estimate_item_cursor:
            print(db_estimate_item_row.name)
            self.__db_estimate_item_table.delete_row(db_estimate_item_row)

        self.__db_session.flush()
        
        db_estimate_row = self.__db_estimate_table.get_row(self.__ui.draft_number)
        if db_estimate_row:
            self.__db_estimate_table.delete_row(db_estimate_row)
        
        self.__db_session.commit()

    def delete_item(self, idx):            
        self.__ui.delete_item_line(idx)
        self.sum_item_list()
        if len(self.__ui.items_list) == idx:
            idx -= 1
        if idx > -1:
            self.__ui.focus_items_list_row(idx) 

    ######
    # Print Estimate into PDF file
    def print_estimate(self):
        if self.__menu_opt == 'operation':
            if not self.__ui.draft_number:
                Message('INFO', 'Plese save the estimate before printing.')
                return

        print('print:', self.__menu_opt, self.__ui.final_number)
        if self.__menu_opt == 'operation':
            if self.__ui.final_number:
                title = 'ESTIMATE'
                estimate_number = self.__ui.final_number
            else:
                title = 'ESTIMATE'
                estimate_number = self.__ui.draft_number
        else:    
            title = 'ESTIMATE'
            estimate_number = self.__ui.final_number
                
        barcode_file = 'barcode-' + self.__ui.terminal_id + '.jpeg'
        with open(barcode_file, 'wb') as f:
            Code128(estimate_number, writer=ImageWriter()).write(f)

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
                    <style>
                        .aligncenter {
                            text-align: center;
                        }
                    </style>
                    """

        print_str += """
                    <table style="width:100%">
                        <tr>
                            <td>
                                <img src="c:\\alignpos\\images\\client_logo.png" alt="al-fareeda" width="125" height="60">
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
                        {}
                    </p>            
                """.format(title)   

        print_str += """
                <p  class="aligncenter" style="font-size:14px; font-weight: bold; font-family:Courier">
                    <img src="c:\\alignpos\\{}" alt="barcode" width="125" height="60" alt="centered image">
                </p>            
                """.format(barcode_file)  

        print_str += """
                <p  style="font-size:14px; font-weight: bold; font-family:Courier">
                    Estimate No: {}<br>
                    Date: {}<br>
                </p>            
                """.format( estimate_number, 
                            self.__ui.current_date
                    )    

        print_str += """
                <p style="font-size:12px; font-family:Courier; margin: 0px;">
                    Code&nbspItem&nbsp
                    Name&nbsp&nbsp&nbsp&nbsp&nbsp
                    Qty&nbsp&nbsp&nbsp&nbsp
                    Amount
                </p>
                <hr style="width:95%;text-align:left;margin-left:0">
            """
            
        for idx in range(len(self.__ui.items_list)): 
            self.__ui.item_line_to_elements(idx)        
            print_str += """
                <p style="font-size:12px; font-family:Courier; margin: 0px;";>
                    {:^4s}&nbsp{:^10s}&nbsp&nbsp{}&nbsp&nbsp{}
                </p>
                """.format( self.__ui.item_code[5:], 
                            self.__ui.item_name[0:10].ljust(10, ' ').replace(' ', ''),
                            str(self.__ui.qty).rjust(5,'*').replace('*', '&nbsp'), 
                            str(self.__ui.item_net_amount).rjust(8,'*').replace('*', '&nbsp')
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
            """.format(str(self.__ui.net_amount).rjust(12,'*').replace('*', '&nbsp'), 
                        str(self.__ui.total_amount).rjust(12,'*').replace('*', '&nbsp'), 
                        str(self.__ui.total_cgst_amount).rjust(12,'*').replace('*', '&nbsp'), 
                        str(self.__ui.total_sgst_amount).rjust(12,'*').replace('*', '&nbsp'),
                        str(self.__ui.net_amount).rjust(12,'*').replace('*', '&nbsp'),                            
                        str(self.__ui.discount_amount).rjust(12,'*').replace('*', '&nbsp'),                            
                        str(self.__ui.roundoff_amount).rjust(12,'*').replace('*', '&nbsp')                           
                )
        print_str += """
            <p style="font-size:15px; font-family:Courier; font-weight: bold">
                Net&nbspAmt&nbsp&nbsp&nbsp:&nbsp&nbsp&nbsp&nbsp{}
            </p>
            """.format(self.__ui.estimate_amount.rjust(10,'*').replace('*', '&nbsp'))
        print_file = 'print-' + self.__ui.terminal_id + '.pdf'
        
        try:    
            pdfkit.from_string(print_str, print_file, options=options)
            os.startfile(print_file)
        except:
            pass

    
class ChangeQty:

    def __init__(self, item_line):
        self.__kb = Controller()
        
        self.__new_qty = 0
        
        self.__canvas = ChangeQtyCanvas()
        
        self.__window = sg.Window("Change Quantity", 
                        self.__canvas.layout, 
                        location=(300,250), 
                        size=(350,210), 
                        modal=True, 
                        finalize=True,
                        keep_on_top = True,
                        icon='images/favicon.ico',
                        return_keyboard_events=True,
                    )

        self.__ui = ChangeQtyUi(self.__window)

        self.__ui.item_name = item_line[2]
        self.__ui.existing_qty = item_line[4]
        
        self.handler()
        
    def handler(self):
        prev_event = '' 
        focus = None
        while True:
            event, values = self.__window.read()
            #print('change_qty_popup=', event)
            
            if self.__window.FindElementWithFocus():
                focus = self.__window.FindElementWithFocus().Key
            print('change_qty=', event, 'prev=', prev_event, 'focus:', focus)
                            
            if event == '_KEYPAD_':        
                result = self.keypad(self.__ui.new_qty)
                self.__ui.new_qty = result
                self.__ui.new_qty_f = self.__ui.new_qty
                self.__ui.focus_new_qty()

            if event in ('Exit', '_CHANGE_QTY_ESC_', 'Escape:27', sg.WIN_CLOSED):
                break             
                
            if event == '\t':
                self.__ui.new_qty_f = self.__ui.new_qty
 
            if event in ('_CHANGE_QTY_OK_', 'F12:123', '\r'):
                self.__new_qty = self.__ui.new_qty
                break

        self.__window.close()

    ######
    # Wrapper function for Keypad
    def keypad(self, current_value):
        keypad = Keypad(current_value)
        return(keypad.input_value)

    def set_new_qty(self, new_qty):
        self.__new_qty = new_qty
        
    def get_new_qty(self):
        return self.__new_qty

    new_qty = property(get_new_qty, set_new_qty)


class Discount:

    def __init__(self, item_line):
        self.__kb = Controller()
        
        self.__item_discount_amount = 0
        
        self.__canvas = DiscountCanvas()
        
        self.__window = sg.Window("Disount", 
                        self.__canvas.layout, 
                        location=(300,250), 
                        size=(350,250), 
                        modal=True, 
                        finalize=True,
                        keep_on_top = True,
                        icon='images/favicon.ico',
                        return_keyboard_events=True,
                    )

        self.__ui = DiscountUi(self.__window)

        self.__ui.item_name = item_line[2]
        self.__ui.selling_price = item_line[5]
        
        self.handler()
        
    def handler(self):
        prev_event = '' 
        focus = None
        while True:
            event, values = self.__window.read()
            #print('discount=', event)
            
            if self.__window.FindElementWithFocus():
                focus = self.__window.FindElementWithFocus().Key
            print('discount=', event, 'prev=', prev_event, 'focus:', focus)
                            
            if event == '_KEYPAD_':        
                result = self.keypad(0)
                self.__ui.item_discount_value = result
                self.__ui.item_discount_value = self.__ui.item_discount_value
                self.__ui.focus_item_discount_value()

            if event in ('Exit', '_DISCOUNT_ESC_', 'Escape:27', sg.WIN_CLOSED):
                break             
                
            if event == '\t':
                self.__ui.item_discount_value_f = self.__ui.item_discount_value
 
            if event in ('_DISCOUNT_OK_', 'F12:123', '\r'):
                if self.__ui.item_discount_option == 'Amount':
                    self.__item_discount_amount = self.__ui.item_discount_value
                else:
                    self.__item_discount_amount = round((float(self.__ui.selling_price) * float(self.__ui.item_discount_value) / 100),2)
                
                break

        self.__window.close()

    ######
    # Wrapper function for Keypad
    def keypad(self, current_value):
        keypad = Keypad(current_value)
        return(keypad.input_value)

    def set_item_discount_amount(self, item_discount_amount):
        self.__item_discount_amount = item_discount_amount
        
    def get_item_discount_amount(self):
        return self.__item_discount_amount

    item_discount_amount = property(get_item_discount_amount, set_item_discount_amount)


class EstimateList:
    def __init__(self, type, terminal_id, branch_id):    
        self.__menu_opt = type
        self.__terminal_id = terminal_id
        self.__branch_id = branch_id

        self.__draft_number = ''

        self.__db_conn = DbConn()

        db_estimate_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabEstimate)

        filter='terminal_id = {}'.format(self.__terminal_id)
        db_estimate_cursor = db_estimate_table.list(filter)

        if (len(db_estimate_cursor) == 0):
            Message('INFO', 'Estimate(s) not found')
            return
       
        kb = Controller()
        self.__kb = kb
        
        self.__canvas = EstimateListCanvas()
        self.__window = sg.Window("List Estimate",
                        self.__canvas.layout,
                        location=(100,100), 
                        size=(800,360), 
                        modal=True, 
                        finalize=True,
                        return_keyboard_events=True, 
                        icon='images/favicon.ico',
                        keep_on_top = True,                    
                    )
    
        self.__ui = EstimateListUi(self.__window)
        
        
        self.__ui.estimates_list = []

        if self.__menu_opt == 'operation':
            self.__base_query = 'select tabEstimate.name, \
tabEstimate.total_amount, \
(tabEstimate.cgst_tax_amount + tabEstimate.sgst_tax_amount) as tax_amount, \
(tabEstimate.total_amount + tabEstimate.cgst_tax_amount + tabEstimate.sgst_tax_amount) as net_amount,\
ifnull(tabEstimate.discount_amount,0) as discount_amount,\
tabEstimate.estimate_amount - ((tabEstimate.total_amount + tabEstimate.cgst_tax_amount + tabEstimate.sgst_tax_amount) - \
(ifnull(tabEstimate.discount_amount,0))) as roundoff_amount, \
tabEstimate.estimate_amount, \
(select count(*) from tabEstimate_Item where tabEstimate_Item.parent = tabEstimate.name) as line_count, \
tabCustomer.mobile_number \
from tabEstimate, tabCustomer \
where tabEstimate.customer = tabCustomer.name and tabEstimate.estimate_number is null'
            self.__order_by = ''
        else:
            self.__base_query = 'select tabEstimate.estimate_number, \
tabEstimate.total_amount, \
(tabEstimate.cgst_tax_amount + tabEstimate.sgst_tax_amount) as tax_amount, \
(tabEstimate.total_amount + tabEstimate.cgst_tax_amount + tabEstimate.sgst_tax_amount) as net_amount,\
ifnull(tabEstimate.discount_amount,0) as discount_amount,\
tabEstimate.estimate_amount - ((tabEstimate.total_amount + tabEstimate.cgst_tax_amount + tabEstimate.sgst_tax_amount) - \
(ifnull(tabEstimate.discount_amount,0))) as roundoff_amount, \
tabEstimate.estimate_amount, \
(select count(*) from tabEstimate_Item where tabEstimate_Item.parent = tabEstimate.name) as line_count, \
tabCustomer.mobile_number \
from tabEstimate, tabCustomer \
where tabEstimate.customer = tabCustomer.name and tabEstimate.estimate_number is not null'
            self.__order_by = ' order by tabEstimate.estimate_number'
            print(self.__base_query + self.__order_by)
                
        db_query = DbQuery(self.__db_conn, self.__base_query + self.__order_by)
        if  db_query.result:
            for db_row in db_query.result:
                self.__ui.draft_number = db_row[0]
                self.__ui.total_amount = db_row[1]
                self.__ui.total_tax_amount = db_row[2]
                self.__ui.net_amount = db_row[3]
                self.__ui.discount_amount = db_row[4]
                self.__ui.roundoff_amount = db_row[5]
                self.__ui.estimate_amount = db_row[6]
                self.__ui.line_items = db_row[7]
                self.__ui.mobile_number = db_row[8]
                self.__ui.add_estimate_line()

        self.__ui.estimate_idx = 0
        self.__ui.focus_estimates_list()
       
        self.handler()


    def handler(self):  
        prev_event = ''
        prev_values = ''
        
        while True:
            event, values = self.__window.read()
            #print('estimate_list=', event, prev_event, values)
            print('estimate_list=', event, prev_event)
            if event in ("Exit", '_ESTIMATE_LIST_ESC_', 'Escape:27') or event == sg.WIN_CLOSED:
                break

            if event in ('_ESTIMATE_LIST_SEARCH_', 'F11', 'F11:122'):
                this_query = ''
                if self.__ui.draft_number_search:
                    if not self.__ui.draft_number_search == '':
                        this_query = ' and tabEstimate.name = "' + self.__ui.draft_number_search + '"'
                if self.__ui.mobile_number_search:
                    if not self.__ui.mobile_number_search == '':
                        this_query = ' and tabCustomer.mobile_number = "' + self.__ui.mobile_number_search + '"'
                new_query = self.__base_query + this_query + self.__order_by
                print('query:', self.__base_query + this_query + self.__order_by)
                db_query = DbQuery(self.__db_conn, self.__base_query + this_query + self.__order_by)     
                if  db_query.result:
                    self.__ui.estimates_list = [] 
                    self.__ui.clear_estimates_list()                   
                    for db_row in db_query.result:
                        self.__ui.draft_number = db_row[0]
                        self.__ui.total_amount = db_row[1]
                        self.__ui.total_tax_amount = db_row[2]
                        self.__ui.net_amount = db_row[3]
                        self.__ui.discount_amount = db_row[4]
                        self.__ui.roundoff_amount = db_row[5]
                        self.__ui.estimate_amount = db_row[6]
                        self.__ui.line_items = db_row[7]
                        self.__ui.mobile_number = db_row[8]
                        self.__ui.add_estimate_line()

            if event in ('_ESTIMATE_LIST_OK_', '\r', 'F12', 'F12:123'):
                if len(self.__ui.estimates_list) > 0:
                    estimate_idx = values['_ESTIMATES_LIST_'][0]
                    self.__ui.estimate_line_to_elements(estimate_idx)
                    self.__draft_number = self.__ui.draft_number
                else:
                    self.__draft_number = ''                
                break
            if event not in ('\t', 'Up:38', 'Down:40', 'UP', 'DOWN'):               
                prev_event = event
            prev_values = values
           
        self.__db_conn.close()           
        self.__window.close()    

      
    def get_estimate_number(self):
        return self.__draft_number

    
    estimate_number = property(get_estimate_number)  


class Payment:

    def __init__(self, input_param):
        self.__final_number = ''
        self.__output_param = dict()
        self.__draft_number = input_param['estimate_number'] 
        self.__mobile_number = input_param['mobile_number'] 
        self.__customer_number = input_param['customer_number']
        self.__customer_name = input_param['customer_name']
        self.__customer_address = input_param['customer_address']        
        self.__net_amount = input_param['net_amount'] 
        
        self.__discount_amount = 0
        self.__paid_amount = 0

        self.__kb = Controller()

        self.__db_conn = DbConn()
        self.__db_session = self.__db_conn.session
        self.__db_customer_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabCustomer)
        self.__db_estimate_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabEstimate)
        
        
        self.__canvas = PaymentCanvas()
        
        self.__window = sg.Window("Payment", 
                        self.__canvas.layout, 
                        location=(400,40), 
                        size=(500,250), 
                        modal=True, 
                        finalize=True,
                        keep_on_top = True,
                        icon='images/favicon.ico',
                        return_keyboard_events=True,
                    )

        self.__ui = PaymentUi(self.__window)

        self.initialize_payment_elements()    
        
        self.handler()
        self.__window.close()
        
    def handler(self):
        prev_event = '' 
        focus = None
        while True:
            event, values = self.__window.read()
            if event in ('\t', 'TAB') and prev_event == '_MOBILE_NUMBER_':
                if not self.__ui.mobile_number == '':
                    self.process_mobile_number()

            if event == '_MOBILE_NUMBER_' and len(self.__ui.mobile_number) > 9:
                self.process_mobile_number()

            if event in ('\t', 'TAB') and prev_event == '_DISCOUNT_AMOUNT_':
                self.__ui.discount_amount = self.__ui.discount_amount       
                self.__ui.discount_amount_hd = self.__ui.discount_amount
                self.__ui.cash_amount = 0
                self.__ui.cash_return = 0            
                self.set_payment_elements()
                                
            if event in ("Exit", '_PAYMENT_ESC_', 'Escape:27') or event == sg.WIN_CLOSED:
                break
                
            if event == "_PAYMENT_OK_" or event == "F12:123":
                self.set_payment_elements()
                self.generate_estimate_number()
                self.set_output_parameters()
                self.update_estimate()
                msg = 'Estimate ' + str(self.__final_number) + ' processed'
                Message('INFO', msg)
                break
                                
            prev_event = event

    def initialize_payment_elements(self):
        self.__ui.mobile_number = self.__mobile_number        
        self.__ui.customer_name = self.__customer_name
        self.__ui.mobile_number_header = self.__mobile_number
        self.__ui.customer_name_header = self.__customer_name
        self.__ui.customer_number = self.__customer_number
        self.__ui.customer_address = self.__customer_address
        self.__ui.net_amount = self.__net_amount
        self.__ui.discount_amount = 0
        estimate_actual_amount = float(self.__ui.net_amount) - float(self.__ui.discount_amount)
        estimate_rounded_amount = round(estimate_actual_amount, 0)
        self.__ui.estimate_amount = estimate_rounded_amount
        self.__ui.roundoff_adjustment = estimate_rounded_amount - estimate_actual_amount
        

    def process_mobile_number(self):    
        filter = "mobile_number='{}'"
        db_customer_row = self.__db_customer_table.first(filter.format(self.__ui.mobile_number))
        if db_customer_row:
            self.__ui.customer_number = db_customer_row.name
            self.__ui.customer_name = db_customer_row.customer_name
            self.__ui.customer_address = db_customer_row.address
            self.__ui.mobile_number_header = db_customer_row.mobile_number
            self.__ui.customer_name_header = db_customer_row.customer_name
            self.__mobile_number = db_customer_row.mobile_number
            self.__customer_number = db_customer_row.name
            self.__customer_name = db_customer_row.customer_name
            self.__customer_address = db_customer_row.address

    def set_payment_elements(self):
        if not self.__ui.discount_amount or self.__ui.discount_amount == '':
           self.__ui.discount_amount = 0
     
        self.__discount_amount = float(self.__ui.discount_amount)
     
        estimate_actual_amount = float(self.__ui.net_amount) - float(self.__ui.discount_amount)
        estimate_rounded_amount = round(estimate_actual_amount, 0)
        self.__ui.estimate_amount = estimate_rounded_amount
        self.__ui.roundoff_adjustment = estimate_rounded_amount - estimate_actual_amount

    def generate_estimate_number(self):
        self.__final_number = self.__draft_number

    def set_output_parameters(self):
        self.__output_param['final_number'] = self.__final_number
        self.__output_param['customer_number'] = self.__ui.customer_number
        self.__output_param['mobile_number'] = self.__ui.mobile_number
        self.__output_param['customer_name'] = self.__ui.customer_name
        self.__output_param['customer_address'] = self.__ui.customer_address        
        self.__output_param['estimate_amount'] = float(self.__ui.estimate_amount)
        self.__output_param['roundoff_adjustment'] = float(self.__ui.roundoff_adjustment)
        self.__output_param['discount_amount'] = float(self.__ui.discount_amount)

    def update_estimate(self):
        db_estimate_row = self.__db_estimate_table.get_row(self.__draft_number)

        if not db_estimate_row:
            return
            
        db_estimate_row.estimate_number = self.__final_number
        db_estimate_row.customer = self.__ui.customer_number
        db_estimate_row.discount_amount = self.__ui.discount_amount
        db_estimate_row.estimate_amount = self.__ui.estimate_amount
        
        self.__db_session.commit()


    def get_output_param(self):
        return self.__output_param

    
    output_param = property(get_output_param)  
