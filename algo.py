import numpy as np

def initmm(grille):
    return minmax(-1, grille, 5)

def minmax(ia, grille, depth):
    if depth == 0 or grille.IsTerminal(): return grille.Value()
    if ia:
        val = -100
        for g in grille.Actions(1):
            val = max(val, minmax(-1, g, depth - 1))
        return val
    else:
        val = 100
        for g in grille.Actions(-1):
            val = min(val, minmax(1, g, depth - 1))
        return val

def initab(grille):
    return alphabeta(-1, grille, 5)

def alphabeta(ia, grille, depth, alpha = -100, beta = 100):
    if grille.IsTerminal() or depth == 0: return grille.Value()
    elif ia == 1:
        val = -100
        for g in grille.Actions(1):
            val = max(val, alphabeta(-1, g, depth - 1, alpha, beta))
            if beta <= val : return val
            alpha = max(alpha, val)
        return val
    else:
        val = 100
        for g in grille.Actions(-1):
            val = min(val, alphabeta(1, g, depth - 1, alpha, beta))
            if alpha >= val : return val
            beta = min(beta, val)
        return val

class Grille:
    def __init__(self, i = None, j = None, grid = None):
        if grid is None:
            self.pos = np.zeros((i,j),np.byte)
        else:
            self.pos = grid.copy()


    def Actions(self, ia):
        res = list()
        for i in range(self.pos.shape[0]):
            for j in range(self.pos.shape[1] - 1,0,-1):
                if self.pos[i][j] == 0 and not self.IsTerminal():
                    e = Grille(grid = self.pos)
                    e.pos[j][i] = ia
                    res.append(e)
                    break
        return res


    def IsWin(self, ia):
        w = list()
        x,y = self.pos.shape[0], self.pos.shape[1]
        for i in range(x - 4):
            for j in range(y - 4):
                w.append(self.pos[0 + i][0 + j] == self.pos[1 + i][1 + j] == self.pos[2 + i][2 + j] == self.pos[3 + i][3 + j] == ia)
                w.append(self.pos[x - i - 1][y - j - 1] == self.pos[x - 2 - i][y - 2 - j] == self.pos[x - 3 - i][y - 3 - j] == self.pos[x - 4 - i][y - 4 - j] == ia)
                w.append(self.pos[0 + i][j] == self.pos[1 + i][j] == self.pos[2 + i][j] == self.pos[3 + i][j] == ia)
                w.append(self.pos[i][0 + j] == self.pos[i][1 + j] == self.pos[i][2 + j] == self.pos[i][3 + j] == ia)
        return True in w

    def IsTerminal(self):
        return self.IsWin(1) or self.IsWin(-1) or not (True in [0 in self.pos[i] for i in range(self.pos.shape[0])])

    def Value(self):
        if self.IsWin(1): return 10
        elif self.IsWin(-1): return -10
        else: return 0

    def playIa(self, alphabeta = True):
        if alphabeta : self.pos = max(self.Actions(1), key=initab).pos
        else : self.pos = max(self.Actions(1), key=initmm).pos

    def __str__(self):
        return str(self.pos)


if __name__ == '__main__':
    m = Grille(5,5)
    fg = True
    while fg:
        fg = not m.IsTerminal()
        if fg : m.playIa()
        print(m)
        print("A vous de jouer")
        fg = not m.IsTerminal()
        if fg :
            c = int(input()) - 1
            for i in range(m.pos.shape[1] - 1, 0, -1):
                if m.pos[i][c] == 0: 
                    m.pos[i][c] = -1
                    break

    print("Fin de partie")
    print(m)
    if m.IsWin(True) : print("Vous avez perdu")
    elif m.IsWin(False) : print("Vous avez gagné")
    else : print("Match nul")