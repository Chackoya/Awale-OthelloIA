# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game
#axe
"""
weightsC = [	[100, -3,  2,   2,   2,  2, -3, 100],
				[-3, -4,  -1,  -1,  -1,  -1, -4, -3],
				[2,  -1,  1,   0,   0,  1,  -1,  2],
				[2,  -1,   0,   1,   1,   0,  -1,   2],
				[2,  -1,   0,   1,   1,   0,  -1,   2],
				[2,  -1,  1,   0,   0,  1,  -1,  2],
				[-3, -4,  -1,  -1,  -1,  -1, -4, -3],
				[100, -3,  2,   2,   2,  2, -3, 100]]
"""


weightsC = [[40 , -30,  20,  20,  20,  20, -30,  40],
           [-30, -40, -10, -10, -10, -10, -40, -30],
           [20 , -10,  10,   0,   0,  10, -10,  20],
           [20 , -10,   0,  10,  10,   0, -10,  20],
           [20 , -10,   0,  10,  10,   0, -10,  20],
           [20 , -10,  10,   0,   0,  10, -10,  20],
           [-30, -40, -10, -10, -10, -10, -40, -30],
           [40 , -30,  20,  20,  20,  20, -30,  40]]
moi = 1
adv = 2
prof = 2
w1 = 1
w2 = 0
w3 = 0
w4 = 0
params=[w1,w2,w3,w4]
def saisieCoup(jeu):

    """ jeu -> coup
    Le coup a jouer apres calcul
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

    if p >= prof: #si profondeur trop élevé, (dernier noeud) renvoie une evaluation de la copie du jeu.
        liste_parcoursPlat= parcoursPlateau(jeu)
        return evaluation(copie,liste_parcoursPlat)

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


def evaluation(jeu, liste):
    return w1*f1(jeu,liste)+w2*f2(jeu,liste)+w3*f3(jeu)+w4*f4(jeu,liste)

def parcoursPlateau(jeu):
    """ jeu -> int
    Score utilisé par rapport
            - au tableau de weightsC(poids pr chaque case)
            - du nombre de pions de couleur noire ou blanche sur le plateau
            - mobilité
            - coins captures
            """
    pio = 0
    mobi = 0
    ccaptur = 0
    for i in range(8):
        for j in range(8):
            if game.getPlateau(jeu)[i][j] == moi:
                pio += weightsC[i][j]
                if [i,j] == [0,0] or [i,j] == [0,7] or [i,j] == [7,0] or [i,j] == [7,7]:
                    ccaptur += 1
            elif game.getPlateau(jeu)[i][j] == adv:
                pio -= weightsC[i][j]
                mobi += 1
                if [i,j] == [0,0] or [i,j] == [0,7] or [i,j] == [7,0] or [i,j] == [7,7]:
                    ccaptur -= 1
    return [pio,mobi,ccaptur]

def f1(jeu,liste):
    """ jeu -> int
    	Stabilite
        """
    return liste[0]

def f2(jeu,liste):
    """ jeu -> int
    	Maximisation
        """
    return liste[1]

def f3(jeu):
    """ jeu -> int
    	Mobilite
        """
    cv = game.getCoupsValides(jeu)
    if game.getJoueur(jeu) == moi:
        return len(cv)
    else:
        return -len(cv)

def f4(jeu,liste):
    """ jeu -> int
    Coins captures
    """
    return liste[2]
def getParams():
    return params

def getNbParams():
    return len(params)

def setParam(i,x):
    params[i]=x

def addParam(i,x):
    params[i]+=x