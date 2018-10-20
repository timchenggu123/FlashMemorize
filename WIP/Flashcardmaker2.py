import tkinter as tk
import random as rd
import sys
import pickle
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QMainWindow,QFrame
from PyQt5.QtCore import pyqtSlot
from tkinter.filedialog import askopenfilename

# initalize global variables
nm = 0 #holds the number of card
currentside = 0 #holds the current state of each card. 
counter = 1

# Declaring Classes
class card:
#This class creates card objects. The class contains the following methods:
#  - __init__('front','back', 1234): The constructor.
#  - flip(self, notRandom =0): flip to the opposite side if not Random = 0, or flip to a random side otherwise
#  - show(): return the text on the current side of the card

    def __init__(self,front,back,ID):
        self.front = front         # String variable. Contains content on the front side of the card
        self.back = back           # String variable. Contains content on the back side of the card
        self.side = 1              # int [0,1]. 1 represent front side and 0 represent back side. determine which side is facing up
        self.timesStudied = 0      # int. How many times the cards been studied
        self.timesCorrect = 0      # int. How many time sthe cards been right
        self.id = ID               # int/string. A unique id for each card
        self.viewed = 0
    def flip(self, notRandom = 1):
        # flip(self, notRandom =0): flip to the opposite side if not Random = 0, or flip to a random side otherwise
        # notRandom: integer or logical. 0 to flip to a random side, 1 to flip to the opposite side.
        if notRandom:
            self.side = abs(self.side -1)
        else:
            self.side = rd.randrange(0,2)
        
        return
    
    def show(self):
        # show(): return the text on the current side of the card
        if self.side == 1:
            return self.front
        else:
            return self.back
    def getStats(self):
        if self.timesStudied != 0:
            return self.timesCorrect/self.timesStudied
        else:
            return 0
    
    
class deck:
# The deck class' main purpose is to hold and manage a list of card objects

    def __init__(self,name,cards = [],):
    # name<string/int>: a unique name for the deck
    # cards<list>: a list containing card objects
        self.cards = cards
        self.subDeck = list()
        self.size = len(cards)
        self.order = list(range(len(cards))) # A list containing the order by which the cards are sorted
        self.name = name
        
    def shuffle(self,allCards = 1,rndFlip = 0):
    #Shuffle the deck
    #allCards<int/logical> [0,1]: 1 then the deck is shuffled such that all cards are included at least once
    #rndFlip<int> [0,1,2]: 0: all cards facing front; 1: all cards randomly flipped; 2: all cards facing back
        self.order = list(range(len(self.cards)))
        if allCards:
            rd.shuffle(self.order)
        else:
            for i in self.order:
                self.order[i] = rd.randrange(0,len(self.order))
                
        if rndFlip == 0:
            for i in self.cards:
                i.side = 1
        elif rndFlip == 1:
            for i in self.cards:
                i.flip(notRandm = 0)
        else:
            for i in self.cards:
                i.side = 0
                
    def append(self,card):
        # Add a new card to the bottom of the deck and restore order. Call this method instead of directly modifying self.cards.
        # card: the card object to be appended
        self.cards.append(card)
        self.size = len(self.cards)
        self.order = list(range(len(self.cards)))
       
    def getdeck(self):
        # return a list containing cards sorted according to self.order
        dk = list()
        for i in self.order:
            dk.append(self.cards[i])
        
        return dk
    
    def newSubdeck(self,subIDs):
        self.subDeck.append(deck([self.cards[indx] for indx in subIDs]))
    
    def deckStats(self):
        #returns the overall correct rate of the deck
        accuracy = 0
        totaltimes = 0
        totalviewed = 0
        for i in self.cards:
            accuracy = accuracy + i.getStats()
            totaltimes = totaltimes + i.timesStudied
            totalviewed = totalviewed + i.viewed
        accuracy = accuracy/totalviewed
        return [accuracy, totaltimes]
        
    def rankCards(self):
        cardsStats = [self.cards[indx].getStats() for indx in range(self.size)]
        cardsID = [self.cards[indx].id for indx in range(self.size)]
        statsID = zip(cardsStats,cardsID)   
        statsID = sorted(statsID)
        rank = [ID for _,ID in statsID ]
        return rank
        
class mainProgram(QWidget):
    
    def __init__(self,deck):
    # deck: a deck object to be displayed by the program
        super().__init__()
        
        self.dk = deck
        self.i = 0           # a counter keeping track of the current card index in self.cards
        self.correct = 1
        
        self.initUI()
        
        
    def initUI(self):
        
        # Shuffle cards
        self.shuffle()
        
        # The main canvas
        self.stats = QLabel('% accuracy: 0% Cards Studied: 0 Total Cards: ' + str(self.dk.size),self)
        self.stats.setGeometry(1,1,400,20)
        self.dispID = QLabel('CardID:' + str(self.cards[self.i].id),self)
        self.dispID.setGeometry(30,30,100,20)
        
        self.canvas = QLabel('',self)
        self.canvas.setGeometry(30,30,400,200)
        self.canvas.setFrameStyle(QFrame.Panel)
        
        
        # The buttons 
        btnGood = QPushButton('Good')
        btnFlip = QPushButton('Flip')
        btnPrev = QPushButton('Previous',self)
        btnShuf = QPushButton('Shuffle',self)
        btnBad = QPushButton('Bad',self)
        btnNext = QPushButton('Next',self)
        
        btnPrev.clicked.connect(self.Prev)
        btnFlip.clicked.connect(self.Flip)
        btnGood.clicked.connect(self.Good)
        btnShuf.clicked.connect(self.shuffle)
        btnBad.clicked.connect(self.Bad)
        btnNext.clicked.connect(self.Next)
        
        # Create Boxes
        hbox = QHBoxLayout()
       
        hbox.addWidget(btnPrev)
        hbox.addWidget(btnFlip)
        hbox.addWidget(btnNext)
        hbox.addWidget(btnGood)
        hbox.addWidget(btnBad)
        hbox.addWidget(btnShuf)
        
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        
#        self.setGeometry(300,300,300,220)
#        self.setWindowTitle('SmartFlashCard')
#        
#        self.show()
    
    def readCard(self,i):
    #Return the text on the current side of card[i]
    # i <int> the ith card in the deck
        return(self.cards[i].show()) 
    
    def showCard(self):
    #Display the text on canvas
        self.canvas.setText(self.readCard(self.i)) 
        self.dispID.setText('CardID:' + str(self.cards[self.i].id))
    def moveCard(self,step,updateStats = 1):
        if updateStats:
            self.updateStats()
#        else:
#            currentId = self.cards[self.i].id
#            self.dk.cards[currentId].viewed = 1
        
        ncards = self.dk.size
        self.i = self.i + step
        if self.i == ncards:
            self.i = 0
        elif self.i < 0:
            self.i = self.dk.size - 1
        
        
    
    @pyqtSlot()
    def Good(self):
    # pyqt slot. show next card in deck on the canvas
    
        self.moveCard(1)
        self.showCard()
        
    @pyqtSlot()
    def Prev(self):
    # pyqt slot. show previous card on canvas
    # fuck you xinghao
    
        self.moveCard(-1,0)
        self.showCard()
    
    @pyqtSlot()
    # flip the current card and show it on canvas
    def Flip(self):
        self.cards[self.i].flip()
        self.showCard()

    def shuffle(self):
    # shuffle deck
    # Can have more arguments to allow different shuffle modes (see method shuffle() in class deck)
        self.i = 0
        self.dk.shuffle()
        self.cards = self.dk.getdeck()
    
    @pyqtSlot()
    def Bad(self):
    # update the current card status to be wrong
        self.correct = 0
        self.moveCard(1)
        self.showCard()
        print('marked')
    
    @pyqtSlot()
    def Next(self):
        self.moveCard(1,0)
        self.showCard()
                
    def updateStats(self):
    #update the times correct stats of a card
    # correct <int> [0,1]. 0 represent the answer is wrong, 1 represent the answer is correct
        currentId= self.cards[self.i].id
        self.dk.cards[currentId].timesStudied = self.dk.cards[currentId].timesStudied + 1
        self.dk.cards[currentId].timesCorrect = self.dk.cards[currentId].timesCorrect + self.correct
        self.dk.cards[currentId].viewed = 1
        deckStats = self.dk.deckStats()
        self.stats.setText('% accuracy: ' + str(round(deckStats[0]*100)) + '% Cards Studied:  ' 
                           +  str(deckStats[1]) + ' Total Cards: ' + str(self.dk.size))
        self.correct = 1
        
    def saveDeck(self):
        filename = input()
        outfile = open(filename,'wb')
        pickle.dump(self.dk,outfile)
        outfile.close()
        
# test
class mainWindow(QMainWindow):
    
    def __init__(self,deck):
        super().__init__()
        self.deck = deck
        self.initUI()
        
        
    def initUI(self):               
        
        self.mp = mainProgram(self.deck)
        self.setCentralWidget(self.mp)
        
        self.statusBar().showMessage('Ready')
        
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Statusbar')    
        self.show()
        
    def showStats(self):
        stats = self.mp.dk.deckStats()
        self.statusBar().showMessage(str(stats[0]) + '/' + str(stats[1]))
        
#Prompt user to select source file & extract lines from source file
tk.Tk().withdraw()  
filename = askopenfilename()
file = open(filename, 'r')
lines = file.readlines()

all_cards = list()
ID = 0

# generating deck
for l in lines:
    if l.find('\t') > 0:
        a = l.find('\t') 
        b = l.find('\t') +1
    front = l[0:a] 
    front = front.replace('\\n','<br>')
    back = l[b:]
    back = back.replace('\\n','<br>')
    all_cards.append(card(front,back,ID))
    ID = ID +1

dk = deck(filename,all_cards)
cards = dk.getdeck()


#Entering Mainloop
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = mainWindow(dk)
sys.exit(app.exec_())
