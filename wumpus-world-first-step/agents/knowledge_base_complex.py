# Author: Hannah Brock

from __future__ import division
from sympy import *i
import itertools

class KnowledgeBase:
    """Represents the knowledge of a logical agent"""

    def __init__(self, cols, rows):
        self.knowledge = And(1)
        self.model = []
        self.loc = '11'
    
    def add_fact(self, fact):
        expr = sympify(fact)
        self.knowledge = And(self.knowledge,And(expr))

    def __create_sym__(self, name, loc):
        if loc[0] >= 0 and loc[0] < 4:
            if loc[1] >= 0 and loc[1] < 4:
                return name+str(loc[0])+str(loc[1])
        return ''

    def prep_loc(self, loc):
        self.loc = str(loc[0])+str(loc[1])
        sloc = str(loc[0]) + str(loc[1])
        adjP = [ self.__create_sym__('P', (loc[0]+1, loc[1])),
                 self.__create_sym__('P', (loc[0]-1, loc[1])),
                 self.__create_sym__('P', (loc[0], loc[1]+1)),
                 self.__create_sym__('P', (loc[0], loc[1]-1)) ]
        B = 'B' + sloc
        Gl = 'Gl' + sloc
        G = 'G' + sloc
        # todo add wumpus
        # add gold implications
        self.add_fact(Gl + ' >> ' + G) 
        self.add_fact(G + ' >> ' + Gl) 
        # add pit implications
        adjPs = ''
        for s in adjP:
            if not adjPs.endswith('|'):
                adjPs += ' |'
            adjPs += s
        self.add_fact(B + ' >> ' + adjPs)
        self.add_fact(adjPs + ' >> ' + B)
        self.add_fact('Not(P' + str(loc[0]) + str(loc[1]) + ')')

    def __evaluate__(self):
        syms = list(self.knowledge.atoms(Symbol))
        possibilities = itertools.product([True, False], len(syms))
        model = []
        for p in possibilities:
            exp = copy.deepcopy(self.knowledge)
            i = 0
            for s in syms:
                exp = exp.subs(s, p[i])
                i += 1
            isTrue = Eq(True, exp)
            if isTrue:
                model.append(p)

    def get_next_move(self, percepts):
        self.__evaluate__()
        
        return
