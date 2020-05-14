#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import awele
import sys
# Debut du decompte du temps
start_time = time.time()

sys.path.append("..")
import game
game.game=awele
sys.path.append("./Joueurs")

import awele_alphaBeta
import awele_minMax
import awele_alea
import awele_joueur_humain
import awele_PremierCoupValide
import Keira
"""
"""
import Triss
import Geralt
import pedro
import Ciri
import Oracle
#game.joueur1=awele_alphaBeta
#game.joueur2=awele_alphaBeta
"""
"""
playerONE=1
playerTWO=2
nbRounds=100

def jouePARTIE(j1,j2):
    global playerONE
    global playerTWO

#On initialise a ALEA les 4 premier Coups pr que ce soit équilibré et pr éviter même partie.
    for i in range(1):
       jeu=game.initialiseJeu()
       game.joueur1=awele_alea
       game.joueur2=awele_alea
       
       while not game.finJeu(jeu):
           #game.affiche(jeu)
           coup=game.saisieCoup(jeu)
           game.joueCoup(jeu,coup)
           if len(game.getCoupsJoues(jeu))==4:    
               game.joueur1=j1 
               game.joueur2=j2
        
           if i==nbRounds/2 :
               game.joueur1=j2
               game.joueur2=j1
               #playerONE=2
               #playerTWO=1
               
           #print ("Nombre de tours : " + str(len(game.getCoupsJoues(jeu))))
    #print("Gagnant de la partie est : ",game.getGagnant(jeu))
    gagnant=game.getGagnant(jeu)
    
    return gagnant

wins=[0,0,0]# wins => stockage des nb de victoire de chaque joueurs et ainsi que les match nuls.
print("****************************DEBUT****************************")
for i in range(nbRounds):#MODIF ICI JOUEURS
    g=jouePARTIE(Oracle,Triss)
    if(i>=nbRounds/2) and (g==playerONE):
        print("Gagnant de la partie num ",i+1," est : ",playerTWO)
        wins[playerTWO]+=1
    elif (i>=nbRounds/2) and (g==playerTWO):
        print("Gagnant de la partie num ",i+1," est : ",playerONE)
        wins[playerONE]+=1
    else:
        print("Gagnant de la partie num ",i+1," est : ",g)
        wins[g]+=1


print("partie terminée...")
print("****************************SCORES****************************")
print("Joueur 1:",str(wins[1]),"\nJoueur 2:",str(wins[2]),"\nMatchs NULS:",str(wins[0]))

# Affichage du temps d execution
print("Temps d'execution: %s secondes --" % (time.time() - start_time))
       
#game.game.affichage(jeu)

"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import awele
import sys

sys.path.append("..")
import game
game.game=awele
sys.path.append("./Joueurs")

import awele_minMax
import awele_alea

victories=[0,0,0]
i=0
game.joueur1=awele_alea 
game.joueur2=awele_alea 
#joueur_premierCoupValide   

partie=0


while(partie<100):
    
    jeu=game.initialiseJeu()
    while not game.finJeu(jeu):
        if(i==0):
            game.joueur1=awele_alea 
            game.joueur2=awele_alea
        if(i==4):
            game.joueur1=awele_minMax 
            game.joueur2=awele_alea
        
        game.affiche(jeu)
        coup=game.saisieCoup(jeu)
        game.joueCoup(jeu,coup)
        i+=1
    i=0
    print(game.getScore(jeu,0))
    print(game.getScore(jeu,1))
    print ("Nombre de tours : " + str(len(game.getCoupsJoues(jeu))))
        
    g=game.getGagnant(jeu)
    
    victories[g]+=1
    print("Gagnant de la partie est : ",game.getGagnant(jeu))
    partie+=1
    



print("****************************DEBUT****************************")

    


print("partie terminée...")
print("****************************SCORES****************************")
print("Joueur 1:",str(victories[1]),"\nJoueur 2:",str(victories[2]),"\nMatchs NULS:",str(victories[0]))


       
#game.game.affichage(jeu)
 """