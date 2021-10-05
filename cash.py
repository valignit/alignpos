import os
import PySimpleGUI as sg
import json
from pynput.keyboard import Key, Controller

from config import Config
from utilities import Message, Keypad
from db_orm import DbConn, DbTable, DbQuery
from cash_layout import CashCanvas
from cash_ui import CashUi
from common import ItemList, CustomerList, Denomination


class Cash:
    def __init__(self, menu_opt, user_id, terminal_id, branch_id):    
        self.__terminal_id = terminal_id
        self.__branch_id = branch_id

        self.__name = ''

        self.__db_conn = DbConn()

        self.__db_cash_transaction_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabCash_Transaction)
        filter=''
        db_cash_transaction_cursor = self.__db_cash_transaction_table.list(filter)

        if (len(db_cash_transaction_cursor) == 0):
            sg.popup('Transaction(s) not found', keep_on_top = True, icon='images/INFO.png')                    
            return

        self.__db_cash_transaction_denomination_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabCash_Transaction_Denomination)
       
        kb = Controller()
        self.__kb = kb
        
        self.__canvas = CashCanvas()

        title = 'Cash'

        self.__window = sg.Window(title, 
                        self.__canvas.layout,
                        font='Helvetica 11', 
                        finalize=True, 
                        location=(50,50), 
                        size=(1000,630), 
                        keep_on_top=False, 
                        resizable=False,
                        return_keyboard_events=True, 
                        use_default_focus=False,
                        icon='images/favicon.ico',
                        modal=True
                    )
    
        self.__ui = CashUi(self.__window)
                
        self.__ui.cashs_list = []
        self._empty_list = []

        self.__base_query = 'select tabCash_Transaction.name, \
        tabCash_Transaction.transaction_type, \
        tabCash_Transaction.transaction_context, \
        tabCash_Transaction.transaction_reference, \
        tabCash_Transaction.receipt_amount, \
        tabCash_Transaction.payment_amount \
        from tabCash_Transaction \
        where tabCash_Transaction.branch_id = "' + self.__branch_id + '" and tabCash_Transaction.terminal_id = "' + self.__terminal_id + '"'

        self.__order_query = 'order by tabCash_Transaction.name  DESC '

        
        db_query = DbQuery(self.__db_conn, self.__base_query + self.__order_query)        
        if  db_query.result:
            self.__ui.cashs_list.clear()
            for db_row in db_query.result:
                self.__ui.name = db_row[0]
                self.__ui.transaction_type = db_row[1]
                self.__ui.transaction_context = db_row[2]
                self.__ui.transaction_reference = db_row[3]
                self.__ui.receipt_amount = db_row[4]
                self.__ui.payment_amount = db_row[5]
                self.__ui.balance = 0
                self.__ui.add_cash_line()

        self.__ui.cash_idx = 0
        self.__ui.focus_cash_list()
       
        self.handler()


    def handler(self):  
        prev_event = ''
        prev_values = ''
        
        while True:
            event, values = self.__window.read()
            #print('customer_list=', event, prev_event, values)
            if event in ("Exit", '_CASH_LIST_ESC_', 'Escape:27') or event == sg.WIN_CLOSED:
                break

            if event in ('_CASH_LIST_SEARCH_', 'F11', 'F11:122'):
                this_query = ''
                if self.__ui.transaction_type_search:
                    if not self.__ui.transaction_type_search == '':
                        this_query += ' and tabCash_Transaction.transaction_type = "' + self.__ui.transaction_type_search + '"'

                if self.__ui.transaction_context_search:
                    if not self.__ui.transaction_context_search == '':
                        this_query += ' and tabCash_Transaction.transaction_context = "' + self.__ui.transaction_context_search + '"'

                self.__ui.cashs_list = []
                        
                db_query = DbQuery(self.__db_conn, self.__base_query + this_query + self.__order_query)
                if  db_query.result:
                    
                    for db_row in db_query.result:
                        self.__ui.name = db_row[0]
                        self.__ui.transaction_type = db_row[1]
                        self.__ui.transaction_context = db_row[2]
                        self.__ui.transaction_reference = db_row[3]
                        self.__ui.receipt_amount = db_row[4]
                        self.__ui.payment_amount = db_row[5]
                        self.__ui.balance = 0
                        self.__ui.add_cash_line()
                    
            if event in ('_CASH_LIST_DENOMINATION_', '\r', 'F3', 'F3:114'):
                cash_idx = values['_CASH_LIST_'][0]
                self.__ui.cash_line_to_elements(cash_idx)
                self.__name = self.__ui.name
                #print('Den:', self.__name)
                
                default_amount_dict = dict()
    
                filter = "parent='{}'"
                db_cash_transaction_denomination_cursor = self.__db_cash_transaction_denomination_table.list(filter.format(self.__name))
                for db_cash_transaction_denomination_row in db_cash_transaction_denomination_cursor:
                    #print(db_cash_transaction_denomination_row.denomination, db_cash_transaction_denomination_row.count)
                    default_amount_dict[db_cash_transaction_denomination_row.denomination] = db_cash_transaction_denomination_row.count
                
                self.denomination(default_amount_dict, 'view')
                        
            if event not in ('\t', 'Up:38', 'Down:40', 'UP', 'DOWN'):               
                prev_event = event
            prev_values = values
           
        self.__db_conn.close()           
        self.__window.close()    

      
    ######
    # Wrapper function for Denomination
    def denomination(self, amount, mode):
        denomination = Denomination(amount, mode)
        return denomination.denomination_count_dict


    def get_name(self):
        return self.__name

    
    name = property(get_name)


