# Author: Hannah Brock

from agent import WumpusAgent
import random

class RandomAgent(WumpusAgent):
    """Implementation of a random wumpus agent"""

    def get_action(self, percept):
        """See WumpusAgent.get_action for further
        documentation.
        """
        if 'Gl11' in percept:
            return WumpusAgent.GRAB
        return random.randint(0, 2)
