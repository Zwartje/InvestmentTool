import yfinance as yf
import PySimpleGUI as sg
import matplotlib.pyplot as plt


def draw_plot(ticker_name):
    stock_ticker = yf.Ticker(ticker_name)
    hist = stock_ticker.history(period="max")
    plt.plot(hist['Close'])
    plt.show(block=False)


#    plt.show(block=False)

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
