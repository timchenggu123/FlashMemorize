# initializing program
import tkinter as tk
from tkinter.filedialog import askopenfilename

#Prompt user to select source file & extract lines from source file
tk.Tk().withdraw()  
filename = askopenfilename()
file = open(filename, 'r')
lines = file.readlines() 

for l in lines:
    if l.find('    ') > 0:
        a = l.find('    ') 
        b = l.find('    ') + 4
    front = l[0:a]
    back = l[b:]
    
top = tk.Tk()
T1 = tk.Text(top,height = 5, width = 30)
T1.pack()
T1.insert(tk.END, front)

top.mainloop()
