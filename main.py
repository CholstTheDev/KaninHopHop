""" 
    Implementering af Monte Carlo simulering af børnespillet 'KaninHopHop' 
    
    Benytter PySimpleGUI til brugergrænseflade og matplotlib til visualisering
"""
import PySimpleGUI as sg
import simulation as sim
import game_settings
import analysis

def Start():
    layout = [[sg.Text('Enter number of players:'), sg.Input('3')],
            [sg.Text('Enter number of rabbits:'), sg.Input('20')],
            [sg.Text('Enter number of iterations:'), sg.Input('1000')],
            [sg.Text('Variant: '), sg.Combo(['normal', 'fast', 'slow'], default_value='normal', readonly=True), 
             sg.Text('Graftype'), sg.Combo(['Histogram (p%)', 'Histogram (sum)'], default_value='Histogram (p%)', readonly=True)],
            [sg.Button('Start simulation')]]

    window = sg.Window('Kanin Hop Hop - Monte Carlo simulering', layout = layout,finalize = True)


    while True:
        event,value = window.read()

        if event == sg.WIN_CLOSED:
            break



Start()