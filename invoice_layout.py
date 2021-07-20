import PySimpleGUI as sg
from common_layout import ElementStyle as ap_style


###
# Invoice Layout               
class InvoiceLayout:
    def __init__(self, config, w, h):
        sg.theme(config["ui_theme"])

        menu_def = [
                ['&File', ['E&xit']],      
                ['Help', 'About'], 
        ]
                
        self.__layout = [
            [
                sg.Menu(menu_def, tearoff=False, font=(("Helvetica", 10)), pad=(200, 1)),
                sg.Text('Invoice', size=(30,1) ,font=("Helvetica", 18), pad=((0,30),(0,0))),
            ]      
        ]


    def get_layout(self):
        return self.__layout

    layout = property(get_layout) 


###
if __name__ == "__main__":
    print('***Not an executable module, please call the main script')
