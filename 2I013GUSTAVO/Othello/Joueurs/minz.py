# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game

poidsCases = [	[200, -20,  20,   5,   5,  20, -20, 200],
				[-20, -40,  -5,  -5,  -5,  -5, -40, -20],
				[20,  -5,  15,   3,   3,  15,  -5,  20],
				[5,  -5,   3,   3,   3,   3,  -5,   5],
				[5,  -5,   3,   3,   3,   3,  -5,   5],
				[20,  -5,  15,   3,   3,  15,  -5,  20],
				[-20, -40,  -5,  -5,  -5,  -5, -40, -20],
				[200, -20,  20,   5,   5,  20, -20, 200]]



X1 = [-1, -1, 0, 1, 1, 1, 0, -1];
Y1 = [0, 1, 1, 1, 0, -1, -1, -1];

moi = 1
adv = 2
prof = 2
w1 = 10 #parite coins
w2 = 80 #frontieres
w3 = 80  #mobilite
w4 = 800 #coins captures
w5 = 300 #proximite aux coins
w6 = 10 #poids cases

params = [w1,w2,w3,w4,w5,w6]

nbNoeuds = 0

def saisieCoup(jeu):
	global moi
	moi = game.getJoueur(jeu)
	coup = decision(jeu,game.getCoupsValides(jeu))
	return coup

def decision(jeu, listeCoups):
	global moi
	global adv
	moi = game.getJoueur(jeu)
	adv = game.getJoueurAdverse(jeu)
	m = -1000000
	coup = listeCoups[0]
	for c in listeCoups:
		s = estimation(jeu,c,1)
		#print "Decision",c,s
		if s > m:
			m = s
			coup = c
	return coup

def estimation(jeu, coup, p):
	global nbNoeuds
	nbNoeuds+=1
	copie = game.getCopieJeu(jeu)
	game.joueCoup(copie,coup)
	if game.finJeu(jeu):
		g = game.getGagnant(jeu)
		if g == moi:
			return 100000
		else:
			if g == 0:
				return -100
			else:
				return -100000
	if p == prof:
		l = parcoursPlateau(jeu)
		return evaluation(copie,l)
	cp = game.getCoupsValides(copie)
	m = 0
	for c in cp:
		s = estimation(copie,c,p+1)
		if p%2 == 0:
			if s >= m:
				m = s
		else:
			if s <=m:
				m = s
	return m

def evaluation(jeu, liste):
	return w1*f1(jeu,liste)+w2*f2(jeu,liste)+w3*f3(jeu,liste)+w4*f4(jeu,liste)+w5*f5(jeu,liste)+w6*f6(jeu,liste)

def parcoursPlateau(jeu):
	""" jeu -> int
		Retourne score d utilite calcule en fonction :
			- du tableau poidsCases
			- du nombre de pions de couleur noire ou blanche sur l echiquier
			- de la mobilite
			- du nombre de coins captures
	"""
	plateau = game.getPlateau(jeu)
	pionsMoi = 0
	pionsAdv = 0
	pionsFrontiereMoi = 0 #pions en frontiere = pions adjacents a des cases vides
	pionsFrontiereAdv = 0
	coinsMoi = 0 #coins captures
	coinsAdv = 0
	pionsProchesCoinsMoi = 0 #pions proches des coins
	pionsProchesCoinsAdv = 0
	scorePlateauPondere = 0
	for i in range(8):
		for j in range(8):
			if plateau[i][j] == moi:
				scorePlateauPondere += poidsCases[i][j]
				pionsMoi +=1
				if [i,j] == [0,0] or [i,j] == [0,7] or [i,j] == [7,0] or [i,j] == [7,7]:
					coinsMoi += 1
			elif plateau[i][j] == adv:
				scorePlateauPondere -= poidsCases[i][j]
				pionsAdv +=1
				if [i,j] == [0,0] or [i,j] == [0,7] or [i,j] == [7,0] or [i,j] == [7,7]:
					coinsAdv = 1
			if plateau[i][j] != 0:
				for k in range(8):
					x = i + X1[k]
					y = j + Y1[k]
					if x >= 0 and x < 8 and y >= 0 and y < 8 and plateau[x][y] == 0:
						if plateau[i][j] == moi:
							pionsFrontiereMoi += 1
						else:
							pionsFrontiereAdv +=1
						break
	if plateau[0][0] == 0:
		if (plateau[0][1] == moi):
			pionsProchesCoinsMoi += 1
		elif (plateau[0][1] == adv):
			pionsProchesCoinsAdv += 1
		if (plateau[1][1] == moi):
			pionsProchesCoinsMoi += 1
		elif (plateau[1][1] == adv):
			pionsProchesCoinsAdv += 1
		if (plateau[1][0] == moi):
			pionsProchesCoinsMoi += 1
		elif (plateau[1][0] == adv):
			pionsProchesCoinsAdv += 1
	if (plateau[0][7] == 0):
		if (plateau[0][6] == moi):
			pionsProchesCoinsMoi += 1
		elif (plateau[0][6] == adv):
			pionsProchesCoinsAdv += 1
		if (plateau[1][6] == moi):
			pionsProchesCoinsMoi += 1
		elif (plateau[1][6] == adv):
			pionsProchesCoinsAdv += 1
		if (plateau[1][7] == moi):
			pionsProchesCoinsMoi += 1
		elif (plateau[1][7] == adv):
			pionsProchesCoinsAdv += 1
	if (plateau[7][0] == 0):
		if (plateau[7][1] == moi):
			pionsProchesCoinsMoi += 1
		elif (plateau[7][1] == adv):
			pionsProchesCoinsAdv += 1
		if (plateau[6][1] == moi):
			pionsProchesCoinsMoi += 1
		elif (plateau[6][1] == adv):
			pionsProchesCoinsAdv += 1
		if (plateau[6][0] == moi):
			pionsProchesCoinsMoi += 1
		elif (plateau[6][0] == adv):
			pionsProchesCoinsAdv += 1
	if(plateau[7][7] == 0):
		if (plateau[6][7] == moi):
			pionsProchesCoinsMoi += 1
		elif (plateau[6][7] == adv):
			pionsProchesCoinsAdv += 1
		if (plateau[6][6] == moi):
			pionsProchesCoinsMoi += 1
		elif (plateau[6][6] == adv):
			pionsProchesCoinsAdv += 1
		if (plateau[7][6] == moi):
			pionsProchesCoinsMoi += 1
		elif (plateau[7][6] == adv):
			pionsProchesCoinsAdv += 1

	return [pionsMoi,pionsAdv,pionsFrontiereMoi,pionsFrontiereAdv,coinsMoi,coinsAdv,pionsProchesCoinsMoi,pionsProchesCoinsAdv,scorePlateauPondere]

def f1(jeu,liste):
	""" jeu -> int
		Parite des coins
	"""
	return (liste[0]-liste[1])/(liste[0]+liste[1])

def f2(jeu,liste):
	""" jeu -> int
		Frontiere
	"""
	if liste[2]+liste[3] != 0:
		return (liste[2]-liste[3])/(liste[2]+liste[3])
	return 0

def f3(jeu,liste):
	""" jeu -> int
		Mobilite
	"""
	cvAdv = game.getCoupsValides(jeu)
	game.changeJoueur(jeu)
	cvMoi = game.getCoupsValides(jeu)
	game.changeJoueur(jeu)
	if (game.getJoueur == moi and (cvMoi+cvAdv != 0)):
		return (cvMoi-cvAdv)/(cvMoi+cvAdv)
	return 0

def f4(jeu,liste):
	""" jeu -> int
		Coins captures
	"""
	return (liste[4]-liste[5])/4

def f5(jeu,liste):
	""" jeu -> int
		Proximite aux coins
	"""
	return (liste[6]-liste[7])/12

def f6(jeu,liste):
	""" jeu -> int
		Poids cases
	"""
	return liste[8]