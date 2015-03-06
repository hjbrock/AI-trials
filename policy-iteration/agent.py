# Author: Hannah Brock

from mdp import MDP
from value_iteration import value_iteration
from utility import get_meu
from policy_iteration import policy_iteration

class ValueIterationAgent:
    """Agent for navigating world from Ch 17"""

    def __init__(self, reward, discount):
        self.mdp = MDP(reward, discount)

    def get_policy(self, max_error, max_iterations):
        """Generate policy based on the given reward, discount, and max
           error for the value iteration process
        """
        # get the utility function
        U, iterations = value_iteration(self.mdp, max_error, max_iterations)
        # find action leading to the highest MEU for each state
        policy = [ MDP.UP for x in range(0,12) ]
        for state in self.mdp.states:
            meu, a = get_meu(self.mdp, state, U)
            policy[state] = a
        return policy, U, iterations

class PolicyIterationAgent:
    """Agent for navigating world from Ch 17"""

    def __init__(self, reward, discount):
        self.mdp = MDP(reward, discount)

    def get_policy(self, max_iterations):
        """Generate policy using policy iteration"""
        return policy_iteration(self.mdp, max_iterations)
