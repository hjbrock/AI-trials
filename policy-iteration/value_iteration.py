# Author: Hannah Brock

from mdp import MDP
from utility import get_meu
import copy

def value_iteration(mdp, max_error, max_iterations):
    discount = mdp.discount*1.0
    rewards = mdp.reward
    max_error = max_error*1.0

    # set up utility vector
    utilities = [ 0.0 for x in range(0,12) ]
    new_utils = [ 0.0 for x in range(0,12) ]
    # iterate
    iterations = []
    while True:
        max_change = float("-inf")
        new_utils = [ 0.0 for x in range(0,12) ]

        for state in mdp.states:
            meu, action = get_meu(mdp, state, utilities)
            new_utils[state] = rewards[state] + (discount*meu)
            change = abs(new_utils[state] - utilities[state])
            if change > max_change:
                max_change = change
        utilities = copy.deepcopy(new_utils)

        iterations.append(copy.deepcopy(new_utils))
        if max_change < (max_error*((1.0-discount)/discount)):
            break
        if len(iterations) == max_iterations:
            break
    return utilities, iterations
