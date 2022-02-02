import datetime
      

class DayEndUi:
    def __init__(self, window):
        self.__window = window
        self.__current_date = ''
        self.__current_status = ''

        self.__window["_CURRENT_DATE_"].Widget.config(takefocus=0)
        self.__window["_CURRENT_STATUS_"].Widget.config(takefocus=0)
        self.__window["_DAY_END_OK_"].Widget.config(takefocus=0) 
        self.__window["_DAY_END_ESC_"].Widget.config(takefocus=0) 
        
    def set_current_date(self, current_date):
        self.__current_date = current_date
        self.__window.Element('_CURRENT_DATE_').update(value = self.__current_date)
        
    def get_current_date(self):
        return self.__current_date
        
    def set_current_status(self, current_status):
        self.__current_status = current_status
        self.__window.Element('_CURRENT_STATUS_').update(value = self.__current_status)
        
    def get_current_status(self):
        return self.__current_status
        

    current_date = property(get_current_date, set_current_date)     
    current_status = property(get_current_status, set_current_status)     


