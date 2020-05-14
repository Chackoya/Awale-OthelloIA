import othello
import sys
sys.path.append("..")
import game
game.game=othello
sys.path.append("./Joueurs")
import random
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
eps = 5
N = 10

game.joueur1 =Yennefer
joueur_ref = game.joueur1
game.joueur2 = othello_alphaBeta 
joueur_ap= game.joueur2



def Train():
    
    g1 = JoueN(joueur_ap,joueur_ref) #g1= nombre de victoire de joueur ap
    it = 0
    while it <25: #tant que it (compteur) est inferieur au nombre de partie
         
         j=int(random.random()*joueur_ap.getNbParams())
         s=random.random()
         if(s>0.5):
          print (joueur_ap.getParams())
          joueur_ap.addParam(j, eps)
         else :
             joueur_ap.addParam(j,-eps)
             print (joueur_ap.getParams())
         g2 = JoueN(joueur_ap,joueur_ref)
         
        
         if(g2<g1) :
             if(s>0.5) : 
                 joueur_ap.addParam(j,-eps)
                 print (joueur_ap.getParams())
             else : 
                 joueur_ap.addParam(j,eps)
                 print (joueur_ap.getParams())
         else : g1 = g2
         it+=1


def JoueN(joueur1,joueur2): # joue 10 partie (variable N) et compte le nombre de victoire de joueur 1 (l'eleve)
    global j1,j2
    victoires=0
        
    for i in range(N):
        game.joueur1 = othello_alea #transforme mes joueur en joueur aleatoire
        game.joueur2 = othello_alea #permet de tirer des coups aleatoire au debut, sinon tjr meme partie
        jeu = game.initialiseJeu()
        while not game.finJeu(jeu):
            coup = game.saisieCoup(jeu) #joues different coups tant que cest pas la fin du jeu
            game.joueCoup(jeu,coup)
            if len(game.getCoupsJoues(jeu)) == 4: #apres 4 coups aleatoire,le jeu commence vraiment
                  game.joueur2=joueur2
                  game.joueur1=joueur1
            g=game.getGagnant(jeu)
        if g == j1: #on compte le nbre de victoire de leleve
            victoires+=1
        if i == N/2:
            game.joueur1=joueur2 #apres N/2 partie, on echange les joeuur , pour quon ai pas le meme joueur qui commence
            game.joueur2=joueur1
            j1=game.joueur2

        
    j1=game.joueur1
        
    return victoires

Train()
print (joueur_ap.getParams())