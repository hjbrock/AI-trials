# Author: Hannah Brock

from mdp import MDP

def get_eu(state, action, mdp, U):
    """Get EU for a given state and action"""
    eu = 0.0
    for new_state in mdp.states:
        prob = mdp.transition(new_state, state, action)
        eu += prob * U[new_state]
    return eu

def get_meu(mdp, state, U):
    """Get the max expected utility"""
    meu = float("-inf")
    a = MDP.UP
    for action in mdp.actions[state]:
        eu = get_eu(state, action, mdp, U)
        if eu > meu:
            meu = eu
            a = action
    if len(mdp.actions[state]) == 0:
        meu = 0.0
    return meu, a
