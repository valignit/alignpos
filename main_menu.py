import PySimpleGUI as sg
import json
from subprocess import run

from db_nosql import KvDatabase
from main_menu_layout import MainMenuCanvas
from main_menu_ui import MainMenuUi
from estimate import Estimate
from invoice import Invoice
from cash import Cash

sg.theme('DefaultNoMoreNagging')


class MainMenu():   
    
    def __init__(self, user_id, terminal_id, branch_id, current_date):
        self.__user_id = user_id
        self.__terminal_id = terminal_id
        self.__branch_id = branch_id
        self.__current_date = current_date

        self.__kv_settings = KvDatabase('kv_settings')
        self.__kv_strings = KvDatabase('kv_strings')

        self.__welcome_text = self.__kv_settings.get('welcome_text')   
                
        w, h = sg.Window.get_screen_size()
        
        self.__canvas = MainMenuCanvas(w, h)
               
        self.__window = sg.Window('Alignpos Menu', 
                        self.__canvas.layout, 
                        font='Helvetica 11', 
                        finalize=True, 
                        location=(0,0), 
                        size=(w,h), 
                        keep_on_top=False, 
                        resizable=False,
                        return_keyboard_events=True, 
                        icon='c:/alignpos/images/favicon.ico',
                        use_default_focus=False,
                 )        
     
        self.__window.maximize()
        self.__window['_LEFT_PANES_'].Widget.configure(borderwidth=1, relief=sg.DEFAULT_FRAME_RELIEF)
        self.__window['_RIGHT_PANES_'].Widget.configure(borderwidth=1, relief=sg.DEFAULT_FRAME_RELIEF)
          
        self.__ui = MainMenuUi(self.__window)
        
        self.initialize_ui()

        self.handler()

    def handler(self):
        prev_event = '' 
        focus = None    
        while True:
            event, values = self.__window.read()
            if self.__window.FindElementWithFocus():
                focus = self.__window.FindElementWithFocus().Key
                
            #print('window=', event, 'prev=', prev_event, 'focus=', focus)

            if event == sg.WIN_CLOSED:
                self.__window.close()
                break

            if event == 'Escape:27':
                self.__window.close()
                break
                
            if event in ('E', 'e', 'Estimate', '_ESTIMATE_'):
                self.estimate_window(self.__user_id, self.__terminal_id, self.__branch_id, self.__current_date)

            if event in ('I', 'i', 'Invoice', '_INVOICE_'):
                self.invoice_window(self.__user_id, self.__terminal_id, self.__branch_id, self.__current_date)

            if event in ('N', 'n', 'Invoice History', '_INVOICE_HISTORY_'):
                self.invoice_history_window(self.__user_id, self.__terminal_id, self.__branch_id, self.__current_date)

            if event in ('S', 's', 'Estimate History', '_ESTIMATE_HISTORY_'):
                self.estimate_history_window(self.__user_id, self.__terminal_id, self.__branch_id, self.__current_date)
                
            if event in ('C', 'c', 'Cash', '_CASH_'):
                self.cash_window(self.__user_id, self.__terminal_id, self.__branch_id, self.__current_date)
                
            if event == 'Exit':
                break
                
        self.__window.close()

    ######
    # Wrapper function for Estimate window
    def estimate_window(self, user_id, terminal_id, branch_id, current_date):
        estimate = Estimate('operation', user_id, terminal_id, branch_id, current_date)

    ######
    # Wrapper function for Order window
    def estimate_history_window(self, user_id, terminal_id, branch_id, current_date):
        estimate = Estimate('history', user_id, terminal_id, branch_id, current_date)

    ######
    # Wrapper function for Billing window
    def invoice_window(self, user_id, terminal_id, branch_id, current_date):
        draft_invoice = Invoice('operation', user_id, terminal_id, branch_id, current_date)
          
    ######
    # Wrapper function for Invoice window
    def invoice_history_window(self, user_id, terminal_id, branch_id, current_date):
        tax_invoice = Invoice('history', user_id, terminal_id, branch_id, current_date)
          
    ######
    # Wrapper function for Cash window
    def cash_window(self, user_id, terminal_id, branch_id, current_date):
        cash = Cash('operation', user_id, terminal_id, branch_id, current_date)
        

    def initialize_ui_detail_pane(self):
        None

    def initialize_ui_footer_pane(self):
        self.__ui.user_id = self.__user_id
        self.__ui.terminal_id = self.__terminal_id
        self.__ui.branch_id = self.__branch_id
        self.__ui.current_date = self.__current_date

    def initialize_ui_summary_pane(self):
        self.__ui.welcome_text = self.__welcome_text

    def initialize_ui(self):
        self.initialize_ui_detail_pane()
        self.initialize_ui_footer_pane()
        self.initialize_ui_summary_pane()

     
