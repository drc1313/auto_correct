import tkinter as tk
from tkinter import ttk

from tkinter import *
'''
#def auto_correct_gui(filename)
# Open sample text file
fin = open('auto_correct_text_file.txt', 'r')

# Create the application window
window = tk.Tk()

# Create the user interface
my_label = ttk.Label(window, text = 'Did you mean' + fin.readline() + '?')
my_label.grid(row=1, column=1)

# Start the GUI event loop
window.mainloop()
'''


root = Tk()
def retrieve_input():
	inputValue = textBox.get("1.0", "end-1c")
	#print(inputValue)

	# Open sample text file
	fin = open('auto_correct_text_file.txt', 'r')
	# Create the application window
	window = tk.Tk()
	# Create the user interface
	my_label = ttk.Label(window, text = 'Did you mean "' + fin.readline() + '" ?')
	my_label.grid(row=1, column=1)
	# Start the GUI event loop
	window.mainloop()

textBox = Text(root, height = 20, width = 100)
textBox.pack()
buttonCommit = Button(root, height = 1, width = 50, 
	text = "Check your spelling", command = lambda: retrieve_input())
#command = lambda: retrieve_input() >>> just means do this when
#					I press the button
buttonCommit.pack()

mainloop()