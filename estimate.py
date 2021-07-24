import PySimpleGUI as sg
from pynput.keyboard import Key, Controller

from alignpos_db import DbConn, DbTable, DbQuery

from estimate_layout import EstimateCanvas, ChangeQtyCanvas
from estimate_ui import EstimateUi, ChangeQtyUi
from common import ItemLookup, ConfirmMessage as confirm_message


class Estimate():

    def __init__(self):

        w, h = sg.Window.get_screen_size()
        
        kb = Controller()
    
        self.__canvas = EstimateCanvas()
        
        self.__window = sg.Window('Estimate', 
                        self.__canvas.layout,
                        font='Helvetica 11', 
                        finalize=True, 
                        location=(0,0), 
                        size=(w,h),
                        keep_on_top=False, 
                        resizable=False,
                        return_keyboard_events=True, 
                        use_default_focus=False,
                        modal=True
                    )

        self.__window.maximize()
        
        self.__window['_LEFT_PANES_'].Widget.configure(borderwidth=1, relief=sg.DEFAULT_FRAME_RELIEF)
        self.__window['_RIGHT_PANES_'].Widget.configure(borderwidth=1, relief=sg.DEFAULT_FRAME_RELIEF)
        self.__window['_BARCODE_'].bind('<FocusIn>', '+CLICK+')
        self.__window['_SEARCH_NAME_'].bind('<FocusIn>', '+CLICK+')

        self.__ui = EstimateUi(self.__window)

        self.__db_conn = DbConn()
        self.__db_customer_table = DbTable(self.__db_conn, 'tabCustomer')
        self.__db_item_table = DbTable(self.__db_conn, 'tabItem')
        self.__db_estimate_table = DbTable(self.__db_conn, 'tabEstimate')
        self.__db_estimate_item_table = DbTable(self.__db_conn, 'tabEstimate_Item')

        self.__kb = kb
        
        self.initialize_ui()
        self.goto_last_row()               
        self.__ui.focus_barcode()        

        self.handler()


    def handler(self):
        prev_event = '' 
        focus = None    
        while True:
            event, values = self.__window.read()
            print('est:', event)
            
            if self.__window.FindElementWithFocus():
                focus = self.__window.FindElementWithFocus().Key
                
            #print('window=', event, 'prev=', prev_event, 'focus=', focus)

            if event == sg.WIN_CLOSED:
                break

            if event == 'Escape:27':
                break

            if event == 'ENTER':        
                self.__kb.press(Key.enter)
                self.__kb.release(Key.enter)
                
            if event == 'ESC':
                self.__kb.press(Key.esc)
                self.__kb.release(Key.esc)
                
            if event == 'TAB':        
                self.__kb.press(Key.tab)
                self.__kb.release(Key.tab)
                
            if event == 'DEL':
                self.__kb.press(Key.delete)
                self.__kb.release(Key.delete)
                
            if event == 'UP':        
                self.__kb.press(Key.up)
                self.__kb.release(Key.up)
                
            if event == 'DOWN':
                self.__kb.press(Key.down)
                self.__kb.release(Key.down)
                
            if event == 'RIGHT':
                self.__kb.press(Key.right)
                self.__kb.release(Key.right)
                
            if event == 'LEFT':
                self.__kb.press(Key.left)
                self.__kb.release(Key.left)
                
            if event == 'BACKSPACE':
                self.__kb.press(Key.backspace)
                self.__kb.release(Key.backspace)
                
            if event == '+CLICK+':
                self.initialize_action_pane()
               
            if event in ('\t') and prev_event == '_SEARCH_NAME_':
                self.__ui.focus_items_list()

            if focus == '_ITEMS_LIST_':
                if len(self.__ui.items_list) > 0:
                    self.initialize_action_pane()
                else:
                    self.__ui.focus_barcode()        
            else:
                self.initialize_action_pane()
                self.__ui.items_list = self.__ui.items_list

            if event in ('Prior:33', '_BEGIN_'):
                self.goto_first_row()

            if event in ('Left:37', '_PREVIOUS_'):
                self.goto_previous_row()
                
            if event in ('Right:39', '_NEXT_'):
                self.goto_next_row()

            if event in ('Next:34', '_END_'):
                self.goto_last_row()

            if event in ('F1:112', 'F1'):        
                confirm_test = confirm_message('OK_CANCEL', self.item_lookup('', 100,100))

            if event in ('F2:113', 'F2'):        
                confirm_test = confirm_message('OK_CANCEL', 'Called from Estimate F2 event')

            if event in ('F3:114', 'F3'):
                item_idx = values['_ITEMS_LIST_'][0]
                new_qty = self.change_qty(self.__ui.items_list[item_idx])
                self.process_change_qty(new_qty, item_idx)
                self.__ui.focus_barcode()        
                
            if event in ('F4:115', 'F4'):
                item_idx = values['_ITEMS_LIST_'][0]
                self.process_weight(item_idx)
                self.sum_item_list()
                self.__ui.focus_barcode()        

            if event == 'v:86' and focus == '_BARCODE_':
                self.process_barcode(self.__ui.barcode)
                self.initialize_search_pane()

            if event in ('T1','T2','T3','T4','T5','T6','T7','T8','T9','T0') and focus == '_BARCODE_':
                inp_val = self.__ui.barcode
                inp_val += event[1]
                self.__ui.barcode = inp_val
                if (self.__ui.barcode[0].isnumeric() and len(self.__ui.barcode) > 12) or \
                   (self.__ui.barcode[0] == 'I' and len(self.__ui.barcode) > 8) or \
                   (self.__ui.barcode[0] == 'E' and len(self.__ui.barcode) > 8):
                    self.process_barcode(self.__ui.barcode)
                    self.initialize_search_pane()
                    
            if event in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0') and focus == '_BARCODE_':
                if self.__ui.barcode:
                    if (self.__ui.barcode[0].isnumeric() and len(self.__ui.barcode) > 12) or \
                       (self.__ui.barcode[0] == 'I' and len(self.__ui.barcode) > 8) or \
                       (self.__ui.barcode[0] == 'E' and len(self.__ui.barcode) > 8):
                        self.process_barcode(self.__ui.barcode)
                        self.initialize_search_pane()

            if event.isalnum() and focus == '_SEARCH_NAME_':
                print(self.__ui.search_name, len(self.__ui.search_name))
                if len(self.__ui.search_name) > 2:
                    filter = "upper(item_name) like upper('%{}%')".format(self.__ui.search_name)
                    item_code = self.item_lookup(filter, 385, 202)
                    self.initialize_search_pane()
                
            if event == 'Exit':
                break

            if event not in ('\t', 'Up:38', 'Down:40', 'UP', 'DOWN', 'DEL', 'Delete:46', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
                prev_event = event

        self.__db_conn.close()
        self.__window.close()
       
    
    ######
    # Wrapper function for Item Lookup
    def item_lookup(self, filter, lin, col):
        item_lookup = ItemLookup(filter, lin, col)
        return item_lookup.item_code


    ######
    # Wrapper function for Change Qty
    #      whole line is sent as parameter so that item_name and old_qty also can be used
    def change_qty(self, item_line):
        change_qty = ChangeQty(item_line)
        return(change_qty.new_qty)


    def initialize_header_pane(self):
        self.__ui.estimate_number = ''
        self.__ui.payment_status = ''
        self.__ui.mobile_number = '0000000000'
        self.__ui.customer_number = ''
        self.__ui.customer_name = ''
        self.__ui.customer_address = ''
 
 
    def initialize_search_pane(self):
        self.__ui.barcode = ''
        self.__ui.item_name = ''


    def initialize_detail_pane(self):
        self.__ui.items_list = []
        self.__ui.item_code = str('')
        self.__ui.barcode = str('')
        self.__ui.item_name = str('')
        self.__ui.uom = str('')
        self.__ui.qty = float(0.0)
        self.__ui.selling_price = float(0.00)
        self.__ui.selling_amount = float(0.00)
        self.__ui.tax_rate = float(0.00)
        self.__ui.tax_amount = float(0.00)
        self.__ui.net_amount = float(0.00)
        self.__ui.cgst_tax_rate = float(0.00)
        self.__ui.sgst_tax_rate = float(0.00)
        self.__ui.item_line = [] 


    def initialize_action_pane(self):
        self.__window.Element('F1').update(text='New\nF1')    
        self.__window.Element('F2').update(text='Specs\nF2')
        self.__window.Element('F3').update(text='Quantity\nF3')
        self.__window.Element('F4').update(text='Weight\nF4')
        self.__window.Element('F5').update(text='Price\nF5')
        self.__window.Element('F6').update(text='Save\nF6')
        self.__window.Element('F7').update(text='Delete\nF7')
        self.__window.Element('F8').update(text='Submit\nF8')
        self.__window.Element('F9').update(text='Print\nF9')


    def initialize_footer_pane(self):
        self.__ui.user_id = 'XXX'
        self.__ui.terminal_id = '101'
        self.__ui.current_date = '2021/06/13'


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
    

    def goto_first_row(self):
        db_estimate_row = self.__db_estimate_table.first('')
        if db_estimate_row:
            self.clear_ui()    
            self.show_ui(db_estimate_row)    


    def goto_previous_row(self):
        if self.__ui.estimate_number:
            name = self.__ui.estimate_number
            filter = "name < '{}'"
            db_estimate_row = self.__db_estimate_table.last(filter.format(name))
            if db_estimate_row:
                self.clear_ui()    
                self.show_ui(db_estimate_row)


    def goto_next_row(self):
        if self.__ui.estimate_number:
            name = self.__ui.estimate_number
            filter = "name > '{}'"
            db_estimate_row = self.__db_estimate_table.first(filter.format(name))
            if db_estimate_row:
                self.clear_ui()    
                self.show_ui(db_estimate_row)


    def goto_last_row(self):
        db_estimate_row = self.__db_estimate_table.last('')
        if db_estimate_row:
            self.clear_ui()
            self.show_ui(db_estimate_row)


    def show_ui(self, db_estimate_row):
        if not db_estimate_row:
            return
            
        self.__ui.estimate_number = db_estimate_row.name

        customer_number = db_estimate_row.customer
        db_customer_row = self.__db_customer_table.get_row(customer_number)
        if db_customer_row:
            self.__ui.mobile_number = db_customer_row.mobile_number
            self.__ui.customer_number = db_customer_row.name
            self.__ui.customer_name = db_customer_row.customer_name
            self.__ui.customer_address = db_customer_row.address

        self.__ui.item_line = []
        filter = "parent='{}'"
        db_estimate_item_cursor = self.__db_estimate_item_table.list(filter.format(self.__ui.estimate_number))    
        for db_estimate_item_row in db_estimate_item_cursor:
            self.move_db_estimate_item_to_ui_detail_pane(db_estimate_item_row)
        self.sum_item_list()
        if (db_estimate_row.discount_amount):
            self.__ui.discount_amount = db_estimate_row.discount_amount
        else:
            self.__ui.discount_amount = 0.00       
        self.__ui.estimate_amount = db_estimate_row.estimate_amount


    def move_db_item_to_ui_detail_pane(self, db_item_row):
        self.__ui.item_code = db_item_row.name
        self.__ui.item_barcode = db_item_row.barcode
        self.__ui.item_name = db_item_row.item_name
        self.__ui.uom = db_item_row.uom
        self.__ui.qty = 1
        self.__ui.selling_price = db_item_row.selling_price
        self.__ui.cgst_tax_rate = db_item_row.cgst_tax_rate
        self.__ui.sgst_tax_rate = db_item_row.sgst_tax_rate
        self.__ui.selling_amount = float(self.__ui.qty) * float(self.__ui.selling_price)
        self.__ui.tax_rate = float(self.__ui.cgst_tax_rate) + float(self.__ui.sgst_tax_rate)
        tax_amount = float(self.__ui.selling_amount) * float(self.__ui.tax_rate) / 100
        self.__ui.tax_amount = round(tax_amount, 2)
        self.__ui.item_net_amount = float(self.__ui.selling_amount) + float(self.__ui.tax_amount)
        
        self.__ui.add_item_line()    

 
    def move_db_estimate_item_to_ui_detail_pane(self, db_estimate_item_row):
        self.__ui.item_code = db_estimate_item_row.item
        
        db_item_row = self.__db_item_table.get_row(db_estimate_item_row.item)
        if db_item_row:
            self.__ui.item_barcode = db_item_row.barcode
            self.__ui.item_name = db_item_row.item_name
            self.__ui.uom = db_item_row.uom
            self.__ui.selling_price = db_item_row.selling_price

        self.__ui.qty = db_estimate_item_row.qty
        self.__ui.cgst_tax_rate = db_estimate_item_row.cgst_tax_rate
        self.__ui.sgst_tax_rate = db_estimate_item_row.sgst_tax_rate
        self.__ui.selling_amount = float(self.__ui.qty) * float(self.__ui.selling_price)
        self.__ui.tax_rate = float(self.__ui.cgst_tax_rate) + float(self.__ui.sgst_tax_rate)
        self.__ui.tax_amount = float(self.__ui.selling_amount) * float(self.__ui.tax_rate) / 100
        self.__ui.item_net_amount = float(self.__ui.selling_amount) + float(self.__ui.tax_amount)
        
        self.__ui.add_item_line()    


    def sum_item_list(self):
        line_items = 0
        total_amount = 0.00
        total_tax_amount = 0.00
        total_cgst_amount = 0.00
        total_sgst_amount = 0.00
        net_amount = 0.00
       
        for item_line in self.__ui.items_list:
            self.__ui.item_line_to_elements(line_items)
            total_amount += float(self.__ui.selling_amount)
            total_tax_amount += float(self.__ui.tax_amount)
            net_amount += float(self.__ui.item_net_amount)
            cgst_rate = float(self.__ui.cgst_tax_rate)
            sgst_rate = float(self.__ui.sgst_tax_rate)
            cgst_amount = float(self.__ui.selling_amount) * cgst_rate / 100
            sgst_amount = float(self.__ui.selling_amount) * sgst_rate / 100       
            total_cgst_amount += cgst_amount
            total_sgst_amount += sgst_amount
            line_items += 1

        self.__ui.line_items = line_items
        self.__ui.total_amount = total_amount
        self.__ui.total_tax_amount = total_tax_amount
        self.__ui.net_amount = net_amount
        self.__ui.total_cgst_amount = total_cgst_amount
        self.__ui.total_sgst_amount = total_sgst_amount
        #estimate_actual_amount = net_amount - float(self.__ui.discount_amount)
        estimate_actual_amount = net_amount
        estimate_rounded_amount = round(net_amount, 0)
        self.__ui.estimate_amount = estimate_rounded_amount
        self.__ui.roundoff_amount = estimate_rounded_amount - estimate_actual_amount    


    def process_change_qty(self, new_qty, item_idx):
        print('here1')
        if float(new_qty) > 0:
            print('here2')
            self.__ui.qty = new_qty
            self.__ui.selling_amount = float(self.__ui.qty) * float(self.__ui.selling_price)
            self.__ui.tax_rate = float(self.__ui.cgst_tax_rate) + float(self.__ui.sgst_tax_rate)
            self.__ui.tax_amount = float(self.__ui.selling_amount) * float(self.__ui.tax_rate) / 100
            self.__ui.item_net_amount = float(self.__ui.selling_amount) + float(self.__ui.tax_amount)
            self.__ui.update_item_line(item_idx) 
            self.sum_item_list()
       

    def process_weight(self, idx):
        self.__ui.item_line_to_elements(idx)
        if self.__ui.uom == 'Kg':          
            self.__ui.qty = 0.35
            self.__ui.selling_amount = float(self.__ui.qty) * float(self.__ui.selling_price)
            self.__ui.tax_rate = float(self.__ui.cgst_tax_rate) + float(self.__ui.sgst_tax_rate)
            self.__ui.tax_amount = float(self.__ui.selling_amount) * float(self.__ui.tax_rate) / 100
            self.__ui.item_net_amount = float(self.__ui.selling_amount) + float(self.__ui.tax_amount)
            self.__ui.update_item_line(idx)
            self.sum_item_list()
        else:
            sg.popup('Not applicable to this UOM', keep_on_top = True)         


    def process_barcode(self, barcode):
        if not barcode:
            return
             
        if (self.__ui.barcode[0].isnumeric() and len(self.__ui.barcode) > 12):
            filter = "barcode='{}'"
            db_item_row = self.__db_item_table.first(filter.format(barcode))
            if db_item_row:
                self.move_db_item_to_ui_detail_pane(db_item_row)       
        elif (self.__ui.barcode[0] == 'I' and len(self.__ui.barcode) > 8):
            filter = "item_code='{}'"   
            db_item_row = self.__db_item_table.first(filter.format(barcode))
            if db_item_row:
                self.move_db_item_to_ui_detail_pane(db_item_row)
        else:
            return
        print('here')    
        self.sum_item_list()


class ChangeQty:

    def __init__(self, item_line):

        self.__kb = Controller()
        
        self.__canvas = ChangeQtyCanvas()
        
        self.__window = sg.Window("Change Quantity", 
                        self.__canvas.layout, 
                        location=(300,250), 
                        size=(530,280), 
                        modal=True, 
                        finalize=True,
                        keep_on_top = True,
                        return_keyboard_events=True
                    )

        self.__ui = ChangeQtyUi(self.__window)

        self.__ui.item_line = item_line

        self.__ui.item_name = self.__ui.item_line[2]
        self.__ui.existing_qty = self.__ui.item_line[4]
        self.__ui.new_qty_f = 0.00
        self.__ui.focus_new_qty()
        self.__new_qty = 0.00
        
        self.handler()
        

    def handler(self):
        prev_event = '' 
        focus = None
        while True:
            event, values = self.__window.read()
            #print('change_qty_popup=', event)
            
            if self.__window.FindElementWithFocus():
                focus = self.__window.FindElementWithFocus().Key
            print('eventc=', event, 'prev=', prev_event, 'focus:', focus)
            
            if event == 'ENTER':        
                self.__kb.press(Key.enter)
                self.__kb.release(Key.enter)
                
            if event == 'TAB':        
                self.__kb.press(Key.tab)
                self.__kb.release(Key.tab)
                
            if event == 'DEL':
                self.__kb.press(Key.delete)
                self.__kb.release(Key.delete)
                
            if event == 'BACKSPACE':
                self.__kb.press(Key.backspace)
                self.__kb.release(Key.backspace)
                
            if event in ('Exit', '_CHANGE_QTY_ESC_', 'Escape:27', sg.WIN_CLOSED):
                break             
                
            if event in ('T1','T2','T3','T4','T5','T6','T7','T8','T9','T0'):
                if focus == '_NEW_QTY_':
                    self.__ui.append_char('_NEW_QTY_', event[1])
              
            if event == '\t':
                if focus == '_NEW_QTY_':     
                    self.__ui.new_qty_f = self.__ui.new_qty
                    self.__ui.focus_new_qty()       

            if event in ('_CHANGE_QTY_OK_', 'F12:123', '\r'):
                self.__new_qty = self.__ui.new_qty
                break

        self.__window.close()

    def set_new_qty(self, new_qty):
        self.__new_qty = new_qty
        
    def get_new_qty(self):
        return self.__new_qty

    new_qty = property(get_new_qty, set_new_qty)
        


     