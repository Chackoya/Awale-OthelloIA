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
"""
"""
import lol
import Geralt
import pedro
import Ciri

def jouePARTIE():
    jeu = game.initialiseJeu()
    while not game.finJeu(jeu):
        game.affiche(jeu)
        coup = game.saisieCoup(jeu)
        game.joueCoup(jeu,coup)
        print ("Nombre de tours : " + str(len(game.getCoupsJoues(jeu)))) #str permet de cast, sinon on peut pas concatener un str et un int
    if game.getGagnant(jeu)==0:
        print ("\nEgalite parfaite !")
    else:
        print ("\nLe joueur "+ str(game.getGagnant(jeu)) + " a gagne !")
    print ("\nPlateau de fin de jeu: ")
    game.game.affiche(jeu)
    g=game.getGagnant(jeu)
    return g

victories=[0,0,0]
print("****************************DEBUT****************************")
for i in range(10):
    g=jouePARTIE();
    
    victories[g] += 1
    


print("partie terminée...")
print("****************************SCORES****************************")
print("Joueur 1:",str(victories[1]),"\nJoueur 2:",str(victories[2]),"\nMatchs NULS:",str(victories[0]))

# -*- coding: utf-8 -*-

