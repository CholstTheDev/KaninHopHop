"""Analysis of the outcomes of the simulation."""
import matplotlib.pyplot as plt
import numpy as np

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


def CreateHistogramFig(playerCount, winnerList):
    playerBins = []
    for i in range(0, playerCount+1):
        playerBins.append(i)
    
    #histogram = np.histogram(winnerList, bins)
    plt.hist(winnerList, playerBins)
    plt.title("Histogram over winners")
    plt.show()

        
    
    #return fig

#CreateHistogramFig(3, [0,2,2,2,2,2,2,2,1])