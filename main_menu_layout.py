import PySimpleGUI as sg
from common_layout import ElementStyle as ap_style


###
# Main Menu Layout               
class MainMenuCanvas:
    def __init__(self, w, h):
            
        lw = w*78/100
        rw = w*22/100
        lh = h
        rh = h

        menu_def = [
                ['&File', ['E&xit']],      
                ['&Operations', ['&Estimate', '&Draft Invoice', '&Tax Invoice', '&Cash', '---', 'Day Close']],      
                ['&Interface', ['&Download Customer', '&Download Item', '&Download Exchange', '---', '&Upload Invoice']],      
                ['&Reports', ['&Daily Sales', 'Cash &Position']],      
                ['&Help', '&About'], 
        ]
                 
        ui_header_pane_layout = [
            [
                sg.Text('Menu', **ap_style.page_title, pad=((0,0),(0,3))),
            ]
        ]

        ui_detail_pane_layout = [
            [
                sg.Column(
                    [
                        [
                            sg.Text('Operations',**ap_style.menu_text),
                        ],
                        [
                            sg.Button(key='_ESTIMATE_', button_text='E̲stimate',**ap_style.menu_button),
                        ],
                        [
                            sg.Button(key='_DRAFT_INVOICE_', button_text='D̲raft Invoice',**ap_style.menu_button),
                        ],
                        [
                            sg.Button(key='_TAX_INVOICE_', button_text='T̲ax Invoice',**ap_style.menu_button),
                        ],
                        [
                            sg.Button(key='_CASH_OPTION_', button_text='C̲ash',**ap_style.menu_button),
                        ],
                        [
                            sg.Button(key='_DAY_CLOSE_OPTION_', button_text='D̲ay Close',**ap_style.menu_button),
                        ],
                    ],
                    vertical_alignment = 'top', 
                    justification = 'left',
                    pad = ((0,0),(50,0))
                ),
                sg.Column(
                    [
                        [
                            sg.Text('Interface',**ap_style.menu_text),
                        ],
                        [
                            sg.Button(key='_DOWNLOAD_CUSTOMERS_', button_text='Download Cu̲stomer',**ap_style.menu_button),
                        ],
                        [
                            sg.Button(key='_DOWNLOAD_ITEMS_', button_text='Download It̲em',**ap_style.menu_button),
                        ],
                        [
                            sg.Button(key='_DOWNLOAD_EXCHANGES_', button_text='Download Exch̲ange',**ap_style.menu_button),
                        ],
                        [
                            sg.Button(key='_UPLOAD_INVOICES_', button_text='Upload Inv̲oice',**ap_style.menu_button),
                        ],
                    ],
                    vertical_alignment = 'top', 
                    justification = 'left',
                    pad = ((0,0),(50,0))
                ),
                sg.Column(
                    [
                        [
                            sg.Text('Reports',**ap_style.menu_text),
                        ],
                        [
                            sg.Button(key='_OPTION1_', button_text='Daily S̲ales',**ap_style.menu_button),
                        ],
                        [
                            sg.Button(key='_OPTION2_', button_text='Cash P̲osition',**ap_style.menu_button),
                        ],
                    ],
                    vertical_alignment = 'top', 
                    justification = 'left',
                    pad = ((0,0),(50,0))
                ),
            ]
        ]

        ui_footer_pane_layout = [
            [
                sg.Text('USER:', **ap_style.footer_text),
                sg.Input(key='_USER_ID_', **ap_style.footer_input),
                sg.Text('COUNTER:', **ap_style.footer_text),
                sg.Input(key='_TERMINAL_ID_', **ap_style.footer_input),
                sg.Text('DATE:', **ap_style.footer_text),
                sg.Input(key='_CURRENT_DATE_', **ap_style.footer_input)
            ]
        ]

        ui_top_pane_layout = [
            [
                sg.Image(filename = 'images/al_fareeda_logo.PNG', background_color = 'white', pad = ((55,55),(0,0)))
            ],
        ]

        ui_summary_pane_layout = [
            [
                sg.Image(filename = 'images/grossery.PNG', background_color = 'white', pad = ((0,0),(10,0)))
            ],
            [
                sg.Text('', key='_WELCOME_TEXT_', **ap_style.welcome_text, pad = ((5,5),(10,5))),
            ],
        ]        
        
        ui_bottom_pane_layout = [
            [
                sg.Image(filename = 'images/alignpos_logo.PNG', background_color = 'white', pad = ((52,53),(0,0))),
            ]
        ]
        
        ui_left_panes_layout = [
            [
                sg.Frame('',
                    ui_header_pane_layout, 
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((5,0),(5,0)),
                )     
            ],
            [
                sg.Frame('',
                    ui_detail_pane_layout,
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((5,0),(0,0)),
                )     
            ],
            [
                sg.Frame('',
                    ui_footer_pane_layout, 
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((5,0),(285,0)),
                )     
            ],
        ]

        ui_right_panes_layout = [
            [
                sg.Frame('',
                    ui_top_pane_layout, 
                    background_color = 'white',
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((0,0),(10,0)),
                )     
            ],
            [
                sg.HorizontalSeparator(color = 'white', pad = ((0,0),(7,0))),
            ],
            [
                sg.Frame('',
                    ui_summary_pane_layout, 
                    background_color = 'white',
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((15,0),(2,0)),
                )     
            ],
            [
                sg.HorizontalSeparator(color = 'white', pad = ((0,0),(5,10))),
            ],
            [
                sg.Frame('',
                    ui_bottom_pane_layout, 
                    background_color = 'white',
                    vertical_alignment = 'top',
                    border_width = 0,                   
                    pad = ((0,0),(13,0)),
                )     
            ],
        ]
            
        self.__layout = [
            [
                sg.Menu(menu_def, tearoff=False, font=(("Helvetica", 10))),
                sg.Column(
                    ui_left_panes_layout,
                    key='_LEFT_PANES_',
                    size=(lw,lh),
                    justification = 'Left',
                    vertical_alignment = 'top', 
                    #pad = ((0,0),(0,0)), 
                ),
                sg.Column(
                    ui_right_panes_layout,
                    key='_RIGHT_PANES_',
                    background_color='White',
                    size=(rw,rh), 
                    justification = 'Center',
                    vertical_alignment = 'top', 
                    #pad = ((0,0),(0,0)), 
                )   
            ]      
        ]

    def get_layout(self):
        return self.__layout

    layout = property(get_layout) 


###
if __name__ == "__main__":
    print('***Not an executable module, please call the main script')
