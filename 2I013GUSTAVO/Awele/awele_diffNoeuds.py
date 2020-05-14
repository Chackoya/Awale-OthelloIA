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
import awele_alphaBeta
import awele_minMax
game.joueur1 = awele_alphaBeta
game.joueur2 = awele_minMax
game.joueurinter1 = game.joueur1
game.joueurinter2 = game.joueur2
s1 = "joueur IA"
s2 = "autre joueur"

tabParties = []
n =5
winsPlayer1=0
winsPlayer2=0
j1=1
j2=2
scoreMoyen1=0
scoreMoyen2=0
matchNul=0
nbc=0
tabNoeudsJ1 = []
tabNoeudsJ2 = []
profondeur = []

#winsPlayer1:nombre de victoires du joueur 1
#winsPlayer2:nombre de victoires du joueur 2
#matchNul (nombre de matchs nuls)
#scoreMoyen1 et scoreMoyen2 (scores moyens de chaque joueur)
#nbc (nombre de coups joues en moyenne)

for i in range(1,n+1):
    game.joueur1 = awele_alea
    game.joueur2 = awele_alea
    jeu = game.initialiseJeu()
    while not game.finJeu(jeu) :
        #game.affiche(jeu)
        coup = game.saisieCoup(jeu)
        game.joueCoup(jeu,coup)
        
        

        """# print(game.joueur1)
        # print(game.joueur2)
        # print("Nombre de tours : " + str(len(game.getCoupsJoues(jeu))))"""
    
        
        if len(game.getCoupsJoues(jeu)) == 4:#fin coup aleatoire
            game.joueur1=game.joueurinter1
            game.joueur2=game.joueurinter2
    if game.getGagnant(jeu) == j1:
        winsPlayer1+=1
    elif game.getGagnant(jeu) == j2:
        winsPlayer2+=1
    else:
        matchNul+=1
    scoreMoyen1 += game.getScore(jeu,j1)#additionne les scores de j1 puis va diviser par n ensuite
    scoreMoyen2 += game.getScore(jeu,j2)
    nbc += len(game.getCoupsJoues(jeu))
    jeuCopie = game.getCopieJeu(jeu)
    jeuCopie[1] = game.getGagnant(jeu)
    tabParties.append(jeuCopie)
    #game.affiche(jeu)
    tabNoeudsJ1.append(awele_alphaBeta.nombreDeNoeuds)
    tabNoeudsJ2.append(awele_minMax.nombreDeNoeuds)
    profondeur.append(awele_alphaBeta.prof)
    print ("1:",tabNoeudsJ1)#affichage tab des noeuds qu'on utilisera pr les graph
    print("2:",tabNoeudsJ2)
    game.joueur1.prof += 1
    game.joueur2.prof += 1
    if i == n/2 :#changement de coté pour joueur
        game.joueurinter1=game.joueur2
        game.joueurinter2=game.joueur1
        j1=2
        j2 =1
    game.joueurinter1.nbNoeuds = 0
    game.joueurinter2.nbNoeuds = 0



print("*********")
print("Stats des matchs:")
print("    *"+s1+":*")
print("    Winrate:"+str((float(winsPlayer1)/n)*100)+"% des match")
print("    Son score moyen est:"+str((float(scoreMoyen1)/n)))
print("\n")

print("    *"+s1+":*")
print("    Son score moyen est:"+str((float(scoreMoyen2)/n)))
print("\n")
print("    "+str((float(matchNul)/n)*100)+"% match nuls")
print("*********\n")
x = np.array(profondeur)
y1 = np.array(tabNoeudsJ1)
y2 = np.array(tabNoeudsJ2)
plt.plot(x, y1)
plt.plot(x, y2)
plt.title('Difference de noeuds parcourus entre minmax et ab')
plt.savefig("diffNoeuds_MinMax_ABdepart1.pdf", format = 'pdf')
plt.show()