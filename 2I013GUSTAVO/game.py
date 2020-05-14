#!/usr/bin/env python
# -*- coding: utf-8 -*-

# plateau: List[List[nat]]
# liste de listes (lignes du plateau) d'entiers correspondant aux contenus des cases du plateau de jeu

# coup:[nat nat]
# Numero de ligne et numero de colonne de la case correspondante a un coup d'un joueur

# Jeu
# jeu:[plateau nat List[coup] List[coup] List[nat nat]]
# Structure de jeu comportant :
#           - le plateau de jeu
#           - Le joueur a qui c'est le tour de jouer (1 ou 2)
#           - La liste des coups possibles pour le joueur a qui c'est le tour de jouer
#           - La liste des coups joues jusqu'a present dans le jeu
#           - Une paire de scores correspondant au score du joueur 1 et du score du joueur 2

game=None #Contient le module du jeu specifique: awele ou othello
joueur1=None #Contient le module du joueur 1
joueur2=None #Contient le module du joueur 2
import copy

#Fonctions minimales 

def getCopieJeu(jeu):
    """ jeu->jeu
        Retourne une copie du jeu passe en parametre
        Quand on copie un jeu on en calcule forcement les coups valides avant

    """	
   
    return copy.deepcopy(jeu)

def finJeu(jeu):
    """ jeu -> bool
        Retourne vrai si c'est la fin du jeu
	
    """
    return game.finJeu(jeu)

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
        On suppose que la fonction n'est appelee que si il y a au moins un coup valide possible
        et qu'elle retourne obligatoirement un coup valide
    """
    if(getJoueur(jeu)==1):
        coup=joueur1.saisieCoup(jeu)
    else:
        coup=joueur2.saisieCoup(jeu)
	#Coup VALIDE donc on le return , sinon on reappele la fct
    if(coup in game.getCoupsValides(jeu)):
        return coup
    print("WARNING, Coup invalide, jouez un autre")
    
    return saisieCoup(jeu)

def getCoupsValides(jeu):
    """ jeu  -> List[coup]
        Retourne la liste des coups valides dans le jeu passe en parametre
        Si None, alors on met � jour la liste des coups valides
    """
    jeu[3]=game.getCoupsValides(jeu)
    return jeu[3]
	

def coupValide(jeu,coup):
    """jeu*coup->bool
        Retourne vrai si le coup appartient a la liste de coups valides du jeu
   """
    if coup in getCoupsValides(jeu):
        return True
    return False	
	

def joueCoup(jeu,coup):
    """jeu*coup->void
        Joue un coup a l'aide de la fonction joueCoup defini dans le module game
        Hypothese:le coup est valide
        Met tous les champs de jeu à jour (sauf coups valides qui est fixée à None)
    """
    jeu[2].append(coup)
    game.joueCoup(jeu,coup)
    return 
	
def initialiseJeu():
    """ void -> jeu
        Initialise le jeu (nouveau plateau, liste des coups joues vide, liste des coups valides None, scores a 0 et joueur = 1)
    """
    
    return [game.initPlateau() , 1 , [] , None , game.initScores()]
	
def getGagnant(jeu):
    """jeu->nat
    Retourne le numero du joueur gagnant apres avoir finalise la partie. Retourne 0 si match nul
    """
    if (finJeu(jeu)==True): #verif si fin de partie
        if(jeu[4][0]<jeu[4][1]):
            return 2
        elif(jeu[4][0]>jeu[4][1]):
            return 1
    return 0 # 0 si match nul
						

def affiche(jeu):
    """ jeu->void
        Affiche l'etat du jeu de la maniere suivante :
                 Coup joue = <dernier coup>
                 Scores = <score 1>, <score 2>
                 Plateau :

                         |       0     |     1       |      2     |      ...
                    ------------------------------------------------
                      0  | <Case 0,0>  | <Case 0,1>  | <Case 0,2> |      ...
                    ------------------------------------------------
                      1  | <Case 1,0>  | <Case 1,1>  | <Case 1,2> |      ...
                    ------------------------------------------------
                    ...       ...          ...            ...
                 Joueur <joueur>, a vous de jouer
                    
         Hypothese : le contenu de chaque case ne depasse pas 5 caracteres
    """
    
    print ("Coup joue : ",("aucun" if getCoupsJoues(jeu) == [] else getCoupsJoues(jeu)[ len(getCoupsJoues(jeu)) - 1 ]))
    print("Scores =",getScores(jeu))
    print("Plateau:")
    #affichage plat#
    game.affichage(jeu)
    print("Joueur",getJoueur(jeu),", a vous de jouer")
   


# Fonctions utiles

def getPlateau(jeu):
    """ jeu  -> plateau
        Retourne le plateau du jeu passe en parametre
    """
    return jeu[0]

def getCoupsJoues(jeu):
    """ jeu  -> List[coup]
        Retourne la liste des coups joues dans le jeu passe en parametre
    """
    return jeu[2]


def getScores(jeu):
    """ jeu  -> Pair[nat nat]
        Retourne les scores du jeu passe en parametre
    """
    return jeu[4]


def getJoueur(jeu):
    """ jeu  -> nat
        Retourne le joueur a qui c'est le tour de jouer dans le jeu passe en parametre
    """
    return jeu[1]
###
def getJoueurAdverse(jeu):
    """ jeu  -> int
    Retourne l'adversaire dans le jeu passe en parametre
    """
    return [1,2][(jeu[1])%2]

def changeJoueur(jeu):
    """ jeu  -> void
        Change le joueur a qui c'est le tour de jouer dans le jeu passe en parametre (1 ou 2)
    """
    if(jeu[1]==1):
        jeu[1]=2
    else:
        jeu[1]=1
    return 

def getScore(jeu,joueur):
    """ jeu*nat->int
        Retourne le score du joueur
        Hypothese: le joueur est 1 ou 2
    """
    return jeu[4][joueur-1]

def getCaseVal(jeu, ligne, colonne):
    """ jeu*nat*nat -> nat
        Retourne le contenu de la case ligne,colonne du jeu
        Hypothese: les numeros de ligne et colonne appartiennent bien au plateau  : ligne<=getNbLignes(jeu) and colonne<=getNbColonnes(jeu)
    """
    return jeu[0][ligne][colonne]

    


###SET:
def setCaseVal(jeu,ligne,colonne,val):
    jeu[0][ligne][colonne]=val
    return

def setPlayerScore(jeu,joueur,score):
    jeu[4][joueur-1]=score
    return


def setAtmPlayerScore(jeu,score):
    jeu[4][getJoueur(jeu)-1]=score
    return 



