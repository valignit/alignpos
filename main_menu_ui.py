import PySimpleGUI as sg
import alignpos_ui


###
# Main Menu Window Layout               
class MainMenuWindow:
    def __init__(self, config):
        sg.theme(config["ui_theme"])
        w, h = sg.Window.get_screen_size()
        lw = w*78/100
        rw = w*22/100

        menu_def = [
                ['&File', ['E&xit']],      
                ['Operations', ['Estimate', 'Invoice', 'Weight', 'Price']],      
                ['Reports', ['Daily Sales', 'Cash Position']],      
                ['Help', 'About'], 
        ]
                 
        self.__layout = [
            [
                sg.Text('AlignPos Menu', size=(30,1) ,font=("Helvetica", 18), pad=((0,30),(0,0))),
                sg.Menu(menu_def, tearoff=False, font=(("Helvetica", 10)), pad=(200, 1)),
            ]      
        ]


    def get_layout(self):
        return self.__layout

    layout = property(get_layout) 


###
if __name__ == "__main__":
    print('***Not an executable module, please call the main script')
