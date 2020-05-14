import sys
sys.path.append("../..")
import game

def saisieCoup(jeu):
    """jeu->coup
    
    Retourne un coup A jouer (1ER COUP VALIDE)"""
    return game.getCoupsValides(jeu)[0]
