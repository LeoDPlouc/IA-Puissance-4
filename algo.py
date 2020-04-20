import numpy as np

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

def alphabeta(player, grille, depth, alpha = -100, beta = 100):
    if grille.IsTerminal() or depth == 0: return grille.Value()
    elif player == 1:
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
        x,y = self.pos.shape[1], self.pos.shape[0]
        for i in range(y):
            for j in range(x):
                if i < y - 4:
                    if j < x - 4 :
                        w.append(self.pos[0 + i][0 + j] == self.pos[1 + i][1 + j] == self.pos[2 + i][2 + j] == self.pos[3 + i][3 + j] == player)
                        w.append(self.pos[x - i - 1][0 + j] == self.pos[x - 2 - i][1 + j] == self.pos[x - 3 - i][2 + j] == self.pos[x - 4 - i][3 + j] == player)
                    w.append(self.pos[0 + i][j] == self.pos[1 + i][j] == self.pos[2 + i][j] == self.pos[3 + i][j] == player)
                if j < x - 4:
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
            for a in self.Actions(1):
                e = alphabeta(player, a, depth, alpha, beta)
                if e > v: v,g = e,a
            self.pos = g.pos
        else : 
            v,g = -100,None
            for a in self.Actions(1):
                e = minmax(player, a, depth)
                if e > v: v,g = e,a
            self.pos = g.pos

    def apply(self, column):
        c = column - 1
        for i in range(self.pos.shape[0] - 1, -1, -1):
            if self.pos[i][c] == 0: 
                self.pos[i][c] = -1
                break

    def __str__(self):
        return str(self.pos)


if __name__ == '__main__':

    m = Grille(12,7)
    ia = True

    fg = True
    while fg:
        fg = not m.IsTerminal()
        if fg : m.play(depth = 2)
        print(m)

        fg = not m.IsTerminal()
        if fg :
            if ia:
                m.play(player = -1, depth = 2)
            else:
                m.apply(input("A vous de jouer"))
            print(m)

    print("Fin de partie")
    print("-----------------------")
    print(m)
    if m.IsWin(1) : print("Vous avez perdu")
    elif m.IsWin(-1) : print("Vous avez gagné")
    else : print("Match nul")