import time
import game
import awele
import sys
import matplotlib.pyplot as plt
import numpy as np


sys.path.append("..")
game.game=awele
sys.path.append("./Joueurs")
start = time.time()
###############################################
import Triss
import Oracle
import Geralt
import awele_alea
import Keira

listejoueurs=[Oracle,Triss,Keira]
listejoueursnom=["8.2, 4.0, 1.7","0.4,0.5,0.3","10.70, 9.70, 8.70"]
game.joueur1=Oracle
game.joueurinter1 = game.joueur1
game.joueur2=Geralt
game.joueurinter2 = game.joueur2

"""
# =============================================================================
#     tableau avec toutes les parties (pour les stats)
#     Sructure comportant :
#               - le plateau de jeu
#               - Le joueur gagnant
#               - La liste des coups possibles pour le joueur a qui c'est le tour de jouer
#               - La liste des coups joues jusqu'a present dans le jeu
#               - Une paire de scores correspondant au score du joueur 1 et du score du joueur 2
# 
# =============================================================================
"""

def joueN(n) :
    global y
    v1,j1 = 0,1
    
    """
# =============================================================================
#         - v1 (nombre de victoires du joueur 1), v2 (nombre de victoires du joueur 2), mn (nombre de matchs nuls)
#         - sc1 et sc2 (scores moyens de chaque joueur)
#         - nbc (nombre de coups joues en moyenne)
# =============================================================================
    """
    #lancer une partie, 3 coups alea au debut puis chaque joueur se met a jouer
    for i in range(n):
        game.joueur1 = awele_alea
        game.joueur2 = awele_alea
        jeu = game.initialiseJeu()
        while not game.finJeu(jeu) :
            coup = game.saisieCoup(jeu)
            game.joueCoup(jeu,coup)
            if len(game.getCoupsJoues(jeu)) == 4:
                game.joueur1=game.joueurinter1
                game.joueur2=game.joueurinter2
               
        if game.getGagnant(jeu) == j1:
            v1+=1
        
    v1=float(v1)/float(n) #ratio victoire/nbre de match
    y.append(v1) #y=liste de victoire éfféctué (ou on ajoute a la fin de la liste le nombre de victoire pour n partie faite)





game.joueur1.prof=1# les joueurs challenger commence prof 1 et augmente jusqua prof 5
game.joueur2.prof=5# le joeur Etalon commence et reste prof 5 (joueur séléctionné)

n =100

p = 5

x=[i for i in range(1,p+1)]
y=[]# au debut y vide
for j in range(len(listejoueurs)):#permet de faire joueur tous les joueur de ma liste contre mon joueur slectionné
    game.joueur1=listejoueurs[j]
    game.joueurinter1 = game.joueur1
    
    game.joueur2=Geralt #joueur selectionné qui se bat contre tous les autres joueur
    game.joueurinter2 = game.joueur2
    game.joueur1.prof=1
    for i in range(p):#lance n partie, puis incremente la prof de chaque joueur. de 1 jusqua P
        joueN(n) #ajoute une valeur a y qui est le taux de victoire pour n partie
        game.joueurinter1.prof +=1
        print("on augmente la prof de ",game.joueurinter1,"elle est mnt de :",game.joueurinter1.prof)
        
    plt.plot(x,y,'--*',label=listejoueursnom[j]) #lance le tracé de type "--", x= profondeur allant de 1 a 5 en fonction de y qui est le ratio de victoire 
    y=[]
    print("changement de joueur")
    
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=2, mode="expand", borderaxespad=0.) #crée boite legende avec parametre voire doc matplotlib
plt.ylabel('% victoires')
plt.xlabel('profondeur')
plt.xlim(1,p) #absisse
plt.ylim(0,1) #ordonnée
plt.grid(True)
plt.title('pourcentage de victoire en fonction de la prof contre h5 0.5,0.2,0.3') #titre
plt.savefig("Vict-profn2.pdf", format = 'pdf') #sauvegarde
# =============================================================================
# #https://matplotlib.org/api/_as_gen/matplotlib.pyplot.legend.html
# =============================================================================
end = time.time()
print(end - start)