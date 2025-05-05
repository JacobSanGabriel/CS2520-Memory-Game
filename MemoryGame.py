import tkinter as tk
from tkmacosx import Button # support button colors on MacOS
import random
import time
from threading import Thread

def main():
    # Create/setup Tkinter
    root = tk.Tk()
    root.title("Memory Game")
    root.geometry('500x500') # Dimensions

    # Game settings
    COLORS = ["red", "blue", "green", "yellow"]
    
    # Message display
    status = tk.Label(root, text="Press Start to Begin", font=("Arial", 16))
    status.pack(pady=10)

    # Create buttons
    frame = tk.Frame(root)
    frame.pack()

    buttons = {} # Color buttons
    for i, color in enumerate(COLORS):
        button = Button(frame, bd=0, bg=color, width=130, height=130, focuscolor='')
        button.grid(row=i//2, column=i%2, padx=3, pady=3)
        buttons[color] = button

    start = Button(root, text="Start", height=40, focuscolor='') # Start button
    start.pack(pady=20)

    # Keep window running
    root.mainloop()

if __name__ == "__main__":
    main()