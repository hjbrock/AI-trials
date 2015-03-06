# Author: Hannah Brock

from mdp import MDP
from utility import get_meu, get_eu
from sympy import Symbol, Eq, solve
import random
import copy

def random_policy(mdp):
    """Generate a random policy for a given MDP"""
    policy = [ 0 for x in range(0,len(mdp.states)) ]
    for s in mdp.states:
        actions = mdp.actions[s]
        if len(actions) > 0:
            choice = random.randint(0,len(actions)-1)
            policy[s] = actions[choice]
    return policy

def get_util_equations(policy, mdp, util_syms):
    eqs = [ 0 for x in range(0,len(mdp.states)) ]
    for s in mdp.states:
        a = policy[s]
        eq = mdp.reward[s]
        for new_s in mdp.states:
            prob = mdp.transition(new_s, s, a)
            if prob != 0.0:
                eq = eq + (prob*util_syms[new_s])
        eq = Eq(util_syms[s], eq)
        eqs[s] = eq
    return eqs

def policy_evaluation(policy, utilities, mdp):
    """Get utilities for policy"""
    util_syms = [ Symbol('U'+str(x)) for x in range(0,len(mdp.states)) ]
    eqs = get_util_equations(policy, mdp, util_syms)
    solution = solve(eqs, util_syms, dict=True)
    if len(solution) == 0:
        return False
    for i in range(0,len(util_syms)):
        val = solution[0][util_syms[i]]
        utilities[i] = val
    return True

def policy_iteration(mdp, max_iterations):
    """Run policy iteration to generate an optimal policy"""
    # set up utility vector and policy vector
    utilities = [ 0.0 for x in range(0,12) ]
    policy = random_policy(mdp)
    # iterate
    changed = True
    iterations = []
    while changed:
        had_solution = policy_evaluation(policy, utilities, mdp)
        if not had_solution:
            policy = random_policy(mdp)
            continue
        changed = False
        for state in mdp.states:
            meu, action = get_meu(mdp, state, utilities)
            current_eu = get_eu(state, policy[state], mdp, utilities)
            if meu > current_eu:
                policy[state] = action
                changed = True
        iterations.append(copy.deepcopy(utilities))
        if len(iterations) == max_iterations:
            break
    return policy, utilities, iterations
