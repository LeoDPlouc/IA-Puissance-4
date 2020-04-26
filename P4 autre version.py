# -*- coding: utf-8 -*-

nb_lignes=6
nb_colonnes=12

#Une grille de morpion est de 3 case par 3

#Initialisation de la grille
grille={}
for i in range(nb_lignes):
    for j in range(nb_colonnes):
        grille[(i,j)]=' '

#S0 étant l'état initial de la grille (vide)


def Actions(s):
    Ens_Act=[]
    for i in range(nb_lignes-1,-1,-1):
        for j in range(nb_colonnes):
            if(s[(i,j)]==' ' and (i==nb_lignes-1 or s[(i+1,j)]!=' ')):
                Ens_Act.append((i,j))
    return Ens_Act


def Result(s,a,joueur): #s la grille, a l'action et joueur = 1 pour la machine; 0 pour l'humain
    s1={}
    s1.update(s)
    if(joueur==1):
        s1[a]='X'
    else:
        s1[a]='O'
    return s1
    

#Le jeu est terminé si 3 cases voisines ont la même valeur (X ou O)
#Ou si toutes les cases sont remplies

def Terminal_Test(s):
    #h=hauteur(s)
    fin=False #On part du principe que la partie n'est pas finie

                        
    for i in range(nb_lignes):

        for j in range(nb_colonnes):

            if i < nb_lignes - 3:

                if j < nb_colonnes - 3 :

                    if(s[(0 + i,0 + j)] == s[(1 + i,1 + j)] == s[(2 + i,2 + j)] == s[(3 + i,3 + j)] != ' '):
                        fin = True

                    if(s[(nb_lignes - i - 1,0 + j)] == s[(nb_lignes - 2 - i,1 + j)] == s[(nb_lignes - 3 - i,2 + j)] == s[(nb_lignes - 4 - i,3 + j)] != ' '):
                        fin=True

                    if(s[(0 + i,j)] == s[(1 + i,j)] == s[(2 + i,j)] == s[(3 + i,j)] != ' '):
                        fin =True

            if j < nb_colonnes - 3:

                if(s[(i,0 + j)] == s[(i,1 + j)] == s[(i,2 + j)] == s[(i,3 + j)] != ' '):
                    fin=True
                        
    return fin


def Utility(s,profondeur): # Le raisonnement est le même que pour Terminal_Test
    #h=hauteur(s)
    gain=0 #Le gain est nul (égalité)
    res=False
    for i in range(nb_lignes):

        for j in range(nb_colonnes):

            if i < nb_lignes - 3:

                if j < nb_colonnes - 3 :

                    if(s[(0 + i,0 + j)] == s[(1 + i,1 + j)] == s[(2 + i,2 + j)] == s[(3 + i,3 + j)] != ' '):
                        res = True
                        val = s[(0 + i,0 + j)]
                            
                    if(s[(nb_lignes - i - 1,0 + j)] == s[(nb_lignes - 2 - i,1 + j)] == s[(nb_lignes - 3 - i,2 + j)] == s[(nb_lignes - 4 - i,3 + j)] != ' '):
                        res=True
                        val = s[(nb_lignes - i - 1,0 + j)]
                    if(s[(0 + i,j)] == s[(1 + i,j)] == s[(2 + i,j)] == s[(3 + i,j)] != ' '):
                        res =True
                        val = s[(0 + i,j)]

            if j < nb_colonnes - 3:

                if(s[(i,0 + j)] == s[(i,1 + j)] == s[(i,2 + j)] == s[(i,3 + j)] != ' '):
                    val = s[(i,0 + j)]
                    res=True
                    
            if(res):
                if(val=='X'):
                    gain=100+profondeur*10 # on maximise le gain avec la profondeur comme 'heuristique'
                elif(val=='O'):
                    gain=-100-profondeur*10 # on minimise le gain avec la profondeur comme 'heuristique'
    return gain
    


def Alpha_Beta_Search(s,alpha=-10000,beta=10000,profondeur=100):
    i=0

    res=Max_Value_Alpha_Beta(s, alpha, beta, profondeur)
    for a in Actions(s):
        if res==Min_Value_Alpha_Beta(Result(s,a,1), alpha, beta, profondeur-1): #On cherche pour toutes les actions celle qui correspond a
            i=a                                                                 #la maximisation de minimax avec l'élagage alpha beta
            
    return i

def Max_Value_Alpha_Beta(s,alpha,beta,profondeur):
    if(Terminal_Test(s) or profondeur==0):
        return Utility(s,profondeur)
    v=-10000
    for a in Actions(s):
        v=max(v,Min_Value_Alpha_Beta(Result(s, a,1),alpha,beta,profondeur-1))
        if v>= beta:
            return v
        alpha=max(alpha,v)
    return v

def Min_Value_Alpha_Beta(s,alpha,beta,profondeur):
    if(Terminal_Test(s) or profondeur==0):
        return Utility(s,profondeur)
    v=10000
    for a in Actions(s):
        v=min(v,Max_Value_Alpha_Beta(Result(s, a,0),alpha,beta,profondeur-1))
        if v<=alpha:
            return v
        beta=min(beta,v)
    return v



def AfficheGrille(s):
    for i in range(nb_lignes):
        print([s[(i,j)] for j in range(nb_colonnes)])
        
def Joueur(s): #Choix de l'action de l'humain
    
    
    choix_colonne=eval(input("Colonne ? "))
    l=0
    for i in range(nb_lignes-1,-1,-1):
        if s[(i,choix_colonne)]==' ':
            l=i
            break
        
    ind = (l,choix_colonne)
    return ind

def Jeu(s):
    
    while(Terminal_Test(s)==False): #Le jeu se termine alors on arrête la boucle
        AfficheGrille(s)
        choix=Joueur(s)
        s=Result(s, choix, 0) #La grille prend la valeur de l'action de l'humain
        s=Result(s, Alpha_Beta_Search(s,profondeur=5),1) #c'est au tour de l'ordinateur (on impose par exemple une profondeur de 6)
    AfficheGrille(s)
    if Utility(s,0)<0: # résultat gagnant si max est inf à 0 => min gagne
        print("Gagné!")
    elif Utility(s,0)>0:# résultat perdant si max est sup à 0 => min perd
        print("Perdu!")
    else:
        print("Match nul") # égalité si max=min =0
        

Jeu(grille)
