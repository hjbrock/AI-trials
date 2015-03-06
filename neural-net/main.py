# Author: Hannah Brock

from network import Network
import sys, itertools

if len(sys.argv) < 3:
    print('usage: main.py (AND|OR) (num inputs) (iterations) (learning_rate) (activation_function)')
    exit(1)

function = sys.argv[1]
num_inputs = int(sys.argv[2])
k = 10000
learning_rate = 1.0
activation_function = 'logistic'

if len(sys.argv) > 3:
    k = int(sys.argv[3])
if len(sys.argv) > 4:
    learning_rate = float(sys.argv[4])
if len(sys.argv) > 5:
    activation_function = sys.argv[5]

if function != 'AND' and function != 'OR':
    print('Invalid function. Must be one of: AND, OR')
    exit(1)

# Create data
examples = [ list(x) for x in list(itertools.product([0.0,1.0], repeat=num_inputs)) ]
targets = [ ]
for x in examples:
    if function == 'OR':
        if 1 in x:
            targets.append([1])
        else:
            targets.append([0])
    else:
        if 0 in x:
            targets.append([0])
        else:
            targets.append([1])

test_x = examples[0]
if function == 'AND':
    test_x = examples[len(examples)-1]

net = Network(examples, targets, num_inputs, num_inputs, 1, k, learning_rate, activation_function, test_x)
print(net)
print('Final results:')
for ex in examples:
    y = net.get_output(ex)
    print('Ex: ' + str(ex) + ' Result: ' + str(y))

