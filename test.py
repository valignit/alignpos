import PySimpleGUI as pSG

layout = [
    [pSG.Column([[pSG.Button(f"Testing{i}", font=("Courier New", -20)),
    pSG.Button(f"Testing{i}", font=("Courier New", -20)),
    pSG.Button(f"Testing{i}", font=("Courier New", -20)),
    ] for i in range(10)],
                scrollable=True,vertical_scroll_only = False, size=(100,100) )]
]
window = pSG.Window("test", layout, margins=(0, 0), size=(300,300))

while True:
    event, values = window.Read()
    if event is None or event == 'Exit':
        break
window.Close()