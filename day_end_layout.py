import PySimpleGUI as sg

from styles import ElementStyle as ap_style
from config import Config
from db_nosql import KvDatabase


###
# Day End Layout               

class DayEndCanvas:
    def __init__(self):
    
        day_end_layout = [
            [
                sg.Text('Current Date:', size=(15,1),  font=("Helvetica", 11)),     
                sg.Input(key='_CURRENT_DATE_',
                    readonly=True, 
                    font=("Helvetica", 11),
                    size=(15,1),
                    justification = 'right'
                )
            ],
            [
                sg.Text('Current Status:', size=(15,1),  font=("Helvetica", 11), pad=((5,5),(10,10))),             
                sg.Input(key='_CURRENT_STATUS_',
                    readonly=True, 
                    font=("Helvetica", 11),
                    size=(15,1),
                    justification = 'center'
                )
            ],
            [
                sg.HorizontalSeparator(color = 'grey99', pad = ((0,0),(20,10)))
            ],                        
            [
                sg.Button('Ok-F12', **ap_style.search_button_short, key='_DAY_END_OK_'), 
                sg.Button('Exit-Esc', **ap_style.search_button_short, key='_DAY_END_ESC_'), 
            ]           
        ]
        
        self.__layout = [
            [
                sg.Column(day_end_layout, vertical_alignment = 'top', pad = None),
            ]
        ]

    def get_layout(self):
        return self.__layout
    
    layout = property(get_layout)         


###
if __name__ == "__main__":
    print('***Not an executable module, please call the main script')
