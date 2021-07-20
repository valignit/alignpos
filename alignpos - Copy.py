import PySimpleGUI as sg
import os
from subprocess import run
import datetime
import json
import sys
import platform
import pdfkit
import webbrowser
from pynput.keyboard import Key, Controller

from alignpos_db import DbConn, DbTable, DbQuery
from main_menu_layout import MainMenuLayout
from estimate_layout import EstimateLayout
from invoice_layout import InvoiceLayout

from estimate_ui import UiTitlePane, UiHeaderPane, UiSearchPane, UiDetailPane, UiActionPane, UiSummaryPane

from estimate import Estimate


######
# Global variables
with open('./alignpos.json') as file_config:
  config = json.load(file_config)

w, h = sg.Window.get_screen_size()

kb = Controller()

db_pos_host = config["db_pos_host"]
db_pos_port = config["db_pos_port"]
db_pos_database = config["db_pos_database"]
db_pos_user = config["db_pos_user"]
db_pos_passwd = config["db_pos_passwd"] 

db_conn = DbConn(db_pos_host, db_pos_port, db_pos_database, db_pos_user, db_pos_passwd)
db_session = db_conn.session




def estimate_window():
    estimate_layout = EstimateLayout(config, w, h)
    ui_window = sg.Window('Estimate', 
                    estimate_layout.layout,
                    location=(-7,0),
                    font='Helvetica 11', 
                    finalize=True, 
                    keep_on_top=False, 
                    resizable=True,
                    return_keyboard_events=True, 
                    use_default_focus=False,
                    modal=True
                )
             
    #ui_window.maximize()
    estimate = Estimate(db_conn, ui_window)
       
    estimate.initialize_ui()
    estimate.goto_last_row()
    
    ui_window['_BARCODE_'].bind('<FocusIn>', '+CLICK+')
    ui_window['_ITEM_NAME_'].bind('<FocusIn>', '+CLICK+')
    
    prev_event = '' 
    focus = None    
    while True:
        event, values = ui_window.read()
        if ui_window.FindElementWithFocus():
            focus = ui_window.FindElementWithFocus().Key
            
        #print('window=', event, 'prev=', prev_event, 'focus=', focus)

        if event == sg.WIN_CLOSED:
            ui_window.close()
            break

        if event == 'Escape:27':
            ui_window.close()
            break

        if event == 'ENTER':        
            kb.press(Key.enter)
            kb.release(Key.enter)
            
        if event == 'ESC':
            kb.press(Key.esc)
            kb.release(Key.esc)
            
        if event == 'TAB':        
            kb.press(Key.tab)
            kb.release(Key.tab)
            
        if event == 'DEL':
            kb.press(Key.delete)
            kb.release(Key.delete)
            
        if event == 'UP':        
            kb.press(Key.up)
            kb.release(Key.up)
            
        if event == 'DOWN':
            kb.press(Key.down)
            kb.release(Key.down)
            
        if event == 'RIGHT':
            kb.press(Key.right)
            kb.release(Key.right)
            
        if event == 'LEFT':
            kb.press(Key.left)
            kb.release(Key.left)
            
        if event == 'BACKSPACE':
            kb.press(Key.backspace)
            kb.release(Key.backspace)
            
        if event == 'Estimate':
            ui_window.hide()
            run([sys.executable, 'estimate_entry.py'])
            ui_window.un_hide()
            
        if event == 'Exit':
            break

    ui_window.close()


def invoice_window():
    invoice_layout = InvoiceLayout(config, w, h)
    ui_window = sg.Window('Invoice', 
                    invoice_layout.layout, 
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
    ui_window.maximize()
   
    prev_event = '' 
    focus = None    
    while True:
        event, values = ui_window.read()
        if ui_window.FindElementWithFocus():
            focus = ui_window.FindElementWithFocus().Key
            
        #print('window=', event, 'prev=', prev_event, 'focus=', focus)

        if event == sg.WIN_CLOSED:
            ui_window.close()
            break

        if event == 'Escape:27':
            ui_window.close()
            break

        if event == 'ENTER':        
            kb.press(Key.enter)
            kb.release(Key.enter)
            
        if event == 'ESC':
            kb.press(Key.esc)
            kb.release(Key.esc)
            
        if event == 'TAB':        
            kb.press(Key.tab)
            kb.release(Key.tab)
            
        if event == 'DEL':
            kb.press(Key.delete)
            kb.release(Key.delete)
            
        if event == 'UP':        
            kb.press(Key.up)
            kb.release(Key.up)
            
        if event == 'DOWN':
            kb.press(Key.down)
            kb.release(Key.down)
            
        if event == 'RIGHT':
            kb.press(Key.right)
            kb.release(Key.right)
            
        if event == 'LEFT':
            kb.press(Key.left)
            kb.release(Key.left)
            
        if event == 'BACKSPACE':
            kb.press(Key.backspace)
            kb.release(Key.backspace)
            
        if event == 'Estimate':
            ui_window.hide()
            run([sys.executable, 'estimate_entry.py'])
            ui_window.un_hide()
            
        if event == 'Exit':
            break

    ui_window.close()

    
def main_menu():
    main_menu_layout = MainMenuLayout(config, w, h)
    ui_window = sg.Window('Alignpos Menu', 
                    main_menu_layout.layout, 
                    font='Helvetica 11', 
                    finalize=True, 
                    location=(0,0), 
                    size=(w,h), 
                    keep_on_top=False, 
                    resizable=False,
                    return_keyboard_events=True, 
                    use_default_focus=False,
             )
    ui_window.maximize()
   
    prev_event = '' 
    focus = None    
    while True:
        event, values = ui_window.read()
        if ui_window.FindElementWithFocus():
            focus = ui_window.FindElementWithFocus().Key
            
        #print('window=', event, 'prev=', prev_event, 'focus=', focus)

        if event == sg.WIN_CLOSED:
            ui_window.close()
            break

        if event == 'Escape:27':
            ui_window.close()
            break

        if event == 'ENTER':        
            kb.press(Key.enter)
            kb.release(Key.enter)
            
        if event == 'ESC':
            kb.press(Key.esc)
            kb.release(Key.esc)
            
        if event == 'TAB':        
            kb.press(Key.tab)
            kb.release(Key.tab)
            
        if event == 'DEL':
            kb.press(Key.delete)
            kb.release(Key.delete)
            
        if event == 'UP':        
            kb.press(Key.up)
            kb.release(Key.up)
            
        if event == 'DOWN':
            kb.press(Key.down)
            kb.release(Key.down)
            
        if event == 'RIGHT':
            kb.press(Key.right)
            kb.release(Key.right)
            
        if event == 'LEFT':
            kb.press(Key.left)
            kb.release(Key.left)
            
        if event == 'BACKSPACE':
            kb.press(Key.backspace)
            kb.release(Key.backspace)
            
        if event == 'Estimate':
            estimate_window()

        if event == 'Invoice':
            invoice_window()
            
        if event == 'Exit':
            break
            
    ui_window.close()


######
# Main function
def main():
    
    main_menu()
    
    
######
if __name__ == "__main__":
    main()
