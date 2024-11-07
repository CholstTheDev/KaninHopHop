"""Handles simulating 'Kanin Hop Hop."""
import random
import game_settings as gs


def Run_Simulations(settings: gs.Simulation_Settings, progress_callback: callable) -> list:
    """
    Returns list of winners. The length of the list is equal to simulation count.
    """
    #run simulations
    sim_counter = 0
    results = [] #A list of the winner. Sums can be created after the fact
    while sim_counter <= settings.simulation_iterations:
        results.append(Single_Simulation(settings))
        sim_counter += 1
        progress_callback()
    
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

    while rabbit_counter > 0: # Game logic. Runs until there are no more rabbits
        diceRoll = random.randint(0,5) 

        # if the roll is rabbit
        if diceRoll == 5:
            if settings.variant == gs.Variant.NORMAL or settings.variant == gs.Variant.FAST: # in the first to variations (0 and 1 in the enum), the player is awarded a rabbit
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
            if rabbit_holes[diceRoll]: # Check if there is a rabbit in the hole
                player_scores[current_player] += 1 # if there is, a single point is earned
                rabbit_holes[diceRoll] = False
                
            else:
                rabbit_holes[diceRoll] = True # If there isn't, no points are earned
                rabbit_counter -= 1 #a rabbit is moved from the middle
                
            

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