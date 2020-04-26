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


def hauteur(s):
    res=nb_lignes
    for i in range(nb_lignes-1,-1,-1):
        if (s[(i,j)] == 0 for j in range(nb_colonnes)):
            if res>i:
                res=i
    return res-1
"""
def largeur(s):
    res1,res2=3,9
    
        """

def Actions(s):
    Ens_Act=[]
    h = hauteur(s)
    for i in range(nb_lignes-1,h,-1):
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
    """
    res=True
    for i in range(nb_lignes):
        for j in range(nb_colonnes):
            if(s[(i,j)]==' '):
                res=False
                
    if(res):
        fin=True # On a testé si toutes les cases étaient pleines
    
    else:
        for i in range(nb_lignes):
            for j in range(nb_colonnes-4):
                val = s[(i,j)]
                if(val!=' '):
                    res=True
                    for k in range(1,4):
                        if s[(i,j+k)]!=val:
                            res=False
                    if(res):
                        fin=True
        
        for j in range(nb_colonnes):
            for i in range(nb_lignes-4):
                val=s[(i,j)]
                if(val!=' '):
                    res=True
                    for k in range(1,4):
                        if (s[(i-k,j)]==val):
                            res=False
                    if(res):
                        fin=True"""
                        
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
                        
                        
                        
                        
                        
                        
                        
                    """              
        for i in range(nb_lignes-4):
            for j in range(nb_colonnes-4):
                
                val = s[(i,j)]
                val1 = s[(i,j+k)]
                val2 = s[(i+k,j)]
                if(val!=' '):
                    res=True
                    res1=True
                    res2=True
                    for k in range(1,5):
                        if (s[(i,j+k)]!=val1):
                            res1=False
                        if(s[(i+k,j+k)]!=val ):
                            res=False
                        if(s[(i+k,j)]!=val2):
                            res2=False
                    if(res1 or res2 or res):
                        fin = True
        
        #On a testé si une diagonale est composée de 3 O ou X => un gagnant donc fin 
        
        for i in range(nb_lignes-5,3,-1):
            for j in range(nb_colonnes-5,3,-1):
                val = s[(i,j)]
                val1 = s[(i,j-k)]
                val2 = s[(i-k,j)]
                if(val!=' '):
                    res=True
                    res1=True
                    res2=True
                    for k in range(1,5):
                        if (s[(i,j+k)]!=val1):
                            res1=False
                        if(s[(i+k,j+k)]!=val ):
                            res=False
                        if(s[(i+k,j)]!=val2):
                            res2=False
                    if(res1 or res2 or res):
                        fin = True"""
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

"""
#Puissanse 4

#Initialisation de la grille P4
grilleP4={}
for i in range(6):
    for j in range(7):
        grilleP4[(i,j)]=' '
        
def gravite(s,i,j):
    res=False
    if(i==5):
        res = True
    elif (s[(i+1,j)]!=' '):
        res = True
    return res
        
def ActionsP4(s):
    Ens_Act=[]
    for i in range(5,1,-1):
        for j in range(6,1,-1):
            if(s[(i,j)]==' ' and gravite(s, i, j)):
                Ens_Act.append((i,j))
    print('Actions possibles: ',Ens_Act)
    return Ens_Act

#Le jeu est terminé si 4 cases voisines ont la même valeur (X ou O)
#Ou si toutes les cases sont remplies

def Terminal_TestP4(s):
    fin=False
    
    res=True
    for i in range(6):
        for j in range(7):
            if(s[(i,j)]==' '):
                res=False
    if(res):
        fin=True
    else:
        for i in range(6):
            
            val=s[(i,0)]
            if(val!=' '):
                res=True
                k=0
                for j in range(1,7):
                    if k<5:
                        if (s[(i,j)]!=val):
                            res=False
                            k=0
                        else:
                            k=k+1
                    
                
            if(res):
                fin=True
        
        for j in range(7):
            
            val=s[(0,j)]
            if(val!=' '):
                res=True
                k=0
                for i in range(1,6):
                    if k<5:
                        if (s[(i,j)]!=val):
                            res=False
                            k=0
                        else:
                            k=k+1
                
            if(res):
                fin=True
        
        
        for i in range(5):
            for j in range(6):
                if(s[(i,j)]!=' '):
                    res=True
                    k=0
                    val = s[(i,j)]
                    for z in range(min(6-i,7-j)):
                        if(k<5):
                            if(s[(z,z)]!=val):
                                res = False
                                k=0
                            else:
                                k=k+1
        
        if(res):
            fin=True
        
        for i in range(5):
            for j in range(6):
                if(s[(i,j)]!=' '):
                    res=True
                    k=0
                    val = s[(i,j)]
                    for z in range(max(6-i,7-j),0,-1):
                        if(k<5):
                            if(s[(z,z)]!=val):
                                res = False
                                k=0
                            else:
                                k=k+1
        
        if(res):
            fin=True
    
    return fin

def UtilityP4(s,profondeur):
    
    gain=0
    res=True
    for i in range(6):
        val=s[(i,0)]
        if(val!=' '):
            res=True
            k=0
            for j in range(1,7):
                if k<5:
                    if (s[(i,j)]!=val):
                        res=False
                        k=0
                    else:
                        k=k+1
                    
            if(res):
                if(val=='X'):
                    gain=1+profondeur
                elif(val=='O'):
                    gain=-1-profondeur
        
    for j in range(7):
        val=s[(0,j)]
        if(val!=' '):
            res=True
            k=0
            for i in range(1,6):
                if k<5:
                    if (s[(i,j)]!=val):
                        res=False
                        k=0
                    else:
                        k=k+1
            if(res):
                if(val=='X'):
                    gain=1+profondeur
                elif(val=='O'):
                    gain=-1-profondeur
    
    for i in range(5):
        for j in range(6):
            if(s[(i,j)]!=' '):
                res=True
                k=0
                val = s[(i,j)]
                for z in range(min(6-i,7-j)):
                    if(k<5):
                        if(s[(z,z)]!=val):
                            res = False
                            k=0
                        else:
                            k=k+1
                if(res):
                    if(val=='X'):
                        gain=1+profondeur
                    elif(val=='O'):
                        gain=-1-profondeur
        
    
    for i in range(5):
        for j in range(6):
            if(s[(i,j)]!=' '):
                res=True
                k=0
                val = s[(i,j)]
                for z in range(max(6-i,7-j),0,-1):
                    if(k<5):
                        if(s[(z,z)]!=val):
                            res = False
                            k=0
                        else:
                            k=k+1
                if(res):
                    if(val=='X'):
                        gain=1+profondeur
                    elif(val=='O'):
                        gain=-1-profondeur
                        
    return gain

def AfficheGrilleP4(s):
    for i in range(6):
        print([s[(i,j)]for j in range(7)])
        
def JoueurP4():
    
    choix_ligne=eval(input("Ligne ?")) # A sécuriser 
    choix_colonne=eval(input("Colonne ?"))
    ind = (choix_ligne,choix_colonne)
    return ind


def Alpha_Beta_SearchP4(s,alpha=-10000,beta=10000,profondeur=100):
    i=0

    res=Max_Value_Alpha_BetaP4(s, alpha, beta, profondeur)
    print(res)
    for a in ActionsP4(s):
        if res==Min_Value_Alpha_BetaP4(Result(s,a,1), alpha, beta, profondeur-1):
            print(res)
            i=a
            
    return i

def Max_Value_Alpha_BetaP4(s,alpha,beta,profondeur):
    if(Terminal_TestP4(s) or profondeur==0):
        return UtilityP4(s,profondeur)
    v=-10000
    for a in ActionsP4(s):
        v=max(v,Min_Value_Alpha_BetaP4(Result(s, a,1),alpha,beta,profondeur-1))
        if v>= beta:
            return v
        alpha=max(alpha,v)
    return v

def Min_Value_Alpha_BetaP4(s,alpha,beta,profondeur):
    if(Terminal_TestP4(s) or profondeur==0):
        return UtilityP4(s,profondeur)
    v=10000
    for a in ActionsP4(s):
        v=min(v,Max_Value_Alpha_BetaP4(Result(s, a,0),alpha,beta,profondeur-1))
        if v<=alpha:
            return v
        beta=min(beta,v)
    return v




def JeuP4(s):
    
    while(Terminal_TestP4(s)==False):
        AfficheGrilleP4(s)
        choix=JoueurP4()
        s=Result(s, choix, 0)
        s=Result(s, Alpha_Beta_SearchP4(s,profondeur=10),1)
    AfficheGrilleP4(s)
    if UtilityP4(s,0)<0:
        print("Gagné!")
    elif UtilityP4(s,0)>0:
        print("Perdu!")
    else:
        print("Match nul")

JeuP4(grilleP4)"""