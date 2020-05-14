#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import sys
sys.path.append("../..")
import game

def saisieCoup(jeu):
    """ jeu -> coup 
    JOUEUR ALEATOIRE: Retourne un random coup a jouer
    """
    
    return game.getCoupsValides(jeu)[random.randrange(len(game.getCoupsValides(jeu)))]
