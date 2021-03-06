import numpy as np
import os
from math import inf
from random import shuffle
from scipy.signal import convolve2d as convolve
import time

#Retourne une matrice diagonale de taille n, rotation a 90° avec rot
def diag(n, rot=False): 
    d = np.identity(n)
    if rot: d = np.rot90(d)
    return d

#Retourne une matrice ligne de taille n, rotation a 90° avec rot
def line(n, rot=False):
    l = np.array([np.ones(n), np.zeros(n)])
    if rot: l = np.rot90(l)
    return l

#Algorithme minmax avec élagage alphabeta
def alphabeta(cplayer, eplayer, grille, depth, t, alpha = -inf, beta = inf):
    #Si la grille est un etat finale on renvoie sa valeur
    if time.time() - t >= 9 or depth == 0 or grille.IsWin(-eplayer) or grille.IsTerminal() : return grille.Value(cplayer,depth)
    #Si c'est au joueur de jouer on cherche son coup de plus grande valeur
    elif cplayer == eplayer:
        val = -inf
        for g in grille.Actions(eplayer):
            val = max(val, alphabeta(cplayer, -eplayer, g, depth - 1, t, alpha, beta))
            if beta <= val : return val
            alpha = max(alpha, val)
        return val
    #Si c'est a l'adversaire on cherche son coup de plus basse valeur
    else:
        val = inf
        for g in grille.Actions(eplayer):
            val = min(val, alphabeta(cplayer, -eplayer, g, depth - 1, t, alpha, beta))
            if alpha >= val : return val
            beta = min(beta, val)
        return val

class Grille:
    #Initialise une grille de puissance 4 de dimension i,j ou avec une grille grid prédéfinie
    def __init__(self, i = None, j = None, grid = None, a = -1):
        if grid is None:
            self.pos = np.zeros((i,j),np.byte)
        else:
            self.pos = grid.copy()
        self.a = a

    #Retourne la liste des coups possible a partir de cette grille pour le joueur player
    def Actions(self, player):
        res = list()
        
        for j in range(self.pos.shape[1]):
            for i in range(self.pos.shape[0] - 1,-1,-1):
                if self.pos[i][j] == 0 and not self.IsTerminal():
                    e = Grille(grid = self.pos, a = j + 1)
                    e.pos[i][j] = player
                    res.append(e)
                    break
        shuffle(res)
        return res

    #Retourne vrai si le joueur player a gagné dans cette grille
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

    #Retourne vrai si la grille est remplie
    def IsTerminal(self):
        return not 0 in self.pos

    #Retourne la valeur de la grille pour le joueur player
    def Value(self, player, depth):
        val = 0
        val += -abs(self.pos.shape[1] - self.a/2)
        val += sum(sum(convolve(player * self.pos,diag(3))))
        val += sum(sum(convolve(player * self.pos,diag(3,True))))
        val += sum(sum(convolve(player * self.pos,line(3))))
        val += sum(sum(convolve(player * self.pos,line(3,True))))
        if self.IsWin(player): val += 1000 + depth
        elif self.IsWin(-player): val += -1000 - depth
        return val

    #Fait jouer l'IA en tant que joueur player
    def play(self, player = 1, depth = 5, alpha = -inf, beta = inf):
        v,g = -inf,None
        t = time.time()
        for a in self.Actions(player):
            e = alphabeta(player, -player, a, depth, t, alpha, beta)
            if e > v: v,g = e,a
        return g.a

    #Joue un coup column pour le joueur player
    def apply(self, column, player):
        c = column - 1
        for i in range(self.pos.shape[0] - 1, -1, -1):
            if self.pos[i][c] == 0: 
                self.pos[i][c] = player
                break

    #Decrit la grille sous forme de texte, O pour le joueur 1, X pour le joueur 2
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

    cont = True

    n = 0

    while cont:
        cont = not (m.IsWin(-1) or m.IsTerminal())
        if cont :
            if ia1:
                start = time.time()
                jeu = m.play(player = 1, depth = 4)
                m.apply(jeu, 1)
                print("Colonne",jeu)
                end = time.time()
                print(end - start, "Sec")
            else:
                m.apply(int(input("A vous de jouer")), 1)
            n+=1
            print("Jeton",n)
            print(m)

        cont = not (m.IsWin(1) or m.IsTerminal()) and cont
        if cont :
            if ia2:
                start = time.time()
                jeu = m.play(player = -1, depth = 4)
                m.apply(jeu, -1)
                print("Colonne",jeu)
                end = time.time()
                print(end - start, "Sec")
            else:
                m.apply(int(input("A vous de jouer")), -1)
            n+=1
            print("Jeton",n)
            print(m)
        if(n >= 42): cont = False

    print("Fin de partie")
    print("-----------------------")
    print(m)
    if m.IsWin(1) : print("J1 a gagné")
    elif m.IsWin(-1) : print("J2 a gagné")
    else : print("Match nul")