# Author: Hannah Brock
# Class: CS 5300, Fall 2014
# Assignment: A2

from towers_of_hanoi import TowersOfHanoi, Node

class TowersOfHanoiAStar(TowersOfHanoi):
    """This class implements a BFS to find a solution
    to the Towers of Hanoi problem with 3 rings
    """

    def search(self):
        """Performs a search for a solution using BFS

        Returns: (path, nodes_created, nodes_expanded, success)
        """
        expanded = 0
        created = 1
        node = Node(created, self.initial, 0, None, self.heuristic)
        self.store_tree_node(node)
        # check goal on creation if told to
        if self.check_creation and self.is_goal(node.state):
            return ( node.get_path(), created, expanded, True )
        frontier = [ ( node.f(), created, node ) ]
        explored = []
        while len(frontier) > 0:
            expanded += 1
            f, c, node = frontier.pop(0)
            explored.append(node.state)
            # check for goal
            if not self.check_creation and self.is_goal(node.state):
                return ( node.get_path(), created, expanded, True )
            actions = self.get_possible_actions(node)
            for action in actions:
                child = Node(created, action[2], 1, node, self.heuristic)
                self.store_tree_node(child)
                created += 1
                # check goal on creation if told to
                if self.check_creation and self.is_goal(child.state):
                    return ( child.get_path(), created, expanded, True )
                # avoid duplicate nodes if set
                if not self.avoid_dups:
                    frontier.append( ( child.f(), created, child ) )
                elif child.state not in explored and not self.in_queue(child.state, frontier):
                    frontier.append( ( child.f(), created, child ) )
            frontier = sorted(frontier)
        return ( [], created, expanded, False )

    @staticmethod
    def heuristic(state):
        cost = 0
        max_disk = 0
        for x in range(0,3):
            if len(state[x]) > 0 and max(state[x]) > max_disk:
                max_disk = max(state[x])
        for x in range(0,3):
            for num in state[x]:
                if num == max_disk and x != 2:
                    cost += 1
                elif (num + 1) not in state[x]:
                    cost += 1
        return cost

    @staticmethod
    def in_queue(state, queue):
        for f, c, node in queue:
            if node.state == state:
                return True
        return False
