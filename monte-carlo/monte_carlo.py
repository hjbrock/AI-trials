# Author: Hannah Brock

from  wumpus_world import *

def monte_carlo(trials, knowledge):
    """Runs an MC algorithm to determine probabilities for P and W"""
    pits = [0.0]*16
    wumpus = [0.0]*16
    num = 0
    generated = 0
    while num < trials:
        world = generate_world()
        generated += 1
        if not matches_knowledge(world, knowledge):
            continue
        for i in range(0,16):
            if world[i][2]:
                pits[i] += 1
            if world[i][3]:
                wumpus[i] += 1
        num += 1
    print('Generated: ' + str(generated))
    for i in range(0,16):
        pits[i] = pits[i]/num
        wumpus[i] = wumpus[i]/num
    return pits, wumpus
