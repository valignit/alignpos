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
from common_layout import ItemLookupLayout

from main_menu_ui import UiDetailPane, UiFooterPane, UiSummaryPane
from estimate_ui import UiHeaderPane, UiSearchPane, UiDetailPane, UiActionPane, UiFooterPane, UiSummaryPane
from invoice_ui import UiHeaderPane, UiSearchPane, UiDetailPane, UiActionPane, UiFooterPane, UiSummaryPane
from common_ui import UiItemLookup

from main_menu import MainMenu
from estimate import Estimate
from invoice import Invoice
from common import ItemLookup


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


######
# Popup window for selecting Item
def item_lookup_popup(filter, lin, col):
    item_lookup_layout = ItemLookupLayout()       
    ui_popup = sg.Window("Item Name", 
                    item_lookup_layout.layout,
                    location=(lin,col), 
                    size=(348,129), 
                    modal=True, 
                    finalize=True,
                    return_keyboard_events=True, 
                    no_titlebar = True, 
                    element_padding=(0,0), 
                    background_color = 'White', 
                    keep_on_top = True,                    
                    margins=(0,0)
                )
    ui_popup.bind('<FocusIn>', '+FOCUS IN+')
    ui_popup.bind('<FocusOut>', '+FOCUS OUT+')
   
    item_lookup = ItemLookup(db_conn, ui_popup)
    item_lookup.populate_item_list(filter)  
    item_lookup.ui_item_lookup.focus_item_list()
    item_lookup.ui_item_lookup.idx = 0

    item_lookup.sel_item_code = None

    prev_event = ''    
    while True:
        event, values = ui_popup.read()
        #print('item_name_popup=', event)
        if event == 'Down:40':
            item_lookup.ui_item_lookup.next_item_line()
        if event == 'Up:38':
            item_lookup.ui_item_lookup.prev_item_line()            
        if event in ("Exit", '_ITEM_NAME_ESC_', 'Escape:27', '+FOCUS OUT+') or event == sg.WIN_CLOSED:
            break        
        if event == '\r':
            item_lookup.sel_item_code =  values['_ITEM_NAME_LIST_'][0][0]
            ui_popup.close()
            break
    ui_popup.close()


def estimate_window():
    estimate_layout = EstimateLayout(config, w, h)
    ui_window = sg.Window('Estimate', 
                    estimate_layout.layout,
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
    estimate = Estimate(db_conn, ui_window)
       
    estimate.initialize_ui()
    estimate.goto_last_row()
    
    ui_window['_BARCODE_'].bind('<FocusIn>', '+CLICK+')
    ui_window['_ITEM_NAME_'].bind('<FocusIn>', '+CLICK+')
    
    estimate.ui_search_pane.focus_barcode()        
    
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
            estimate.initialize_ui_action_pane()
           
        if event in ('\t') and prev_event == '_ITEM_NAME_':
            estimate.ui_detail_pane.focus_items_list()

        if focus == '_ITEMS_LIST_':
            if len(estimate.ui_detail_pane.items_list) > 0:
                estimate.initialize_ui_action_pane()
            else:
                estimate.ui_search_pane.focus_barcode()        
        else:
            estimate.initialize_ui_action_pane()
            estimate.ui_detail_pane.items_list = estimate.ui_detail_pane.items_list

        if event in ('F1:112', 'F1'):        
            item_lookup_popup('', 100,100)

        if event == 'Exit':
            break

        if event not in ('\t', 'Up:38', 'Down:40', 'UP', 'DOWN', 'DEL', 'Delete:46', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
            prev_event = event

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
           
        print(prev_event)
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
        print(event)
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
            #ui_window.hide()
            estimate_window()
            #ui_window.un_hide()

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
