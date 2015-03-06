# Author: Hannah Brock

from wumpus_world import WumpusWorld
from agents import WumpusAgent
import operator, copy

class Simulator:
    """Simulator class for Wumpus World"""
    OK = 0
    BUMP = 1
    SCREAM = 2
    PIT = 3
    WUMPUS = 4
    SUCCESS = 5
    DEAD = 6

    def __init__(self, num_pits, has_wumpus, agent):
        self.world = WumpusWorld(num_pits, has_wumpus)
        self.agent = agent
        self.agent_loc = (0,0)
        self.agent_dir = (1,0) # facing right
        self.augment = []
        self.wumpus_dead = False
        self.success = False
        self.scream = False
        self.bump = False

    def __move__(self):
        new_loc = tuple(map(operator.add, self.agent_dir, self.agent_loc))
        if not self.world.in_range(new_loc):
            return Simulator.BUMP
        self.agent_loc = new_loc
        if self.world.has_wumpus(self.agent_loc):
            return Simulator.WUMPUS
        if self.world.has_pit(self.agent_loc):
            return Simulator.PIT
        return Simulator.OK

    def __turn__(self, direction):
        x, y = (self.agent_dir[1], self.agent_dir[0])
        if direction == WumpusAgent.LEFT:
            x  = -1 * x
        if direction == WumpusAgent.RIGHT:
            y  = -1 * y
        self.agent_dir = (x, y)

    def __execute_action__(self, action):
        if action == WumpusAgent.LEFT or action == WumpusAgent.RIGHT:
            self.__turn__(action)
        if action == WumpusAgent.FORWARD:
            res = self.__move__()
            if res == Simulator.PIT:
                return Simulator.DEAD
            if res == Simulator.WUMPUS and not self.wumpus_is_dead:
                return Simulator.DEAD
            self.bump = (res == Simulator.BUMP)
        if action == WumpusAgent.SHOOT:
            # TODO
            return Simulator.OK
        if action == WumpusAgent.GRAB:
            if self.world.has_gold(self.agent_loc):
                return Simulator.SUCCESS
        return Simulator.OK

    def print_world(self):
        board = []
        final = ''
        for y in range(0, len(self.world.world[0])):
            row = ''
            for x in range(0, len(self.world.world)):
                stuff = copy.deepcopy(self.world.world[x][y])
                if self.agent_loc == (x, y):
                    stuff.append('A')
                row += ' ' + str(stuff)
            board.append(row)
        for row in board:
            final = row + '\n' + final
        print(final)

    def run(self):
        res = Simulator.OK
        while res == Simulator.OK:
            # get action from the agent
            percept = copy.deepcopy(self.world.get_percept(self.agent_loc))
            percept.extend(self.augment)
            percept.append('A' + str(self.agent_loc[0]) + str(self.agent_loc[1]))
            action = self.agent.get_action(percept)
            # execute action
            res = self.__execute_action__(action)
            # augment next percept with bump or scream if needed
            self.augment = []
            if self.scream:
                self.augment.append('Sc')
            if self.bump:
                self.augment.append('Bp')
        return res

    def reset(self):
        self.wumpus_dead = False
        self.agent_loc = (0,0)
        self.agent_dir = (1,0)
        return
