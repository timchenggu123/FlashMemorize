import tkinter as tk
import random as rd
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
    
class deck:
    def __init__(self,name,cards = [],):
        self.cards = cards
        self.order = list(range(len(cards)))
        self.name = name
        
    def shuffle(self,allCards = 1):
        self.order = list(range(len(self.cards)))
        if allCards:
            rd.shuffle(self.order)
        else:
            for i in self.order:
                self.order[i] = rd.randrange(0,len(self.order))
                
    def getdeck(self):
        dk = list()
        for i in self.order:
            dk.append(self.cards[i])
        
        return dk
        
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



    
            
    
