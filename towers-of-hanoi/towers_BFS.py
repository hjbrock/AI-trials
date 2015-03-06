# Author: Hannah Brock
# Class: CS 5300, Fall 2014
# Assignment: A2

from towers_of_hanoi import TowersOfHanoi, Node

class TowersOfHanoiBFS(TowersOfHanoi):
    """This class implements a BFS to find a solution
    to the Towers of Hanoi problem with 3 rings
    """

    def search(self):
        """Performs a search for a solution using BFS

        Returns: (path, nodes_created, nodes_expanded, success)
        """
        expanded = 0
        created = 1
        node = Node(created, self.initial, 0)
        self.store_tree_node(node)
        # check goal on creation if told to
        if self.check_creation and self.is_goal(node.state):
            return ( node.get_path(), created, expanded, True )
        frontier = [ node ]
        explored = []
        while len(frontier) > 0:
            expanded += 1
            node = frontier.pop(0)
            explored.append(node.state)
            # check for goal
            if not self.check_creation and self.is_goal(node.state):
                return ( node.get_path(), created, expanded, True )
            actions = self.get_possible_actions(node)
            for action in actions:
                child = Node(created, action[2], 1, node)
                created += 1
                self.store_tree_node(child)
                # check goal on creation if told to
                if self.check_creation and self.is_goal(child.state):
                    return ( child.get_path(), created, expanded, True )
                # avoid duplicate nodes if set
                if not self.avoid_dups:
                    frontier.append(child)
                elif child.state not in explored and child not in frontier:
                    frontier.append(child)
        return ( [], created, expanded, False )
        
