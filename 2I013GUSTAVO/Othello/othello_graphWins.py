import numpy as np
import matplotlib.pyplot as plt
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

s1 = "Mon Joueur"
s2 = "autre joueur"
tableauParties = []
n = 25

winsPlayer1=0
winsPlayer2=0
j1=1
j2=2
scoreMoyen1=0
scoreMoyen2=0
matchNul=0
nbc=0
#winsPlayer1:nombre de victoires du joueur 1
#winsPlayer2:nombre de victoires du joueur 2
#matchNul (nombre de matchs nuls)
#scoreMoyen1 et scoreMoyen2 (scores moyens de chaque joueur)
#nbc (nombre de coups joues en moyenne)
victoiresj1 = []
victoiresj2 = []
profondeur = []

winsPlayer1,winsPlayer2,j1,j2,scoreMoyen1,scoreMoyen2,nbc,matchNul = 0,0,1,2,0,0,0,0
for k in range(3): #assigne nos joueur 
    game.joueur1 = Vesemir
    game.joueur2 = othello_PremierCoupValide
    game.joueurinter1 = game.joueur1 #assigne joueur intermediaire
    game.joueurinter2 = game.joueur2
    winsPlayer1,winsPlayer2,j1,j2,scoreMoyen1,scoreMoyen2,nbc,matchNul = 0,0,1,2,0,0,0,0
    for i in range(1,n+1): 
        game.joueur1 = othello_alea #coup aleatoire
        game.joueur2 = othello_alea
        jeu = game.initialiseJeu() #demarre jeu
        while not game.finJeu(jeu) :
            coup = game.saisieCoup(jeu)
            game.joueCoup(jeu,coup)
            if len(game.getCoupsJoues(jeu)) == 4: #fin coup aleatoire
                game.joueur1=game.joueurinter1
                game.joueur2=game.joueurinter2
        if game.getGagnant(jeu) == j1: #compte vicoire j1
            winsPlayer1+=1
        elif game.getGagnant(jeu) == j2: #compte vicoire j2
            winsPlayer2+=1
        else: #♀compte match nul
            matchNul+=1
        scoreMoyen1 += game.getScore(jeu,j1) #additionne les scores de j1 puis va diviser par n ensuite
        scoreMoyen2 += game.getScore(jeu,j2)#additionne les scores de j1 puis va diviser par n ensuite
        nbc += len(game.getCoupsJoues(jeu)) 
        jeuCopie = game.getCopieJeu(jeu)
        jeuCopie[1] = game.getGagnant(jeu) 
        tableauParties.append(jeuCopie) #tableaupartie: copie du jeu et gagnat du jeu
        #AFFICHAGE TABLEAU
        #game.affiche(jeu)
        #
        if i == n/2 : #changement de coté pour joueur
            game.joueurinter1=game.joueur2
            game.joueurinter2=game.joueur1
            j1,j2 = 2,1
        
    print("*********")
    print("Stats des matchs:")
    print("    *"+s1+":*")
    print("    Winrate:"+str((float(winsPlayer1)/n)*100)+"% des match")
    print("    Son score moyen est:"+str((float(scoreMoyen1)/n)))
    print("\n")
    
    print("    *"+s1+":*")
    print("    Winrate:"+str((float(winsPlayer2)/n)*100)+"% des match")
    print("    Son score moyen est:"+str((float(scoreMoyen2)/n)))
    print("\n")
    
    print("    "+str((float(matchNul)/n)*100)+"% match nuls")
    print("*********\n")
    victoiresj1.append((float(winsPlayer1)/n)*100)
    victoiresj2.append((float(winsPlayer2)/n)*100)
    profondeur.append(Vesemir.prof)
    print("Profondeuf:", Vesemir.prof)
    Vesemir.prof += 1

"""
from scipy.interpolate import spline
x = np.linspace(0,3,10)
y = spline(profondeur,victoiresj1,x)
plt.plot(x, y)
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=2, mode="expand", borderaxespad=0.)
plt.ylabel('Pourcentage de victoires')
plt.xlabel('Profondeur')
plt.xlim(1,3)
plt.ylim(0,110)
plt.grid(True)
plt.title('Pourcentage de victoires en fonction de la profondeur sur 100 parties')
plt.savefig("VictoiresProfAB4.pdf", format = 'pdf')
plt.show()
"""