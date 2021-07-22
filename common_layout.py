import PySimpleGUI as sg


###
# Common UI Styles             
class ElementStyle:

    page_title:  dict = {           
                        'font':("Calibri 18 bold"),
                        'size':(10,1),
                        'text_color': 'grey30',
                    }

    pad_button:  dict = {
                        'size':(4, 2), 
                        'font':('Calibri 11 bold'), 
                        'button_color': ('grey20','grey80'),
                 }

    pad_button_wide:  dict = {
                        'size':(10, 2), 
                        'font':('Calibri 11 bold'), 
                        'button_color': ('grey20','grey80'),
                      }

    nav_button:  dict = {
                        'size':(5, 1), 
                        'font':('Calibri 11 bold'), 
                        'button_color': ('grey20','grey80'),
                        'use_ttk_buttons': True
                 }

    nav_button_wide:  dict = {
                        'size':(8, 1), 
                        'font':('Calibri 11 bold'), 
                        'button_color': ('grey20','grey80'),
                        'use_ttk_buttons': True
                      }
                    
    action_button:  dict = {
                        'size':(10, 1), 
                        'font':('Calibri 11 bold'), 
                        'button_color': ('grey20', 'grey80'),
                        'use_ttk_buttons': True
                    }

    exit_button:  dict = {
                        'size':(10, 1), 
                        'font':('Calibri 11 bold'), 
                        'button_color': ('grey20', 'grey80'),
                        'use_ttk_buttons': True
                    }

    menu_button:  dict = {
                        'size':(30, 1), 
                        'font':('Calibri 16'), 
                        'button_color': ('grey20', 'grey80'),
                        'use_ttk_buttons': True
                    }

    summary_text:  dict = {           
                        'font':("Helvetica 11"),
                        'size':(10,1)  ,
                        'background_color': 'White'
                    }
                    
    summary_text_bold:  dict = {           
                        'font':("Helvetica 13 bold"),
                        'text_color': "navyblue",
                        'background_color': 'White',
                        'size':(10,1)                        
                        }
                        
    summary_input:  dict = {           
                        'readonly':True, 
                        'justification':'right', 
                        'disabled_readonly_text_color':'grey32', 
                        'disabled_readonly_background_color':'grey89', 
                        'default_text':'0.00' , 
                        'font':("Helvetica", 10),
                        'size':(11,1)                        
                    }

    summary_input_bold:  dict = {           
                            'readonly':True, 
                            'justification':'right', 
                            'disabled_readonly_text_color':"white", 
                            'disabled_readonly_background_color':"navyblue", 
                            'default_text':'0.00' , 
                            'font':("Helvetica 14 bold"),
                            'size':(8,1)                        
                        }

    title_text:  dict = {           
                        'font':("Helvetica 10"),
                        'size':(9,1),
                        'justification': 'right',
                    }    

    title_input:  dict = {           
                        'readonly':True, 
                        'justification':'right', 
                        'disabled_readonly_text_color':'grey32', 
                        'disabled_readonly_background_color':'grey89', 
                        'font':("Helvetica", 10),
                        'size':(9,1)                        
                    }

    header_text:  dict = {           
                        'font':("Helvetica 12"),
                        'size':(9,1),
                        'justification': 'right'
                    }    

    header_input:  dict = {           
                        'readonly':True, 
                        'justification':'right', 
                        'disabled_readonly_text_color':'grey32', 
                        'disabled_readonly_background_color':'grey89', 
                        'font':("Helvetica", 11),
                        'size':(11,1)                        
                    }

    footer_text:  dict = {           
                        'font':("Helvetica 8"),
                        'size':(8,1),
                        'justification': 'left'
                    }    

    footer_input:  dict = {           
                        'readonly':True, 
                        'justification':'right', 
                        'disabled_readonly_text_color':'grey32', 
                        'disabled_readonly_background_color':'grey89', 
                        'font':("Helvetica", 8),
                        'size':(10,1)                        
                    }

    search_text:  dict = {           
                        'font':("Helvetica 11"),
                        'size':(9,1),
                        'justification': 'left'
                    }    

    search_input:  dict = {           
                        'justification':'left', 
                        'font':("Helvetica", 10),
                        'enable_events':True                    
                    }

    search_button:  dict = {
                        'size':(13, 1), 
                        'font':('Calibri 11 bold'),
                        'button_color':('grey20','chocolate2'),
                        'use_ttk_buttons': True
                    }

    welcome_text:  dict = {           
                        'font':("Calibri 13"),
                        'size':(20,15)  ,
                        'background_color': 'White'
                    }
                    


class ItemLookupLayout:
    
    def __init__(self):
        self.__layout = [
            [sg.Listbox(values=[], 
                key='_ITEM_NAME_LIST_', 
                size=(60,6),  font=("Helvetica Bold", 11), 
                select_mode='LISTBOX_SELECT_MODE_SINGLE', 
                enable_events=True, 
                bind_return_key=True)
            ]
        ]

    def get_layout(self):
        return self.__layout
    
    layout = property(get_layout)         