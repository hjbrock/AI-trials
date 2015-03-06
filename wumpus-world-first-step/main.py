# Author: Hannah Brock

from agents import RandomAgent, LogicalAgent
from simulator import Simulator

# Main script for running the wumpus world simulators

# Run random agent
sim = Simulator(4, RandomAgent())
runs = 100
results = {}
boards = []
# no danger: adjacent pit (not in the space the agent is facing)
boards.append({ 'id':0, 'pits':4, 'ploc':[(1,2),(1,4),(2,4),(3,4)], 'wloc':(4,4), 'gloc':(3,3)  })
# danger: adjacent pit in the space the agent is facing
boards.append({ 'id':1, 'pits':4, 'ploc':[(2,1),(1,4),(2,4),(3,4)], 'wloc':(4,4), 'gloc':(3,3)  })
# danger: adjacent pit in the space the agent is facing
boards.append({ 'id':2, 'pits':4, 'ploc':[(1,2),(2,1),(1,4),(2,4)], 'wloc':(4,4), 'gloc':(3,3)  })
# no danger: but wumpus in adjacent square
boards.append({ 'id':3, 'pits':4, 'ploc':[(4,4),(1,4),(2,4),(3,4)], 'wloc':(1,2), 'gloc':(3,3)  })
# danger: wumpus in square agent is facing
boards.append({ 'id':4, 'pits':4, 'ploc':[(4,4),(1,4),(2,4),(3,4)], 'wloc':(2,1), 'gloc':(3,3)  })
# danger: wumpus in square agent is facing and pit nearby, BUT gold in 1,1
boards.append({ 'id':5, 'pits':4, 'ploc':[(1,2),(1,4),(2,4),(3,4)], 'wloc':(2,1), 'gloc':(1,1)  })
for b in boards:
    sim.new_board(b['pits'], b['ploc'], b['wloc'], b['gloc'])
    rcounts = { 'gold':0, 'not dead':0, 'dead':0 }
    lcounts = { 'gold':0, 'not dead':0, 'dead':0 }
    # Run random agent
    sim.set_agent(RandomAgent())
    print('Running random agent on board ' + str(b))
    for x in range(0,runs):
        res = sim.run()
        if res == Simulator.SUCCESS:
            rcounts['gold'] += 1
        elif res != Simulator.DEAD:
            rcounts['not dead'] += 1
        else:
            rcounts['dead'] += 1
        sim.reset()
    # switch to logical agent
    print('Running logical agent on board ' + str(b))
    lagent = LogicalAgent()
    sim.set_agent(lagent)
    for x in range(0,runs):
        lagent.reset()
        res = sim.run()
        if res == Simulator.SUCCESS:
            lcounts['gold'] += 1
        elif res != Simulator.DEAD:
            lcounts['not dead'] += 1
        else:
            lcounts['dead'] += 1
        sim.reset()
    results[b['id']] = (rcounts, lcounts, sim.world_str())

for b in results:
    print('\n------\nFor board: ')
    print(results[b][2])
    print('\nRandom agent:')
    print('Got gold: ' + str(results[b][0]['gold']))
    print('Survived: ' + str(results[b][0]['not dead']))
    print('Died: ' + str(results[b][0]['dead']))
    print('% Success: ' + str((results[b][0]['not dead']+results[b][0]['gold']) / (1.0*runs)))

    print('\nLogical agent:')
    print('Got gold: ' + str(results[b][1]['gold']))
    print('Survived: ' + str(results[b][1]['not dead']))
    print('Died: ' + str(results[b][1]['dead']))
    print('% Success: ' + str((results[b][1]['not dead']+results[b][1]['gold']) / (1.0*runs)))
