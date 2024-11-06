"""Handles simulating 'Kanin Hop Hop."""
import random
import game_settings as gs

SimSettings = gs.Simulation_Settings(simulation_iterations=1000, player_count=5)

def Run_Simulations(settings: gs.Simulation_Settings) -> list:
    """
    Returns list of winners. The length of the list is equal to simulation count.
    """
    #sanity check
    if not isinstance(settings.player_count, int):
        print("You have to enter a whole number for the player count")
        return
    
    if not (1 < settings.player_count <= 10):
        print("Player count should be between 2 - 10")
        return

    if not isinstance(settings.rabbit_count, int):
        print("You have to enter a whole number for the rabbit count")
        return
    
    if not (1 <= settings.rabbit_count <= 100):
        print("Rabbit count should be between 2 - 100")
        return
    
    #run simulations
    sim_counter = 0
    results = [] #A list of the winner. Sums can be created after the fact
    while sim_counter <= settings.simulation_iterations:
        results.append(Single_Simulation(settings))
        sim_counter += 1
    
    #return game results as list of ints (single winner) and lists (multiple winners)
    return results


def Single_Simulation(settings: gs.Simulation_Settings):
    """
    Logic for a single game. Returns the winner(s) in a list.
    """
    rabbit_holes = [False, False, False, False, False]
    current_player = 0
    player_scores = [0] * settings.player_count
    rabbit_counter = settings.rabbit_count

    while rabbit_counter >= 0: # Game logic. Runs until there are no more rabbits
        diceRoll = random.randint(0,5) 

        # if the roll is rabbit
        if diceRoll == 5:
            if settings.variant == gs.Variant.NORMAL or gs.Variant.FAST: # in the first to variations (0 and 1 in the enum), the player is awarded a rabbit
                player_scores[current_player] += 1
                rabbit_counter -= 1

                if settings.variant == gs.Variant.FAST: # with the fast game, the player gets to go again
                    current_player -= 1
            else:
                if player_scores[current_player] > 0: # in the slow game, the player simply loses a rabbit, and one is added back
                    player_scores[current_player] -= 1 
                    rabbit_counter += 1
        # if the roll is not "rabbit"
        else:
            if not rabbit_holes[diceRoll]: # Check if there is a rabbit in the hole
                rabbit_holes[diceRoll] = True # If there isn't, no points are earned
            else:
                player_scores[current_player] += 1 # if there is, a single point is earned
            
            rabbit_counter -= 1

        current_player += 1 # The player counter is iterated
        if current_player >= settings.player_count:
            current_player = 0
    
    highest_score = max(player_scores) #Get the highest score of the game

    if player_scores.count(highest_score) > 1: # Check if there is more than one winner
        winner_list = []
        for i in range(0, settings.player_count):
            if player_scores[i] == highest_score:
                winner_list.append(i)
        return winner_list
    else:
        return player_scores.index(highest_score)
    

def Tally_Simulations(settings: gs.Simulation_Settings, results: list):
    """
    Takes a list of results, and finds the sum of each players victories
    """
    player_scores = [0] * settings.player_count

    for x in range(0, len(results)):
        if isinstance(results[x], list):
            for y in range(0, len(results[x])):
                player_scores[results[x][y]] += 1
        else:
            player_scores[results[x]] += 1

    print(player_scores)
    for i in range(0,settings.player_count):
        print(f"Player {i} won {player_scores[i]} times out of {settings.simulation_iterations} games. p = {player_scores[i]/settings.simulation_iterations}")


#Tally_Simulations(SimSettings, Run_Simulations(SimSettings))

#Run_Simulation(3, 20)


