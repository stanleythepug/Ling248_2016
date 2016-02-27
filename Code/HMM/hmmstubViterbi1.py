#!/usr/bin/python

'''Feb. 27 2016: modified the function computeBestPathViterbi. It seems to run pretty fast. I inputted "This sentence has quite a few words in it and we will see how long it takes to process it ." which, if I measured the time correctly, took about 0.027 seconds to process, giving as the most probable tag sequence: 0.0 DT NN VBZ RB DT JJ NNS IN NP CC PRP MD VB WRB JJ NP VB TO NN NP RB'''

from collections import defaultdict, Counter
import pdb
from itertools import product
from operator import itemgetter
import time

pi = None
b = None
a = None

def loadPi():
    f = "pi.tab"
    r = Counter()
    
    fd = open(f, "r")
    for l in fd:
        state,num,prob = l.split('\t')
        r[state] = float(prob)
    
    return r
    
def loadA():
    f = "a.tab"
    r = defaultdict(lambda: defaultdict(float))
    
    fd = open(f, "r")
    for l in fd:
        statei, statej,num,prob = l.split('\t')
        r[statei][statej] = float(prob)
    return r


def loadB():
    f = "b.tab"
    r = defaultdict(lambda: defaultdict(float))
    
    fd = open(f, "r")
    for l in fd:
        statei, termk,num,prob = l.split('\t')
        r[statei][termk] = float(prob)
    
    return r

def viterbiLoop(obss, model):
    pass
def viterbi(time, state, obss, model, store):
    
    pass

def computeBestPathViterbi(model):
    pi, a, b = model

    states = a.keys()
    terms = set()
    for d in b.values():
        terms.update(set(d.keys()))

    try:
        while 1:
            inp = raw_input("What is your string?")
            inp = inp.lower()
            print time.clock()
            inputTerms = inp.split(' ')

            uniqTerms = set(inputTerms)
            diff = uniqTerms - terms
            if diff != set(): #there are some illegal terms
                print diff
                print "These aren't legal words for this model."
            else:
                o = inputTerms
                bestStatePath = defaultdict(lambda: [[], 0]) #Keep track of best past states and probability
                newBestStatePath = defaultdict(lambda: [[], 0]) #We need to hold off on updating the best path for each state until we have gone through all states at a given timestep so we hold the new past states in this dictionary until we are ready to update
                for state in states:
                    bestStatePath[state][1] = pi[state]*b[state][o[0]] #initialize bestStatePath with its prob

                for t in inputTerms[1:]: #We already considered the first term when we initialized
                    maxProb = 0.0
                    bestPrevState = None
                    for state2 in states:
                        #find best path to that state
                        #We just need to find the best previous state with its history
                        for state1 in states:
                            prob = bestStatePath[state1][1]*a[state1][state2]
                            if prob > maxProb:
                                maxProb = prob
                                bestPrevState = state1
                        newBestStatePath[state2][0] = list(bestStatePath[bestPrevState][0]) + [bestPrevState]
                        #It's necessary to use the "list" function here to update the variable. Otherwise we can get strange results.
                        #The updated best state path is the path to the best previous state plus the current state
                        newBestStatePath[state2][1] = maxProb*b[state2][t]
                        #Multiply by the emission probability for the current term
                    for state in states:
                        bestStatePath[state][0] = list(newBestStatePath[state][0])
                        bestStatePath[state][1] = newBestStatePath[state][1]
                maxProb = 0.0
                bestSeq = None
                for state in states:
                    if bestStatePath[state][1] > maxProb:
                        maxProb = prob
                        bestSeq = state
                print maxProb, ' '.join(bestStatePath[bestSeq][0]), bestSeq
                print time.clock()
                #We need to append to the print function the last state: i.e. the variable bestSeq since the bestStatePath for a given state doesn't include the state itself, just its best past sates.


#                for sSeq in product(states, repeat=length):
#
#
#
#                    stateHistory = sSeq[:-1]
#                    obsHistory = o[:-1]
#                    histProb = lookup(stateHistory, obsHistory)
#                    
#                    thisObsProd = b[sSeq[-1]][o[-1]]
#                    thisTransProb = a[sSeq[-2]][sSeq[-1]]
#
#                    total = histProb * thisObsProd * thisTransProb
#
#                    if total > maxProb:
#                        maxProb = total
#                        bestSeq = sSeq
#
#                print maxProb, ' '.join(bestSeq)
    except EOFError:
        return


def computeBestPath(model):
    pi, a, b = model
    
    states = a.keys()
    terms = set()
    for d in b.values():
        terms.update(set(d.keys()))
    
    try:
        while 1:
            inp = raw_input("What is your string?")
            inp = inp.lower()
            inputTerms = inp.split(' ')

            uniqTerms = set(inputTerms)
            diff = uniqTerms - terms
            if diff != set(): #there are some illegal terms
                print diff
                print "These aren't legal words for this model."
            else:
                o = inputTerms
                length = len(o)
                totalProb = 0.0
                #sSeq = [states[0]] * length
                
                maxProb = 0.0
                bestSeq = None
                for sSeq in product(states, repeat=length):

                    print sSeq
                    start = sSeq[0]
                    startProb = pi[start]
                
                    transProd = 1.0
                
                    for i in range(0,len(sSeq)-1): 
                        transProd *= a[sSeq[i]][sSeq[i+1]]
                
                    obsProd = 1.0
                    for i in range(0,len(sSeq)):
                        obsProd *= b[sSeq[i]][o[i]]
                    
                    total = startProb * transProd * obsProd
                    
                    if total > maxProb:
                        maxProb = total
                        bestSeq = sSeq
                        
                print maxProb, ' '.join(bestSeq)
    except EOFError:
        return

    
def alpha(time, state, obss, model, store):
    pass

def computeObsProbAlpha(model):
    pi, a, b = model
    
    states = a.keys()
    terms = set()
    for d in b.values():
        terms.update(set(d.keys()))
    
    try:
        while 1:
            inp = raw_input("What is your string?")
            inp = inp.lower()
            inputTerms = inp.split(' ')

            uniqTerms = set(inputTerms)
            diff = uniqTerms - terms
            if diff != set(): #there are some illegal terms
                print diff
                print "These aren't legal words for this model."
            else:
                o = inputTerms
                length = len(o)
                totalProb = 0.0
                store = {}
                for s in states:
                    v = alpha(length-1, s, o, model, store)
                    #print s, v
                    totalProb += v
                print totalProb
                for key,val in sorted([x for x in store.items() if x[1] != 0], key=itemgetter(0)):
                    print key, val
    except EOFError:
        return


def computeObsProb(model):
    pi, a, b = model
    
    states = a.keys()
    terms = set()
    for d in b.values():
        terms.update(set(d.keys()))
    
    try:
        while 1:
            inp = raw_input("What is your string?")
            inp = inp.lower()
            inputTerms = inp.split(' ')

            uniqTerms = set(inputTerms)
            diff = uniqTerms - terms
            if diff != set(): #there are some illegal terms
                print diff
                print "These aren't legal words for this model."
            else:
                o = inputTerms
                length = len(o)
                totalProb = 0.0
                for x in product(states, repeat =length ):
                    piVal = pi[x[0]]
                    outputProb = b[x[0]][o[0]]
                    transProb = 1
                    
                    if length > 1: #handle the first transition and the last output
                        transProb *= a[x[0]][x[1]]
                        #outputProb *= b[x[-1]][o[-1]]                        
                    
                    for i in range(1,length):
                        try:
                            transProb *= a[x[i]][x[i+1]]
                        except IndexError:
                            pass
                        outputProb *= b[x[i]][o[i]]
                    
                    xTotal = piVal * transProb * outputProb
                    totalProb += xTotal
                    print x, piVal, transProb, outputProb, xTotal
                print totalProb
    except EOFError:
        return

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Take a sentences of form word_pos and compute pos->pos transition probabilities and pos->term output probabilities')
                       
    args = parser.parse_args()
    

    pi = loadPi()
    a = loadA()
    b = loadB()
    
    model = (pi, a, b)
    
    #computeObsProbAlpha(model)
    computeBestPathViterbi(model)
