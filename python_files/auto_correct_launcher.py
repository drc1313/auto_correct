import tkinter as tk
from tkinter import *
from word_finder import *
root = Tk()

textL = Label(root, text='Enter Text')
textL.grid(row=0,column=0,sticky=NW)
suggestL = Label(root, text='Suggestions:',justify=LEFT)
suggestL.grid(row=2,column=0,sticky=NW)
word_suggest_list=[]

#When spacebar is press this will put the word before it into the word_suggest function in word_finder
def click(key):
    input=str(repr(key.char))
    if input==repr(' '):
        line=entry.get()
        word_list=line.split()
        word=word_list[-1]
        word_suggest_list=word_suggest(word)
        new_text='Suggestions:'
        for word in word_suggest_list:
            new_text=new_text+'\n'+word
        suggestL.config(text=new_text,font=("Calibri",20))
        
entry = Entry(width=1000,font=("Calibri",20))
entry.grid(row=1,column=0,sticky=NW)
entry.bind("<Key>", click)
root.mainloop()