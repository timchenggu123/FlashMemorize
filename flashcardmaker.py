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
nm = 0
side = 0

#Prompt user to select source file & extract lines from source file
tk.Tk().withdraw()  
filename = askopenfilename()
file = open(filename, 'r')
lines = file.readlines() 
    
#Constructing functions
def card(nm,side = rd.randrange(0,1)):
    global currentside
    currentside = side
    l = lines[nm]
    if l.find('    ') > 0:
        a = l.find('    ') 
        b = l.find('    ') +4
    front = l[0:a]
    back = l[b:]

    if side ==1:
        return front
    else:
        return back

def Disp(nm,currentside = []):
    T1.delete(1.0,tk.END)
    T1.insert(tk.END, card(nm))

def nextcard():
    global nm
    nm = nm + 1
    Disp(nm)
    return

def flip():
    global currentside
    currentside = abs(currentside-1)
    T1.delete(1.0,tk.END)
    T1.insert(tk.END, card(nm,currentside))
    return

#Constructing Gui
top = tk.Tk()

T1 = tk.Text(top,height = 5, width = 30)
T1.insert(tk.END, card(nm))
T1.pack()
    
fm = tk.Frame(top)
fm.pack()

btn1 = tk.Button(fm, text="Previous")
btn1.pack(side=tk.LEFT)
btn2 = tk.Button(fm,text = "Flip",command = flip)
btn2.pack(side=tk.LEFT)
btn3 = tk.Button(fm,text = "Next",command = nextcard)
btn3.pack(side=tk.LEFT)



top.mainloop()
