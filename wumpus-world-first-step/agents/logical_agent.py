# Author: Hannah Brock

from agent import WumpusAgent
from knowledge_base import KnowledgeBase

class LogicalAgent(WumpusAgent):
    """Implementation of a logcial wumpus agent"""

    def __init__(self):
        self.kb = KnowledgeBase()

    def get_action(self, percept):
        """See WumpusAgent.get_action for further
        documentation.
        """
        for p in percept:
            self.kb.tell(p)
        if self.kb.ask('GRAB'):
            return WumpusAgent.GRAB
        if self.kb.ask('FORWARD'):
            return WumpusAgent.FORWARD
        return WumpusAgent.LEFT

    def reset(self):
        self.kb = KnowledgeBase()
