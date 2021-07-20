import PySimpleGUI as sg
from common_layout import ElementStyle as ap_style


###
# Main Menu Layout               
class MainMenuLayout:
    def __init__(self, config, w, h):
        sg.theme(config["ui_theme"])
        lw = w*78/100
        rw = w*22/100

        menu_def = [
                ['&File', ['E&xit']],      
                ['Operations', ['Estimate', 'Billing', 'Invoice', 'Cash']],      
                ['Reports', ['Daily Sales', 'Cash Position']],      
                ['Help', 'About'], 
        ]
                 
        ui_title_pane_layout = [
            [
                sg.Column(
                [
                    [
                        sg.Image(filename = 'alignpos_logo.PNG', background_color = 'white', pad=((0,100),(0,0))),
                        sg.Text('MENU', **ap_style.page_title, pad=((0,50),(0,0))),
                        sg.Text('USER:', **ap_style.title_text),
                        sg.Input(key='_USER_ID_', **ap_style.title_input),
                        sg.Text('COUNTER:', **ap_style.title_text),
                        sg.Input(key='_TERMINAL_ID_', **ap_style.title_input),
                        sg.Text('DATE:', **ap_style.title_text),
                        sg.Input(key='_CURRENT_DATE_', **ap_style.title_input, pad=((0,60),(0,0))),
                        sg.Image(filename = 'al_fareeda_logo.PNG', background_color = 'white')
                    ]
                ], background_color = 'white')
            ]
        ]

        self.__layout = [
            [
                sg.Menu(menu_def, tearoff=False, font=(("Helvetica", 10))),
                sg.Column(ui_title_pane_layout,
                    background_color = 'white',
                    vertical_alignment = 'top', 
                    pad = None, 
                ),
            ],
            [
                sg.Column(
                    [
                        [
                            sg.Button(key='_ESTIMATE_OPTION_', button_text='Estimate',**ap_style.menu_button, pad = ((0,0),(0,0))),
                        ],
                        [
                            sg.Button(key='_BILLING_OPTION_', button_text='Billing',**ap_style.menu_button, pad = ((0,0),(0,0))),
                        ],
                        [
                            sg.Button(key='_INVOICE_OPTION_', button_text='Invoice',**ap_style.menu_button, pad = ((0,0),(0,0))),
                        ],
                        [
                            sg.Button(key='_CASH_OPTION_', button_text='Cash',**ap_style.menu_button, pad = ((0,0),(0,0))),
                        ],
                    ],
                    background_color = 'white',
                    vertical_alignment = 'top', 
                    pad = None
                ),
                sg.Column(
                    [
                        [
                            sg.Button(key='_OPTION1_', button_text='Report1',**ap_style.menu_button, pad = ((0,0),(0,0))),
                        ],
                        [
                            sg.Button(key='_OPTION2_', button_text='Report2',**ap_style.menu_button, pad = ((0,0),(0,0))),
                        ],
                        [
                            sg.Button(key='_OPTION3_', button_text='Report3',**ap_style.menu_button, pad = ((0,0),(0,0))),
                        ],
                    ],
                    background_color = 'white',
                    vertical_alignment = 'top', 
                    pad = None
                ),
            ]
        ]


    def get_layout(self):
        return self.__layout

    layout = property(get_layout) 


###
if __name__ == "__main__":
    print('***Not an executable module, please call the main script')
