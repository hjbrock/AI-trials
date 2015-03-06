# Author: Hannah Brock

import random

def generate_world():
    """Generates a random wumpus world"""
    gold = random.randint(1,15)
    wumpus = -10000
    while wumpus == -10000:
        i = random.randint(1,15)
        if i != gold:
            wumpus = i
    
    pits = []
    for x in range(1,16):
        if random.random() <= 0.2:
            pits.append(x)
    
    world = []
    for x in range(0,16):
        breeze = calc_breeze(x, pits)
        stench = calc_stench(x, wumpus)
        # X, Y, Pit, Wumpus, Gold, Breeze, Stench
        cell = [ x % 4, x / 4, x in pits, x == wumpus, x == gold, breeze, stench ]
        world.append(cell)
    return world

def calc_breeze(x, pits):
    breeze = False
    if x % 4 == 0:
        breeze = (x+1) in pits
    elif x % 4 == 3:
        breeze = (x-1) in pits
    else:
        breeze = ((x-1) in pits) or ((x+1) in pits)
    if x / 4 == 0:
        breeze = breeze or ((x+4) in pits)
    elif x / 4 == 3:
        breeze = breeze or ((x-4) in pits)
    else:
        breeze = breeze or ((x+4) in pits) or ((x-4) in pits)
    return breeze
    
def calc_stench(x, wumpus):
    s = False
    if x % 4 == 0:
        s = ((x+1) == wumpus)
    elif x % 4 == 3:
        s = ((x-1) == wumpus)
    else:
        s = ((x-1) == wumpus) or ((x+1) == wumpus)
    if x / 4 == 0:
        s = s or ((x+4) == wumpus)
    elif x / 4 == 3:
        s = s or ((x-4) == wumpus)
    else:
        s = s or ((x+4) == wumpus) or ((x-4) == wumpus)
    return s

def get_neighbors(i):
    """Gets the list of neighbors for a given cell index"""
    n = [ i+1, i-1, i+4, i-4, i+4+1, i+4-1, i-4+1, i-4-1]
    x = i % 4
    y = i /4
    if x == 0:
        n.remove(i-1)
        n.remove(i+4-1)
        n.remove(i-4-1)
    if x == 3:
        n.remove(i+1)
        n.remove(i+4+1)
        n.remove(i-4+1)
    if y == 0:
        n.remove(i-4)
        if (i-4+1) in n: 
            n.remove(i-4+1)
        if (i-4-1) in n: 
            n.remove(i-4-1)
    if y == 3:
        n.remove(i+4)
        if (i+4+1) in n: 
            n.remove(i+4+1)
        if (i+4-1) in n: 
            n.remove(i+4-1)
    return n

def print_world(world):
    print('\nWorld:')
    for y in range(0,4):
        j = 3 - y
        for x in range(0,4):
            i = x + (4*j)
            print('\t'),
            if world[i][2]:
                print('P'),
            if world[i][5]:
                print('B'),
        print('')

def place_agent(world):
    """Return the index of a safe place for the agent"""
    agent = -1
    while agent == -1:
        i = random.randint(0,15)
        if not world[i][2] and not world[i][3]:
            agent = i
    return agent

def matches_knowledge(world, knowledge):
    """Checks if a wumpus world matches some knowledge"""
    # fact in form: [x, y, Pit, Wumpus, Gold, Breeze, Stench]
    for fact in knowledge:
        index = fact[0] + (4*fact[1])
        cell = world[index]
        for x in range(0,len(cell)):
            if cell[x] != fact[x]:
                return False
    return True

