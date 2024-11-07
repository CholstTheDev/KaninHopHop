"""Analysis of the outcomes of the simulation."""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import game_settings as gs

def GenerateSumList(playerCount, winnerList, simulationLimit):
    """
    Converts a list of winners, to a nested list, that keeps track of wins over 'time'
    """
    playerHistogramScores = []
    for i in range(0, playerCount+1):
        playerHistogramScores.append([])
        
        iterationCounter = 0
        currentScoreCounter = 0
        while iterationCounter <= simulationLimit:
            if winnerList[iterationCounter] == i:
                currentScoreCounter += 1
            playerHistogramScores[i].append(currentScoreCounter)
                
    
    return playerHistogramScores


"""def CreateHistogramFig(playerCount, winnerList):
    playerBins = []
    for i in range(0, playerCount+1):
        playerBins.append(i)
    
    fig = plt.subplot()
    fig.hist(winnerList, playerBins)
    fig.title("Histogram over winners")
    fig.show()
    return fig"""


def Create_Fig_P(settings, winnerList):
    fig = plt.figure(figsize=(8,6))
    
    for i, sublist in enumerate(winnerList):
        plt.plot(sublist, label=f'Player {i + 1}') 

    plt.xlabel("No. of games")
    plt.ylabel("p%")
    plt.title("p% chance of winning")
    plt.legend() 

    return fig

def Create_Fig_Sum(settings, winnerList):
    fig = plt.figure(figsize=(8,6))
    
    for i, sublist in enumerate(winnerList):
        plt.plot(sublist, label=f'Player {i + 1}') 

    plt.xlabel("No. of games")
    plt.ylabel("Cumulative Victories")
    plt.title("Sum of victories")
    plt.legend() 

    return fig

def CreateHistogramFig(settings: gs.Simulation_Settings, winnerList):
    playerBins = list(range(settings.player_count + 1))  # Define the bin edges based on player count


    # Create a figure and an axis
    fig, ax = plt.subplots()  # 'fig' is the figure, 'ax' is the subplot axis
    
    # Plot the histogram on the axis
    ax.hist(winnerList, bins=playerBins)
    ax.set_title("Histogram of Winners")  # Set title on the axis
    ax.set_xlabel("Player Number")
    ax.set_ylabel("Frequency")

    # Display the plot
    #plt.show()  # Show the entire figure window
    return fig

        
def draw_figure(canvas, figure):
    """Draws the matplotlib figure onto a Tkinter canvas."""
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


#CreateHistogramFig(3, [0,2,2,2,2,2,2,2,1])