#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    
    
    print("La liste des coups valides est:", game.getCoupsValides(jeu))
    ligne = int(input("Entrer la ligne du coup à jouer: "))
    colonne = int(input("Entrer la colonne du coup à jouer: "))
    return [ligne, colonne]

