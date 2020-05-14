# -*- coding: utf-8 -*-
import sys
import copy
sys.path.append("../..")
import game
import random
"""
    coeff1=>attaque
    coeff2=>defense
    prof=>horizon max d'anticipation
"""
coeff1 = 1
coeff2 = 0
moi = 1
prof =1
 
debut_j = []
pmax =5
nombreDeNoeuds=0
def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    global debut_j,moi
    #debut_j = game.getCopieJeu(jeu)#copie
    moi = game.getJoueur(jeu)
    #adv = game.getJoueurAdverse(jeu)
    adv=moi%2 +1
    coup = decision(jeu,game.getCoupsValides(jeu))
    return coup

def decision(jeu,coupsV):
    
    """jeu*ListeCoupValide->coup
    choix parmis les coupsValides, on voit celui qui a l'estimation qui nous arrange
    """
    maxi=-1234567
    coup = coupsV[0]
    for c in coupsV:
        est = estimation(jeu,c,1)
        if est>=maxi:
            maxi=est
            coup= c
    return coup

def estimation(jeu,coup,p):
    global nombreDeNoeuds
    nombreDeNoeuds+=1
    copie = game.getCopieJeu(jeu)
    game.joueCoup(copie,coup)
    if game.finJeu(copie):
        g=game.getGagnant(copie)
        if g == moi:   #si c'est moi le vainqueur alors estimation élevée
            return 12345
        else:
            if g == 0:  #si c'est nul alors estimation moyenne
                return -123
            else: #pire cas estimation faible
                return -12345
    if p>=prof:
        #max profondeur donc on evalue 
        return evaluation(jeu,copie)
    else:
        coupsV=game.getCoupsValides(copie)
        mValue=0
        for c in coupsV:
            est =estimation(copie,c,p+1)
            if p%2 == 0:#MAX
                if est >= mValue:
                    mValue= est
            else:#MIN
                if est <=mValue:
                    mValue = est
                
    return mValue

def evaluation(jeu1,jeu2):
	"""
	jeu*jeu -> float
	Retourne un nombre compris entre [0,1] qui evalue l'effacite d'un coup joue par rapport au nombre de cases à 0 , 1 ou 2 graines chez le joueur
	"""

	return coeff1*attaque(jeu1,jeu2) + coeff2*defense(jeu1,jeu2)

def attaque(jeu1,jeu2):
	"""
		jeu*jeu -> float
		Retourne un nombre compris entre [0,1] qui evalue l'effacite d'un coup joue par rapport au score
	"""
	if float(game.getScore(jeu1,moi)-game.getScore(jeu2,moi))/18 >0:
		return float(abs(game.getScore(jeu1,moi)-game.getScore(jeu2,moi)))/18
	else:
		return 0

def defense(jeu1,jeu2):
	"""
		jeu*jeu -> float
		Retourne un nombre compris entre [0,1] qui evalue l'effacite d'un coup joue par rapport au nombre de cases à 0 , 1 ou 2 graines chez le joueur
	"""
	nbCases = 0
	for i in range(6):
		if game.getCaseVal(jeu2,moi-1,i)<3:
			nbCases+=1
	return 1.0 - float(nbCases)/6
