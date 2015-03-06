# Author: Hannah Brock
# Class: CS 5300, Fall 2014
# Assignment: A2

import copy

class TowersOfHanoi:
    """Inherit this class to implement a Towers of Hanoi
    solution search
    """
    def __init__(self, avoid_dups, num_disks, check_on_creation):
        self.avoid_dups = avoid_dups
        self.set_goal(num_disks)
        self.check_creation = check_on_creation

    def set_goal(self, num_disks):
        """Sets the initial and goal states for
        a given number of disks
        """
        self.num_disks = num_disks
        self.goal = [ [], [], [] ]
        self.initial = [ [], [], [] ]
        self.tree = {}
        for x in range(1, num_disks + 1):
            self.goal[2].append(x)
            self.initial[0].append(x)

    def store_tree_node(self, node):
        if node.parent == None:
            self.tree['root'] = node
        else:
            nodes = self.tree[node.parent.to_string()]
            nodes.append(node)
        self.tree[node.to_string()] = []

    def search(self):
        """Performs a search for a solution to the Towers
        of Hanoi problem.

        Returns (int nodes_created, int nodes_expanded, bool success)
        """
        return ( [], 0, 0, False)

    def is_goal(self, state):
        """Checks if a state is a goal state"""
        if len(state[2]) == self.num_disks:
            return True
        return False

    def move(self, state, source, dest):
        """Moves a ring from one tower to another

        Arguments:
        state -- the current state
        source -- the index of the source tower
        dest -- the index of the destination tower

        Returns:
        tuple -- (bool success, list new_state)
        """
        if len(state[source]) < 1:
            return ( False, state )
        minDest = self.num_disks + 1
        minSource = min(state[source])
        length = len(state[dest])
        if length > 0:
            minDest = min(state[dest])
        if minSource > minDest:
            return ( False, state )
        new_state = copy.deepcopy(state)
        new_state[source].remove(minSource)
        new_state[dest].insert(0, minSource)
        return ( True, new_state)

    def get_possible_actions(self, node):
        """Returns a list of possible actions from a given
        node, with each action a tuple:
        ( source, dest, new state )
        """
        actions = []
        for source in range(0, len(node.state)):
            for dest in range(0, len(node.state)):
                if source != dest:
                    res = self.move(node.state, source, dest)
                    if res[0] is True:
                        actions.append( ( source, dest, res[1] ) )
        return actions

    def print_tree(self):
        """Prints the current search tree"""
        node = self.tree['root']
        self.print_node(node, 0)

    def print_node(self, node, spaces):
        for x in range(0,spaces):
            print(' '),
        print('|'),
        for x in range(0,4):
            print('-'),
        print(node.to_string())
        for x in range(0,spaces):
            print(' '),
        print('|')
        for n in self.tree.get(node.to_string(), []):
            self.print_node(n, spaces + 3)

class Node:
    """A node in a Towers of Hanoi search tree"""
    def __init__(self, nodeID, state, cost, parent=None, heuristic=lambda x: 0):
        self.state = state
        self.nodeID = nodeID
        self.parent = parent
        self.cost = cost
        if parent != None:
            self.cost += parent.cost
        self.heuristic = heuristic

    def g(self):
        return self.cost

    def h(self):
        return self.heuristic(self.state)

    def f(self):
        return self.g() + self.h()

    def get_path(self):
        path = []
        node = self.parent
        while node != None:
            path.insert(0, node)
            node = node.parent
        path.append(self)
        return path

    def to_string(self):
        if self.parent != None:
            return str(self.parent.state) + '->' + str(self.state) + ', ' + str(self.nodeID)
        return str(self.state) + ', ' + str(self.cost)
            
    def __eq__(self, other):
        if other == None:
            return False
        return self.state == other.state
    
    def __hash__(self):
        if self.parent != None:
            return hash(self.to_string())
        return hash(self.to_string())
