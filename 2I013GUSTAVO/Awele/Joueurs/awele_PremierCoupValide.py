#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

def saisieCoup(jeu):
    """ jeu -> coup
    Retourne un coup a jouer
    """
    
    return game.getCoupsValides(jeu)[0]
