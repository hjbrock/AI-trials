# Author: Hannah Brock

# Main testing file for monte carlo

from monte_carlo import *
from wumpus_world import *
import argparse
import sys, random


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--trials', required=False, default='10000', help='MC trials per world')
    parser.add_argument('-n', '--num', required=False, default='100', help='number of worlds to try')
    return parser.parse_args()


### MAIN ###
args = parse_args()
trials = int(args.trials)
num = int(args.num)

mc_died = 0
r_died = 0
for w in range(0, num):
    world = generate_world()
    loc = place_agent(world)
    n = get_neighbors(loc)
    # pick 2 neighbors randomly
    n1 = random.randint(0,len(n)-1)
    n2 = random.randint(0,len(n)-1)
    while n2 == n1:
        n2 = random.randint(0,len(n)-1)
    n1 = n[n1]
    n2 = n[n2]
    n.remove(n1)
    n.remove(n2)
    knowledge = []
    knowledge.append(world[loc])
    knowledge.append(world[n1])
    knowledge.append(world[n2])
    # run monte carlo
    pits, wumpus = monte_carlo(trials, knowledge)
    # pick the least dangerous unknown neighbor
    low = 2.0
    i = -1
    for neighbor in n:
        prob_danger = pits[neighbor] + wumpus[neighbor] - (pits[neighbor]*wumpus[neighbor])
        if prob_danger < low:
            low = prob_danger
            i = neighbor
    # see if the choice is good
    if world[i][2] or world[i][3]:
        mc_died += 1
    # record a random choice for this world as well
    i = random.randint(0, len(n)-1)
    i = n[i]
    if world[i][2] or world[i][3]:
        r_died += 1

# see how we did
print('MC died: ' + str(mc_died/(1.0*num)))
print('Random died: ' + str(r_died/(1.0*num)))
