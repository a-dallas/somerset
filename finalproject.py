import sys
import pandas as pd
import copy
import time
import math
import random

random.seed(0) # want to be able to duplicate results

debugPrinting = False
def debugprint(string):
    if debugPrinting:
        print(string)


class Game:
    def __init__(self):
        self.round = 1
        self.currPlayer = 1
        self.cardsInTrick = 0
        self.firstPlayedCard = None
        self.winningCard = None
        self.trumpSuit = None
        self.team1Score = 0
        self.team2Score = 0
        self.deck = {}
        self.deck[(0,0)] = 0 #0 means it has not been seen yet
        self.deck[(-1,-1)] = 0
        self.deck[(0,2)] = 0
        self.deck[(1,2)] = 0
        self.deck[(2,2)] = 0
        self.deck[(0,4)] = 0
        self.deck[(1,4)] = 0
        self.deck[(2,4)] = 0
        self.deck[(3,4)] = 0
        self.deck[(4,4)] = 0
        self.deck[(0,6)] = 0
        self.deck[(1,6)] = 0
        self.deck[(2,6)] = 0
        self.deck[(3,6)] = 0
        self.deck[(4,6)] = 0
        self.deck[(5,6)] = 0
        self.deck[(6,6)] = 0
        self.deck[(0,8)] = 0
        self.deck[(1,8)] = 0
        self.deck[(2,8)] = 0
        self.deck[(3,8)] = 0
        self.deck[(4,8)] = 0
        self.deck[(5,8)] = 0
        self.deck[(6,8)] = 0
        self.deck[(7,8)] = 0
        self.deck[(8,8)] = 0
        self.deck[(0,10)] = 0
        self.deck[(1,10)] = 0
        self.deck[(2,10)] = 0
        self.deck[(3,10)] = 0
        self.deck[(4,10)] = 0
        self.deck[(5,10)] = 0
        self.deck[(6,10)] = 0
        self.deck[(7,10)] = 0
        self.deck[(8,10)] = 0
        self.deck[(9,10)] = 0
        self.deck[(10,10)] = 0
        self.deck[(0,12)] = 0
        self.deck[(1,12)] = 0
        self.deck[(2,12)] = 0
        self.deck[(3,12)] = 0
        self.deck[(4,12)] = 0
        self.deck[(5,12)] = 0
        self.deck[(6,12)] = 0
        self.deck[(7,12)] = 0
        self.deck[(8,12)] = 0
        self.deck[(9,12)] = 0
        self.deck[(10,12)] = 0
        self.deck[(11,12)] = 0
        self.deck[(12,12)] = 0
        
    def dealDeck(self):
        cardList = list(self.deck.keys())
        
        cardSample = random.sample(cardList, 12)
        for card in cardSample:
            self.deck[card] = 1 #means it is in player 1s hand
            cardList.remove(card)
        
        cardSample = random.sample(cardList, 12)
        for card in cardSample:
            self.deck[card] = 2 #means it is in player 2s hand
            cardList.remove(card)
            
        cardSample = random.sample(cardList, 12)
        for card in cardSample:
            self.deck[card] = 3 #means it is in player 3s hand
            cardList.remove(card)
            
        cardSample = random.sample(cardList, 12)
        for card in cardSample:
            self.deck[card] = 4 #means it is in player 4s hand
            cardList.remove(card)
    
          
    def setTrump(self,trumpSuit):
        self.trumpSuit = trumpSuit
        trumpLoc = self.deck[(-1,-1)]
        del self.deck[(-1,-1)]
        self.deck[(-1,trumpSuit)] = trumpLoc
        self.winningCard = (-2,trumpSuit) #this is necessary to force playing a trump card on the first round
        self.firstPlayedCard = (-2,trumpSuit) #this is necessary to force playing a trump card on the first round

    def printHand(self,playerNum):
        listOfPlayerCards = []
        for c in self.deck:
            c1, c2 = c
            if self.deck[c] == playerNum:
                listOfPlayerCards.append(c)
        print(listOfPlayerCards)

    def getActions(self,playerNum):
        
        #play highest card that can, play lowest card that can, play biggest points card (default to lowest card)
        #round, place in round or am i last, are we winning, do we have card that can beat winning card
        
        #check first played
        #play highest (or highest if you are first play) (1), play points (2), play lowest (3), play 0/0(8)
        actions = []
        correspondingCards = []
        listOfPlayerCards = []
        # print(self.deck)
        for c in self.deck:
            c1, c2 = c
            if self.deck[c] == playerNum:
                listOfPlayerCards.append(c)
                    

        if not self.firstPlayedCard == None:
            f1, f2 = self.firstPlayedCard
            numberCards = len(listOfPlayerCards)
            numberFirstPlayed = 0
            for c in listOfPlayerCards:
                c1, c2 = c
                if c2 == f2:
                    numberFirstPlayed += 1
                    
            if numberFirstPlayed > 0:
                maxFirst = None
                minFirst = None
                pointsCard = False
                for c in listOfPlayerCards:
                    c1, c2 = c
                    if c2 == f2:
                        
                        if maxFirst == None:
                            maxFirst = c1
                        elif c1 > maxFirst:
                            maxFirst = c1
                            
                        if minFirst == None:
                            minFirst = c1
                        elif c1 < minFirst:
                            minFirst = c1
                        
                        if c1*2 == c2:
                            pointsCard = True

                actions.append(1)
                correspondingCards.append((maxFirst, f2))
                
                if pointsCard == True:
                    actions.append(2)
                    correspondingCards.append((int(f2/2), f2))

                actions.append(3)
                correspondingCards.append((minFirst, f2))
                
                    
            else: #we don't have any of the first played card
                maxTrump = None
                minTrump = None
                garbageCard = False
                highPointsCard = None
                lowestCard = None
                highestCard = None
                for c in listOfPlayerCards:
                    c1, c2 = c
                    if c == (0,0):
                        actions.append(8) #can play 0,0
                        correspondingCards.append((0,0))
                    elif c2 == self.trumpSuit:
                        
                        if maxTrump == None:
                            maxTrump = c1
                        elif c1 > maxTrump:
                            maxTrump = c1
                            
                        if minTrump == None:
                            minTrump = c1
                        elif c1 < minTrump:
                            minTrump = c1
                    elif 2*c1 == c2:
                        highPointsCard = (c1, c2)
                    else:
                        if not lowestCard == None:
                            l1, l2 = lowestCard
                            ratioLow = float(l1)/float(l2)
                            ratioCard = float(c1)/float(c2)
                            if ratioCard < ratioLow:
                                lowestCard = c
                        else:
                            lowestCard = c
                        if not highestCard == None:
                            h1, h2 = highestCard
                            ratioHigh = float(h1)/float(h2)
                            ratioCard = float(c1)/float(c2)
                            if ratioCard > ratioHigh:
                                highestCard = c
                        else:
                            highestCard = c
                if not lowestCard == None:
                    actions.append(3)
                    correspondingCards.append(lowestCard)
                if not highPointsCard == None:
                    actions.append(2)
                    correspondingCards.append(highPointsCard)
                if not maxTrump == None:
                    actions.append(1)
                    correspondingCards.append((maxTrump, self.trumpSuit))
                elif not highestCard == None:
                    actions.append(1)
                    correspondingCards.append(highestCard)
                    
        else:
            maxTrump = None
            minTrump = None
            garbageCard = False
            highPointsCard = None
            lowestCard = None
            highestCard = None
            for c in listOfPlayerCards:
                c1, c2 = c
                if c == (0,0):
                    actions.append(8) #can play 0,0
                    correspondingCards.append((0,0))
                elif c2 == self.trumpSuit:
                    
                    if maxTrump == None:
                        maxTrump = c1
                    elif c1 > maxTrump:
                        maxTrump = c1
                        
                    if minTrump == None:
                        minTrump = c1
                    elif c1 < minTrump:
                        minTrump = c1
                elif 2*c1 == c2:
                    highPointsCard = (c1, c2)
                else:
                    if not lowestCard == None:
                        l1, l2 = lowestCard
                        ratioLow = float(l1)/float(l2)
                        ratioCard = float(c1)/float(c2)
                        if ratioCard < ratioLow:
                            lowestCard = c
                    else:
                        lowestCard = c
                    if not highestCard == None:
                        h1, h2 = highestCard
                        ratioHigh = float(h1)/float(h2)
                        ratioCard = float(c1)/float(c2)
                        if ratioCard > ratioHigh:
                            highestCard = c
                    else:
                        highestCard = c
            if not lowestCard == None:
                actions.append(3)
                correspondingCards.append(lowestCard)
            if not highPointsCard == None:
                actions.append(2)
                correspondingCards.append(highPointsCard)
            if not maxTrump == None:
                actions.append(1)
                correspondingCards.append((maxTrump, self.trumpSuit))
            elif not highestCard == None:
                actions.append(1)
                correspondingCards.append(highestCard)
        return actions, correspondingCards
        
    def playRandomCard(self,playerNum):
        actions, correspondingCards = self.getActions(playerNum)
        card = random.choice(correspondingCards)
        self.cardsInTrick += 1
        self.deck[card] = 4 + playerNum
        debugprint("Player " + str(playerNum) + " has played " + str(card))
        if self.firstPlayedCard == None:
            self.firstPlayedCard = card
            self.winningCard = card
            debugprint("Winning Card now " + str(self.winningCard))
        else:
            c1, c2 = card
            w1, w2 = self.winningCard
            if w1 == 0 and w2 == 0:
                if c1 == c2:
                    self.winningCard = card
                    debugprint("Winning Card now " + str(self.winningCard))
            else:
                if c2 == w2:
                    if c1 > w1:
                        self.winningCard = card
                        debugprint("Winning Card now " + str(self.winningCard))
                else:
                    if c2 == self.trumpSuit:
                        self.winningCard = card
                        debugprint("Winning Card now " + str(self.winningCard))

    def getInitialState(self):
        # State is defined as
        # suit of most trumps
        # number of that suit
        # have -1 card
        numberTwos = 0
        numberFours = 0
        numberSixes = 0
        numberEights = 0
        numberTens = 0 
        numberTwelves = 0
        
        haveNeg1 = 0
        for c in self.deck:
            c1, c2 = c
            if self.deck[c] == 1:
                if c1 == -1:
                    numberTwos += 1
                    numberFours += 1
                    numberSixes += 1
                    numberEights += 1
                    numberTens += 1
                    numberTwelves += 1
                    haveNeg1 = 1
                else:
                    if c2 == 2:
                        numberTwos += 1
                    if c2 == 4:
                        numberFours += 1
                    if c2 == 6:
                        numberSixes += 1
                    if c2 == 8:
                        numberEights += 1
                    if c2 == 10:
                        numberTens += 1
                    if c2 == 12:
                        numberTwelves += 1
        maxTrumpSuit = 2
        maxTrumpNumber = 0
        
        if (numberTwelves >= numberTwos) and (numberTwelves >= numberFours) and (numberTwelves >= numberSixes) and (numberTwelves >= numberEights) and (numberTwelves >= numberTens):
            maxTrumpSuit = 12
            maxTrumpNumber = numberTwelves
        if (numberTens >= numberTwos) and (numberTens >= numberFours) and (numberTens >= numberSixes) and (numberTens >= numberEights) and (numberTens >= numberTwelves):
            maxTrumpSuit = 10
            maxTrumpNumber = numberTens
        if (numberEights >= numberTwos) and (numberEights >= numberFours) and (numberEights >= numberSixes) and (numberEights >= numberTens) and (numberEights >= numberTwelves):
            maxTrumpSuit = 8
            maxTrumpNumber = numberEights
        if (numberSixes >= numberTwos) and (numberSixes >= numberFours) and (numberSixes >= numberEights) and (numberSixes >= numberTens) and (numberSixes >= numberTwelves):
            maxTrumpSuit = 6
            maxTrumpNumber = numberSixes
        if (numberFours >= numberTwos) and (numberFours >= numberSixes) and (numberFours >= numberEights) and (numberFours >= numberTens) and (numberFours >= numberTwelves):
            maxTrumpSuit = 4
            maxTrumpNumber = numberFours
        if (numberTwos >= numberFours) and (numberTwos >= numberSixes) and (numberTwos >= numberEights) and (numberTwos >= numberTens) and (numberTwos >= numberTwelves):
            maxTrumpSuit = 2
            maxTrumpNumber = numberTwos
            
        return (maxTrumpSuit, maxTrumpNumber, haveNeg1)
    
    def getInitialActions(self):
        initActions = []
        for c in self.deck:
            c1, c2 = c
            if self.deck[c] == 1:
                if c2 == 2 and 2 not in initActions:
                    initActions.append(2)
                if c2 == 4 and 4 not in initActions:
                    initActions.append(4)
                if c2 == 6 and 6 not in initActions:
                    initActions.append(6)
                if c2 == 8 and 8 not in initActions:
                    initActions.append(8)
                if c2 == 10 and 10 not in initActions:
                    initActions.append(10)
                if c2 == 12 and 12 not in initActions:
                    initActions.append(12)
        return initActions
        
    def getState(self):
        #  State is going to be defined as a tuple of:
        #  round
        #  place in trick (first - 0, second - 1, third - 2, fourth - 3)
        #  is team 1 winning the trick? (0 means its first card, 1 means team 1 winning, 2 is team 2 winning)
        #  will our high card beat the current highest card (no - 0, yes - 1)
        #  number of cards remaining that can beat my high card (none - 0, less than 3 - 1, 3 or more - 2)
        #  can play points card 
        
        # team1 winning
        team1winning = 0
        if self.firstPlayedCard == None or self.firstPlayedCard == (-2, self.trumpSuit):
            team1winning = 0
        else:
            for c in self.deck:
                if c == self.winningCard:
                    if self.deck[c] == 5 or self.deck[c] == 7:
                        team1winning = 1
                    else:
                        team1winning = 2
        
        
        numberTrumpsPlayer = 0
        numberTrumpsUnseen = 0
        listOfPlayerCards = []
        for c in self.deck:
            c1, c2 = c
            if self.deck[c] == 1:
                listOfPlayerCards.append(c)
                if c2 == self.trumpSuit:
                    numberTrumpsPlayer += 1
            elif not self.deck[c] == -1 and not self.deck[c] == 1:
                if c2 == self.trumpSuit:
                    numberTrumpsUnseen += 1
        # if self.round == 1:
        #     print(listOfPlayerCards)
        # have better card
        haveBetterCard = 0
        if not self.firstPlayedCard == None:
            f1, f2 = self.firstPlayedCard
            highOfFirstPlayedCard = -3
            for c in listOfPlayerCards:
                c1, c2 = c
                if c2 == f2:
                    if c1 > highOfFirstPlayedCard:
                        highOfFirstPlayedCard = c1
            if highOfFirstPlayedCard > f1 or numberTrumpsPlayer > 0:
                haveBetterCard = 1
        else:
            haveBetterCard = 1
        
        canPlayPoints = 0
        havePlayablePoints = False
        if self.firstPlayedCard == None:
            for c in listOfPlayerCards:
                c1, c2 = c
                if c1*2 == c2:
                    havePlayablePoints = True
        else:
            f1, f2 = self.firstPlayedCard
            haveFirstSuit = False
            havePlayablePoints = False
            for c in listOfPlayerCards:
                c1, c2 = c
                if c2 == f2:
                    haveFirstSuit = True
                    if c1*2 == f2:
                        havePlayablePoints = True
            if haveFirstSuit == False:
                for c in listOfPlayerCards:
                    c1, c2 = c
                    if c1*2 == c2:
                        havePlayablePoints = True
                
        if havePlayablePoints == True:
            canPlayPoints = 1
            
        
        percentUnseen = float(numberTrumpsUnseen)/float(self.trumpSuit + 1)
        percentUnseenState = 0
        if percentUnseen < 0.5:
           percentUnseenState = 0
        elif percentUnseen < 0.75:
           percentUnseenState = 1
        else:
           percentUnseenState = 2

        highPointsCard = None
        lowestCard = None
        highestCard = None
        haveHighestCard = 0
        for c in listOfPlayerCards:
            c1, c2 = c
            if not c2 == self.trumpSuit:
                if not highestCard == None:
                    h1, h2 = highestCard
                    if not h2 == 0 and not c2 == 0:
                        ratioHigh = float(h1)/float(h2)
                        ratioCard = float(c1)/float(c2)
                        if ratioCard > ratioHigh:
                            highestCard = c
                        if ratioCard > 0.99:
                            haveHighestCard = 1
                else:
                    highestCard = c
                    if not c2 == 0:
                        ratioCard = float(c1)/float(c2)
                        if ratioCard > 0.99:
                            haveHighestCard = 1
        numberPlayed = 0
        for c in self.deck:
                if self.deck[c] == 6 or self.deck[c] == 7 or self.deck[c] == 8:
                    numberPlayed += 1
        amLast = 0
        if numberPlayed == 3:
            amLast = 1
        
        return (self.round, self.cardsInTrick, team1winning, haveBetterCard, canPlayPoints, numberTrumpsPlayer, self.trumpSuit)
    
    def computeWinnerAndReward(self):
        score = 1
        self.cardsInTrick = 0
        for c in self.deck.keys():
            c1, c2 = c
            
            if self.deck[c] == 5 or self.deck[c] == 6 or self.deck[c] == 7 or self.deck[c] == 8:
                if c1 == -1:
                    score += 3
                if 2*c1 == c2 and not c1 == 0 and c2 > 7:
                    score += 2
                elif 2*c1 == c2 and not c1 == 0:
                    score += 1
                    
            if c == self.winningCard:
                winningVal = self.deck[c]
                
        if winningVal == 5 or winningVal == 7:
            self.team1Score += score
            reward = score
            debugprint("Team 1 wins the trick")
        else:
            self.team2Score += score
            reward = 0
            debugprint("Team 2 wins the trick")
            
        debugprint("Team 1 score: " + str(self.team1Score))
        debugprint("Team 2 score: " + str(self.team2Score))
        
        self.round += 1
        debugprint("")
        debugprint("Now beginnng round " +str(self.round))
        for c in self.deck.keys():
            if self.deck[c] == 5 or self.deck[c] == 6 or self.deck[c] == 7 or self.deck[c] == 8:
                self.deck[c] = -1 #indicate it has been seen
        return winningVal, reward
    
    def kickOffNextHand(self,winningVal):
        if self.round < 13:
            # self.round += 1
            self.firstPlayedCard = None
            self.winningCard = None
            if winningVal == 5:
                state = self.getState()
                return state
            elif winningVal == 6:
                self.playRandomCard(2)
                self.playRandomCard(3)
                self.playRandomCard(4)
                state = self.getState()
                return state
            elif winningVal == 7:
                self.playRandomCard(3)
                self.playRandomCard(4)
                state = self.getState()
                return state
            elif winningVal == 8:
                self.playRandomCard(4)
                state = self.getState()
                return state
        else:
            return (13,)
    
    def playCard(self, card):
        # print(card)
        gameComplete = False
        if self.round == 12:
            gameComplete = True
        self.deck[card] = 5
        if self.cardsInTrick == 0:
            self.firstPlayedCard = card
            self.winningCard = card
        else:
            w1, w2 = self.winningCard
            c1, c2 = card
            if w2 == self.trumpSuit:
                if c2 == self.trumpSuit:
                    if c1 > w1:
                        self.winningCard = card
            else:
                if c2 == self.trumpSuit:
                    self.winningCard = card
                else:
                    if w1 == w2:
                        if c1 == c2:
                            if c1 > c2:
                                self.winningCard = card
                    else:
                        if c1 == 0 and c2 == 0:
                            self.winningCard = card
                        else:
                            if c2 == w2:
                                if c1 > w1:
                                    self.winningCard = card
                        
        self.cardsInTrick += 1
        
        if self.cardsInTrick == 4:
            winningVal, reward = self.computeWinnerAndReward()
            state = self.kickOffNextHand(winningVal)
            return state, reward, gameComplete
        else:
            self.playRandomCard(2)
            if self.cardsInTrick == 4:
                winningVal, reward = self.computeWinnerAndReward()
                state = self.kickOffNextHand(winningVal)
                return state, reward, gameComplete
            self.playRandomCard(3)
            if self.cardsInTrick == 4:
                winningVal, reward = self.computeWinnerAndReward()
                state = self.kickOffNextHand(winningVal)
                return state, reward, gameComplete
            self.playRandomCard(4)
            if self.cardsInTrick == 4:
                winningVal, reward = self.computeWinnerAndReward()
                state = self.kickOffNextHand(winningVal)
                return state, reward, gameComplete
            

                
def manualGame():
    global debugPrinting
    debugPrinting = True
    #init Q
    g = Game()
    g.dealDeck()
    debugprint("Here is your hand: ")
    g.printHand(1)
    trumpVal = int(input("What would you like to set as the trump value? "))
    g.setTrump(trumpVal)
    gameComplete = False
    while not gameComplete:
        actions, correspondingCards = g.getActions(1)
        print("You can play these cards " + str(correspondingCards))
        a = int(input("What's the position of the card in the above list you would like to play? (position starts at 0) "))
        state, reward, gameComplete = g.playCard(correspondingCards[a])
    print("Game Complete")
    print("Team 1 final score: " + str(g.team1Score))
        
            
def playRandomGames(outFile):
    outF = open(outFile, 'w')
    debugPrinting = False
    #init Q
    outF = open('randomGames.csv', 'w')
    for i in range(10000):
        g = Game()
        g.dealDeck()
        g.setTrump(random.choice(g.getInitialActions()))
        gameComplete = False
        state = g.getState()
        while not gameComplete:
            actions, correspondingCards = g.getActions(1)
            debugprint("You can play these cards " + str(correspondingCards))
            state, reward, gameComplete = g.playCard(random.choice(correspondingCards))
            debugprint("Game Complete: " + str(gameComplete))
            
        print("Team 1 final score: " + str(g.team1Score))
        outF.write(str(i) + ',' + str(g.team1Score)+ ',' + str(g.team2Score)+ '\n')
    outF.close()

def learnQ(outFile):
    outF = open(outFile, 'w')
    debugPrinting = False
    discount = 1.0
    
    #init Q
    Q = {}
    
    # Set up trump setting states:
    for suit in [2,4,6,8,10,12]:
        for maxNum in range(2, suit+3):
            for neg1Card in range(2):
                dummyState = (suit, maxNum, neg1Card)
                for dummyAction in [2,4,6,8,10,12]:
                    Q[(dummyState, dummyAction)] = 0
                    
    Occur = {}
    # Set up trump setting states:
    for suit in [2,4,6,8,10,12]:
        for maxNum in range(2, suit+3):
            for neg1Card in range(2):
                dummyState = (suit, maxNum, neg1Card)
                for dummyAction in [2,4,6,8,10,12]:
                    Q[(dummyState, dummyAction)] = 0
                    Occur[(dummyState, dummyAction)] = 0
            
     
    # Set up card playing states
    for a in range(1, 13):
        for b in range(0,4):
            for c in range(0,3):
                for d in range(0,2):
                    for e in range(0,2):
                        for numberTrump in range(0,14):
                            for tSuit in [2,4,6,8,10,12]:
                                dummyState = (a,b,c,d,e,numberTrump,tSuit)
                                for dummyAction in range(1,9):
                                    Q[(dummyState, dummyAction)] = 0
    terminalState = (13,)
    for dummyAction in range(1,9):
        Q[(terminalState, dummyAction)] = 0
        
    for i in range(100000):
        
        # epsilon greedy for now
        epsilon = 5000.0/(5000.0+i)
        
        learningRate = 0.1
        
        g = Game()
        g.dealDeck()
        
        initState = g.getInitialState()
        actions = g.getInitialActions()
        
        if random.uniform(0.0, 1.0) < epsilon: # choose random
            trumpSuit = random.choice(actions)
            g.setTrump(trumpSuit)
        else: # choose best
            bestQ = -1
            for j in range(len(actions)):
                if Q[(initState, actions[j])] > bestQ:
                    bestQ = Q[(initState, actions[j])]
                    trumpSuit = actions[j]
            g.setTrump(trumpSuit)
        
        gameComplete = False
        state = g.getState()
        
        maxNextQ = -1
        for dummyAction in range(1,9):
            if Q[(state, dummyAction)] > maxNextQ:
                maxNextQ = Q[(state, dummyAction)]
        
        Q[(initState, trumpSuit)] =  Q[(initState, trumpSuit)] + learningRate * ( discount * maxNextQ -  Q[(initState, trumpSuit)]) # Note: reward for this action is 0
        Occur[(initState, trumpSuit)] =  Occur[(initState, trumpSuit)] + 1
        
            
        while not gameComplete:
            actions, correspondingCards = g.getActions(1)
            # print("Action vals " +str(actions))
            # choose action based on strategy

            cardToPlay = None
            action = None
            bestQ = -1
            if random.uniform(0.0, 1.0) < epsilon: # choose random
                cardToPlay = random.choice(correspondingCards)
                action = actions[correspondingCards.index(cardToPlay)]
            else: # choose best    
                for j in range(len(actions)):
                    if Q[(state, actions[j])] > bestQ:
                        cardToPlay = correspondingCards[j]
                        bestQ = Q[(state, actions[j])]
                        action = actions[j]
                        
            debugprint("You can play these cards " + str(correspondingCards))
            nextState, reward, gameComplete = g.playCard(cardToPlay)
            # Bellmans equation
            maxNextQ = 0
            for dummyAction in range(1,9):
                if Q[(nextState, dummyAction)] > maxNextQ:
                    maxNextQ = Q[(nextState, dummyAction)]
            
            Q[(state, action)] =  Q[(state, action)] + learningRate * (reward + discount * maxNextQ -  Q[(state, action)])
            
            state = nextState
            debugprint("Game Complete: " + str(gameComplete))
            
        print("Team 1 final score: " + str(g.team1Score))
        outF.write(str(i) + ',' + str(g.team1Score)+ ',' + str(g.team2Score)+ '\n')
    print(Q)
    outF.close()
    
    for suit in [2,4,6,8,10,12]:
        for maxNum in range(2, suit+3):
            for neg1Card in range(2):
                dummyState = (suit, maxNum, neg1Card)
                for dummyAction in [2,4,6,8,10,12]:
                    print(str((dummyState, dummyAction)) + ": " + str(Q[(dummyState, dummyAction)]) + ": " + str(Occur[(dummyState, dummyAction)]))


def learnQLambda(outFile):
    outF = open(outFile, 'w')
    debugPrinting = False
    discount = 1.0
    lambdaVal = 0.9
    
    #init Q
    Q = {}
    
    # Set up trump setting states:
    for suit in [2,4,6,8,10,12]:
        for maxNum in range(2, suit+3):
            for neg1Card in range(2):
                dummyState = (suit, maxNum, neg1Card)
                for dummyAction in [2,4,6,8,10,12]:
                    Q[(dummyState, dummyAction)] = 0
                    
    Occur = {}
    # Set up trump setting states:
    for suit in [2,4,6,8,10,12]:
        for maxNum in range(2, suit+3):
            for neg1Card in range(2):
                dummyState = (suit, maxNum, neg1Card)
                for dummyAction in [2,4,6,8,10,12]:
                    Q[(dummyState, dummyAction)] = 0
                    Occur[(dummyState, dummyAction)] = 0
            
     
    # Set up card playing states
    for a in range(1, 13):
        for b in range(0,4):
            for c in range(0,3):
                for d in range(0,2):
                    for e in range(0,2):
                        for numberTrump in range(0,14):
                            for tSuit in [2,4,6,8,10,12]:
                                dummyState = (a,b,c,d,e,numberTrump,tSuit)
                                for dummyAction in range(1,9):
                                    Q[(dummyState, dummyAction)] = 0
    terminalState = (13,)
    for dummyAction in range(1,9):
        Q[(terminalState, dummyAction)] = 0
        
    for i in range(300000):
        
        seenSAPairs = []
        N = {}
        # epsilon greedy for now
        epsilon = 20000.0/(20000.0+i)
        
        learningRate = 0.1
        
        g = Game()
        g.dealDeck()
        
        initState = g.getInitialState()
        actions = g.getInitialActions()
        
        if random.uniform(0.0, 1.0) < epsilon: # choose random
            trumpSuit = random.choice(actions)
            g.setTrump(trumpSuit)
        else: # choose best
            bestQ = -1
            for j in range(len(actions)):
                if Q[(initState, actions[j])] > bestQ:
                    bestQ = Q[(initState, actions[j])]
                    trumpSuit = actions[j]
            g.setTrump(trumpSuit)
        
        N[(initState, trumpSuit)] = 1.0
        seenSAPairs.append((initState, trumpSuit))
        
        gameComplete = False
        state = g.getState()
        
        maxNextQ = -1
        for dummyAction in range(1,9):
            if Q[(state, dummyAction)] > maxNextQ:
                maxNextQ = Q[(state, dummyAction)]
        
        delta = discount * maxNextQ -  Q[(initState, trumpSuit)]
        
        for saPair in seenSAPairs:
            Q[saPair] = Q[saPair] + learningRate * delta
            N[saPair] = discount*lambdaVal*N[saPair]
        
        Occur[(initState, trumpSuit)] =  Occur[(initState, trumpSuit)] + 1
        
        # print(str(trumpSuit) + " " + str(initState) + " " + str(state))
            
        while not gameComplete:
            actions, correspondingCards = g.getActions(1)
            # print("Action vals " +str(actions))
            # choose action based on strategy

            cardToPlay = None
            action = None
            bestQ = -24
            if random.uniform(0.0, 1.0) < epsilon: # choose random
                cardToPlay = random.choice(correspondingCards)
                action = actions[correspondingCards.index(cardToPlay)]
            else: # choose best    
                for j in range(len(actions)):
                    if Q[(state, actions[j])] > bestQ:
                        cardToPlay = correspondingCards[j]
                        bestQ = Q[(state, actions[j])]
                        action = actions[j]
            
                
            N[(state, action)] = 1.0
            seenSAPairs.append((state, action))
            
            debugprint("You can play these cards " + str(correspondingCards))

            nextState, reward, gameComplete = g.playCard(cardToPlay)
            # Bellmans equation
            maxNextQ = 0
            for dummyAction in range(1,9):
                if Q[(nextState, dummyAction)] > maxNextQ:
                    maxNextQ = Q[(nextState, dummyAction)]
                    
            delta = reward + discount * maxNextQ -  Q[(state,action)]
            
            for saPair in seenSAPairs:
                Q[saPair] = Q[saPair] + learningRate * delta * N[saPair]
                N[saPair] = discount*lambdaVal*N[saPair]
                   
            state = nextState
            debugprint("Game Complete: " + str(gameComplete))
            
        print("Team 1 final score: " + str(g.team1Score))
        outF.write(str(i) + ',' + str(g.team1Score)+ ',' + str(g.team2Score)+ '\n')
    outF.close()
    
    QValFromStartFile = open('QValFromStart.csv' , 'w')
    for suit in [2,4,6,8,10,12]:
        for maxNum in range(2, suit+3):
            for neg1Card in range(2):
                dummyState = (suit, maxNum, neg1Card)
                for dummyAction in [2,4,6,8,10,12]:
                    QValFromStartFile.write(str((dummyState, dummyAction)) + ": " + str(Q[(dummyState, dummyAction)]) + ": " + str(Occur[(dummyState, dummyAction)])+"\n")

    QValFromStartFile.close()


def main():
    if "manual" == sys.argv[1]:
        manualGame()
    if "random" == sys.argv[1]:
        outFile = sys.argv[2]
        playRandomGames(outFile)
    if "Q" == sys.argv[1]:
        outFile = sys.argv[2]
        learnQ(outFile)
    if "QLambda" == sys.argv[1]:
        outFile = sys.argv[2]
        learnQLambda(outFile)

if __name__ == '__main__':
    main()
