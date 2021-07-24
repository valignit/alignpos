import PySimpleGUI as sg
import json
import datetime


###
# Item Name Popup Interface
class ItemLookupUi:

    def __init__(self, popup):
        self.__popup = popup
        self.__item_code = ''
        self.__item_name = ''
        self.__item_list = []
        self.__item_line = []
        self.__idx = 0

    def set_item_code(self, item_code):
        self.__item_code = item_code
        
    def get_item_code(self):
        return self.__item_code

    def set_item_name(self, item_name):
        self.__item_name = item_name
        
    def get_item_name(self):
        return self.__item_name

    def set_item_list(self, item_list):
        self.__item_list = item_list
        self.__popup.Element('_ITEM_NAME_LIST_').update(values = self.__item_list, set_to_index=self.__idx)
        
    def get_item_list(self):
        return self.__item_list
        
    def get_item_line(self):
        return self.__popup.Element('_ITEM_NAME_LIST_').get()

    def set_item_line(self, item_line):
        self.__item_line = item_line

    def elements_to_item_line(self):
        self.__item_line.append(self.__item_code)
        self.__item_line.append('|')
        self.__item_line.append(self.__item_name.replace(' ', '-')) #otherwise item name will be embedded with {}
       
    def item_line_to_elements(self, idx):
        self.__item_line = self.__items_list[idx]
        self.__item_code = self.__item_line[0]
        self.__item_name = self.__item_line[1]
        
    def add_item_line(self):
        self.__item_line = []
        self.elements_to_item_line()
        self.__item_list.append(self.__item_line)
        self.__popup.Element('_ITEM_NAME_LIST_').update(values = self.__item_list)

    def prev_item_line(self):
        idx = self.__idx
        if idx > 0:
            idx = idx - 1
            self.__idx = idx
            self.__popup.Element('_ITEM_NAME_LIST_').update(set_to_index=self.__idx)
            
    def next_item_line(self):
        idx = self.__idx
        if idx < len(self.__item_list) - 1:
            idx = idx + 1
            self.__idx = idx
            self.__popup.Element('_ITEM_NAME_LIST_').update(set_to_index=self.__idx)
                   
    def focus_item_list(self):
        self.__popup.Element('_ITEM_NAME_LIST_').SetFocus()
        
    def get_item_idx(self):
        return self.__idx
        
    def set_item_idx(self, idx):
        self.__idx = idx
        self.__popup.Element('_ITEM_NAME_LIST_').update(set_to_index=self.__idx)       
        
    item_list = property(get_item_list, set_item_list)     
    item_code = property(get_item_code, set_item_code)
    item_name = property(get_item_name, set_item_name)
    item_line = property(get_item_line, set_item_line)
    idx = property(get_item_idx, set_item_idx)

