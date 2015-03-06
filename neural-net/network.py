# Author: Hannah Brock
#
# This file includes representations of a neural network and nodes

import random, math

class Node:
    """Node in a backpropagation network.
       Includes:
         -layer: layer of the network
         -inputs: set of input nodes
         -h: rather than directly doing the dot product, the multiplication
             is done via the chain rule in the backpropagate method
         -g: activation function
         -a: activation
         -inj: summation
         -w: map from output node id to weight for that output
         -outputs: set of output nodes
         -delta: error
         -bias: whether or not this is a bias node
    """
    def __init__(self, layer, is_bias, idx, activation_function):
        self.idx = idx
        self.layer = layer
        self.inputs = []
        if is_bias:
            self.a = -1.0
            self.bias = True
        else:
            self.a = 0.0
            self.bias = False
        self.w = {}
        self.inj = 0
        self.delta = 0
        self.a_func = activation_function

    def g(self, z):
        if self.a_func == 'logistic':
            return self.logistic(z)
        else:
            return self.tanh(z)

    def gprime(self, z):
        if self.a_func == 'logistic':
            return self.dlogistic(z)
        else:
            return self.dtanh(z)

    def logistic(self, z):
        """Logistic function"""
        try:
            return 1.0 / (1 + math.exp(-z))
        except OverflowError:
            if z > 0:
                return 0.0
            else:
                return 1.0

    def dlogistic(self, z):
        return self.g(z)*(1-self.g(z))

    def tanh(self, z):
        return math.tanh(z)

    def dtanh(self, z):
        return 1.0 - math.tanh(z)**2

    def __str__(self):
        s = ''
        s += ('Node: ' + str(self.idx))
        s += ('\n\tlayer: ' + str(self.layer))
        s += ('\n\tinputs: ' + str(self.inputs))
        s += ('\n\toutputs->weights: ' + str(self.w))
        s += ('\n\ta: ' + str(self.a))
        s += ('\n\tinj: ' + str(self.inj))
        s += ('\n\tdelta: ' + str(self.delta))
        s += ('\n\tbias: ' + str(self.bias))
        return s

    def __repr__(self):
        return self.__str__()

class Network:
    """A backpropagation network"""
    def __init__(self, X, targets, I, H, O, k, learning_rate, activation_function, test_x):
        """Create a backpropagation network for the given parameters:
        X - input examples vector
        targets - examples output vector
        I - number of input nodes
        H - number of hidden layer nodes
        O - number of output nodes
        k - max iterations
        """
        self.input_layer = []
        self.hidden_layer = []
        self.output_layer = []
        idx = 0
        # Create nodes
        for x in range(0, I):
            node = Node(0, False, idx, activation_function)
            idx += 1
            self.input_layer.append(node)
        self.input_layer.append(Node(0, True, idx, activation_function))
        idx += 1
        for x in range(0, H):
            node = Node(1, False, idx, activation_function)
            idx += 1
            self.hidden_layer.append(node)
        self.hidden_layer.append(Node(1, True, idx, activation_function))
        idx += 1
        for x in range(0, O):
            node = Node(2, False, idx, activation_function)
            idx += 1
            self.output_layer.append(node)

        # Assign random weights and match up links
        for node in self.input_layer:
            for output in self.hidden_layer:
                if output.bias:
                    continue
                node.w[output.idx] = self.rand(-0.2, 0.2)
                output.inputs.append(node.idx)
        
        for node in self.hidden_layer:
            for output in self.output_layer:
                node.w[output.idx] = self.rand(-0.2, 0.2)
                output.inputs.append(node.idx)
        # Go!
        self.iterations, self.error = self.train(X, targets, k, learning_rate, test_x)

    def rand(self, lower, upper):
        return (upper-lower) * random.random() + lower

    def train(self, X, targets, k, learning_rate, test_x):
        count = 0
        lastOutput = [ [ 0.0 for x in self.output_layer ] for ex in X ]
        while count < k:
            count += 1
            error = 0.0
            max_change = 0.0
            for i in range(0, len(X)):
                self.update(X[i])
                self.backpropagate(targets[i], learning_rate)
                error += self.error(targets[i])
                output = [ node.a for node in self.output_layer ]
                change = self.calculate_change(output, lastOutput[i])
                if change > max_change:
                    max_change = change
                lastOutput[i] = [ node.a for node in self.output_layer ]
            if max_change < 0.000001:
                return count, error
        return count, error

    def calculate_change(self, current, last):
        change = 0.0
        for i in range(0, len(current)):
            change += abs(last[i] - current[i])
        return change

    def error(self, target):
        """Calculate error on current example"""
        error = 0.0
        for i in range(0, len(target)):
            error += abs(target[i] - self.output_layer[i].a)
        return error
    
    def update(self, x):
        """Update all nodes in the network with the given example"""
        # update input layer activations
        for i in range(0, len(self.input_layer)):
            if not self.input_layer[i].bias:
                self.input_layer[i].a = x[i]
        # update hidden layer activations
        for node in self.hidden_layer:
            if not node.bias:
                node.inj = 0.0
                for input_node in self.input_layer:
                    node.inj += input_node.a * input_node.w[node.idx]
                node.a = node.g(node.inj)
        # update output layer
        for node in self.output_layer:
            node.inj = 0.0
            for hidden_node in self.hidden_layer:
                node.inj += hidden_node.a * hidden_node.w[node.idx]
            node.a = node.g(node.inj)

    def backpropagate(self, target, learning_rate):
        """Propagate error back through the network"""
        # get deltas for output layer first
        for k in range(0, len(self.output_layer)):
            delta = target[k] - self.output_layer[k].a
            self.output_layer[k].delta = self.output_layer[k].gprime(self.output_layer[k].inj) * delta
        # get deltas for hidden layer next
        for node in self.hidden_layer:
            node.delta = 0.0
            for output_node in self.output_layer:
                node.delta += output_node.delta * node.w[output_node.idx]
            node.delta = node.gprime(node.inj) * node.delta
        # update weights coming from hidden layer
        for node in self.hidden_layer:
            for output_node in self.output_layer:
                node.w[output_node.idx] += learning_rate * output_node.delta * node.a
        # update weights coming from input layer
        for node in self.input_layer:
            for hidden_node in self.hidden_layer:
                if not hidden_node.bias:
                    node.w[hidden_node.idx] += learning_rate * hidden_node.delta * node.a

    def get_output(self, example_x):
        """Get output of the network for a new example"""
        self.update(example_x)
        output = []
        for node in self.output_layer:
            output.append(node.a)
        return output

    def __str__(self):
        s = ''
        for node in self.input_layer:
            s += str(node) + '\n'
        for node in self.hidden_layer:
            s += str(node) + '\n'
        for node in self.output_layer:
            s += str(node) + '\n'
        return s

    def __repr__(self):
        return self.__str__()
