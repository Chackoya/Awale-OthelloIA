import awele
import sys
import matplotlib.pyplot as plt
import numpy as np
sys.path.append("..")
import game
game.game=awele
sys.path.append("./Joueurs")
import Triss
import Oracle
import Geralt
import awele_alea
import Keira
import Ciri

game.joueur1 = Ciri
game.joueur2 = Keira
maitre = Oracle
eleve = game.joueur1
adversaire = game.joueur2

sc=[]
a=0.1
while True:
    jeu = game.initialiseJeu()
    game.joueur1 = awele_alea
    game.joueur2 = awele_alea
    while not game.finJeu(jeu):
        if len(game.getCoupsJoues(jeu)) == 4:
            game.joueur1 = eleve
            game.joueur2 = adversaire
        # elif game.getJoueur(jeu)==1 and len(game.getCoupsJoues(jeu)) > 4:
        if game.getJoueur(jeu)==1:
            cp=game.getCoupsValides(jeu)
            ls=[maitre.estimation(game.getCopieJeu(jeu),x,-1000000,1000000,1) for x in cp]  #liste des estimations de l oracle pour chacun des coups possibles
            opt=cp[ls.index(max(ls))]#coup qui serait joue par l oracle
            sopt=game.getCopieJeu(jeu)#sopt correspond a l etat du jeu si le coup choisi par l oracle est joue
            game.joueCoup(sopt,opt)
            m=max(ls)
            ls=[x for x in cp if ls[cp.index(x)]<m]
            for c in ls:
                copie = game.getCopieJeu(jeu)
                cp=game.joueCoup(game.getCopieJeu(jeu),c)
                game.joueCoup(game.getCopieJeu(jeu),c)
                o=eleve.evaluation(sopt)#evaluation du plateau de jeu sopt (plateau meilleur coup joue) selon la fonction d evaluation de l 
                
                s=eleve.evaluation(copie)#evaluation du plateau de jeu sc (pateau coup quelconque joue) selon la fonction d evaluation de l eleve
                if (o-s)<1:#oracle qui a bien joué 
                    for j in range(0,eleve.getNbParams()):
                        # scjc=eleve.evalj(copie)
                        # scjo=eleve.evalj(sopt)
                        scjc=getattr(eleve,"a"+str(j+1))(copie)# ex scjc1 = f1(...) = evaluation f1 du plateau sc
                        scjo=getattr(eleve,"a"+str(j+1))(sopt)# ex scjo1 = f1(...) = evaluation f1 du plateau sopt
                        eleve.addParam(j,-a*(scjc-scjo))#on modifie la valeur de chaque parametre
        c=game.saisieCoup(jeu)
        game.joueCoup(jeu,c)
    a-=0.0025
    if a < 0:
        break
    print (a)
    print (eleve.getParams())
    print (game.getScores(jeu))
    sc.append(game.getScores(jeu)[0]-game.getScores(jeu)[1])
x=len(sc)
xu=np.arange(0,x,1)
plt.plot(xu,sc)
plt.xlabel('it')
plt.ylabel('sc diff')
plt.title('graphe de la fontion')
plt.savefig("inter.pdf", format = 'pdf')
