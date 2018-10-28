import tkinter as tk
import random as rd
import sys
import pickle
import os.path
import json
import numpy
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QMainWindow,QFrame, QFileDialog, QAction, QMenu, 
QMessageBox)
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon,QFont
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
        self.front = front # String variable. Contains content on the front side of the card
        self.back = back # String variable. Contains content on the back side of the card
        
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
            return 1
    
    
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
        self.ver = opt.ver #store the current program version for compatibility purposes
        
    def shuffle(self,allCards = 1,rndFlip = 0):
    #Shuffle the deck
    #allCards<int/logical> [0,1]: 1 then the deck is shuffled such that all cards are included at least once
    #rndFlip<int> [0,1,2]: 0: all cards facing front; 1: all cards randomly flipped; 2: all cards facing back
        self.order = list(range(len(self.cards)))
        if allCards:
            rd.shuffle(self.order)
        else:
            ncards = len(self.order)
            self.order = list()
            accuracy = list()
            pool = list()
            i = 0 
            for card in range(ncards):
                accuracy.append(self.cards[card].getStats())
            temp = 0
            ##print(accuracy)
            card = -1
            for a in accuracy:
                if a == 0:
                    a = 0.01
                a = 1/a
                card = card + 1
                coeff = self.cards[card].timesStudied  # An arbitrary coefficent for probability of a e.g. probability of a is coeff * (1/a)/ncards. In this case, the coeff is based on the total times the card is studied
                if coeff == 0 :
                    coeff = 0.1
                else:
                    coeff = coeff * 0.1
                a = a * coeff 
                a = a + temp
                temp = a
                pool.append(int(a*100))
            ##print(pool)
            for i in range(ncards):
                draw = rd.randrange(0,pool[len(pool)-1])
                ##print(draw)
                nth = -1
                for location in pool:
                    nth = nth +1
                    if draw < location:
                        self.order.append(nth)
                        break
            ##print(pool)
            #print(self.order)
                
        if rndFlip == 0:
            for i in self.cards:
                i.side = 1
        elif rndFlip == 1:
            for i in self.cards:
                i.flip(0)
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
        totalcorrect = 0
        totalstudied = 0
        totalviewed = 0
        for i in self.cards:
            totalcorrect = totalcorrect + i.timesCorrect
            totalstudied = totalstudied + i.timesStudied
            totalviewed = totalviewed + i.viewed
        if totalstudied == 0:
            accuracy = 0
        else:
            accuracy = totalcorrect/totalstudied
        
        return [accuracy, totalstudied,totalviewed]
        
    def rankCards(self):
        cardsStats = [self.cards[indx].getStats() for indx in range(self.size)]
        cardsID = [self.cards[indx].id for indx in range(self.size)]
        statsID = zip(cardsStats,cardsID)   
        statsID = sorted(statsID)
        rank = [ID for _,ID in statsID ]
        return rank
    
    def resetViewed(self):
        for i in self.cards:
            i.viewed = 0
    
    def getSize(self,entireDeck = 1):
        if entireDeck:
            return self.size
        else:
            handsize = len(numpy.unique(self.order))
            return handsize
            
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
        self.cards = self.dk.getdeck()
        
        # The main canvas
        self.stats = QLabel('% accuracy: 0% Cards Studied: 0 Total Cards: ' + str(self.dk.size),self)
        self.stats.setGeometry(1,1,600,20)
        
        self.canvas = QLabel('',self)
        self.canvas.setGeometry(30,30,500,250)
        self.canvas.setFrameStyle(QFrame.Panel)
        self.canvas.setWordWrap(True)
        font = QFont('Arial',12)
        self.canvas.setFont(font)
        self.canvas.setStyleSheet('QLabel {background-color : white}')
        
        self.dispID = QLabel('CardID:' + str(self.cards[self.i].id),self)
        self.dispID.setGeometry(30,30,100,20)
        
        self.showCard()
        self.updateStats(0)
        
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
        text = self.readCard(self.i)
        text = text.replace(opt.var['kwrd_newline'],'<br>')
        self.canvas.setText(text) 
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
        self.updateStats(0)
        
    
    @pyqtSlot()
    def Good(self):
    # pyqt slot. show next card in deck on the canvas
    
        self.moveCard(1)
        self.showCard()
        
        
    @pyqtSlot()
    def Prev(self):
    # pyqt slot. show previous card on canvas
    # fuck you xinghao
    # fuck you rares
        self.moveCard(-1,0)
        self.showCard()
    
    @pyqtSlot()
    # flip the current card and show it on canvas
    def Flip(self):
        self.cards[self.i].flip()
        self.showCard()

    def shuffle(self,initialize = 0):
    # shuffle deck
    # Can have more arguments to allow different shuffle modes (see method shuffle() in class deck)
        if initialize:
            self.cards = self.dk.getdeck()
            self.updateStats(0)
            self.showCard()
        else:
            choice = QMessageBox.question(self,'Shuffle','Do you wish to shuffle?',QMessageBox.Yes|QMessageBox.No)
            
            if choice == QMessageBox.Yes:
                self.i = 0
                self.dk.shuffle(opt.var['shufflemode'],opt.var['rdmflip'])
                self.cards = self.dk.getdeck()
                self.dk.resetViewed()
                self.updateStats(0)
                msg = QMessageBox(self)
                msg.setWindowTitle('')
                msg.setText('completed!')
                msg.exec_();
                self.showCard()
            
    @pyqtSlot()
    def Bad(self):
    # update the current card status to be wrong
        self.correct = 0
        self.moveCard(1)
        self.showCard()
        #print('marked')
    
    @pyqtSlot()
    def Next(self):
        self.moveCard(1,0)
        self.showCard()
                
    def updateStats(self, updateCards = 1):
    #update the times correct stats of a card
    # correct <int> [0,1]. 0 represent the answer is wrong, 1 represent the answer is correct
        currentId= self.cards[self.i].id    
        if updateCards:
                self.dk.cards[currentId].timesStudied = self.dk.cards[currentId].timesStudied + 1
                self.dk.cards[currentId].timesCorrect = self.dk.cards[currentId].timesCorrect + self.correct
                self.dk.cards[currentId].viewed = 1
            
        cardStats = self.dk.cards[currentId].getStats()
        deckStats = self.dk.deckStats()
        self.stats.setText('Current Card Accuracy: ' + str(round(cardStats*100)) + '% Overall accuracy: ' + 
                           str(round(deckStats[0]*100)) + '% Cards Studied:  ' 
                           +  str(deckStats[1]) + ' Total Cards: ' + str(deckStats[2]) + '/' + str(self.dk.getSize(0)))
        self.correct = 1
        
    def saveDeck(self,filename):
        outfile = open(filename,'wb')
        pickle.dump(self.dk,outfile)
        outfile.close()
    
    def loadDeck(self,deck):
        # deck <obj> the deck object to be loaded
        for v in vars(deck):
            setattr(self.dk, v, getattr(deck,v))
        #self.dk = deck
        self.i = 0
        self.updateStats(0)
        self.showCard()
        
# test
class mainWindow(QMainWindow):
    
    def __init__(self,deck):
        super().__init__()
        self.deck = deck
        self.initUI()
        
    def initUI(self):
        
        self.mp = mainProgram(self.deck)
        self.setCentralWidget(self.mp)
        
        # set menu
        menubar = self.menuBar()
        ## filemenu
        fileMenu = menubar.addMenu('&File')
        
        mSave = QAction(QIcon(), '&Save',self)
        mSave.setShortcut('Ctrl+S')
        mSave.setStatusTip('Save current deck')
        mSave.triggered.connect(self.saveToFile)
        
        mLoad = QAction(QIcon(),'&Load',self)
        mLoad.setShortcut('Ctrl+O')
        mLoad.setStatusTip('Open a saved deck')
        mLoad.triggered.connect(self.loadFile)
        
        mSaveConfig = QAction('Save current configuration',self)
        mSaveConfig.triggered.connect(opt.save)
        
        mRestore = QAction('Restore default setting',self)
        mRestore.triggered.connect(opt.restore)
        
        fileMenu.addAction(mSave)
        fileMenu.addAction(mLoad)
        fileMenu.addAction(mSaveConfig)
        fileMenu.addAction(mRestore)
        
        ## Options menu
        optMenu = menubar.addMenu('&Options')
        
        mShuffleMode = QMenu('&Shuffle Mode', self)
        mAllowRepeat = QAction('Allow Repeats',self,checkable = True)
        mAllowRepeat.setChecked(True)
        mAllowRepeat.triggered.connect(opt.setShuffleMode)
        mRdmFlip = QAction('Allow Random Flips',self,checkable = True)
        mRdmFlip.setChecked(True)
        mRdmFlip.triggered.connect(opt.setRdmFlip)
        mShuffleMode.addAction(mAllowRepeat)
        mShuffleMode.addAction(mRdmFlip)
        
        optMenu.addMenu(mShuffleMode)

        ## Manage Menu
        manMenu = menubar.addMenu('&Manage')
        
        self.statusBar().showMessage('Ready')
        
        self.setGeometry(300, 300, 300, 400)
        self.setWindowTitle('FlashCardMaker2.3')
        self.show()
        
    def showStats(self):
        stats = self.mp.dk.deckStats()
        self.statusBar().showMessage(str(stats[0]) + '/' + str(stats[1]))
     
    @pyqtSlot()
    def saveToFile(self):
        f,_ = QFileDialog.getSaveFileName(directory='untitled.dk',filter = 'Deck File (*.dk)')
        self.mp.saveDeck(f)
        
    @pyqtSlot()
    def loadFile(self):
        f,_ = QFileDialog.getOpenFileName(filter = 'Flash Card Files (*.txt *.dk)')
        ftype = os.path.splitext(f)[1]
        #print(ftype)
        if ftype == '.dk':
            file = open(f,'rb')
            dk = pickle.load(file)
            self.mp.loadDeck(dk)
        else:
            file = open(f, 'r',encoding = 'utf-8')
            lines = file.readlines()
            ##print(lines)
            all_cards = list()
            ID = 0
            # generating deck
            for l in lines:
                if l.find('\t') > 0:
                    a = l.find('\t') 
                    b = a +1
                front = l[0:a] 
                front = front.replace('\\n',opt.var['kwrd_newline'])
                
                back = l[b:]
                back = back.replace('\\n',opt.var['kwrd_newline'])
                
                all_cards.append(card(front,back,ID))
                ID = ID +1
            dk = deck(f,all_cards)
            self.mp.loadDeck(dk)
        self.mp.shuffle(initialize = 1)
        file.close()

    @pyqtSlot()
    def expandDeck(self):
        f,_ = QFileDialog.getOpenFileName(filter = 'Flash Card Files (*.txt *.dk)')
        ftype = os.path.splitext(f)[1]
        #print(ftype)
        if ftype == '.dk':
            file = open(f,'rb')
            dk = pickle.load(file)
            cards = dk.cards
            self.mp.dk.append(cards)
        else:
            file = open(f, 'r',encoding = 'utf-8')
            lines = file.readlines()
            ##print(lines)
            all_cards = list()
            ID = 0
            # generating deck
            for l in lines:
                if l.find('\t') > 0:
                    a = l.find('\t') 
                    b = a +1
                front = l[0:a] 
                front = front.replace('\\n',opt.var['kwrd_newline'])
                
                back = l[b:]
                back = back.replace('\\n',opt.var['kwrd_newline'])
                
                all_cards.append(card(front,back,ID))
                ID = ID +1
        self.mp.dk.append(all_cards)
        self.mp.shuffle(initialize = 1)
        file.close()
             
class options:
    def __init__(self):
        self.var_default = {
            'kwrd_side': '\t', #keyword separating the front and back side of a card
            'kwrd_newline' : ' -', #keyword initating a newline on a card
            'shufflemode' : 0, #shuffle mode
            'rdmflip' : 1,  #enable random flip in shuffle mode
            }
        self.var = self.var_default
        self.ver = '2.4.0'
    
    def load(self):
        
        try:
            f = open('options.json','r')
            var = json.load(f)
            for v in var:
                self.var[v] = var[v]
            f.close()
        except:
            self.save()
            self.load()
        
    def save(self):
        f = open('options.json','w')
        json.dump(self.var,f)
        f.close
        
    def restore(self):
        self.var = self.var_default
    
    def setShuffleMode(self,state):
        if state:
            self.var['shufflemode'] = 0
        else:
            self.var['shufflemode'] = 1
    
    def setRdmFlip(self,state):
        if state:
            self.var['rdmflip'] = 1
        else:
            self.var['rdmflip'] =0

#Prompt user to select source file & extract lines from source file

 ## still using the native tk file dialog from version 1. Should be changed in near future
tk.Tk().withdraw()  
filename = askopenfilename()
ext = os.path.splitext(filename)[1]

global opt
opt = options() # initialize an option object
opt.load()

if ext == '.txt':
    file = open(filename, 'r',encoding = 'utf-8')
    lines = file.readlines()
    all_cards = list()
    ID = 0
    # generating deck
    for l in lines:
        if l.find('\t') > 0:
            a = l.find('\t') 
            b = a +1
        front = l[0:a] 
        front = front.replace('\\n',opt.var['kwrd_newline'])
        
        back = l[b:]
        back = back.replace('\\n',opt.var['kwrd_newline'])
        
        all_cards.append(card(front,back,ID))
        ID = ID +1
        dk = deck(filename,all_cards)
elif ext == '.dk':
    file = open(filename,'rb')
    dk = pickle.load(file)
    
file.close()
# Hight resolution support....not sure how this work...
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
# end of high resolution suppport
#Entering Mainloop
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = mainWindow(dk)
sys.exit(app.exec_())
