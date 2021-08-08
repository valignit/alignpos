import PySimpleGUI as sg

column = [
            [
                sg.Image(filename='image_1.png', key='Image1'),
                sg.Image(filename='image_2.png', key='Image2'),
                sg.Image(filename='image_3.png', key='Image3'),
                sg.Image(filename='image_4.png', key='Image4'),
                sg.Image(filename='image_5.png', key='Image5'),
            ]
]
layout = [[sg.Column(column, size=(300, 120), scrollable=True),
          ]]
window = sg.Window('test', layout, finalize=True)

while True:

    event, values = window.read()
    print(event, values)
    if event == sg.WINDOW_CLOSED:
        break

window.close()