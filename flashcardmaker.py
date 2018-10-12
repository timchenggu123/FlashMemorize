# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 09:31:26 2018

@author: TimGU
"""

# initializing program
import tkinter as tk
import random as rd
from tkinter.filedialog import askopenfilename

# initalize global variables
nm = 0 #holds the number of card
currentside = 0 #holds the current state of each card. 

#Prompt user to select source file & extract lines from source file
tk.Tk().withdraw()  
filename = askopenfilename()
file = open(filename, 'r')
lines = file.readlines() 

#Initializing deck
def shuffledeck():
    global deck
    ncards = len(lines)
    deck = list(range(ncards))
    #rdnm = 999
    #for i in lines:
    #    temp = rdnm
    #    rdnm = rd.randrange(0,ncards)
    #    while rdnm ==temp:
    #        rdnm = rd.randrange(0,ncards)
    #        
    #    deck.append(rdnm)
    #n = deck[nm]
    rd.shuffle(deck)
    nm = 0 
    currentside = 0
    
shuffledeck()
n = deck[nm]

#Constructing functions
def card(n,side = rd.randrange(0,2)):
    global currentside
    currentside = side
    l = lines[n]
    if l.find('    ') > 0:
        a = l.find('    ') 
        b = l.find('    ') +4
    front = l[0:a]
    back = l[b:]

    if side ==1:
        return front
    else:
        return back

def Disp(n,currentside = []):
    T1.delete(1.0,tk.END)
    T1.insert(tk.END, card(n))

def nextcard():
    global nm, n
    nm = nm + 1
    if nm == ncards:
        nm = 1
    n = deck[nm]
    Disp(n)
    return

def previouscard():
    global nm,n
    nm = nm -1
    if nm ==0:
        nm = ncards
    n = deck[nm]
    Disp[n]
    
def flip():
    global currentside
    currentside = abs(currentside-1)
    T1.delete(1.0,tk.END)
    T1.insert(tk.END, card(n,currentside))
    return

#Constructing Gui
top = tk.Tk()

T1 = tk.Text(top,height = 5, width = 30)
T1.insert(tk.END, card(n))
T1.pack()
    
fm = tk.Frame(top)
fm.pack(side=tk.LEFT)

btn1 = tk.Button(fm, text="Previous",command = previouscard)
btn1.pack(side=tk.LEFT)
btn2 = tk.Button(fm,text = "Flip",command = flip)
btn2.pack(side=tk.LEFT)
btn3 = tk.Button(fm,text = "Next",command = nextcard)
btn3.pack(side=tk.LEFT)
btn4 = tk.Button(fm,text = 'Shuffle',command = shuffledeck)
btn4.pack(side=tk.LEFT)

fm1 = tk.Frame(top)
fm1.pack(side = tk.LEFT)
T2 = tk.Text(fm1,height = 1, width = 12)
T2.insert(tk.END,'STAT:')

top.mainloop()
