"""Analysis of the outcomes of the simulation."""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def Create_Fig_P(settings, winnerList):
    fig = plt.figure(figsize=(8,6))
    
    for i, sublist in enumerate(winnerList):
        plt.plot(sublist, label=f'Player {i + 1}') 

    plt.xlabel("No. of games")
    plt.ylabel("Probability of winning [%]")
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

        
def draw_figure(canvas, figure):
    """Draws the matplotlib figure onto a Tkinter canvas."""
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg