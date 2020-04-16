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
    def __init__(self, grid = None):
        if grid is None:
            self.pos = [[None, None, None],[None, None, None],[None, None, None]]
        else:
            self.pos = [grid[i].copy() for i in range(3)]


    def Actions(self, ia):
        res = list()
        for i in range(3):
            for j in range(3):
                if self.pos[i][j] is None and not self.IsTerminal():
                    e = Grille(self.pos)
                    e.pos[i][j] = ia
                    res.append(e)
        return res

    def IsWin(self, ia):
        w = list()
        for i in range(3):
                w.append(self.pos[0][i] == self.pos[1][i] == self.pos[2][i] == ia)
                w.append(self.pos[i][0] == self.pos[i][1] == self.pos[i][2] == ia)
        w.append(self.pos[0][0] == self.pos[1][1] == self.pos[2][2] == ia)
        w.append(self.pos[0][2] == self.pos[1][1] == self.pos[2][0] == ia)

        return True in w

    def IsTerminal(self):
        return self.IsWin(True) or self.IsWin(False) or not (True in [None in self.pos[i] for i in range(3)])

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