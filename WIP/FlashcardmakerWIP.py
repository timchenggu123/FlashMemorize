import random as rd
import sys
import pickle
import os.path
import json
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QMainWindow,QFrame, QFileDialog, QAction, QMenu, 
QMessageBox, QLineEdit)
from PyQt5.QtCore import pyqtSlot, QByteArray, QIODevice,QDataStream
from PyQt5.QtGui import QIcon,QFont, QPixmap

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
        self.studyTrend = []
        
        self.front_pic_exist = 0
        self.back_pic_exist = 0
        self.pic_exist = 0
        
        self.addPic(front,back)
        
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
    def getStudyTrend(self):
        total = 0
        trend = []
        for i in range(len(self.studyTrend)):
            total = total + self.studyTrend[i]
            accuracy = total/(i+1)
            trend.append(accuracy)
        return 
    
    def editCard(self,text):
        if self.side == 1:
            self.front = text
            self.addPic(text,'') #empyt string here because we are not editing the back right now
        else:
            self.back = text 
            self.addPic('',text) #empyt string here because we are not editing the front right now
        
        
    def addPic(self,front,back):
        self.front_pic_exist = 0
        self.back_pic_exist = 0
        self.front_pic = QByteArray()
        self.back_pic = QByteArray()
        
        if front.find(opt.var['kwrd_image'][0]) > -1:#Basically if the card contains a image, add the image
            a = front.find(opt.var['kwrd_image'][0])
            b = front.find(opt.var['kwrd_image'][1])
            file = front[a+1:b]
            
            if os.path.exists(file):
                #QPixmap does not support pickling, so we convert it to a data stream here
                pic = QPixmap(file)
                stream = QDataStream(self.front_pic,QIODevice.WriteOnly)
                stream << pic
                self.front_pic_exist = 1
                
        
        if back.find(opt.var['kwrd_image'][0]) > -1:#Basically if the card contains a image, add the image
            a = back.find(opt.var['kwrd_image'][0])
            b = back.find(opt.var['kwrd_image'][1])
            file = back[a+1:b]
            
            if os.path.exists(file):
                #QPixmap does not support pickling, so we convert it to a data stream here
                pic = QPixmap(file)
                stream = QDataStream(self.back_pic,QIODevice.WriteOnly)
                stream << pic
                self.back_pic_exist = 1
            
            
        self.pic_exist = self.front_pic_exist + self.back_pic_exist
        
    def showPic(self):
        if self.side == 1:
            if self.front_pic_exist:
                #for pickling purposes the data is stored as a QDataStream object. We are 
                #converting it back to QPixmap
                pic = QPixmap()
                stream = QDataStream(self.front_pic,QIODevice.ReadOnly)
                stream >> pic
                return  pic
        elif self.side == 0:
            if self.back_pic_exist:
                #for pickling purposes the data is stored as a QDataStream object. We are 
                #converting it back to QPixmap
                pic = QPixmap()
                stream = QDataStream(self.back_pic,QIODevice.ReadOnly)
                stream >> pic
                return pic
    
class deck:
# The deck class' main purpose is to hold and manage a list of card objects
    def __init__(self,name = 'default',cards = [],):
    # name<string/int>: a unique name for the deck
    # cards<list>: a list containing card objects
        if not cards:
            self.cards = [card('Welcome to FlashCardmaker -To start, use load file from file menu -(*.txt *.dk)',
                               'Welcome to FlashCardmaker -To start, use load file from file menu -(*.txt *.dk)',0)]
            #print('123')
        else:
            self.cards = cards
        self.subDeck = list()
        self.size = len(self.cards)
        self.order = list(range(len(self.cards))) # A list containing the order by which the cards are sorted
        self.name = name
        self.ver = opt.ver #store the current program version for compatibility purposes
        
    def shuffle(self,mode = 1,rndFlip = 0,reset = 0, draw = 0):
    #Shuffle the deck. AllCards = 1 shuffle a deck of ncards with every card included exactly once. All cards
    #having any other value will result in the deck shuffling cards based on the accuracy of each card. Draw = 1 
    #returns one random card based on the card accuracy, but only work if allCards is set to 0
    
    #allCards<int/logical> [0,1]: 1 then the deck is shuffled such that all cards are included at least once
    #rndFlip<int> [0,1,2]: 0: all cards facing front; 1: all cards randomly flipped; 2: all cards facing back
    #set reset = 1 to reset deck in order with all cards facing front
        self.order = list(range(len(self.cards)))
        if reset == 0:
            if mode == 1:
                rd.shuffle(self.order)
            else:
                #The random shuffling algorithm utilizes a wighted random algorithm. An anology is that we create
                # a 'pool' that is divided into zones of different sizes. Each zone represent a card in the deck. The
                #size of each zone is inversely proportional to the accuracy of the card. We then randomly 'toss a coin'
                #into the pool and see where it lands. The coin is more likely to land in a zone with a larger area, and 
                #thus we have created a weighted random algorithm. It is worth noticing that the size of each zone
                #is adjusted by an arbitary factor related to the times which the card has been studied. 
                
                ncards = len(self.order)
                self.order2 = list() #creating an empty vector to hold the new deck order temporarily
                accuracy = list()
                pool = list()
                
                for card in range(ncards):
                    accuracy.append(self.cards[card].getStats())
                temp = 0
                ##print(accuracy)
                card = -1
                for a in accuracy: #This for loop adjusts accuracy by an arbitrary factor then creates a pool based on the accuracy
                    if a == 0:
                        a = 0.01 #We don't want an infinitely large weight on cards with a 0 accuracy. Therefore, we hard set it to 0.01
                    a = 1/a
                    card = card + 1
                    coeff = self.cards[card].timesStudied  # An arbitrary coefficent for probability of a e.g. probability of a is coeff * (1/a)/ncards. In this case, the coeff is based on the total times the card is studied
                    if coeff == 0 :
                        coeff = 0.1 #Same logic there, if the card has not been studied at all, we set it 0,1
                    else:
                        coeff = coeff * 0.1
                    a = a * coeff #adjusting the size of the zone by the coefficient which is based on the times the card has been studied
                    a = a + temp
                    temp = a
                    pool.append(int(a*100)) #the 100 just allows us to have a more precise intepretation of the accuracy. 
                ##print(pool)
                temp = -1
                for i in range(ncards):
                    proceed = 0 #The proceed controls where the randomly selected card satisfy our requirements, which in this case is whether it is the exact same card
                                #as the previous card drew. 
                    while proceed == 0:
                        toss = rd.randrange(0,pool[len(pool)-1]) #the toss is a random number between zero and the last and largest number in the pool
                        ##print(toss)
                        nth = -1
                        for zone in pool:
                            nth = nth +1
                            if toss < zone: #since the pool is monotonic and increasing, we can locate our toss this way
                                if temp == nth:
                                    break
                                self.order2.append(nth)
                                temp = nth
                                proceed = 1
                                break
                    if mode == 2 :
                        self.order = list()
                        self.order.append(nth)
                        try:
                            if self.global_temp == nth:
                                self.shuffle(mode,rndFlip,reset,draw)
                            else:
                                self.global_temp = nth
                        except:
                            self.global_temp = nth
                        break
                    
                    self.order = self.order2
                
                
            if rndFlip == 0:
                for i in self.cards:
                    i.side = 1
            elif rndFlip == 1:
                for i in self.cards:
                    i.flip(0)
            else:
                for i in self.cards:
                    i.side = 0
        else:
            for i in self.cards:
                    i.side = 1
                    
        
    def append(self,cards):
        # Add a new card to the bottom of the deck and restore order. Call this method instead of directly modifying self.cards.
        # card: a list of card objects to be appended
        try:
            for card in cards:
                card.id = len(self.cards)
                self.cards.append(card)
        except:
            cards.id = len(self.cards)
            self.cards.append(cards)
        
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
            order = self.order
            order.sort()
            temp = -1
            handsize = 0
            for i in order:
                if i != temp:
                    temp = i
                    handsize = handsize +1
                    
            return handsize
            
    def deleteCard(self,cardID):
        del self.cards[cardID]
        #re-assignming ids to cards in deck
        ID = 0
        
        index = 0
        for i in self.order: #first, delete the target cardID from self.order
            if i == cardID:
                del self.order[index]
                break
            index = index + 1
            
        index = 0
        for i in self.order: #second, minus one to all card IDs larger than the traget cardID since all of them got shifted one forward
            if i > cardID:
                self.order[index] = i - 1 
            index = index + 1
            
        for card in self.cards:
            card.id = ID
            ID = ID + 1
            
        self.size = len(self.order)
        
        
        
class mainProgram(QWidget):
    # this is the main widget to be displayed in the main window
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
        self.canvas.setGeometry(30,30,700,350)
        self.canvas.setFrameStyle(QFrame.Panel)
        self.canvas.setWordWrap(True)
        font = QFont('Arial',12)
        self.canvas.setFont(font)
        self.canvas.setStyleSheet('QLabel {background-color : white}')
        
        self.edit = QLineEdit('',self)
        self.edit.setGeometry(30,30,700,350)
        self.edit.setFont(font)
        self.edit.hide()
        
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
        
        
    def resizeEvent(self,event):
        self.canvas.resize(self.width()-50, self.height()-80)
        self.edit.resize(self.width()-50,self.height()-80)
    def readCard(self,i):
    #Return the text on the current side of card[i]
    # i <int> the ith card in the deck
        return(self.cards[i].show()) 
    
    def showCard(self):
    #Display the text on canvas
        text = self.readCard(self.i)
        text = text.replace(opt.var['kwrd_newline'],'<br>')
        pic = self.cards[self.i].showPic()
        if pic:
            pic = self.cards[self.i].showPic()
            self.canvas.setPixmap(pic.scaled(self.canvas.width() -20,self.canvas.height() -20,QtCore.Qt.KeepAspectRatio))
        else:
            self.canvas.setText(text) 
        
        self.canvas.setToolTip(text)
        self.edit.hide()
        self.canvas.show()
        self.dispID.setText('CardID:' + str(self.cards[self.i].id))
       
    @pyqtSlot()
    def editCard(self):
        text = self.readCard(self.i)
        
        self.canvas.hide()
        self.edit.show()
        self.edit.setText(text) 
        self.edit.setFocus()
        self.edit.returnPressed.connect(self.updateCardText)
                
        self.dispID.setText('CardID:' + str(self.cards[self.i].id))
        
    @pyqtSlot()
    def updateCardText(self):
        #to be called by editCard() method
        text = self.edit.text()

        self.dk.cards[self.cards[self.i].id].editCard(text)
        self.edit.hide()
        self.showCard()
        
    def moveCard(self,step,updateStats = 1):
        if updateStats:
            self.updateStats()
#            currentId = self.cards[self.i].id
#            self.dk.cards[currentId].viewed = 1
        if opt.var['shufflemode'] == 2:
            self.i = 0
            self.dk.shuffle(opt.var['shufflemode'],opt.var['rdmflip'])
            self.cards = self.dk.getdeck()
        else:
            ncards = self.dk.size
            self.i = self.i + step
            if self.i == ncards:
                self.i = 0
            elif self.i < 0:
                self.i = self.dk.size - 1
            
            
        self.updateStats(0) #the 0 here refreshes the stats bar without changing card stats
        
    
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
        if self.i == self.dk.size: #to guard against index going out of range
            self.i = self.i -1
            
        currentId= self.cards[self.i].id    
        if updateCards:
                self.dk.cards[currentId].timesStudied = self.dk.cards[currentId].timesStudied + 1
                self.dk.cards[currentId].timesCorrect = self.dk.cards[currentId].timesCorrect + self.correct
                self.dk.cards[currentId].studyTrend.append(self.correct)
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
            for c in range(len(self.dk.cards)): #loop through all the cards in the deck
                blankcard = card('','',0) #Initiates a new instance of card
                for x in vars(self.dk.cards[c]): #loop through all attributes of the new instance and set them to be the same as the card in the deck to be loaded
                    setattr(blankcard,x,getattr(self.dk.cards[c],x))
                self.dk.cards[c] = blankcard #replace old instance with new instance
        #self.dk = deck
        self.i = 0
        self.updateStats(0)
        self.showCard()
        
    def resetViewed(self,deck):
        self.dk.resetViewed()
        self.updateStats(0)
        
    
    @pyqtSlot()
    def resetOrder(self):
        self.dk.shuffle(reset = 1)
        self.cards = self.dk.getdeck()
        self.dk.resetViewed()
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
        
        mSave = QAction(QIcon(), '&Save File',self)
        mSave.setShortcut('Ctrl+S')
        mSave.setStatusTip('Save current deck')
        mSave.triggered.connect(self.saveToFile)
        
        mLoad = QAction(QIcon(),'&Load File',self)
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
        mAllowRepeat.setChecked(opt.var['shufflemode'] == 0) #set initial state of checked depending on option setting
        
        mAllowRepeat.triggered.connect(lambda: mActiveShuffle.setChecked(False))
        mAllowRepeat.triggered.connect(opt.setShuffleMode)
        mActiveShuffle = QAction('Active Shuffle',self,checkable = True)
        mActiveShuffle.setChecked(opt.var['shufflemode'] == 2) #set initial state of checked depneding on option setting
        mActiveShuffle.triggered.connect(lambda: mAllowRepeat.setChecked(False))
        mActiveShuffle.triggered.connect(opt.setShuffleMode2)

        mRdmFlip = QAction('Allow Random Flips',self,checkable = True)
        mRdmFlip.setChecked(opt.var['rdmflip'] == 1)
        mRdmFlip.triggered.connect(opt.setRdmFlip)
        mShuffleMode.addAction(mAllowRepeat)
        mShuffleMode.addAction(mActiveShuffle)
        mShuffleMode.addAction(mRdmFlip)
        
        mResetDeckOrder = QAction('&Reset Deck Order', self)
        mResetDeckOrder.triggered.connect(self.mp.resetOrder)
        
        optMenu.addMenu(mShuffleMode)
        optMenu.addAction(mResetDeckOrder)

        ## Manage Menu
        manMenu = menubar.addMenu('&Manage')
        
        mResetViewed = QAction('Reset Viewed Cards', self)
        mResetViewed.triggered.connect(self.mp.resetViewed)
        
        mExpandDeck = QAction('Expand Deck',self)
        mExpandDeck.setToolTip('Expand current deck with another deck')
        mExpandDeck.triggered.connect(self.expandDeck)
        
        mEditCard = QAction('Edit Current Card',self)
        mEditCard.triggered.connect(self.mp.editCard)
        
        mNewBlank = QAction('Add a New Blank Card',self)
        mNewBlank.triggered.connect(self.addNewCard)
        
        mDeleteCard = QAction('Delete Current Card',self)
        mDeleteCard.triggered.connect(self.deleteCard)
        
        manMenu.addAction(mDeleteCard)
        manMenu.addAction(mResetViewed)
        manMenu.addAction(mExpandDeck)
        manMenu.addAction(mEditCard)
        manMenu.addAction(mNewBlank)
        
        self.statusBar().showMessage('Ready')
        
        self.setGeometry(300, 300, 750,500)
        self.setWindowTitle('FlashCardMaker')
        self.show()
        
        
    def resizeEvent(self,event):
        self.mp.resize(self.width(),self.height())
        
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
        
        pwd = os.curdir
        os.chdir(os.path.dirname(f))
        
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
        os.chdir(pwd)

    @pyqtSlot()
    def expandDeck(self):
        f,_ = QFileDialog.getOpenFileName(filter = 'Flash Card Files (*.txt *.dk)')
        
        pwd = os.curdir #change current directory to the deck directory for easy access to picture files
        os.chdir(os.path.dirname(f))
        
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
        self.mp.shuffle(initialize = 1) ##initialzizing the modified new deck
        file.close()
        
        os.chdir(pwd)
        
    @pyqtSlot()
    def addNewCard(self):
        newcard = card('','',0)
        self.mp.dk.append(newcard)
        self.mp.shuffle(initialize = 1)
        self.mp.i = self.mp.dk.size -1
        self.mp.showCard()

    @pyqtSlot()
    def deleteCard(self):
        currentCardID = self.mp.cards[self.mp.i].id
        self.mp.dk.deleteCard(currentCardID)
        self.mp.shuffle(initialize = 1)
             
class options:
    def __init__(self):
        self.var_default = {
            'kwrd_side': '\t', #keyword separating the front and back side of a card
            'kwrd_newline' : ' -', #keyword initating a newline on a card
            'shufflemode' : 1, #shuffle mode
            'rdmflip' : 0,  #enable random flip in shuffle mode
            'kwrd_image': '{}' #The characters that shall contains the file address for images to be displayed on cards. Need to be at least two characters long. See showCard() method under mainProgram() class for details
            }
        self.var = self.var_default
        self.ver = '2.6.0'
    
    def load(self): # slot for the file menu
        
        try:
            f = open('options.json','r')
            var = json.load(f)
            for v in var:
                self.var[v] = var[v]
            f.close()
        except:
            self.save()
            self.load()
        
    def save(self): #slot for the file muenu
        f = open('options.json','w')
        json.dump(self.var,f)
        f.close
        
    def restore(self): #slot for the optio menu
        self.var = self.var_default
    
    def setShuffleMode(self,state): #slot for the option menu
        #Set not random shuffle
        if state:
            self.var['shufflemode'] = 0
        else:
            self.var['shufflemode'] = 1
            
    def setShuffleMode2(self,state):
        #Set ActiveShuffle
        if state:
            self.var['shufflemode'] = 2
        else:
            self.var['shufflemode'] = 1
            
    def setRdmFlip(self,state): #slot for the option menu
        if state:
            self.var['rdmflip'] = 1
        else:
            self.var['rdmflip'] =0
            
    
       
#initializing function, creating first instances
opt = options() # initialize an option object
opt.load()
dk = deck()

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
