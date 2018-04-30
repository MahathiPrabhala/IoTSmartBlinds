# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 06:42:25 2018

@author: newguest
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 11:23:34 2018

@author: newguest
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 17:13:11 2017

@author: newguest
"""
import sys
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
from decimal import Decimal
import random

def CountTokensOfTerm(textc,t):
    return textc.count(t)
def TrainMultinomialNB(C,D):
    V ={}
    Nc = [0,0]
    N = len(D)    
    prior = [0,0]
    textc = ['','']    
    for line in D:
        words_in_doc = line.split(',')
        
        word_doc = ''
        for word in words_in_doc:
            word = word.replace("\'","")  
            word = word.replace("\n","")     
            word_doc+= word + " "
            if(word == C[0]):               
                Nc[0]+=1 
                textc[0] += word_doc
            if(word == C[1]):
                Nc[1]+=1 
                textc[1]+=word_doc
            if word not in V:
                V.update({word: 0})
    Vocab = set(V)
    iClassIndex = 0
    condprob = {}
    print(Nc[0],Nc[1])
    print(N)
    for c in C:
            Tct = 0
            prior[iClassIndex] = float(Nc[iClassIndex])/(N)
            print( prior[iClassIndex])
            for t in Vocab:
                textc[iClassIndex].replace("'","")
                Tct = CountTokensOfTerm(textc[iClassIndex],t)
                Totalterms = CountTokensOfTerm(textc[iClassIndex]," ")+1
                
                if t not in condprob:
                    condprob.update({t: [0,0]})
                condprob[t][iClassIndex] = float(Tct+1)/((len(Vocab))+ (Totalterms - Tct))
               
            iClassIndex+=1
    return V,prior,condprob 
def extractTokensFromDoc(V,d):
    Tokens = []
    words_in_doc = d.split(',')
    
    for word in words_in_doc:
        word = word.replace("\'","")
        if word in V:
            Tokens.append(word)
    print('Tokens'+str(len(Tokens)))
    return Tokens
def ApplyMultinomialNB(C,V,prior,condprob,d):
    W = extractTokensFromDoc(V,d)
    
    #print(condprob)
    iClassIndex = 0
    score = [None]*2
    while iClassIndex < 2: 
        if prior[iClassIndex] > 0:
            score[iClassIndex] = math.log(prior[iClassIndex])
        else:
            score[iClassIndex] = math.log(sys.float_info.min)
       
        for t in W:            
           if condprob[t][iClassIndex] > 0:              
               score[iClassIndex]= score[iClassIndex] + math.log(condprob[t][iClassIndex])
        iClassIndex+=1     
    #print(score)
    if score[0] > score[1]:
        return 'open'
    else:
        return 'close'
      
    
    
def getPredictedData(dateNow,timeNow,timeCategory):
    lines = []
    if(timeCategory == 'AM'):
        lines = list(open("Final Project Data AM.csv"))
    else:
        lines = list(open("Final Project Data PM.csv"))
    C = ["open","close"]
    V,prior,condprob = TrainMultinomialNB(C,lines[:200])   
    choiceV = ['close','open'] 
    d = dateNow +','+timeNow+random.choice(choiceV)+timeCategory
    #words_in_doc = d.split(',')
    obtained_class = ApplyMultinomialNB(C,V,prior,condprob,d)
    return obtained_class
       
   
    


       
    