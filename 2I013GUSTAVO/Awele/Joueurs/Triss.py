# -*- coding: utf-8 -*-
# A optimisé au max
# Il semble y avoir un pb lors du changement de joueur SILENCER
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
    0.5,0.2,0.3
"""
param=[0.4,0.5,0.3]
#coef=[2,2,6.1]
coeffparam1 =param[0]
coeffparam2 = param[1]
coeffparam3 = param[2]
prof = 5



#IA en AB
def saisieCoup(jeu):

    """ jeu -> coup
    Retourne un coup a jouer
    """
    global moi,adv
    
    moi = game.getJoueur(jeu)
    adv = moi%2 + 1
    coup = decision(jeu,game.getCoupsValides(jeu))
    return coup



def decision(jeu, coupsValides):
    maxx = 0
    
    coup = coupsValides[0]
    for c in coupsValides:
        alpha = -123456
        beta = 123456
        est = estimation(jeu,c,1,alpha,beta)#estimes le coup le plus optimal pour c dans les coups possible
        if est >= maxx: #si meilleur que coup precedent, remplace
           maxx = est 
           coup = c #choisi ce coup
    return coup

def estimation (jeu, coup, p, alpha, beta):
    #retourne le score d'utilite pour un coup donne
    copie = game.getCopieJeu(jeu)
    game.joueCoup(copie, coup)
    if game.finJeu(copie):
        g = game.getGagnant(copie)
        if g == moi:
            return 123456 #cas gagnant = estimation élevé
        else:
            if g == 0:
                return -123 #cas egalité = estimation neutre-negative
            else:
                return -123456 #cas perdant = estimation NEGATIVE

    elif p >= prof: #si profondeur trop élevé, (dernier noeud) renvoie une evaluation de la copie du jeu.
        return evaluation(copie)
    mValue=0
    coupsV = game.getCoupsValides(copie)
    for c in coupsV:
        est = estimation(copie, c, p+1, alpha, beta)
        if p % 2 == 0: #noeud MAX
            mValue=alpha
            if est >= beta:
            	return beta
            if est > alpha:
                alpha =est#on donne à a l'estimation s, qui sera réincrementé dans la boucle.
                mValue = alpha #on donne a m la valeur de l'estimation, car c'est m qui sera retourné a la fin

        else: #noeud MIN
            mValue=beta
            if est <= alpha:
                return alpha
            if est< beta:
                beta = est
                mValue = beta
    return mValue

def evaluation(jeu2):
	"""
	jeu*jeu -> float
	Retourne un nombre compris entre [0,1] qui evalue l'effacite d'un coup joue par rapport au nombre de cases à 0 , 1 ou 2 graines chez le joueur
	"""
	return coeffparam1*atk(jeu2)+coeffparam2*Defense(jeu2)+coeffparam3*Combo(jeu2)



def a1(jeu):
    """
    jeu*jeu -> float
    Retourne un nombre compris entre [0,1] qui evalue l'effacite d'un coup joue par rapport au score
    """
    return float(game.getScore(jeu,moi)-game.getScore(jeu,adv))/18

def atk(jeu):
    """
    jeu*jeu -> float
    Retourne un nombre compris entre [0,1] qui evalue l'effacite d'un coup joue par rapport au score
    """

    return float(game.getScore(jeu,moi)-game.getScore(jeu,adv))/18


def Defense(jeu):
    """
        jeu*jeu -> float
        commence a la derniere case de notre camps puis remonte jusqua la premiere case ( de gauche a droite)
        si on est dans mon camp et qu'il ya moin de 3 graines, je compte la case
        pas de cases qui se suive
    """
    l=[]
    if moi==1: # si je suis joueur 1, different plateau entre joueur 1 et joueur 2
        i=5#on commence en bout de plateau (bout droit colonne 5)
        while i>0:#compteur pour sortir
            nbCases = 0
            case = [moi-1,i] #[0,5]
            while game.getCaseVal(jeu,moi-1,case[1])<3 and case!=[1,0]:#tant que la case (ligne moi-1=0 et colonne case[1]==colonne 1) a moin de 3 graine. Case [1;0] premiere case ennemie
                nbCases+=1
                case = nextCase(jeu,case)
            if nbCases>1: i=i-nbCases#permet d'évaluer les cases restantes. 3case a risque, 5-3=2 il reste 3 cases a évalué (case 2,1,0), permet de pas faire 2 evaluations
            else: i-=1#decremente compteur pour sortir
            l.append(nbCases)#nbre de case consecutive a risque dans une liste [3,2;0]: 3 case, 2 case et 0 case a risuqe consecutive
    else:#sinon moi==2
        i=0#on commence en bout de plateau (bout gauche colonne 0)
        while i<6:
            nbCases = 0
            case = [moi-1,i]#[1,0]
            while game.getCaseVal(jeu,moi-1,case[1])<3 and case!=[0,5]:#Case [0;5] premiere case ennemie
                nbCases+=1
                case = nextCase(jeu,case)
            if nbCases>1: i+=nbCases
            else: i+=1
            l.append(nbCases)
    return 1-float(max(l))/6 #renvoie la valeur max de la liste , div par/6 pour avoir une valeeur entre 0 et 1 et (1-) pour positive


def Combo(jeu):
    """
    jeu*jeu -> float
        meme chose qu'au dessus, sauf quon regarde si au lieu de moi, cela se passe chez adv
        cases qui se suive chez l'autre
    """
    l=[]
    if adv==1:
        i=5
        while i>0:
            nbCases = 0
            case = [adv-1,i]
            while game.getCaseVal(jeu,adv-1,case[1])<3 and case!=[1,0]:
                nbCases+=1
                case = nextCase(jeu,case)
            if nbCases>1: i-=nbCases
            else: i-=1
            l.append(nbCases)
    else:
        i=0
        while i<6:
            nbCases = 0
            case = [adv-1,i]
            while game.getCaseVal(jeu,adv-1,case[1])<3 and case!=[0,5]:
                nbCases+=1
                case = nextCase(jeu,case)
            if nbCases>1: i+=nbCases
            else: i+=1
            l.append(nbCases)

    return float(max(l))/6


def nextCase(jeu, case):
    """
    jeu*case -> case
    Renvoie la case situee apres celle entree en parametre
    """
    if case == [0,0] : return [1,0]
    elif case == [1,5] : return [0,5]
    elif case[0] == 0 : return [0,case[1] - 1]
    return [1,case[1] + 1]