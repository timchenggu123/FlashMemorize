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
    def __init__(self,front,back,ID):
        self.front = front
        self.back = back
        self.side = 1
        self.timesStudied = 0
        self.timesCorrect = 0
        self.id = ID
    
    def flip(self, notRandom = 1):
        if notRandom:
            self.side = abs(self.side -1)
        else:
            self.side = rd.randrange(0,2)
        
        return
    
    def show(self):
        if self.side == 1:
            return self.front
        else:
            return self.back
    
class deck:
    def __init__(self,name,cards = [],):
        self.cards = cards
        self.size = len(cards)
        self.order = list(range(len(cards)))
        self.name = name
        
    def shuffle(self,allCards = 1,rndFlip = 0):
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
        self.cards = self.dk.getdeck()
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
        self.dk.cards[self.i].flip()
        self.showCard()

    @pyqtSlot()
    def Shuffle(self):
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



    
            
    
