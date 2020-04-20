import numpy as np

def initmm(grille):
    return minmax(False, grille, 5)

def minmax(ia, grille, depth):
    if depth == 0 or grille.IsTerminal(): return grille.Value()
    if ia:
        val = -100
        for g in grille.Actions(True):
            val = max(val, minmax(False, g, depth - 1))
        return val
    else:
        val = 100
        for g in grille.Actions(False):
            val = min(val, minmax(True, g, depth - 1))
        return val

def initab(grille):
    return alphabeta(False, grille)

def alphabeta(ia, grille, alpha = -100, beta = 100):
    if grille.IsTerminal(): return grille.Value()
    elif ia:
        val = -100
        for g in grille.Actions(True):
            val = max(val, alphabeta(False, g, alpha, beta))
            if beta <= val : return val
            alpha = max(alpha, val)
        return val
    else:
        val = 100
        for g in grille.Actions(False):
            val = min(val, alphabeta(True, g, alpha, beta))
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
        for i in range(self.pos.ndim(1)):
            for j in range(self.pos.ndim(0),-1,-1):
                if self.pos[j][i] == 0 and not self.IsTerminal():
                    e = Grille(self.pos)
                    e.pos[j][i] = ia
                    res.append(e)
                    break
        return res


    def IsWin(self, ia):
        w = list()
        x,y = self.pos.ndim(0), self.pos.ndim(1)
        for i in range(self.pos.ndim(0) - 4):
            for j in range(self.pos.ndim(1) - 4):
                w.append(self.pos[0 + i][0 + j] == self.pos[1 + i][1 + j] == self.pos[2 + i][2 + j] == self.pos[3 + i][3 + j] == ia)
                w.append(self.pos[x - i][y - j] == self.pos[x - 1 - i][y- 1 - j] == self.pos[x - 2 - i][y - 2 - j] == self.pos[x - 3 - i][y - 3 - j] == ia)
                w.append(self.pos[0 + i][j] == self.pos[1 + i][j] == self.pos[2 + i][j] == self.pos[3 + i][j] == ia)
                w.append(self.pos[i][0 + j] == self.pos[i][1 + j] == self.pos[i][2 + j] == self.pos[i][3 + j] == ia)
        return True in w

    def IsTerminal(self):
        return self.IsWin(True) or self.IsWin(False) or not (True in [None in self.pos[i] for i in range(self.pos.ndim(0))])

    def Value(self):
        if self.IsWin(True): return 10
        elif self.IsWin(False): return -10
        else: return 0

    def playIa(self, alphabeta = True):
        if alphabeta : self.pos = max(self.Actions(True), key=initab).pos
        else : self.pos = max(self.Actions(True), key=initmm).pos

    def __str__(self):
        return str(self.pos[0]) + "\n" + str(self.pos[1]) + "\n" + str(self.pos[2])


if __name__ == '__main__':
    m = Grille()
    fg = True
    while fg:
        fg = not m.IsTerminal()
        if fg : m.playIa()
        print(m)
        print("A vous de jouer")
        fg = not m.IsTerminal()
        if fg :
            c = int(input()) - 1
            m.pos[(c-(c%3))//3][c%3] = False

    print("Fin de partie")
    print(m)
    if m.IsWin(True) : print("Vous avez perdu")
    elif m.IsWin(False) : print("Vous avez gagné")
    else : print("Match nul")