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
from invoice_layout import InvoiceLayout

from main_menu_ui import UiDetailPane, UiFooterPane, UiSummaryPane
from invoice_ui import UiHeaderPane, UiSearchPane, UiDetailPane, UiActionPane, UiFooterPane, UiSummaryPane

from main_menu import MainMenu
from estimate import Estimate
from invoice import Invoice
from common import ItemLookup, ConfirmMessage


######
# Global variables
with open('./alignpos.json') as file_config:
  config = json.load(file_config)

w, h = sg.Window.get_screen_size()

kb = Controller()

db_conn = DbConn()
db_session = db_conn.session


                
######
# Wrapper function for Item Lookup
def item_lookup(filter, lin, col):
    item_lookup = ItemLookup(filter, lin, col)
    return item_lookup.item_code


######
# Wrapper function for Estimate Window
def estimate_window():
    estimate = Estimate()


######
# Invoice Window
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
    ui_window['_LEFT_PANES_'].Widget.configure(borderwidth=1, relief=sg.DEFAULT_FRAME_RELIEF)
    ui_window['_RIGHT_PANES_'].Widget.configure(borderwidth=1, relief=sg.DEFAULT_FRAME_RELIEF)

    invoice = Invoice(db_conn, ui_window)
       
    invoice.initialize_ui()
    invoice.goto_last_row()
    
    ui_window['_BARCODE_'].bind('<FocusIn>', '+CLICK+')
    ui_window['_ITEM_NAME_'].bind('<FocusIn>', '+CLICK+')
    
    invoice.ui_search_pane.focus_barcode()        
   
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
                       
        if event == '+CLICK+':
            invoice.initialize_ui_action_pane()
           
        if event in ('\t') and prev_event == '_ITEM_NAME_':
            invoice.ui_detail_pane.focus_items_list()

        if focus == '_ITEMS_LIST_':
            if len(invoice.ui_detail_pane.items_list) > 0:
                invoice.initialize_ui_action_pane()
            else:
                invoice.ui_search_pane.focus_barcode()        
        else:
            invoice.initialize_ui_action_pane()
            invoice.ui_detail_pane.items_list = invoice.ui_detail_pane.items_list

        if event in ('F1:112', 'F1'):        
            item_lookup_popup('', 100,100)

        if event == 'Exit':
            break

        if event not in ('\t', 'Up:38', 'Down:40', 'UP', 'DOWN', 'DEL', 'Delete:46', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
            prev_event = event

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
    ui_window['_LEFT_PANES_'].Widget.configure(borderwidth=1, relief=sg.DEFAULT_FRAME_RELIEF)
    ui_window['_RIGHT_PANES_'].Widget.configure(borderwidth=1, relief=sg.DEFAULT_FRAME_RELIEF)

    main_menu = MainMenu(db_conn, ui_window)
       
    main_menu.initialize_ui()
    main_menu.ui_summary_pane.welcome_text = config["welcome_text"]
   
    prev_event = '' 
    focus = None    
    while True:
        event, values = ui_window.read()
        #print(event)
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
            
        if event in ('E', 'e', 'Estimate', '_ESTIMATE_OPTION_'):
            #ui_window.hide()
            estimate_window()
            #ui_window.un_hide()

        if event in ('I', 'i', 'Invoice', '_INVOICE_OPTION_'):
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
