#!/usr/bin/env python
import sys
import PySimpleGUI as sg


sg.theme('DefaultNoMoreNagging')

ui_customer_tab_layout = [
    [
        sg.Text('', font=("Helvetica", 5)),
    ],
    [
        sg.Text('Mobile No.:', size=(12,1),  font=("Helvetica", 11)),     
        sg.Input(key='_MOBILE_NUMBER_',
            focus=True, 
            background_color='white',
            font=("Helvetica", 11),size=(15,1),
            enable_events=True,                                
            justification = 'left'
        )
    ],
    [
        sg.Text('Name:', size=(12,1),  font=("Helvetica", 11)),     
        sg.Input(key='_CUSTOMER_NAME_',
            readonly=True, 
            font=("Helvetica", 11),
            size=(30,1),
            justification = 'left'
        )
    ],
    [
        sg.Text('Address:', size=(12,1),  font=("Helvetica", 11)),         
    ],
    [
        sg.Input(key='_CUSTOMER_ADDRESS_',
            readonly=True, 
            font=("Helvetica", 11),
            size=(45,1),
            justification = 'left'
        )
    ]
]

ui_receive_tab_layout = [
    [
        sg.Text('', font=("Helvetica", 5)),
    ],
    [
        sg.Text('Net Amount:', size=(17,1),  font=("Helvetica", 11)),     
        sg.Input(key='_NET_AMOUNT_',
            readonly=True, 
            font=("Helvetica", 11),
            size=(15,1),
            justification = 'right'
        )
    ],
    [
        sg.Text('Discount Amount:', size=(17,1),  font=("Helvetica", 11)),             
        sg.Input(key='_DISCOUNT_AMOUNT_HD_',
            readonly=True, 
            font=("Helvetica", 11),size=(15,1),
            justification = 'right'
        )
    ],
    [
        sg.Text('Roundoff Adjustment:', size=(17,1),  font=("Helvetica", 11)),             
        sg.Input(key='_ROUNDOFF_ADJUSTMENT_',
            readonly=True, 
            font=("Helvetica", 11),size=(15,1),
            justification = 'right'
        )
    ],
    [
        sg.Text('Invoice Amount:', size=(15,1), font=("Helvetica 12 bold"), text_color='Blue'),             
        sg.Input(key='_INVOICE_AMOUNT_',
            readonly=True, 
            disabled_readonly_text_color='Blue',
            size=(11,1),                
            font=("Helvetica 14 bold"),
            pad = ((8,0),(0,0)),                
            justification = 'right'
        )
    ],
    [sg.HorizontalSeparator(color = 'grey99', pad = ((0,0),(15,15)))],            
    [
        sg.Text('Redeem Adjustment:', size=(17,1),  font=("Helvetica", 11)),     
        sg.Input(key='_REDEEM_ADJUSTMENT_HD_',
            readonly=True, 
            font=("Helvetica", 11),
            size=(15,1),
            justification = 'right'
        )
    ],
    [
        sg.Text('Exchange Adjustment:', size=(17,1),  font=("Helvetica", 11)),     
        sg.Input(key='_EXCHANGE_ADJUSTMENT_HD_',
            readonly=True, 
            font=("Helvetica", 11),
            size=(15,1),
            justification = 'right'
        )
    ],
    [
        sg.Text('Cash Amount:', size=(17,1),  font=("Helvetica", 11)),     
        sg.Input(key='_CASH_AMOUNT_',
            focus=True, 
            background_color='white',
            font=("Helvetica", 11),size=(15,1),
            enable_events=True,                                
            justification = 'left'
        ),
        sg.Text('Reference:', font=("Helvetica", 11)),         
    ],
    [
        sg.Text('Card Amount:', size=(17,1),  font=("Helvetica", 11)),     
        sg.Input(key='_CARD_AMOUNT_',
            background_color='white',
            font=("Helvetica", 11),size=(15,1),
            enable_events=True,                                
            justification = 'left'
        ),        
        sg.Input(key='_CARD_REFERENCE_',
            background_color='white',
            font=("Helvetica", 11),size=(15,1),
            enable_events=True,                                
            justification = 'left'
        ),        
    ],
    [sg.HorizontalSeparator(color = 'grey99', pad = ((0,0),(15,15)))],            
    [
        sg.Text('Cash Return:', size=(15,1), font=("Helvetica 12 bold"), text_color='Blue', pad = ((6,0),(0,15))),             
        sg.Input(key='_CASH_RETURN_',
            readonly=True, 
            disabled_readonly_text_color='Blue',
            size=(11,1),                
            font=("Helvetica 14 bold"),
            pad = ((12,0),(0,15)),                
            justification = 'right'
        )
    ],
]

ui_exchange_tab_layout = [
    [
        sg.Text('', font=("Helvetica", 5)),
    ],
    [
        sg.Text('Voucher:', size=(10,1),  font=("Helvetica", 11)),     
        sg.Combo(key='_EXCHANGE_VOUCHER_',
            values=['xxx','yyy'],
            default_value='xxx',
            background_color='white',
            font=("Helvetica", 11),size=(15,1),
            enable_events=True,                                
        )
    ],
    [
        sg.Text('Adjustment:', size=(10,1),  font=("Helvetica", 11)),     
        sg.Input(key='_EXCHANGE_ADJUSTMENT_',
            readonly=True, 
            font=("Helvetica", 11),
            size=(15,1),
            justification = 'left'
        )
    ],
]

ui_discount_tab_layout = [
    [
        sg.Text('', font=("Helvetica", 5)),
    ],
    [
        sg.Text('Discount:', size=(10,1),  font=("Helvetica", 11)),     
        sg.Input(key='_DISCOUNT_AMOUNT_',
            focus=True, 
            background_color='white',
            font=("Helvetica", 11),size=(15,1),
            enable_events=True,                                
            justification = 'right'
        )
    ],
    [
        sg.Text('PIN:', size=(10,1),  font=("Helvetica", 11)),     
        sg.Input(key='_DISCOUNT_PIN_',
            background_color='white',
            font=("Helvetica", 11),size=(5,1),
            enable_events=True,                                
            justification = 'left'
        )
    ],
]

ui_redeem_tab_layout = [
    [
        sg.Text('', font=("Helvetica", 5)),
    ],
    [
        sg.Text('Available Points:', size=(15,1),  font=("Helvetica", 11)),     
        sg.Input(key='_AVAILABLE_POINTS_',
            readonly=True, 
            font=("Helvetica", 11),
            size=(5,1),
            justification = 'right'
        ),
        sg.Input(key='_AVAILABLE_ADJUSTMENT_',
            readonly=True, 
            font=("Helvetica", 11),
            size=(15,1),
            justification = 'right'
        )        
    ],
    [
        sg.Text('Redeem Points:', size=(15,1),  font=("Helvetica", 11)),     
        sg.Input(key='_REDEEM_POINTS_',
            focus=True, 
            background_color='white',
            font=("Helvetica", 11),size=(5,1),
            enable_events=True,                                
            justification = 'right'
        ),
        sg.Input(key='_REDEEM_ADJUSTMENT_',
            readonly=True, 
            font=("Helvetica", 11),
            size=(15,1),
            justification = 'right'
        )        
    ],
    [
        sg.Text('PIN:', size=(15,1),  font=("Helvetica", 11)),     
        sg.Input(key='_REDEEM_PIN_',
            background_color='white',
            font=("Helvetica", 11),size=(5,1),
            enable_events=True,                                
            justification = 'left'
        )
    ],
]


layout = [
    [
        sg.Text('Customer:', size=(8,1),  font=("Helvetica", 11), pad=((10,0),(10,5))),     
        sg.Input(key='_MOBILE_NUMBER_HEADER_',
            readonly=True, 
            font=("Helvetica", 11),
            size=(12,1),
            justification = 'left',
            pad=((5,0),(10,5))            
        ),    
        sg.Input(key='_CUSTOMER_NAME_HEADER_',
            readonly=True, 
            font=("Helvetica", 11),
            size=(30,1),
            justification = 'left', 
            pad=((5,0),(10,5))
        )
    ],
    [
        sg.Text('Balance:', size=(7,1), font=("Helvetica 12 bold"), text_color='Blue', pad=((10,0),(0,10))),         
        sg.Input(key='_BALANCE_AMOUNT_',
            readonly=True,
            disabled_readonly_text_color='Blue',            
            font=("Helvetica 14 bold"),
            size=(12,1),
            justification = 'left',
            pad=((7,0),(0,10)),            
        ),    
    
    ],
    [
        sg.TabGroup(
            [
                [
                    sg.Tab('Receive-F1', ui_receive_tab_layout, key='_RECEIVE_TAB_'),
                    sg.Tab('Exchange-F2', ui_exchange_tab_layout, key='_EXCHANGE_TAB_'),
                    sg.Tab('Redeem-F3', ui_redeem_tab_layout, key='_REDEEM_TAB_'),
                    sg.Tab('Discount-F4', ui_discount_tab_layout, key='_DISCOUNT_TAB_'),
                    sg.Tab('Customer-F5', ui_customer_tab_layout, key='_CUSTOMER_TAB_'),
                ]
            ],
            key='_PAYMENT_TAB_GROUP_', 
            title_color='grey32',
            font=("Helvetica 11"),
            selected_title_color='white',
            selected_background_color='navy' ,           
            tab_location='topleft'
        ),
    ],
    [
        sg.Button('Ok-F12', 
            size=(8, 1), 
            font='Calibri 12 bold', 
            key='_PAYMENT_OK_',
            pad = ((5,0),(10,10)),                            
        ),

        sg.Button('Exit-Esc', 
            size=(8, 1), 
            font='Calibri 12 bold', 
            key='_PAYMENT_ESC_', 
            pad = ((15,0),(10,10)),                            
        )
    ]                   
]

window = sg.Window('Payment', layout, default_element_size=(12, 1),return_keyboard_events=True, 
)

while True:
    event, values = window.read()
    print(event)
    if event in ('F1:112', 'F1'):
        window['_RECEIVE_TAB_'].select()
        window.Element('_CASH_AMOUNT_').SetFocus() 
    if event in ('F2:113', 'F2'):
        window['_EXCHANGE_TAB_'].select()        
    if event in ('F3:114', 'F3'):
        window['_REDEEM_TAB_'].select()
        window.Element('_REDEEM_POINTS_').SetFocus() 
    if event in ('F4:115', 'F4'):
        window['_DISCOUNT_TAB_'].select()        
    if event in ('F5:116', 'F5'):
        window['_CUSTOMER_TAB_'].select()        
        
    if event == sg.WIN_CLOSED:           # always,  always give a way out!
        break
window.close()
