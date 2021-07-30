import PySimpleGUI as sg
import json
from subprocess import run

from main_menu_layout import MainMenuCanvas
from main_menu_ui import MainMenuUi
from estimate import Estimate

sg.theme('DefaultNoMoreNagging')


class MainMenu():   
    
    def __init__(self, user_id, terminal_id):
        self.__user_id = user_id
        self.__terminal_id = terminal_id
    
        with open('./alignpos.json') as file_config:
          config = json.load(file_config)

        self.__welcome_text = config["welcome_text"]
                
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
                
            if event in ('E', 'e', 'Estimate', '_ESTIMATE_OPTION_'):
                self.estimate_window(self.__user_id, self.__terminal_id)

            if event in ('I', 'i', 'Invoice', '_INVOICE_OPTION_'):
                self.invoice_window(self.__user_id, self.__terminal_id)
                
            if event == 'Exit':
                break
                
        self.__window.close()

    ######
    # Wrapper function for Estimate window
    def estimate_window(self, user_id, terminal_id):
        estimate = Estimate(user_id, terminal_id)

    ######
    # Wrapper function for Invoice window
    def invoice_window(self, user_id, terminal_id):
        None
          
    def initialize_ui_detail_pane(self):
        None

    def initialize_ui_footer_pane(self):
        self.__ui.user_id = self.__user_id
        self.__ui.terminal_id = self.__terminal_id
        self.__ui.current_date = '2021/06/13'

    def initialize_ui_summary_pane(self):
        self.__ui.welcome_text = self.__welcome_text

    def initialize_ui(self):
        self.initialize_ui_detail_pane()
        self.initialize_ui_footer_pane()
        self.initialize_ui_summary_pane()

     
