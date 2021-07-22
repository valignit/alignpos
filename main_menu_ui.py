import PySimpleGUI as sg
import json
import datetime


class UiDetailPane:

    def __init__(self, window):
        self.__window = window


class UiFooterPane:

    def __init__(self, window):
        self.__window = window
        self.__user_id = ''
        self.__terminal_id = ''
        self.__current_date = datetime.datetime(1900, 1, 1)

        self.__window['_USER_ID_'].Widget.config(takefocus=0)
        self.__window['_TERMINAL_ID_'].Widget.config(takefocus=0)
        self.__window['_CURRENT_DATE_'].Widget.config(takefocus=0)

    def set_user_id(self, user_id):
        self.__user_id = user_id
        self.__window.Element('_USER_ID_').update(value = self.__user_id)
        
    def get_user_id(self):
        self.__user_id = self.__window.Element('_USER_ID_').get()
        return self.__user_id
        
    def set_terminal_id(self, terminal_id):
        self.__terminal_id = terminal_id
        self.__window.Element('_TERMINAL_ID_').update(value = self.__terminal_id)        
        
    def get_terminal_id(self):
        self.__terminal_id = self.__window.Element('_TERMINAL_ID_').get()    
        return self.__terminal_id
        
    def set_current_date(self, current_date):
        self.__current_date = current_date
        self.__window.Element('_CURRENT_DATE_').update(value = self.__current_date)        
        
    def get_current_date(self):
        self.__current_date = self.__window.Element('_CURRENT_DATE_').get()        
        return self.__current_date
               
    user_id = property(get_user_id, set_user_id) 
    terminal_id = property(get_terminal_id, set_terminal_id)
    current_date = property(get_current_date, set_current_date)
        

class UiSummaryPane:

    def __init__(self, window):
        self.__window = window
        self.__welcome_text = ''

    def set_welcome_text(self, welcome_text):
        self.__welcome_text = welcome_text
        self.__window.Element('_WELCOME_TEXT_').update(value = self.__welcome_text)
        
    def get_welcome_text(self):
        self.__welcome_text = self.__window.Element('_WELCOME_TEXT_').get()
        return self.__welcome_text
            
    welcome_text = property(get_welcome_text, set_welcome_text)


