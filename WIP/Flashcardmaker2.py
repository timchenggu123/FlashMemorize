import tkinter as tk
import random as rd
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout
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
    
class deck:
# The deck class' main purpose is to hold and manage a list of card objects

    def __init__(self,name,cards = [],):
    # name<string/int>: a unique name for the deck
    # cards<list>: a list containing card objects
        self.cards = cards
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
                self.cards[i].side = 1
        elif rndFlip == 1:
            for i in self.cards:
                self.cards[i].flip(notRandm = 0)
        else:
            for i in self.cards:
                self.cards[i].side = 0
                
    def append(self,card):
        # Add a new card to the bottom of the deck and restore order. Call this method instead of directly modifying self.cards.
        # card: the card object to be appended
        self.cards.append(card)
        self.size = len(self.cards)
        self.order = list(range(len(self.cards)))
       
    def getdeck(self):
        dk = list()
        for i in self.order:
            dk.append(self.cards[i])
        
        return dk

class mainProgram(QWidget):
    
    def __init__(self,deck):
        super().__init__()
        
        self.dk = deck # a deck object
        self.i = 0 # a counter keeping track of where we are in the deck
        
        self.shuffle()
        self.initUI()
        
        
    def initUI(self):
        # The main canvas
        self.label = QLabel(self.readCard(self.i),self)
        
        # The buttons 
        btnNext = QPushButton('Next')
        #btnNext.resize(btnNext.sizeHint())
        
        btnFlip = QPushButton('Flip')
        #btnFlip.resize(btnFlip.sizeHint())
        
        btnPrev = QPushButton('Previous',self)
        #btnPrev.resize(btnPrev.sizeHint())

        btnShuf = QPushButton('Shuffle',self)
        
        btnPrev.clicked.connect(self.Prev)
        btnFlip.clicked.connect(self.Flip)
        btnNext.clicked.connect(self.Next)
        btnShuf.clicked.connect(self.Shuffle)
        
                
        # Create Boxes
        hbox = QHBoxLayout()
       
        hbox.addWidget(btnPrev)
        hbox.addWidget(btnFlip)
        hbox.addWidget(btnNext)
        hbox.addWidget(btnShuf)
        
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        
        self.setGeometry(300,300,300,220)
        self.setWindowTitle('SmartFlashCard')
        
        self.show()
    
    def readCard(self,i):
        return(self.cards[i].show())
    
    def showCard(self):
        self.label.setText(self.readCard(self.i))
        
    @pyqtSlot()
    def Next(self):
        ncards = self.dk.size
        self.i = self.i + 1
        if self.i == ncards:
            self.i = 0
            
        self.showCard()
        
    @pyqtSlot()
    def Prev(self):
        self.i = self.i - 1
        if self.i < 0:
            self.i = self.dk.size - 1
            
        self.showCard()
    
    @pyqtSlot()
    def Flip(self):
        self.cards[self.i].flip()
        self.showCard()

    def Shuffle(self):
        self.cards = self.dk.getdeck()
        self.i = 0
        self.dk.shuffle()
        self.showCard()
    
    
#Prompt user to select source file & extract lines from source file
tk.Tk().withdraw()  
filename = askopenfilename()
file = open(filename, 'r')
lines = file.readlines()

all_cards = list()
ID = 0

# generating deck
for l in lines:
    if l.find('    ') > 0:
        a = l.find('    ') 
        b = l.find('    ') +4
    front = l[0:a]
    back = l[b:]
    all_cards.append(card(front,back,ID))
    ID = ID +1

dk = deck(filename,all_cards)
cards = dk.getdeck()


#Entering Mainloop
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = mainProgram(dk)
    sys.exit(app.exec_())
#
#    w = QWidget()
#    w.reside(250,150)
#    w.move(300,300)
#    w.setWindowTitle('test')
#    w.show()
#    
#    sys.exit(app.exec_())
#    



    
            
    
