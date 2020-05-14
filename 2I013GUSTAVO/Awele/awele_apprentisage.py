import awele
import sys

sys.path.append("..")
import game
game.game=awele
sys.path.append("./Joueurs")
import awele_alea
import awele_joueur_humain
import awele_alphaBeta
import awele_minMax
import awele_PremierCoupValide
import Ciri
import Geralt
import pedro
import Oracle
import random
global N,j1,j2
j1,j2 = 1,2
epsilon = 0.1#marge pr tatonner
N = 10
#Apprentissage avec un "oracle" a valeurs aléatoires param aléa, il faut bcp d'iterations vu que c'est du aléatoire
"""PB AVEC POIDS QUI CHANGEMENT PAS. dans les j """

#courbe ratio victoire de mon apprenant
game.joueur1 = joueur_ref = Oracle
game.joueur2 = joueur_ap =Geralt

game.joueurinter1 = game.joueur1
game.joueurinter2 = game.joueur2


def Train():
    g1 = JoueN(joueur_ap,joueur_ref) #g1= nombre de victoire de joueur ap
    
    it = 0
    while it <250: #tant que it (compteur) est inferieur au nombre de partie
        j=int(random.random()*joueur_ap.getNbParams())
        s=random.random()
        if(s>0.5):
            joueur_ap.addParam(j, epsilon)
        else :
            joueur_ap.addParam(j,-epsilon)
        g2 = JoueN(joueur_ap,joueur_ref)
        print (joueur_ap.getParams())
        print(g1)
        print(g2)
        if(g2<g1) :
            if(s>0.5) : joueur_ap.addParam(j,-epsilon)
            else : joueur_ap.addParam(j,epsilon)
        else : g1 = g2
        it+=1

def JoueN(joueur1,joueur2): # joue 10 partie (variable N) et compte le nombre de victoire de leleve
    global j1,j2
    victoires=0
    for i in range(N):
        game.joueur1 = awele_alea #permet de tirer des coups aleatoire au debut, sinon tjr meme partie
        game.joueur2 = awele_alea
        jeu = game.initialiseJeu()
        while not game.finJeu(jeu):
            coup = game.saisieCoup(jeu) #joues different coups tant que cest pas la fin du jeu
            game.joueCoup(jeu,coup)
            if len(game.getCoupsJoues(jeu)) == 4: #apres 4 coups aleatoire,le jeu commence vraiment
                game.joueur2=joueur2
                game.joueur1=joueur1
            if i == N/2 :
                game.joueur1=joueur2 #apres 5 partie, on echange les joeuur , pour quon ai pas le meme joueur qui commence
                game.joueur2=joueur1
                j1,j2 = 2,1
        g=game.getGagnant(jeu)
        
        if g == j1: #on compte le nbre de victoire de leleve
            victoires+=1
            print(g)
    j1,j2 = 1,2
    return victoires

Train()
print (joueur_ap.getParams())