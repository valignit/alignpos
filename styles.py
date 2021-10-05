###
# Common UI Styles             
class ElementStyle:
   
    page_title:  dict = {           
                        'font':("Calibri 18 bold"),
                        'size':(15,1),
                        'text_color': 'grey30',
                    }

    pad_button_small:  dict = {
                        'size':(3, 1), 
                        'font':('Calibri 12 bold'), 
                        'button_color': ('grey20','grey80'),
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

    action_button_small:  dict = {
                        'size':(7, 1), 
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

    summary_text:  dict = {           
                        'font':("Helvetica 11"),
                        'size':(10,1)  ,
                        'background_color': 'White'
                    }
                    
    menu_text:  dict = {           
                        'font':('Calibri 16'), 
                        'size':(10,1),
                    }
                    
    menu_button:  dict = {
                        'size':(28, 1), 
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
                        'font':("Helvetica 9"),
                        'size':(9,1),
                        'justification': 'left',
                    }    

    footer_input:  dict = {           
                        'readonly':True, 
                        'justification':'left', 
                        'disabled_readonly_text_color':'grey32', 
                        'disabled_readonly_background_color':'grey89', 
                        'font':("Helvetica", 9),
                        'size':(12,1)                        
                    }

    search_text:  dict = {           
                        'font':("Helvetica 11"),
                        'size':(9,1),
                        'justification': 'left'
                    }    

    search_input:  dict = {           
                        'justification':'left', 
                        'font':("Helvetica", 10),
                        'background_color': 'White',
                        'enable_events':True                    
                    }

    search_input_ar:  dict = {           
                        'justification':'right', 
                        'font':("Helvetica", 10),
                        'background_color': 'White',
                        'enable_events':True                    
                    }
                    
    search_button:  dict = {
                        'size':(7, 1), 
                        'font':('Calibri 11 bold'),
                        'button_color':('grey20','grey80'),
                        'use_ttk_buttons': True
                    }

    search_button_wide:  dict = {
                        'size':(29, 1), 
                        'font':('Calibri 11 bold'), 
                        'button_color': ('grey20', 'grey80'),
                        'use_ttk_buttons': True
                    }

    search_button_short:  dict = {
                        'size':(12, 1), 
                        'font':('Calibri 12 bold'), 
                        'button_color': ('grey20', 'grey80'),
                        'use_ttk_buttons': True
                    }

    search_button_medium:  dict = {
                        'size':(16, 1), 
                        'font':('Calibri 12 bold'), 
                        'button_color': ('grey20', 'grey80'),
                        'use_ttk_buttons': True
                    }

    fav_button:  dict = {
                        'font':('Calibri 11 bold'), 
                        'button_color': ('grey20', 'grey80'),
                        'use_ttk_buttons': True
                    }

    welcome_text:  dict = {           
                        'font':("Calibri 13"),
                        'size':(20,15),
                        'background_color': 'White'
                    }

