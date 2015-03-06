# Author: Hannah Brock

from mdp import MDP
from agent import ValueIterationAgent, PolicyIterationAgent
import sys

def print_policy(policy):
    """Print the given policy in a readable state"""
    words = { MDP.UP: "^", MDP.DOWN: "v", MDP.RIGHT:">", MDP.LEFT:"<" }
    for y in range(0,3):
        j = 2 - y
        for x in range(0,4):
            idx = x + j*4
            if idx % 4 == 0:
                if y != 0:
                    print('\n'),
                print('\t'),
            if idx == 11:
                print('+1'),
            elif idx == 7:
                print('-1'),
            elif idx == 5:
                print('  '),
            else:
                print(' '+words[policy[idx]]),
    print('')

def print_utilities(utilities):
    """Print utilities in grid format"""
    for y in range(0,3):
        j = 2 - y
        for x in range(0,4):
            idx = x + j*4
            if idx % 4 == 0 and y != 0:
                    print('\n'),
            if idx == 11:
                print('\t+1'),
            elif idx == 7:
                print('\t-1'),
            elif idx == 5:
                print('\t       '),
            else:
                print('\t'+str(round(utilities[idx], 5))),
    print('')

def print_utility_table(iterations):
    print('Iteration\t(1,1)\t(3,1)\t(3,3)\t(4,1)\t(4,3)')
    for i in range(0,len(iterations)):
        print(str(i+1)+'\t'),
        # 1,1
        print(str(round(iterations[i][0], 5)) + '\t'),
        # 3,1
        print(str(round(iterations[i][2], 5)) + '\t'),
        # 3,3
        print(str(round(iterations[i][10], 5)) + '\t'),
        # 4,1
        print(str(round(iterations[i][3], 5)) + '\t'),
        # 4,3
        print(str(round(iterations[i][11], 5)) + '\t'),
        print('')

#### MAIN ####
if len(sys.argv) != 5:
    print('Usage: main.py reward discount max_error max_iterations')
    exit(1)

reward = float(sys.argv[1])
max_error = float(sys.argv[3])
discount = float(sys.argv[2])
max_iterations = float(sys.argv[4])
# Run value iteration
agent = ValueIterationAgent(reward, discount)
policy, utilities, iterations = agent.get_policy(max_error, max_iterations)
print('Value iteration:')
print('Iterations='+str(len(iterations)))
print('Reward=' + str(reward) + ', Discount=' + str(discount) +
      ', Max Error: ' + str(max_error))
print('Policy=')
print_policy(policy)
print('Final Utilities=')
print_utilities(utilities)
print('Utilities per iteration=')
print_utility_table(iterations)
print("**********************************")

# Run policy iteration
agent = PolicyIterationAgent(reward, discount)
policy, utilities, iterations = agent.get_policy(max_iterations)
print('Policy iteration:')
print('Iterations='+str(len(iterations)))
print('Reward=' + str(reward) + ', Discount=' + str(discount))
print('Policy=')
print_policy(policy)
print('\nUtilities=')
print_utilities(utilities)
print('Utilities per iteration=')
print_utility_table(iterations)
