import PySimpleGUI as sg
from pynput.keyboard import Key, Controller
from datetime import datetime

from config import Config
from utilities import Message, Keypad
from db_nosql import KvDatabase
from db_orm import DbConn, DbTable, DbQuery
from day_end_layout import DayEndCanvas
from day_end_ui import DayEndUi

   
class DayEnd():

    def __init__(self, user_id, terminal_id, branch_id):
    
        config = Config()
        
        self.__terminal_id = terminal_id
        self.__branch_id = branch_id
              
        self.__kv_settings = KvDatabase('kv_settings')
        self.__kv_strings = KvDatabase('kv_strings')
      
        kb = Controller()
        self.__kb = kb
              
        self.__db_conn = DbConn()
        self.__db_session = self.__db_conn.session

        self.__db_branch_table = DbTable(self.__db_conn, self.__db_conn.base.classes.tabBranch)
        db_branch_row = self.__db_branch_table.get_row(self.__branch_id)
        if db_branch_row:
            self.__current_date = db_branch_row.current_date
            self.__current_status = db_branch_row.current_status
        
        self.__canvas = DayEndCanvas()
        
        self.__window = sg.Window("Day End", 
                        self.__canvas.layout, 
                        location=(300,250), 
                        size=(315,160), 
                        modal=True, 
                        finalize=True,
                        keep_on_top = True,
                        icon='images/favicon.ico',
                        return_keyboard_events=True,
                    )

        self.__ui = DayEndUi(self.__window)

        #self.__ui.current_date = datetime.strptime(self.__current_date, "%Y-%m-%d").strftime("%d-%m-%Y")
        self.__ui.current_date = self.__current_date
        self.__ui.current_status = self.__current_status
        
        self.handler()

        
    def handler(self):
        prev_event = '' 
        focus = None
        while True:
            event, values = self.__window.read()
            #print('day_end_popup=', event)
            
            if self.__window.FindElementWithFocus():
                focus = self.__window.FindElementWithFocus().Key
            print('day_end=', event, 'prev=', prev_event, 'focus:', focus)
                            
            if event in ('Exit', '_DAY_END_ESC_', 'Escape:27', sg.WIN_CLOSED):
                break             
                
            if event in ('_DAY_END_OK_', 'F12:123', '\r'):
            
                break

        self.__window.close()

    def validate_cash_balance(self):
        total_query = 'select IFNULL(sum(receipt_amount),0) received_amount from \
        tabCash_Transaction ct where ct.terminal_id = "' + self.__terminal_id + '"'

        db_query = DbQuery(self.__db_conn, total_query + self.__this_query)        
        if  db_query.result:
            for db_row in db_query.result:
                if db_row[0] == None:
                    received_amount = 0
                else:
                    received_amount = float(db_row[0])
       
        total_query = 'select IFNULL(sum(payment_amount),0) paid_amount from \
        tabCash_Transaction ct where ct.terminal_id = "' + self.__terminal_id + '"'

        db_query = DbQuery(self.__db_conn, total_query + self.__this_query)        
        if  db_query.result:
            for db_row in db_query.result:
                if db_row[0] == None:
                    paid_amount = 0
                else:
                    paid_amount = float(db_row[0])
        
        self.__ui.balance_amount = float(received_amount) - float(paid_amount)


