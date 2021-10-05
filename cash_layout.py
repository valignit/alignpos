import PySimpleGUI as sg
from config import Config
from db_nosql import KvDatabase
from styles import ElementStyle


class CashCanvas:
    def __init__(self):
    
        cash_list_layout = [
            [
                sg.Text('Type:', size=(12,1),  font=("Helvetica", 11)),
                sg.Combo(['', 'Payment', 'Receipt'], key='_TRANSACTION_TYPE_SEARCH_',default_value = '',                
                    font=("Helvetica", 11),
                    size=(15,1),
                ),
                sg.Text('Context:', size=(12,1),  font=("Helvetica", 11)),     
                sg.Combo(['', 'Invoice', 'Drawer'], key='_TRANSACTION_CONTEXT_SEARCH_',default_value = '',                
                    font=("Helvetica", 11),
                    size=(15,1),
                ),
                sg.Button('Search-F11', **ElementStyle.search_button_short, key='_CASH_LIST_SEARCH_', pad=((35,0),(0,0))),                                
            ],
            [
                sg.Table(values=[], 
                     key='_CASH_LIST_', 
                     enable_events=True,
                     headings= ['name', 'Type', 'Context', 'Reference', 'Receipt', 'Payment', 'Balance'],
                     font=("Helvetica", 11),
                     auto_size_columns=False,
                     justification='right',
                     row_height=25,
                     alternating_row_color='MistyRose2',
                     num_rows=20,
                     display_row_numbers=False,
                     bind_return_key = True,
                     col_widths=[12, 10, 10, 15, 12, 12, 12, 12],
                     pad=((5,0),(5,5))
                )            
            ],
            [
                sg.Button('Receipt\nF1', **ElementStyle.search_button_medium, key='_CASH_LIST_RECEIPT_'),                
                sg.Button('Payment\nF2', **ElementStyle.search_button_medium, key='_CASH_LIST_PAYMENT_'),                
                sg.Button('Denomination\nF3', **ElementStyle.search_button_medium, key='_CASH_LIST_DENOMINATION_'),                
                sg.Button('Exit\nEsc', **ElementStyle.search_button_medium, key='_CASH_LIST_ESC_'), 
            ]             
        ]
        
        self.__layout = [
            [
                sg.Column(cash_list_layout, vertical_alignment = 'top', pad = ((0,0),(0,0))),
            ]
        ]

    def get_layout(self):
        return self.__layout
    
    layout = property(get_layout)         

 
