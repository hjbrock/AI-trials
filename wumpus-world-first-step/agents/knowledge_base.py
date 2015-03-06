# Author: Hannah Brock

from __future__ import division
from sympy import *
import itertools, copy

class KnowledgeBase:
    """Represents the knowledge of a logical agent"""

    def __init__(self):
        # create symbols
        tmp_syms = symbols('B11 S11 P12 P21 W12 W21 F12 F21 G11 GRAB TURN FORWARD')
        self.syms = {}
        self.syms['B11'] = tmp_syms[0]
        self.syms['S11'] = tmp_syms[1]
        self.syms['P12'] = tmp_syms[2]
        self.syms['P21'] = tmp_syms[3]
        self.syms['W12'] = tmp_syms[4]
        self.syms['W21'] = tmp_syms[5]
        self.syms['F12'] = tmp_syms[6]
        self.syms['F21'] = tmp_syms[7]
        self.syms['Gl11'] = tmp_syms[8]
        self.syms['GRAB'] = tmp_syms[9]
        self.syms['TURN'] = tmp_syms[10]
        self.syms['FORWARD'] = tmp_syms[11]
        # load basic knowledge
        self.knowledge = self.syms['B11'] >> (self.syms['P12'] | self.syms['P21'])
        self.knowledge = self.knowledge & (self.syms['S11'] >> (self.syms['W12'] | self.syms['W21']))
        exp = (self.syms['F12'] & (Not(self.syms['P12'] | self.syms['W12']))) >> self.syms['FORWARD']
        self.knowledge = self.knowledge & exp
        exp = (self.syms['F21'] & (Not(self.syms['P21'] | self.syms['W21']))) >> self.syms['FORWARD']
        self.knowledge = self.knowledge & exp
        self.knowledge = self.knowledge & (self.syms['Gl11'] >> self.syms['GRAB'])
        self.knowledge = self.knowledge & (Not(self.syms['FORWARD']) >> self.syms['TURN'])
        self.model = []
        self.possibilities = []

    def __model__(self):
        model = []
        possibilities = list(itertools.product((True, False), repeat=len(self.syms)))
        for p in possibilities:
            exp = copy.deepcopy(self.knowledge)
            i = 0
            for key in self.syms:
                exp = exp.subs(self.syms[key], p[i])
                i += 1
            test = Eq(True, exp)
            if test == True:
                model.append(p)
        return ( model, possibilities )

    def tell(self, proposition):
        sym = self.syms.get(proposition, None)
        if sym == None:
            sym = symbols(str(proposition))
            self.syms[proposition] = sym
        self.knowledge = self.knowledge & (sym)
        self.model = []
        self.possiblities = []
   
    def ask(self, action):
        if len(self.possibilities) == 0:
            self.model, self.possibilities = self.__model__()
        sym = self.syms.get(action, None)
        if sym == None:
            return False
        i = list(self.syms).index(action)
        alpha = []
        for p in self.possibilities:
            if p[i]:
                alpha.append(p)
        if set(self.model).issubset(set(alpha)):
            return True
        return False
