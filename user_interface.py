import PySimpleGUI as sg


layout = [[sg.Text('Stock name:'), sg.Input(key='IN')],
          [sg.Button('Plot'), sg.Cancel()]]

window = sg.Window('Have some Matplotlib....', layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    elif event == 'Plot':
        draw_plot(values['IN'])
window.close()
