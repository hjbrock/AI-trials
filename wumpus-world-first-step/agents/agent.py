# Author: Hannah Brock

class WumpusAgent:
    """An interface for a wumpus agent"""
    LEFT = 0
    RIGHT = 1
    FORWARD = 2
    GRAB = 3

    def get_action(self, percept):
        """Receive a percept,  where the percept is
        an array of booleans indicating whether or
        not the given item is perceived at that
        room:

        [ breeze, glitter, bump, scream, stench ]


        Returns an action of LEFT, RIGHT, FORWARD,
        GRAB (all integers)
        """
        return 0 
