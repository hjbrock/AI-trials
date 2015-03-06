# Author: Hannah Brock

import random

class WumpusWorld:
    """Class for generating a wumpus world board
    Throughout:
      'W' = wumpus at this square
      'P' = pit at this square
      'S' = stench at this square
      'B' = breeze at this square
      'G' = gold at this square
      'Gl' = glitter at this square
    """

    def __random__(self, num_pits, cols=4, rows=4):
        # randomly add the pits
        self.__populate__(num_pits, cols, rows)
        # add gold
        self.__add_gold__(cols, rows)
        # add the wumpus in a random location
        self.__add_wumpus__(cols, rows)

    def __init__(self, num_pits, pit_locs=[], w_loc=None, g_loc=None,
                 cols=4, rows=4):
        self.world = []
        self.num_pits = num_pits
        for x in range(0,cols+1):
            cells = []
            for y in range(0, rows+1):
                cells.append([])
            self.world.append(cells)
        if len(pit_locs) == 0 or w_loc == None or g_loc == None:
            self.__random__(num_pits, cols, rows)
        else:
            pits = 0
            for p in pit_locs:
                self.world[p[0]][p[1]].append('P')
                self.__add_to_neighbors__(p[0], p[1], 'B')
                pits += 1
            self.world[w_loc[0]][w_loc[1]].append('W')
            self.__add_to_neighbors__(w_loc[0], w_loc[1], 'S')
            self.world[g_loc[0]][g_loc[1]].extend(['G', 'Gl'])
            self.__populate__(num_pits-pits, cols, rows)

    def has_wumpus(self, coordinates):
        x,y = coordinates
        if 'W' in self.world[x][y]:
            return True
        return False

    def has_gold(self, coordinates):
        x,y = coordinates
        if 'G' in self.world[x][y]:
            return True
        return False

    def has_pit(self, coordinates):
        x,y = coordinates
        if 'P' in self.world[x][y]:
            return True
        return False

    def get_percept(self, coordinates):
        x, y = coordinates
        locstr = str(x)+str(y)
        percept = []
        for p in self.world[x][y]:
            percept.append(p+locstr)
        return percept

    def in_range(self, coordinates):
        x, y = coordinates
        if x < 1 or x >= len(self.world):
            return False
        if y < 1 or y >= len(self.world[1]):
            return False
        return True

    def __is_ok__(self, x, y, conflicts):
        if not self.in_range((x, y)):
            return false
        sq = self.world[x][y]
        ok = True
        for item in conflicts:
            if item in sq:
                ok = False
                break
        return ok

    def __add_gold__(self, cols, rows):
        ok = False
        while not ok:
            x = random.randint(1,cols)
            y = random.randint(1,rows)
            ok = self.__is_ok__(x, y, ['P', 'W'])
            if ok:
              self.world[x][y].extend(['G', 'Gl'])

    def __add_wumpus__(self, cols, rows):
        placed = False
        while not placed:
            x = random.randint(1,cols)
            y = random.randint(1,rows)
            if self.__is_ok__(x, y, ['G', 'P']) and not (x==1 and y==1):
                self.world[x][y].append('W')
                self.world[x][y].append('S')
                self.__add_to_neighbors__(x, y, 'S')
                placed = True

    def __populate__(self, num_pits, cols, rows):
        for p in range(0, num_pits):
            placed = False
            while not placed:
                x = random.randint(1,cols)
                y = random.randint(1,rows)
                if self.__is_ok__(x, y, ['G', 'W', 'P']) and not (x==1 and y==1):
                    self.world[x][y].append('P')
                    self.__add_to_neighbors__(x, y, 'B')
                    placed = True

    def __add_to_neighbors__(self, x, y, item):
        y_range = len(self.world[0])
        x_range = len(self.world)
        for xmove in [x-1,x+1]:
            if xmove < x_range and xmove >= 0:
                if item not in self.world[xmove][y]:
                    self.world[xmove][y].append(item)
        for ymove in [y-1,y+1]:
            if ymove < y_range and ymove >=0:
                if item not in self.world[x][ymove]:
                    self.world[x][ymove].append(item)
                
