# Author: Hannah Brock

class MDP:
    """Class representing a Markov decision process, including:
       
       states: set of states, with states[0] being the initial state.
               Each state is an integer, representing the currently
               occupied cell. Cells are indexed as follows:
               ---------------------
               |  8 |  9 | 10 | 11 |
               ---------------------
               |  4 |  5 |  6 |  7 |
               ---------------------
               |  0 |  1 |  2 |  3 |
               ---------------------
       actions: set of actions for each state
       transition model: returning P(s'|s,a)
    """
    UP = 4
    RIGHT = 1
    DOWN = -4
    LEFT = -1

    def __init__(self, reward, discount):
        """Create a new MDP"""
        self.discount = discount
        self.reward = [ 0.0 for x in range(0,12) ]
        self.states = [ x for x in range(0,12) ]
        self.actions = {}
        for state in self.states:
            if state != 11 and state != 7:
                self.actions[state] = [ MDP.UP, MDP.RIGHT, MDP.DOWN, MDP.LEFT ]
                self.reward[state] = reward
            else:
                self.actions[state] = []
                if state == 11:
                    self.reward[state] = 1
                else:
                    self.reward[state] = -1
        self.model = {}
        self.__generate_transition_model__()

    def transition(self, new_state, state, action):
        """Get the probability of reaching each state given a current state
           and a choice of action
        """
        default = [ 0.0 for x in range(0,12) ]
        probs = self.model.get( ( state, action ), default )
        return probs[new_state]

    def get_new_state(self, state, action):
        loc = state + action
        # check for bouncing off walls or trying to enter illegal state (aka state 5)
        if abs((loc % 4) - (state % 4)) == 3:
            loc = state
        if loc < 0 or loc > 11:
            loc = state
        if loc == 5:
            loc = state
        return loc

    def __generate_transition_model__(self):
        """Generate the transition model
           The model is a dictionary from (state, action) pairs to a list of 
           probabilities, with each index being the probability of landing 
           in the corresponding indexed cell
        """
        self.model = {}
        for state in self.states:
            for action in self.actions[state]:
                key = ( state, action )
                probs = self.model.get(key, [ 0.0 for x in range(0,12) ])
                # 0.8 chance of performing chosen action
                loc = self.get_new_state(state, action)
                probs[loc] = 0.8
                # 0.1 chance of going perpendicular in either direction
                perp = [ MDP.UP, MDP.DOWN ]
                if action == MDP.UP or action == MDP.DOWN:
                    perp = [ MDP.RIGHT, MDP.LEFT ]
                for act in perp:
                    loc = self.get_new_state(state, act)
                    probs[loc] += 0.1
                self.model[key] = probs
