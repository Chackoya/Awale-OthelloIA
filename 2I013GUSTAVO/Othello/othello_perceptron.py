# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import othello
import sys
sys.path.append("..")
import game
game.game=othello
sys.path.append("./Joueurs")
import othello_alea
import othello_joueur_humain
import othello_PremierCoupValide
import othello_minMax
import othello_alphaBeta
import othello_alphaBeta2p
import minz
import Vesemir
import Yennefer
import Eredin
import Dandelion


global N,j1,j2
j1 =1
j2 = 2
eps = 1
N = 10
game.joueur1 = Eredin
game.joueur2 = Vesemir
maitre = Vesemir
eleve = game.joueur1
adversaire = game.joueur2


scores=[]
sc=[]

a=0.1
while True:
	jeu = game.initialiseJeu()
	game.joueur1 = othello_alea
	game.joueur2 = othello_alea
	if len(game.getCoupsJoues(jeu)) == 4:
		game.joueur1 = eleve
		game.joueur2 = adversaire
	while not game.finJeu(jeu):
		if game.getJoueur(jeu)==2:
			cp=game.getCoupsValides(jeu)
			ls=[Vesemir.estimation(game.getCopieJeu(jeu),x,-1000000,1000000,1) for x in cp]  #liste des estimations de l oracle pour chacun des coups possibles
			opt=cp[ls.index(max(ls))]  #opt= liste coup valide[index de ls ayant estimation max] coup qui serait joue par l oracle
			sopt=game.getCopieJeu(jeu) #sopt correspond a l etat du jeu si le coup choisi par l oracle est joue
			game.joueCoup(sopt,opt)
			m=max(ls) #estimation du coup que jouerait l oracle
			ls=[x for x in cp if ls[cp.index(x)]<m]#liste des estimations de l oracle pour chacun des coups possibles excepté le coup qu'il aurait joue (coup d estimation maximale)
			for c in ls:
				copie = game.getCopieJeu(jeu)
				cp=game.joueCoup(game.getCopieJeu(jeu),c)
				o=eleve.evaluation(sopt,Yennefer.parcoursPlateau(sopt))#evaluation du plateau de jeu sopt (plateau meilleur coup joue) selon la fonction d evaluation de l eleve
				s=eleve.evaluation(copie,Yennefer.parcoursPlateau(copie))#evaluation du plateau de jeu sc (pateau coup quelconque joue) selon la fonction d evaluation de l eleve
				if (o-s)<1:#si l evaluation de sopt est plus basse que celle de sc, on modifie les parametres de la fonction d evaluation de l eleve
					for j in range(0,eleve.getNbParams()):#on explore l ensemble des parametres
						scjc=getattr(eleve,"f"+str(j+1))(copie,eleve.parcoursPlateau(copie))# ex scjc1 = f1(...) = evaluation f1 du plateau sc
						scjo=getattr(eleve,"f"+str(j+1))(sopt,eleve.parcoursPlateau(sopt))# ex scjo1 = f1(...) = evaluation f1 du plateau sopt
						eleve.addParam(j,-a*(scjc-scjo)) #on modifie la valeur de chaque parametre
		c=game.saisieCoup(jeu)
		game.joueCoup(jeu,c)
	a-=0.0025
	if a < 0:
		break
	print (a)
	print (eleve.getParams())
	print (game.getScores(jeu))
sc.append(game.getScores(jeu)[0]-game.getScores(jeu)[1])




x=len(sc)#x=longueur de l'evaluation du plateau de jeu sc
xu=np.arange(0,x,1)
#xu=(start=0,end=x=longueur de mon tableau, step=pas de 1),Renvoie des valeurs espacées uniformément dans un intervalle donné.
plt.plot(xu,sc)
plt.xlabel('it')
plt.ylabel('sc diff')
plt.title('graphe de la fontion')
plt.savefig("interddf.pdf", format = 'pdf')