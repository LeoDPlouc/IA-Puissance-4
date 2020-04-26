import numpy as np
import os
from math import inf
from random import shuffle
from scipy.signal import convolve2d as convolve

def diag(n, rot=False):
    d = np.identity(n)
    if rot: d = np.rot90(d)
    return d

def line(n, rot=False):
    l = np.array([np.ones(n), np.zeros(n)])
    if rot: l = np.rot90(l)
    return l

def alphabeta(cplayer, eplayer, grille, depth, alpha = -inf, beta = inf):
    if depth == 0 or grille.IsWin(-eplayer) or grille.IsTerminal() : return grille.Value(cplayer,depth)
    elif cplayer == eplayer:
        val = -inf
        for g in grille.Actions(eplayer):
            val = max(val, alphabeta(cplayer, -eplayer, g, depth - 1, alpha, beta))
            if beta <= val : return val
            alpha = max(alpha, val)
        return val
    else:
        val = inf
        for g in grille.Actions(eplayer):
            val = min(val, alphabeta(cplayer, -eplayer, g, depth - 1, alpha, beta))
            if alpha >= val : return val
            beta = min(beta, val)
        return val

class Grille:
    def __init__(self, i = None, j = None, grid = None):
        if grid is None:
            self.pos = np.zeros((i,j),np.byte)
        else:
            self.pos = grid.copy()

    def Actions(self, player):
        res = list()
        
        for j in range(self.pos.shape[1]):
            for i in range(self.pos.shape[0] - 1,-1,-1):
                if self.pos[i][j] == 0 and not self.IsTerminal():
                    e = Grille(grid = self.pos)
                    e.pos[i][j] = player
                    res.append(e)
                    break
        shuffle(res)
        return res

    def IsWin(self, player):
        i = convolve(self.pos,diag(4))/4
        if player in i: return True
        i = convolve(self.pos,diag(4,True))/4
        if player in i: return True
        i = convolve(self.pos,line(4))/4
        if player in i: return True
        i = convolve(self.pos,line(4,True))/4
        if player in i: return True

        return False

    def IsTerminal(self):
        return not 0 in self.pos

    def Value(self, player, depth):
        if self.IsWin(player): return 100 + depth
        elif self.IsWin(-player): return -100 - depth
        else: return 0

    def play(self, player = 1, depth = 5, alpha = -inf, beta = inf):
        v,g = -inf,None
        for a in self.Actions(player):
            e = alphabeta(player, -player, a, depth, alpha, beta)
            if e > v: v,g = e,a
        self.pos = g.pos

    def apply(self, column, player):
        c = column - 1
        for i in range(self.pos.shape[0] - 1, -1, -1):
            if self.pos[i][c] == 0: 
                self.pos[i][c] = player
                break

    def __str__(self):
        res = ""
        for i in range(self.pos.shape[0]):
            for j in range(self.pos.shape[1]):
                if self.pos[i][j] == 0: res += "| |"
                if self.pos[i][j] == 1: res += "|O|"
                if self.pos[i][j] == -1: res += "|X|"
            res += "\n"
        return res


if __name__ == '__main__':
    
    m = Grille(6,12)


    ia1 = True
    ia2 = True

    fg = True
    while fg:
        fg = not (m.IsWin(-1) or m.IsTerminal())
        if fg :
            if ia1:
                m.play(player = 1, depth = 5)
            else:
                m.apply(int(input("A vous de jouer")), 1)
            print(m)

        fg = not (m.IsWin(1) or m.IsTerminal())
        if fg :
            if ia2:
                m.play(player = -1, depth = 5)
            else:
                m.apply(int(input("A vous de jouer")), -1)
            print(m)

    print("Fin de partie")
    print("-----------------------")
    print(m)
    if m.IsWin(1) : print("Vous avez perdu")
    elif m.IsWin(-1) : print("Vous avez gagné")
    else : print("Match nul")