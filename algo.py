import numpy as np
import os

def clearTerm():
    os.system("cls")

def minmax(player, grille, depth):
    if depth == 0 or grille.IsTerminal(): return grille.Value()
    if player:
        val = -100
        for g in grille.Actions(1):
            val = max(val, minmax(-1, g, depth - 1))
        return val
    else:
        val = 100
        for g in grille.Actions(-1):
            val = min(val, minmax(1, g, depth - 1))
        return val

def alphabeta(cplayer, eplayer, grille, depth, alpha = -100, beta = 100):
    if grille.IsTerminal() or depth == 0: return grille.Value()
    elif cplayer == eplayer:
        val = -100
        for g in grille.Actions(eplayer):
            val = max(val, alphabeta(cplayer, -eplayer, g, depth - 1, alpha, beta))
            if beta <= val : return val
            alpha = max(alpha, val)
        return val
    else:
        val = 100
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
        
        for i in range(self.pos.shape[0] - 1,-1,-1):
            for j in range(self.pos.shape[1]):
                if self.pos[i][j] == 0 and not self.IsTerminal():
                    e = Grille(grid = self.pos)
                    e.pos[i][j] = player
                    res.append(e)
                    break
        return res

    def IsWin(self, player):
        w = list()
        x,y = self.pos.shape[0], self.pos.shape[1]
        for i in range(x):
            for j in range(y):
                if i < x - 3:
                    if j < y - 3 :
                        w.append(self.pos[0 + i][0 + j] == self.pos[1 + i][1 + j] == self.pos[2 + i][2 + j] == self.pos[3 + i][3 + j] == player)
                        w.append(self.pos[x - i - 1][0 + j] == self.pos[x - 2 - i][1 + j] == self.pos[x - 3 - i][2 + j] == self.pos[x - 4 - i][3 + j] == player)
                    w.append(self.pos[0 + i][j] == self.pos[1 + i][j] == self.pos[2 + i][j] == self.pos[3 + i][j] == player)
                if j < y - 3:
                        w.append(self.pos[i][0 + j] == self.pos[i][1 + j] == self.pos[i][2 + j] == self.pos[i][3 + j] == player)
        return True in w

    def IsTerminal(self):
        return self.IsWin(1) or self.IsWin(-1) or not (True in [0 in self.pos[i] for i in range(self.pos.shape[0])])

    def Value(self):
        if self.IsWin(1): return 10
        elif self.IsWin(-1): return -10
        else: return 0

    def play(self, player = 1, ab = True, depth = 5, alpha = -100, beta = 100):
        if ab :
            v,g = -100,None
            for a in self.Actions(player):
                e = alphabeta(player, player, a, depth, alpha, beta)
                if e > v: v,g = e,a
            self.pos = g.pos
        else : 
            v,g = -100,None
            for a in self.Actions(1):
                e = minmax(player, player, a, depth)
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
                if self.pos[i][j] == 0: res += " "
                if self.pos[i][j] == 1: res += "O"
                if self.pos[i][j] == -1: res += "X"
            res += "\n"
        return res


if __name__ == '__main__':

    m = Grille(12,5)
    ia1 = True
    ia2 = True

    fg = True
    while fg:
        fg = not m.IsTerminal()
        if fg :
            if ia1:
                m.play(player = 1, depth = 3)
            else:
                m.apply(int(input("A vous de jouer")), 1)
            clearTerm()
            print(m)

        fg = not m.IsTerminal()
        if fg :
            if ia2:
                m.play(player = -1, depth = 3)
            else:
                m.apply(int(input("A vous de jouer")), -1)
            clearTerm()
            print(m)

    clearTerm()
    print("Fin de partie")
    print("-----------------------")
    print(m)
    if m.IsWin(1) : print("Vous avez perdu")
    elif m.IsWin(-1) : print("Vous avez gagné")
    else : print("Match nul")