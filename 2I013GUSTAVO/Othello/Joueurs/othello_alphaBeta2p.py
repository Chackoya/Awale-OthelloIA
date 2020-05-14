# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

moi = 1
adv = 2
prof = 2

def saisieCoup(jeu):
	""" jeu -> coup
		Retourne un coup a jouer
	"""
	global moi
	moi = game.getJoueur(jeu)
	coup = decision(jeu, game.getCoupsValides(jeu))
	return coup

def decision(jeu, coups):
	#print("coups valides ="+str(game.getCoupsValides(jeu)))
	alpha= -123456
	beta = 123456
	coup = coups[0]
	#print "coup "+str(coups[0])+ " = > "+str(coup)
	for c in coups:
		s = estimation(jeu, c, 1, alpha, beta)
		#print "coup "+str(c)+ " = > "+str(s)
		if s > alpha:
			alpha = s
			coup = c
	#print "coup choisi ="+str(coup)
	return coup

def estimation(jeu ,coup, p, a, b):
	copie = game.getCopieJeu(jeu)
	game.joueCoup(copie,coup)
	if game.finJeu(copie):
		g = game.getGagnant(copie)
		if g == moi:
			return 12345
		else:
			if g == 0:
				return -123
			else:
				return -12345
	if p == prof:
		return evaluation(copie)
	else:
		cp = game.getCoupsValides(copie)
		if p % 2 == 0:
			m=a
		else:
			m=b
		for c in cp:
			s = estimation(copie,c,p+1,a,b)
			if p % 2 == 0:
				if s >= m:
					a = s
					m = s
				if s > b:
					return b
			else:
				if s <= m:
					b = s
					m = s
				if s < a:
					return a
		return m

def evaluation(jeu):
	score = 0
	coin = 25
	cote = 5
	frontiere = 5
	for i in range(8):
		for j in range(8):
			add = 1
			if (i == 0 and j == 1) or (i == 1 and 0 <= j <= 1):
				if jeu[0][0][0] == moi: add = cote
				else: add = - frontiere
			elif (i == 0 and j == 6) or (i == 1 and 6 <= j <= 7):
				if jeu[0][7][0] == moi: add = cote
				else: add = - frontiere
			elif (i == 7 and j == 1) or (i == 6 and 0 <= j <= 1):
				if jeu[0][0][7] == moi: add = cote
				else: add = - frontiere
			elif (i == 7 and j == 6) or (i == 6 and 6 <= j <= 7):
				if jeu[0][7][7] == moi: add = cote
				else: add = - frontiere

			if (i == 0 and 1< j <6 ) or (i == 7 and 1< j <6) or (j == 0 and 1< i <6 ) or (j == 7 and 1< i <6): add = 5
			elif (i == 0 and j == 0) or (i == 0 and j == 7) or (i == 7 and j == 0) or (i == 7 and j == 7): add = coin

			if (jeu[0][i][j] == moi): score += add
			elif (jeu[0][i][j] == adv): score -= add
	return score
"""
def getParams():
	return params

def getNbParams():
	return len(params)

def setParam(i,x):
	params[i]=x

def addParam(i,x):
	params[i]+=x# -*- coding: utf-8 -*-

"""