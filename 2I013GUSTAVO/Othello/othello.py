#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
import game

def initPlateau():
    plateauOthello=[]
    for i in range(8):
        L=[]
        for k in range(8):
            L.append(0)  # 0 Pour aucun pion
        plateauOthello.append(L)
    plateauOthello[3][4], plateauOthello[4][3], plateauOthello[3][3], plateauOthello[4][4] = 1,1,2,2  
    return plateauOthello


def affichage(jeu): #RANGE 8
    plat=["","","","","","","",""]
    aff1="       "
    aff2="---------------"
    
    for j in range(len(jeu[0][0])):
        aff1=aff1+"|   %d   "%(j)
    aff1=aff1+" |"
    print(aff1)
    for j in range(len(jeu[0][0])):
        aff2+="-------"
    for i in range(len(jeu[0])):
        for j in range(len(jeu[0][i])):
            plat[i]+="|   %d   "%(game.getCaseVal(jeu,i,j))
    print(aff2)
    for j in range(len(jeu[0])):
        print(("   %d   %s |")%(j,plat[j]))
        print(aff2)

"""
def reduce(f,s,b):
     if len(s)==0: return b	
     a=s[-1]
     return reduce(f,s[0:-1],f(a,b))
 
   """ 
def getCoupsValides(jeu):
    coups=Coups(jeu)
    return [x for x in coups if getEncadrements(jeu,x,False)!=[]]
    
def Coups(jeu):
    """adv=jeu[1]%2+1
    s=[entourageVide(jeu,l,c)for l in range(8) for c in range(8) if jeu[0][l][c]==adv]
    s=reduce(lambda a,b : a|b,s,s)
    return 0"""
    adv=jeu[1]%2+1
    s=[]
    for l in range(8):
        for c in range(8):
            for coup in entourageVide(jeu,l,c):
                if coup not in s and game.getCaseVal(jeu,l,c) == adv:
                    s.append(coup)
    return s

    


def entourageVide(jeu,l,c):
    """Return cases vides autour du parametre case"""
    
    
    res=[]
    if (l>0):
        
        if(game.getCaseVal(jeu,l-1,c)==0):
            res.append([l-1,c])
            if(c>0):
                if(game.getCaseVal(jeu,l-1,c-1)==0):
                    res.append([l-1,c-1])
            if(c<7):
                if(game.getCaseVal(jeu,l-1,c+1)==0):
                    res.append([l-1,c+1])
    if (l<7):

        if(game.getCaseVal(jeu,l+1,c)==0):
            res.append([l+1,c])
            
            if(c>0):
                if(game.getCaseVal(jeu,l+1,c-1)==0):
                    res.append([l+1,c-1])
            if(c<7):
                if(game.getCaseVal(jeu,l+1,c+1)==0):
                    res.append([l+1,c+1])
                    
    if (c < 7):
        if (game.getCaseVal(jeu, l, c + 1) == 0):
            res.append([l, c+1])
    
    if (c > 0):
        if (game.getCaseVal(jeu, l, c - 1) == 0):
            res.append([l, c-1])
            
    return res
    



def getEncadrements(jeu,case,all=True):
    """retourne la liste des directions qui peuvent mener
    à un encadrement"""
    ret = []
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if (not((i==0)and(j==0))):
                if (checkEncadrementDirection(jeu,case[0],case[1],i,j)):
                    ret.append([i,j])
                    if not all:
                        return ret
    return ret

def checkEncadrementDirection(jeu,l,c,nL,nC):#encadr
    """Return true si encadrement possible false sinon;"""
    
    i=0
    joueur = game.getJoueur(jeu)
    while True:
        l +=nL
        c +=nC
        if (l>7) or (l<0) or (c>7) or (c<0):
            return False
        
        val = game.getCaseVal(jeu,l,c)
        if (val==joueur):
            if (i==0):
                return False
            else:
                return True
        if (val==0):
            return False
        i+=1
    return False

    

def joueCoup(jeu,coup):
    """
    jeu[0][coup[0]][coup[1]]=jeu[1]
    jeu[4][jeu[1]]+=1 #ajout de points au score
    d=getEncadrements(jeu,coup,True)
    for x in d:
        retournePions(jeu,coup,d)
    jeu[3].append(coup)
    jeu[2]=None
    jeu[1]=jeu[1]%2+1
    global r 
    version:
        
    """
    #retournePions(jeu,coup,d) 
    j = game.getJoueur(jeu)
    adv = game.getJoueurAdverse(jeu)
    score = game.getScores(jeu)
    enca = getEncadrements(jeu,coup,True)
    for d in enca:
        l = coup[0]
        c = coup[1]
        game.setCaseVal(jeu,l,c,j)
        while True:
            l+=d[0]
            c+=d[1]
            if game.getCaseVal(jeu,l,c) == j:
                break
            game.setCaseVal(jeu,l,c,j)
            score[j-1]+=1
            score[adv-1]-=1
            
           
    game.setPlayerScore(jeu,j,score[j-1]+1)
    game.setPlayerScore(jeu,adv,score[adv-1])
    game.changeJoueur(jeu)
    jeu[3] = []
        
        
    """    
def retournePions(jeu,coup,x):
    l=coup[0]
    c=coup[1]
    score=game.getScores(jeu)
    j=game.getJoueur(jeu)
    adv=game.getJoueurAdverse(jeu)
    game.setCaseVal(jeu,l,c)
    while True:
        l=l+x[0]
        c=c+x[1]
       
        if game.getCaseVal(jeu,l,c)==j:
            break
        game.getCaseVal(jeu,l,c,j)
        score[j-1]+=1
        score[adv -1]-=1
 """   

    
    
        
def initScores():
    return [2,2]



def finJeu(jeu):
    if len(game.getCoupsJoues(jeu)) == 64 or game.getCoupsValides(jeu) == []:
        return True
    return False


