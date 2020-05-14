#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    print("Les coups valides sont:")
    print(str(game.getCoupsValides(jeu)))
    i= int(input("Entrer la colonne du coup à jouer: "))
    return [jeu[1] - 1, i]