import PySimpleGUI as sg
from alignpos_db import DbConn, DbTable, DbQuery

from common_layout import ConfirmMessageCanvas, ItemLookupCanvas
from common_ui import ItemLookupUi

 
class ConfirmMessage():
    
    def __init__(self, type, message):
        self.__canvas = ConfirmMessageCanvas()

        self.__window = sg.Window("Confirm", 
                        self.__canvas.layout,
                        keep_on_top = True, 
                        return_keyboard_events = True, 
                        modal=True, 
                        finalize=True
                    )

        self.__window.bind('<FocusIn>', '+FOCUS IN+')
        self.__window.bind('<FocusOut>', '+FOCUS OUT+')

        self.__window.Element("_MESSAGE_").update(value=message)       
        self.__window["_OK_"].Widget.config(takefocus=0) 
        self.__window["_CANCEL_"].Widget.config(takefocus=0)

        self.__type = type
        self.__message = message
        self.__result = ''

        self.handler()

    def handler(self):
        if self.__type == 'OK':
            self.__window.Element("_CANCEL_").update(visible=False)
        else:
            self.__window.Element("_CANCEL_").update(visible=True)

        while True:
            event, values = self.__window.read()
            #print('message_popup:', event)
            if event in ('Escape:27', '_OK_', '_CANCEL_', 'F12:123', 'F12', '\r', '+FOCUS OUT+'):
                break
            if event == sg.WIN_CLOSED:
                self.__result = 'Cancel'
        if event in ('Escape:27', '_CANCEL_', '+FOCUS OUT+'):
            self.__result = 'Cancel'
        else:
            self.__result = 'Ok'
        self.__window.close()

    def get_result(self):
        return self.__result
    
    result = property(get_result)         


       
class ItemLookup():

    def __init__(self, filter, lin, col):
        self.__item_code = None
        self.__canvas = ItemLookupCanvas()
        self.__window = sg.Window("Item Name",
                        self.__canvas.layout,
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
        self.__window.bind('<FocusIn>', '+FOCUS IN+')
        self.__window.bind('<FocusOut>', '+FOCUS OUT+')    
    
        self.__ui = ItemLookupUi(self.__window)
        
        self.__db_conn = DbConn()
        db_item_table = DbTable(self.__db_conn, 'tabItem')
        db_item_cursor = db_item_table.list(filter)

        self.__ui.item_list = []
        for db_item_row in db_item_cursor:
            self.__ui.item_code = db_item_row.item_code
            self.__ui.item_name = db_item_row.item_name
            self.__ui.add_item_line()

        self.__ui.focus_item_list()

        self.handler()


    def handler(self):
        prev_event = ''    
        while True:
            event, values = self.__window.read()
            print('item_name_popup=', event, prev_event, values)
            if event == 'Down:40':
                self.__ui.next_item_line()
            if event == 'Up:38':
                self.__ui.prev_item_line()            
            if event in ("Exit", '_ITEM_NAME_ESC_', 'Escape:27', '+FOCUS OUT+') or event == sg.WIN_CLOSED:
                break        
            if event in ('\r'):
                if values['_ITEM_NAME_LIST_']:
                    self.__item_code =  values['_ITEM_NAME_LIST_'][0][0]
                    break
            if event in ('_ITEM_NAME_LIST_') and prev_event in ('_ITEM_NAME_LIST_'):
                self.__item_code =  values['_ITEM_NAME_LIST_'][0][0]
                break
            prev_event = event
            
        self.__db_conn.close()           
        self.__window.close()    

      
    def get_item_code(self):
        return self.__item_code
    
    item_code = property(get_item_code)         
