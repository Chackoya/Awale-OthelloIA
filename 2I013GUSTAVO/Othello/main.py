#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

# Debut du decompte du temps
start_time = time.time()
import othello
import sys

sys.path.append("..")
import game
game.game=othello
sys.path.append("./Joueurs")

import othello_alea
import othello_joueur_humain
import othello_PremierCoupValide
import othello_minMax
import othello_alphaBeta
import othello_alphaBeta2p
import minz
"""

game.joueur1=awele_alea
game.joueur2=awele_alea

"""
playerONE=1
playerTWO=2
nbRounds=30
def jouePARTIE(j1,j2):
    global playerONE
    global playerTWO

#On initialise a ALEA les 4 premier Coups pr que ce soit équilibré et pr éviter même partie.
    for i in range(1):
       jeu=game.initialiseJeu()
       game.joueur1=othello_alea
       game.joueur2=othello_alea
       
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
    g=jouePARTIE(othello_alphaBeta,othello_alphaBeta)
    if(i>=nbRounds/2) and (g==playerONE):
        print("Gagnant de la partie num",i+1," est : ",playerTWO)
        wins[playerTWO]+=1
    elif (i>=nbRounds/2) and (g==playerTWO):
        print("Gagnant de la partie num",i+1," est : ",playerONE)
        wins[playerONE]+=1
    else:
        print("Gagnant de la partie num",i+1,"est : ",g)
        wins[g]+=1


print("partie terminée...")
print("****************************SCORES****************************")
print("Joueur 1:",str(wins[1]),"\nJoueur 2:",str(wins[2]),"\nMatchs NULS:",str(wins[0]))


# Affichage du temps d execution
print("Temps d'execution: %s secondes --" % (time.time() - start_time))

"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import othello
import sys
sys.path.append("..")
import game
game.game=othello
sys.path.append("./Joueurs")
import othello_alea
import othello_joueur_humain
import othello_PremierCoupValide

game.joueur1=othello_alea
game.joueur2=othello_alea


def jouePARTIE():
    jeu=game.initialiseJeu()
    
    game.joueur1=othello_alea
    game.joueur2=othello_alea 
    
    
    while not game.finJeu(jeu):
        if len(game.getCoupsJoues(jeu))==4:
            #########INITIALISER JOUEURS ICI:############
            game.joueur1=othello_alea
            game.joueur2=othello_alea
        game.affiche(jeu)
        coup=game.saisieCoup(jeu)
        game.joueCoup(jeu,coup)
     
        print ("Nombre de tours : " + str(len(game.getCoupsJoues(jeu))))
                
    print("Gagnant de la partie est : ",game.getGagnant(jeu))
    g=game.getGagnant(jeu)
    return g
    
    


victories=[0,0,0]
print("****************************DEBUT****************************")
for i in range(100):
    g=jouePARTIE();
    
    victories[g] += 1
    


print("partie terminée...")
print("****************************SCORES****************************")
print("Joueur 1:",str(victories[1]),"\nJoueur 2:",str(victories[2]),"\nMatchs NULS:",str(victories[0]))

"""