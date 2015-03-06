# Author: Hannah Brock
# Class: CS 5300, Fall 2014
#
# For usage information, see simulator.py

import os, random, time

class CleaningAgent:
    """A simple cleaning agent."""

    CLEAN = -1
    
    def __move__(self):
        """Pick a direction to move.
        Returns a choice in [0,7]
        """
        return random.randint(0,7)

    def do_step(self, squareIsClean):
        """Notify the agent that a new time step has
         begun. Agent chooses to clean or move.

       Returns an integer. -1 for cleaning,
       [0-7] for a move.
        """
        if squareIsClean:
            return self.CLEAN
        return self.__move__()

class CleaningSimulator:
    """Simulates an environment containing n cleaning agents in an m x n grid
    with each square on the grid having probability p of being dirty.
    """
    __moves__ = [ (-1,-1), # move upper left
                  (-1, 0), # move left
                  (-1, 1), # move lower left
                  ( 0, 1), # move down
                  ( 1, 1), # move lower right
                  ( 1, 0), # move right
                  ( 1,-1), # move upper right
                  ( 0,-1)  # move up
                ]

    def __init__(self, rows, cols, prob_dirty, num_agents, visualize, delay, print_moves, max_time):
        """Set up the grid.

        Arguments:
        rows -- number of rows in the grid
        cols -- number of columns in the grid
        prob_dirty -- float, probability each square is dirty
        num_agents -- number of cleaning agents
        visualize -- boolean, visualize the run
        delay -- float, delay in seconds for each step of the visualization
        """
        self.visualize = visualize
        self.delay = delay
        self.rows = rows
        self.cols = cols
        self.prob_dirty = prob_dirty
        self.num_agents = num_agents
        self.print_moves = print_moves
        self.max_time = max_time
        self.reset()

    def reset(self):
        """Reset the grid to its starting state."""
        self.grid = [[0 for x in xrange(self.cols)] for x in xrange(self.rows)]
        for y in range(0, self.rows):
            for x in range(0, self.cols):
                if (random.random() < self.prob_dirty):
                    self.grid[y][x] = 1
        self.agents = [ CleaningAgent() for x in xrange(self.num_agents) ]
        self.agent_grid = { agent: (0, 0) for agent in self.agents }
    
    def is_grid_clean(self):
        """Checks if all squares are clean"""
        for y in self.grid:
            for x in y:
                if x == 1:
                    return False
        return True

    def get_percent_clean(self):
        """Returns the percentage of cells clean"""
        total = self.rows * self.cols
        clean = 0.0
        for x in range(0, self.rows):
            for y in range(0, self.cols):
                if self.grid[x][y] == 0:
                    clean += 1.0
        return clean / total

    def print_grid(self):
        """Prints the grid to the screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print '|',
        for col in range(0, len(self.grid[0])):
            print '=',
        print '|'
        for y in range(0, len(self.grid)):
            print '|',
            for x in range(0, len(self.grid[0])):
                if (y,x) in self.agent_grid.values():
                    print 'X',
                elif self.grid[y][x] == 1:
                    print '-',
                else:
                    print ' ',
            print '|'
        print '|',
        for col in range(0, len(self.grid[0])):
            print '=',
        print '|'

    def run(self):
        """Runs the simulation and returns stats"""
        steps = 0
        moves = 0
        if self.visualize:
            self.print_grid()
        while not self.is_grid_clean() and steps < self.max_time:
            steps = steps + 1
            choices = {}
            # get all of the choices, then apply consequences to the environment
            for agent in self.agents:
                loc = self.agent_grid[agent]
                choices[agent] = agent.do_step(self.grid[loc[0]][loc[1]])
            
            for agent in choices:
                loc = self.agent_grid[agent]
                choice = choices[agent]
                if choice == agent.CLEAN:
                    self.grid[loc[0]][loc[1]] = 0
                    if self.print_moves:
                        print 'CLEAN'
                        time.sleep(self.delay)
                else:
                    moves = moves + 1
                    new_loc = ( loc[0] + self.__moves__[choice][0], loc[1] + self.__moves__[choice][1] )
                    if new_loc[0] >= 0 and new_loc[0] < len(self.grid) and new_loc[1] >= 0:
                        if new_loc[1] < len(self.grid[0]):
                            self.agent_grid[agent] = new_loc
                    if self.print_moves:
                        print 'Move: (' + str(self.__moves__[choice][1]) + ',',
                        print str(self.__moves__[choice][0]) + ')'
                        time.sleep(self.delay)
            if self.visualize:
                self.print_grid()
                time.sleep(self.delay)
        return (steps, moves, self.get_percent_clean())

