# -*- coding: utf-8 -*-
# A optimisé au max
# Il semble y avoir un pb lors du changement de joueur
import sys
import copy
sys.path.append("../..")
import game
import random
"""
	coeff1=>attaque
	coeff2=>preparation attaque
	coeff3=>defense
	prof=>horizon max d'anticipation
	j_initial=>jeu sans modifs
"""
coeff1 = 0.5
coeff2 = 0.2
coeff3 = 0.3
prof = 3
def estimation (jeu, coup, a, b, p):
    #retourne le score d'utilite pour un coup donne
    copie = game.getCopieJeu(jeu)
    game.joueCoup(copie, coup)
    if game.finJeu(copie):
        g = game.getGagnant(copie)
        if g == moi:
            return 100000
        else:
            if g == 0:
                return -100
            else:
                return -100000

    elif p >= prof:
        return evaluation(copie)
    m=0
    coups = game.getCoupsValides(copie)
    for c in coups:
        s = estimation(copie, c, a, b, p+1)
        if p % 2 == 0:
            m=a
            if s >= b:
            	return b
            if s > a:
                a = s
                m = s

        else:
            m=b
            if s <= a:
                return a
            if s < b:
                b = s
                m = b
    return m

def decision(jeu, coups):
    ma = 0
    coup=coups[0]
    for c in coups:
        al = -100000
        be = 100000
        s = estimation(jeu, c, al, be, 1)
        if s >= ma:
           ma = s
           coup = c
    return coup

def saisieCoup(jeu):
	""" jeu -> coup
		Retourne un coup a jouer
	"""
	global moi,lautre,tours,coeff1,coeff2,coeff3
	# if tours < 2:
	# 	coeff1+=0.05
	# 	coeff2+=0.025
	# 	coeff3-=0.025
	# elif (game.getScore(jeu,moi)-game.getScore(jeu,lautre) )< 0:
	# 	coeff1=0.8
	# 	coeff2=0.1
	# 	coeff3=0.1
	# else :
	# 	coeff1=0.7
	# 	coeff2=0.15
	# 	coeff3=0.15
	moi = game.getJoueur(jeu)
	lautre = moi % 2 + 1
	coup = decision(jeu,game.getCoupsValides(jeu))
	return coup
# jeu1 => jeu de base
# jeu2 => jeu modifie
# def evaluation(jeu1,jeu2):


def evaluation(jeu2):
	"""
	jeu*jeu -> float
	Retourne un nombre compris entre [0,1] qui evalue l'effacite d'un coup joue par rapport au nombre de cases à 0 , 1 ou 2 graines chez le joueur
	"""
	return coeff1*f1(jeu2)+coeff2*f2(jeu2)+coeff3*f3(jeu2)



def f1(jeu):
	"""
		jeu*jeu -> float
		Retourne un nombre compris entre [0,1] qui evalue l'effacite d'un coup joue par rapport au score
	"""
	return float(game.getScore(jeu,moi)-game.getScore(jeu,lautre))/18


def f3(jeu):
	"""
		jeu*jeu -> float
		pas de cases qui se suive
	"""
	l=[]
	if moi==1:
		i=5
		while i>0:
			nbCases = 0
			case = [moi-1,i]
			while game.getCaseVal(jeu,moi-1,case[1])<3 and case!=[1,0]:
				nbCases+=1
				case = caseSuivante(jeu,case)
			if nbCases>1: i-=nbCases
			else: i-=1
			l.append(nbCases)
	else:
		i=0
		while i<6:
			nbCases = 0
			case = [moi-1,i]
			while game.getCaseVal(jeu,moi-1,case[1])<3 and case!=[0,5]:
				nbCases+=1
				case = caseSuivante(jeu,case)
			if nbCases>1: i+=nbCases
			else: i+=1
			l.append(nbCases)
	return 1-float(max(l))/6

def f4(jeu):
	"""
		jeu*jeu -> float
		pas de cases qui se suive
		en debut de partie
	"""
	l=[]
	if moi==1:
		i=5
		while i>0:
			nbCases = 0
			case = [moi-1,i]
			while game.getCaseVal(jeu,moi-1,case[1])<6 and case!=[1,0]:
				nbCases+=1
				case = caseSuivante(jeu,case)
			if nbCases>1: i-=nbCases
			else: i-=1
			l.append(nbCases)
	else:
		i=0
		while i<6:
			nbCases = 0
			case = [moi-1,i]
			while game.getCaseVal(jeu,moi-1,case[1])<6 and case!=[0,5]:
				nbCases+=1
				case = caseSuivante(jeu,case)
			if nbCases>1: i+=nbCases
			else: i+=1
			l.append(nbCases)
	return 1-float(max(l))/6

def f2(jeu):
	"""
		jeu*jeu -> float
		cases qui se suive chez l'autre
	"""
	l=[]
	if lautre==1:
		i=5
		while i>0:
			nbCases = 0
			case = [lautre-1,i]
			while game.getCaseVal(jeu,lautre-1,case[1])<3 and case!=[1,0]:
				nbCases+=1
				case = caseSuivante(jeu,case)
			if nbCases>1: i-=nbCases
			else: i-=1
			l.append(nbCases)
	else:
		i=0
		while i<6:
			nbCases = 0
			case = [lautre-1,i]
			while game.getCaseVal(jeu,lautre-1,case[1])<3 and case!=[0,5]:
				nbCases+=1
				case = caseSuivante(jeu,case)
			if nbCases>1: i+=nbCases
			else: i+=1
			l.append(nbCases)

	return float(max(l))/6

def caseSuivante(jeu, case):
	"""
		jeu*case -> case
		Renvoie la case situee apres celle entree en parametre
	"""
	if case == [0,0] : return [1,0]
	elif case == [1,5] : return [0,5]
	elif case[0] == 0 : return [0,case[1] - 1]
	return [1,case[1] + 1]