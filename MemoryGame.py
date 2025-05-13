import tkinter as tk
from tkmacosx import Button #support button colors on MacOS
import random
import time
from threading import Thread
import sounddevice as sd
import soundfile as sf


class MemoryGame:
    def __init__(self,root):
        
        self.root=root
        self.root.title("Memory Game")
        self.root.geometry('500x500') #Dimensions
        
        self.COLORS = ["red", "blue", "green", "yellow"]
        self.sequence=[] #Default colors game shows
        self.playerSequence=[] #Will track the colors the player clicks
        self.level = 0  #Will track game levels
        self.gamePlaying = False #By default game is not running till we click start
        self.inSequence = False
        self.messages = [ "Correct! Well done!",
                         "That's right! Keep it up!",
                         "Nice job!",
                         "Exactly!",
                         "Yup! That’s right ",
                         "So smart!",
                         "Doing great!"
        ]
        self.sound = ['c6.mp3', 'f6.mp3', 'b6.mp3', 'g6.mp3', 'incorrect.mp3']

        #Top Status for Press Start
        self.ScreenStatus = tk.Label(root, text="Press Start to Begin", font=("Arial", 16))
        self.ScreenStatus.pack(pady=10)

        #Need Frames which have previously been defined
        self.frame = tk.Frame(root)
        self.frame.pack()
        self.buttons = {} # Color buttons dictionary
           
            #Create colored buttons for the button in the list
        for x, color in enumerate(self.COLORS):
            button = Button(
                self.frame,text="", bg=color,  height=130, width=130,
                bd=0,  
                focuscolor='',  
                command=lambda c=color: self.click(c) 
            )
            
            #Layout for 4 buttons
            button.grid(row=x//2,column=x%2,padx=5,pady=5)
            #Store button
            self.buttons[color] = button

        #Start button for color buttons
        self.startButton = Button(root, text="Start", height=40, focuscolor='', command=self.gameStart) 
        self.startButton.pack(pady=20)

    def gameStart(self):
        
        #Make sure they are empty before game starts
        self.sequence.clear() 
        self.playerSequence.clear() 
        self.level = 0 
        
        #Game will finally start
        self.gamePlaying=True 
       
        #Disable start button 
        self.startButton.pack_forget()
        self.startButton.config(state=tk.DISABLED)
        self.nextRound()
        
    def nextRound(self):
        self.level+=1 #Go up a level
        self.ScreenStatus.config(text=f"Level: {self.level}")
        self.playerSequence =[] #Clear Again
        self.sequence.append(random.choice(self.COLORS)) #Add new color to sequence
        
        #Will call white for the sequence
        Thread(target=self.whiteSequence).start()
    
    def playSound(self, color):
        if color == self.COLORS[0]:#Check red
            data, samplerate = sf.read("Sounds\\c6.mp3")
        elif color == self.COLORS[1]:#Check blue
            data, samplerate = sf.read("Sounds\\f6.mp3")
        elif color == self.COLORS[2]:#Check green
            data, samplerate = sf.read("Sounds\\g6.mp3")
        elif color == self.COLORS[3]:#Check yellow
            data, samplerate = sf.read("Sounds\\b6.mp3")
        else: data, samplerate = sf.read("Sounds\\incorrect.mp3")
        sd.play(data, samplerate)

    def whiteSequence(self):
        self.ScreenStatus.config(text="Memorize The Pattern")
        time.sleep(1) #Delay before we change the color
        for color in self.sequence:
            self.playSound(color)

            #Change the buttons to white
            self.buttons[color].configure(bg="white") 
            self.root.update()
            time.sleep(.5) #it will be white for .5 secs
            
            #Revert the buttons color
            self.buttons[color].configure(bg=color)
            self.root.update() 
           
            time.sleep(.3) #pause before next color change
        self.ScreenStatus.config(text=f"Level: {self.level}")
        self.inSequence = False #Let player click

    def click(self, color):
        
        if not self.gamePlaying:
            self.playSound(color)
            #If game isnt playing then return
            return
        
        if self.inSequence:
            #If inSequence return
            return
        
        #otherwise
        self.playerSequence.append(color)
        if self.playerSequence == self.sequence[:len(self.playerSequence)]:
            #Play Sound
            self.playSound(color)

            #Checking if player is correct
            self.ScreenStatus.config(text=self.messages[len(self.playerSequence)%7])
            
            #Next round if completed
            if len(self.playerSequence) == len(self.sequence):
                self.inSequence = True #Prevent player from clicking
                self.root.after(1000, self.nextRound)
        else:
            self.playSound("")
            #if player is not correct then game is over
            self.ScreenStatus.config(text="Wrong! Game Over.")
           
            #set game to over
            self.gamePlaying = False
           
            #Resetting start button
            self.startButton.config(state=tk.NORMAL)
            self.startButton.pack()
            
            #Set sequence to clear again
            self.sequence.clear()
            
            #Reset level to 0
            self.level = 0


def main():

    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()

main()
