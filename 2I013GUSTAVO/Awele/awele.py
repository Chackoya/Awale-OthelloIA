#!/usr/bin/env python
# -*- coding: utf-8 -*-

#LE PLATEAU
import sys
sys.path.append("..")
import game

def initPlateau():
    """initialisation du plateau awele"""
    plateauAwele=[]
    for i in range(2):
        L=[]
        for k in range(6):
            L.append(4)
        plateauAwele.append(L)
    return plateauAwele




def affichage(jeu):
    """ plateau """    
    aff1 = "       |"
    for i in range(6):
        aff1 += "   "+str(i)+"   |"
    print (aff1)
    aff2 = ""
    for i in range((len(aff1))):
        aff2+= "-"
    print (aff2)
    for i in range(2):   #len(jeu[0])
        affiche="   "+str(i)+"   |"
        for k in range(6): #len(jeu[0][0])
            affiche+="   "+str(game.getCaseVal(jeu,i,k))+"   |"
        print (affiche)
        print (aff2)
    return
####################################
def initScores():
	return [0,0]
#############################################
#########################
        
def getCoupsValides(jeu):
    
    #ret=[(j-1,i) for i in range(6) if (game.getCaseVal(jeu,j-1,i)>0) and (not advAffame(jeu)) or nourrit(jeu,(j-1,i))]
    #return ret
    #TRANSFORMATION EN AUTRE VERSION EN PLUSIEURES LIGNES :
    
    j = game.getJoueur(jeu)
    lc=[]
    #print("k")
    #print(j)
    
    
    for i in range(6):
        if game.getCaseVal(jeu,j-1,i)>0:
            lc.append([j-1,i])
    #print("ok")
    if not advAffame(jeu):
        return lc
    
    ret=[]
    for c in lc:
        if nourrit(jeu,c):
            ret.append(c)
    return ret
    
    
    

  

#################

def nourrit(jeu, coup):
    """Retourne true si le coup peut nourrir l'adv, faux sinon"""
    j=game.getJoueur(jeu)
    if(j==1):
        return coup[1]<game.getCaseVal(jeu,coup[0],coup[1])
    
    return game.getCaseVal(jeu,coup[0],coup[1])>(5 - coup[1])

################


def advAffame(jeu):
    """verifie si adv est affamé(true) , false sinon"""
    #j=game.getJoueur(jeu)
    #adv=j%2+1
    #return (sum(jeu[0][adv])==0)
    if jeu[0][game.getJoueurAdverse(jeu)-1]==[0 for i in range (6)]:
        return True
    return False

def nextCase(jeu,case):
    """retourne case en sens antihoraire"""
    if case == [0,0]:
        return [1,0]
    elif case == [1,5]:
        return [0,5]
    elif case[0] == 0:
        return [0,case[1] - 1]
    return [1,case[1] + 1]
  
def nextCaseHoraire(jeu,case):
    """retourne case en sens horaire"""
    if case == [1,0]:
        return [0,0]
    elif case == [0,5]:
        return [1,5]
    elif case[0] == 0:
        return [0,case[1] + 1]
    return [1,case[1] - 1]
       
def distribue(jeu,coup,v):
    """On effectue une distribution en antihoraire des graines a compter de la case sivante du coup en param 
    jeu*coup-> case"""
    
    
    case=coup
    #v= game.getCaseVal(jeu,coup[0],coup[1])
    while v>0:
        case=nextCase(jeu,case)
        if case == coup:                        #si on a fait un tour complet ie si on a distribue k*12 graines avce k>1
            case = nextCase(jeu,case)          #alors on saute la case de depart
        jeu[0][case[0]][case[1]]+=1
        v-=1
    return case

def recolte(jeu,case):
    """jeu*ligne*colonne( case) -> nombre de Graines mangées
    Return nombre de graines mangées et les enleve du jeu"""
    
    res=game.getCaseVal(jeu,case[0],case[1])
    
    game.setCaseVal(jeu,case[0],case[1],0)
    
    
    return res
 
    

    
def joueCoup(jeu,coup):
    
    
    save = game.getCopieJeu(jeu) #on simule d'abord le coup pour vérifier que celui-ci ne va pas affamer l'adversaire
    v= game.getCaseVal(save,coup[0],coup[1])
    game.setCaseVal(save,coup[0],coup[1],0)
    case = distribue(save,coup,v) #la fonction distribue renvoie la derniere case ou une graine a ete depose
    score =game.getScore(save , game.getJoueur(save))
    while case[0]==game.getJoueurAdverse(save)-1 and (save[0][case[0]][case[1]]==2 or save[0][case[0]][case[1]]==3):
        score= score+recolte(save,case)
        case=nextCase(save , case)
    if advAffame(save):
        distribue(jeu,coup,v)
    else:
        game.setCaseVal(jeu,coup[0],coup[1],0)
        case = distribue(jeu,coup,v)
        score =game.getScore(jeu,game.getJoueur(jeu))
        while case[0]==game.getJoueurAdverse(jeu)-1 and (jeu[0][case[0]][case[1]]==2 or jeu[0][case[0]][case[1]]==3):
            score= score + recolte(jeu,case)
            case=nextCase(jeu,case)
    game.setAtmPlayerScore(jeu,score)
    game.changeJoueur(jeu)
    return
    
    
def finJeu(jeu):
    if (jeu[0]==[[0 for i in range(6) ] for j in range(2) ]) or getCoupsValides(jeu)==[] or len(game.getCoupsJoues(jeu)) == 100:
        return True
    
    return False

    
    
    
    
    
    
    
    
    
    
    
    
    
    