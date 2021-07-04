import PySimpleGUI as sg
import sys
    

window = sg.Window('Window Title', [[sg.Text('My one-shot window.')],      
                 [sg.Yes('Ok'), sg.Yes('Cancel')]])    

event, values = window.read()
print (event, values)
window.close()

