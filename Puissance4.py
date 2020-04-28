#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 01:41:59 2020

@author: chendeb
"""

import http.client
import time
import numpy as np
from algo import Grille

CRED = '\33[31m'
CEND = '\033[0m'
CBLUE   = '\33[34m'

servergame="chendeb.free.fr"


def jouerWEB(idjeu,monid,tour,jeu,server=servergame):
    conn = http.client.HTTPConnection(server)
    conn.request("GET", "/Puissance6?status=JeJoue&idjeu="+idjeu+"&idjoueur="+monid+"&tour="+str(tour)+"&jeu="+str(jeu))
    r1 = conn.getresponse()
    return (r1.status, r1.reason)  

def getJeuAdv(idjeu,idAdv,tour,server=servergame):
    conn = http.client.HTTPConnection(server)
    conn.request("GET", "/Puissance6?status=GetJeuAdv&idjeu="+idjeu+"&idjoueur="+idAdv+"&tour="+str(tour))
    r1 = conn.getresponse()
    advJeu=None
    if(r1.status==200):
        temp=r1.read()
        print(temp)
        if(temp.decode('UTF-8')!='PASENCOREJOUE'):
            advJeu=int(temp)
    return advJeu  

def loopToGetJeuAdv( inetvalle,idjeu,idAdv,tour,server=servergame):
    advJeu=getJeuAdv(idjeu,idAdv,tour,server)
    while(advJeu==None):
        time.sleep(inetvalle)
        advJeu=getJeuAdv(idjeu,idAdv,tour,server)
    return advJeu

def remplirGrille(joueur, jeu):
    for i in range(grilleDim-1,-1,-1):
        if(grille[i][jeu]==0):
            grille[i][jeu]=joueur
            break
            
def printGrille():
    for i in range(grilleDim):
        print("|",end=' ')
        for j in range(grilleDim):
            if(grille[i][j]==1):
                print(CBLUE+'0'+CEND,end=' ')
            elif grille[i][j]==2:
                print(CRED+'0'+CEND,end=' ')
            else:
                print(" ",end=' ')
            print("|",end=' ')
        print()
    print("|",end=' ')
    for i in range(grilleDim):
        print("_",end=" ")
        print("|",end=' ')
    print()
    print("|",end=' ')
    for i in range(grilleDim):
        print(i%10,end=" ")
        print("|",end=' ')
    print()
    







#############################################################
#                                                           #
#  Vous n'avez qu'a remplacer les deux methodes monjeu et   #
#      appliqueJeuAdv  selon votre IA                       #
#                                                           #
#  Bien definir un idjeu pour l'id de la partie de jeu      #
#  votre nom et celui du joueur distant                     #
#  puis bien préciser si vous commencer le jeu True,        #
#  False signifie que le joueurDistant qui commence.        #
#                                                           #
#                                                           #
#############################################################



grilleDim=12
grille=np.zeros((grilleDim,grilleDim),dtype=np.byte)



#idjeu est un id unique, si vous abondonnez une partie, pensez à créer un nouveau idjeu
idjeu="ID280420201"
idjoueurLocal="leo"
idjoueurDistant="tristan"

# bien préviser si vous commencer le jeu ou c'est l'adversaire qui commence
joueurLocalquiCommence=False



#cette methode est à remplacer par votre une fonction IA qui propose le jeu
def monjeu():
    return int(input("vueillez saisir la colonne de votre jeu entre 0 et "+ str(grilleDim-1) +" : "))


# cette fonction est à remplacer une qui saisie le jeu de l'adversaire à votre IA
def appliqueJeuAdv(jeu):
    print("jeu de l'adversair est ", jeu)




if(joueurLocalquiCommence):
    joueurLocal=2
    joueurDistant=1
else:
    joueurLocal=1
    joueurDistant=2
    
    
tour=0
while(True):
    
    grilleJeu = Grille(grilleDim, grilleDim)
    
    if(joueurLocalquiCommence):
        jeu= grilleJeu.play(1,5)
        jouerWEB(idjeu,idjoueurLocal,tour,jeu)
        grilleJeu.apply(jeu,1)
        print(grilleJeu)
        jeuAdv=loopToGetJeuAdv( 10,idjeu,idjoueurDistant,tour)
        #c'est ce jeu qu'on doit transmettre à notre IA
        appliqueJeuAdv(jeuAdv)
        grilleJeu.apply(jeuAdv, -1)
        print(grilleJeu)
    else:
        jeuAdv=loopToGetJeuAdv( 10,idjeu,idjoueurDistant,tour)
        #c'est ce jeu qu'on doit transmettre à notre IA
        appliqueJeuAdv(jeuAdv)
        grilleJeu.apply(jeuAdv, -1)
        print(grilleJeu)
        jeu=grilleJeu.play(1,5)
        jouerWEB(idjeu,idjoueurLocal,tour,jeu)
        grilleJeu.apply(jeu,1)
        print(grilleJeu)
        
    tour+=1        
    

