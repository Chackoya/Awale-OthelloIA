# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")
import game
prof=2
moi=1
adv=2

weights = [[40 , -30,  20,  20,  20,  20, -30,  40],
           [-30, -40, -10, -10, -10, -10, -40, -30],
           [20 , -10,  10,   0,   0,  10, -10,  20],
           [20 , -10,   0,  10,  10,   0, -10,  20],
           [20 , -10,   0,  10,  10,   0, -10,  20],
           [20 , -10,  10,   0,   0,  10, -10,  20],
           [-30, -40, -10, -10, -10, -10, -40, -30],
           [40 , -30,  20,  20,  20,  20, -30,  40]]



X1 = [-1, -1, 0, 1, 1, 1, 0, -1];
Y1 = [0, 1, 1, 1, 0, -1, -1, -1];
#Poids des heurestiques sont adaptables en fonction de l'état du jeu
w1=1 #COIN PARITY
w2=1 #FRONTIERS -> PIONS ADJACENTS A DES CASES VIDES
w3=2  #MOBILITY(debut de partie -> poids fort mais tend vers 0 qd c'est vers la fin de partie)
w4 =3 #CORNERS CAPTURED
w5=5 #PROXIMITY TO CORNERS
w6 =4 #POIDS CASES

params = [w1,w2,w3,w4,w5,w6]
debut_j=[]
nombreDeNoeuds = 0
#ELAGAGE ALPHA BETA
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
    global nombreDeNoeuds
    nombreDeNoeuds+=1
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
    return w1*func1(jeu,liste)+w2*func2(jeu,liste)+w3*func3(jeu,liste)+w4*func4(jeu,liste)+w5*func5(jeu,liste)+w6*func6(jeu,liste)

def setParam(i,x):
    params[i]=x

def addParam(i,x):
    params[i]+=x

def getNbParams():
    return len(params)

def getParams():
    return params

def evalj(jeu):
    #pas sur de la fonction
    return game.getScore(jeu,game.getJoueur(jeu))

#FONCTIONS ATTACK / DEFENSES

def func1(jeu,liste):
    """ jeu -> int
    	Parite des coins
    """
    return (liste[0]-liste[1])/(liste[0]+liste[1])

def func2(jeu,liste):
    """ jeu -> int
    Frontiere
    """
    if liste[2]+liste[3] != 0:
        return (liste[2]-liste[3])/(liste[2]+liste[3])
    return 0

def func3(jeu,liste):
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

def func4(jeu,liste):
    """ jeu -> int
    	Coins captures
    """
    return (liste[4]-liste[5])/4

def func5(jeu,liste):
    """ jeu -> int
    Proximite aux coins
    """
    return (liste[6]-liste[7])/12

def func6(jeu,liste):
    """ jeu -> int
    Poids cases
    """
    return liste[8]


##FONCTION PR PARCOURIR TT LE TABLEAU PR OBTENIR LES VALEURS PR LES SCORES
def parcoursPlateau(jeu):
    """ jeu -> int
        Retourne score d utilite calcule en fonction :
        * du tableau weights qui correspond au poids de chaque Case du plateau
    -   * du nombre de pions de chaque couleur sur le plateau(noir/blanche)
        * de la mobilite
        * du nombre de corners captures(plus haut p)
        """
    plateau = game.getPlateau(jeu)
    moi_pions= 0 #NB de pions 
    adv_pions= 0
    moi_pionsFrontier = 0 #pions a moi adjacents a cases vides
    adv_pionsFrontier= 0#pions adv adjacents a cases vides
    moi_Corners =0 #coins captures par moi
    adv_Corners =0#coins capturés par l'adversaire
    moi_pionsNearCorners=0#pions proches des coins valeur pr moi
    adv_pionsNearCorners=0#pions proches des coins valeur pr adversaire
    
    scoreP=0
    
    for i in range (8):
        for j in range(8):
            if plateau[i][j]==moi: #VERIF SI piece est a moi si oui on incremente score pions
                scoreP = scoreP+ weights[i][j]
                moi_pions+=1
                
                if (i==0 and j==0) or (i==7 and j==0)or(i==0 and j==7)or(i==7 and j==7):
                    moi_Corners=moi_Corners+1
            
            
            elif plateau[i][j]==adv:
                
                
                scoreP = scoreP - weights[i][j]
                adv_pions+=1
                if(i==0 and j==0) or (i==7 and j==0)or(i==0 and j==7)or(i==7 and j==7):
                    adv_Corners=adv_Corners+1
                    
            if plateau[i][j]!=0:
                
                for k in range(8):
                    x=i+X1[k]
                    y=j+Y1[k]
                    if x>=0 and x<8 and y>=0 and y<8 and plateau[x][y]==0:
                        if plateau[i][j]==moi:
                            moi_pionsFrontier=moi_pionsFrontier +1
                        else:
                            adv_pionsFrontier=moi_pionsFrontier+1
                        
                        
                        break
                    
#on verifie s'il y a des pieces posées autour des corners...
#COIN haut gauche:
    if plateau[0][0]==0:
        if(plateau[0][1]==adv):
            adv_pionsNearCorners+=1
        elif(plateau[0][1]==moi):
            moi_pionsNearCorners+=1

        if(plateau[1][0]==adv):
            adv_pionsNearCorners+=1
        elif(plateau[1][0]==moi):
            moi_pionsNearCorners+=1

        if (plateau[1][1]==adv):
            adv_pionsNearCorners+=1
        elif(plateau[1][1]==moi):
            moi_pionsNearCorners+=1

#COIN bas gauche:
    if(plateau[7][0]==0):
        if(plateau[6][1]==adv):
            adv_pionsNearCorners+=1
        elif(plateau[6][1]==moi):
            moi_pionsNearCorners+=1

        if(plateau[6][0]==adv):
            adv_pionsNearCorners+=1
        elif(plateau[6][0]==moi):
            moi_pionsNearCorners+=1

        if (plateau[7][1]==adv):
            adv_pionsNearCorners+=1
        elif(plateau[7][1]==moi):
            moi_pionsNearCorners+=1

#COIN haut droit
    if(plateau[0][7]==0):
        if(plateau[0][6]==adv):
            adv_pionsNearCorners+=1
        elif(plateau[0][6]==moi):
            moi_pionsNearCorners+=1

        if(plateau[1][6]==adv):
            adv_pionsNearCorners+=1
        elif(plateau[1][6]==moi):
            moi_pionsNearCorners+=1

        if (plateau[1][6]==adv):
            adv_pionsNearCorners+=1
        elif(plateau[1][6]==moi):
            moi_pionsNearCorners+=1

#COIN bas droit
    if(plateau[7][7]==0):
        if(plateau[6][6]==adv):
            adv_pionsNearCorners+=1
        elif(plateau[6][6]==moi):
            moi_pionsNearCorners+=1

        if(plateau[7][6]==adv):
            adv_pionsNearCorners+=1
        elif(plateau[7][6]==moi):
            moi_pionsNearCorners+=1

        if (plateau[6][7]==adv):
            adv_pionsNearCorners+=1
        elif(plateau[6][7]==moi):
            moi_pionsNearCorners+=1

    return [moi_pions,adv_pions,moi_pionsFrontier,adv_pionsFrontier , moi_Corners,adv_Corners,moi_pionsNearCorners,adv_pionsNearCorners,scoreP]