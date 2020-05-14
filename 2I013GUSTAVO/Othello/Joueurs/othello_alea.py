import sys
sys.path.append("../..")
import game
import random

def saisieCoup(jeu):
	""" jeu -> coup
		Retourne un coup a jouer
	"""
	return game.getCoupsValides(jeu)[random.randrange(len(game.getCoupsValides(jeu)))]