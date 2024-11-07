""" 
    Implementering af Monte Carlo simulering af børnespillet 'KaninHopHop' 
    
    Benytter PySimpleGUI til brugergrænseflade og matplotlib til visualisering
"""
import PySimpleGUI as sg
import simulation as sim
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import game_settings as gs
import analysis

# Global variables are only used for the sake of the progress bar
window = None
sim_settings = None
progress = 0.0
inv_iteration = 1/1000

def Start():
    """
    Sets up PySimpleGUI, and executes the program loop
    """
    # Import of global variables for the progress bar
    global window
    global sim_settings
    global inv_iteration
    global progress

    # The layout of the program
    layout = [[sg.Text('Enter number of players:'), sg.Input('3',size=10, key=('-PLAYER_COUNT-'), enable_events=True),
            sg.Text('Enter number of rabbits:'), sg.Input('20',size=10, key=('-RABBIT_COUNT-'), enable_events=True),
            sg.Text('Enter number of iterations:'), sg.Input('1000',size=10, key='-ITERATION_COUNT-', enable_events=True)],
            [sg.Text('Variant: '), sg.Combo(['normal', 'fast', 'slow'], default_value='normal', key='-VARIANT-', readonly=True, change_submits=True), 
             sg.Text('Graphtype'), sg.Combo(['Histogram (p%)', 'Histogram (sum)'], default_value='Histogram (p%)', key='-GRAPH_TYPE-', readonly=True, change_submits=True)],
            [sg.Button('Start simulation', key='-START_SIMULATION-')],
            [sg.ProgressBar(max_value=1000, key='-PROGRESS_BAR-', visible=True, size_px=(800, 20))],
            [sg.Canvas(key='-CANVAS-')]]

    window = sg.Window('Kanin Hop Hop - Monte Carlo simulering', layout = layout,finalize = True,location=(100,100))
    window.size = (800, 700)

    playerLimits = (2,20) # Limits for how many players can be in the game. Stops at 20, because the legend can no longer be properly displayed
    rabbitLimits = (6, 99999) # Limits the number of rabbits
    iterationLimits = (1, 999999) # Limits the number of games

    sim_settings = gs.Simulation_Settings() # Instantiate a game settings class, with default settings

    winner_history_raw = None # A list of either ints or lists of ints, with a length equal to simulation iterations
    winner_history_sum = None # A list of lists. The lists contained are the length of the player count. Used to display cumulative sum of victories
    winner_history_p = None # Same as previous, but with chance of winning.

    figure_canvas_agg = None

    while True: # The rest of the program stays within this loop, and listens for events
        event,values = window.read()

        if event == sg.WIN_CLOSED:
            break
        # region enforcing types for input
        elif event == '-PLAYER_COUNT-':
            input = values['-PLAYER_COUNT-']
            if input.isdigit():
                newValue = int(input)
                sim_settings.player_count = newValue   
            elif input == '':
                pass  
            else:
                window['-PLAYER_COUNT-'].update(str(sim_settings.player_count))
        elif event == '-RABBIT_COUNT-':
            input = values['-RABBIT_COUNT-']
            if input.isdigit():
                newValue = int(input)
                sim_settings.rabbit_count = newValue   
            elif input == '':
                pass  
            else:
                window['-RABBIT_COUNT-'].update(str(sim_settings.rabbit_count))
        elif event == '-ITERATION_COUNT-':
            input = values['-ITERATION_COUNT-']
            if input.isdigit():
                newValue = int(input)
                sim_settings.simulation_iterations = newValue
            elif input == '':
                pass  
            else:
                window['-ITERATION_COUNT-'].update(str(sim_settings.simulation_iterations))
        # endregion
        elif event == "-START_SIMULATION-":
            # region Sanity checks
            if values['-PLAYER_COUNT-'] == '': #Check the player input
                Simple_Error(f"Player field is empty. Should be between {playerLimits[0]} - {playerLimits[1]}")
                sim_settings.player_count = playerLimits[0]
                window['-PLAYER_COUNT-'].update(str(sim_settings.player_count))
            elif int(values['-PLAYER_COUNT-']) < playerLimits[0]:
                Simple_Error(f"Too few players. Should be between {playerLimits[0]} - {playerLimits[1]}")
                sim_settings.player_count = playerLimits[0]
                window['-PLAYER_COUNT-'].update(str(sim_settings.player_count))
            elif int(values['-PLAYER_COUNT-']) > playerLimits[1]:
                Simple_Error(f"Too many players. Should be between {playerLimits[0]} - {playerLimits[1]}")
                sim_settings.player_count = playerLimits[1]
                window['-PLAYER_COUNT-'].update(str(sim_settings.player_count))
            elif values['-RABBIT_COUNT-'] == '': # Check the rabbit input
                Simple_Error(f"Rabbit field is empty. Should be between {rabbitLimits[0]} - {rabbitLimits[1]}")
                sim_settings.rabbit_count = rabbitLimits[0]
                window['-RABBIT_COUNT-'].update(str(sim_settings.rabbit_count))
            elif int(values['-RABBIT_COUNT-']) < rabbitLimits[0]:
                Simple_Error(f"Too few rabbits. Should be between {rabbitLimits[0]} - {rabbitLimits[1]}")
                sim_settings.rabbit_count = rabbitLimits[0]
                window['-RABBIT_COUNT-'].update(str(sim_settings.rabbit_count))
            elif int(values['-RABBIT_COUNT-']) > rabbitLimits[1]:
                Simple_Error(f"Too many rabbits. Should be between {rabbitLimits[0]} - {rabbitLimits[1]}")
                sim_settings.rabbit_count = rabbitLimits[1]
                window['-RABBIT_COUNT-'].update(str(sim_settings.rabbit_count))
            elif values['-ITERATION_COUNT-'] == '': # Check the iteration input
                Simple_Error(f"Iteration field is empty. Should be between {iterationLimits[0]} - {iterationLimits[1]}")
                sim_settings.simulation_iterations = iterationLimits[0]
                window['-ITERATION_COUNT-'].update(str(sim_settings.simulation_iterations))
            elif int(values['-ITERATION_COUNT-']) < iterationLimits[0]:
                Simple_Error(f"Too few iterations. Should be between {iterationLimits[0]} - {iterationLimits[1]}")
                sim_settings.simulation_iterations = iterationLimits[0]
                window['-ITERATION_COUNT-'].update(str(sim_settings.simulation_iterations))
            elif int(values['-ITERATION_COUNT-']) > iterationLimits[1]:
                Simple_Error(f"Too many iterations. Should be between {iterationLimits[0]} - {iterationLimits[1]}")
                sim_settings.simulation_iterations = iterationLimits[1]
                window['-ITERATION_COUNT-'].update(str(sim_settings.simulation_iterations))
            else:
            # endregion
                window['-PROGRESS_BAR-'].update(current_count=0)
                window['-PROGRESS_BAR-'].MaxValue

                progress = 0.0
                inv_iteration = 1/sim_settings.simulation_iterations*1000 
                winner_history_raw = sim.Run_Simulations(sim_settings, Increment_Progress)
                window['-PROGRESS_BAR-'].update(current_count=0)
                winner_history_sum = Sum_Victories(sim_settings, winner_history_raw)
                winner_history_p = Sum_Victories_P(sim_settings, winner_history_sum)

                if figure_canvas_agg:
                        figure_canvas_agg.get_tk_widget().forget()

                if values['-GRAPH_TYPE-'] == 'Histogram (p%)':
                    #fig = analysis.CreateHistogramFig(sim_settings, winner_history_p)
                    fig = analysis.Create_Fig_P(sim_settings, winner_history_p)
                else:
                    fig = analysis.Create_Fig_Sum(sim_settings, winner_history_sum)

                figure_canvas_agg = analysis.draw_figure(window["-CANVAS-"].TKCanvas, fig)
        elif event == '-GRAPH_TYPE-':
            if winner_history_raw:
                if figure_canvas_agg:
                        figure_canvas_agg.get_tk_widget().forget()
                if values['-GRAPH_TYPE-'] == 'Histogram (p%)':
                    fig = analysis.Create_Fig_P(sim_settings, winner_history_p)
                else:
                    fig = analysis.Create_Fig_Sum(sim_settings, winner_history_sum)
                
                figure_canvas_agg = analysis.draw_figure(window["-CANVAS-"].TKCanvas, fig)
        elif event == '-VARIANT-':
            if values['-VARIANT-'] == 'normal':
                sim_settings.variant = gs.Variant.NORMAL
            elif values['-VARIANT-'] == 'fast':
                sim_settings.variant = gs.Variant.FAST
            else:
                sim_settings.variant = gs.Variant.SLOW

def Sum_Victories(settings: gs.Simulation_Settings, raw_history: list):
    """
    Takes a list of raw game results from a flat list and finds the sum of each players victories
    (value is winning player(s) in either int or list of ints)
    """
    #summed_history = [[0]] * settings.player_count
    summed_history = [[0] for _ in range(settings.player_count)]

    for x in range(0, len(raw_history)):
        if isinstance(raw_history[x], list):
            for i in range(0, settings.player_count):
                if i in raw_history[x]:
                    summed_history[i].append(summed_history[i][-1]+1)
                else:
                    summed_history[i].append(summed_history[i][-1])
        else:
            for i in range(0,settings.player_count):
                if i == raw_history[x]:
                    summed_history[i].append(summed_history[i][-1]+1)
                else:
                    summed_history[i].append(summed_history[i][-1])

    return summed_history               

def Sum_Victories_P(settings: gs.Simulation_Settings, summed_history: list):
    """
    Takes a list of summed game results from a list of lists and finds the chance of each players victories calculated after each game
    """
    #summed_history = [[0]] * settings.player_count
    summed_history_p = [[] for _ in range(settings.player_count)]

    for x in range(0, len(summed_history)):
        for y in range(1, len(summed_history[x])):
            summed_history_p[x].append(float(summed_history[x][y])/float(y))

    return summed_history_p

def Simple_Error(text: str):
    """Displays a simple error"""
    display_text = 'An error occured'
    if text:
        display_text = text
    sg.popup_error(display_text, title="Error")

def Increment_Progress():
    """Increments the progress bar."""
    global window
    global sim_settings
    global progress
    global inv_iteration
    progress += inv_iteration
    #print(progress)
    window['-PROGRESS_BAR-'].update(current_count=int(progress))


Start()