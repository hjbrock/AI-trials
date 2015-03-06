# Author: Hannah Brock

from wumpus_world import WumpusWorld
from agents import WumpusAgent
import operator, copy

class Simulator:
    """Simulator class for Wumpus World"""
    OK = 0
    BUMP = 1
    SUCCESS = 2
    DEAD = 3

    def __init__(self, num_pits, agent):
        self.world = WumpusWorld(num_pits)
        self.num_pits = num_pits
        self.agent = agent
        self.agent_loc = (1,1)
        self.agent_dir = (1,0) # facing right

    def __move__(self):
        new_loc = tuple(map(operator.add, self.agent_dir, self.agent_loc))
        if not self.world.in_range(new_loc):
            return Simulator.BUMP
        self.agent_loc = new_loc
        if self.world.has_wumpus(self.agent_loc):
            return Simulator.DEAD
        if self.world.has_pit(self.agent_loc):
            return Simulator.DEAD
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
            return res
        if action == WumpusAgent.GRAB:
            if self.world.has_gold(self.agent_loc):
                return Simulator.SUCCESS
        return Simulator.OK

    def __facing__(self):
        new_loc = tuple(map(operator.add, self.agent_dir, self.agent_loc))
        return 'F' + str(new_loc[0]) + str(new_loc[1])

    def set_agent(self, agent):
        self.agent = agent

    def world_str(self):
        board = []
        final = ''
        for y in range(1, len(self.world.world[0])):
            row = ''
            for x in range(1, len(self.world.world)):
                stuff = copy.deepcopy(self.world.world[x][y])
                if self.agent_loc == (x, y):
                    stuff.append('A')
                row += ' ' + str(stuff)
            board.append(row)
        for row in board:
            final = row + '\n' + final
        return final

    def print_world(self):
        print(self.world_str())

    def run(self):
        res = Simulator.OK
        # get action from the agent
        percept = copy.deepcopy(self.world.get_percept(self.agent_loc))
        percept.append(self.__facing__())
        action = self.agent.get_action(percept)
        # execute action
        return self.__execute_action__(action)

    def reset(self):
        self.agent_loc = (1,1)
        self.agent_dir = (1,0)

    def new_random_board(self):
        self.world = WumpusWorld(self.num_pits, True)
        self.reset()

    def new_board(self, num_pits, pit_loc, w_loc, g_loc):
        self.world = WumpusWorld(num_pits, pit_loc, w_loc, g_loc)
        self.reset()
