import tkinter as tk
from tkmacosx import Button #support button colors on MacOS
import random
import time
from threading import Thread
import sounddevice as sd
import soundfile as sf
from datetime import datetime


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

        #section to be able to set game difficulty
        self.flash_duration = 0.5  # default (medium)
        self.pause_duration = 0.3

        #Difficulty selection screen options
        self.difficulty_frame = tk.Frame(root)
        self.difficulty_label = tk.Label(self.difficulty_frame, text="Select Difficulty", font=("Arial", 16))
        self.difficulty_label.pack(pady=10)

        Button(self.difficulty_frame, text="Easy", width=130, height=40, command=lambda: self.setDifficulty("easy")).pack(pady=5)
        Button(self.difficulty_frame, text="Medium", width=130, height=40, command=lambda: self.setDifficulty("medium")).pack(pady=5)
        Button(self.difficulty_frame, text="Hard", width=130, height=40, command=lambda: self.setDifficulty("hard")).pack(pady=5)

        self.difficulty_frame.pack(pady=100)

        self.messages = [ "Correct! Well done!",
                         "That's right! Keep it up!",
                         "Nice job!",
                         "Exactly!",
                         "Yup! That’s right ",
                         "So smart!",
                         "Doing great!"
        ]
        self.sound = ['c6.mp3', 'f6.mp3', 'b6.mp3', 'g6.mp3', 'incorrect.mp3']

        #MAIN GAME UI
        self.main_frame = tk.Frame(root)
        self.main_frame.pack_forget()  # Hide initially until difficulty is selected

        #Top Status for Press Start
        self.ScreenStatus = tk.Label(self.main_frame, text="Press Start to Begin", font=("Arial", 16))
        self.ScreenStatus.pack(pady=10)

        #Used for logging info thats put into output.txt
        self.difficulty = "Medium"  #default but gets overwritten
        self.session_data = []
        self.level_start_time = None #time when the level starts 

        #Need Frames which have previously been defined
        self.frame = tk.Frame(self.main_frame)
        self.frame.pack_forget()
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

        #Start button for color buttons hidden until difficulty is selected
        self.startButton = Button(self.main_frame, text="Start", height=40, focuscolor='', command=self.gameStart)
        self.startButton.pack_forget()

        #GAME OVER STAT SCREEN variables
        self.stat_frame = tk.Frame(self.root)
        self.stat_label = tk.Label(self.stat_frame, text="", font=("Arial", 16))
        self.stat_label.pack(pady=10)

        Button(self.stat_frame, text="Try Again", width=130, height=40, command=self.retrySameDifficulty).pack(pady=5)
        Button(self.stat_frame, text="Change Difficulty", width=130, height=40, command=self.changeDifficulty).pack(pady=5)
        Button(self.stat_frame, text="Quit", width=130, height=40, command=self.root.quit).pack(pady=5)

        self.stat_frame.pack_forget()  #Hide it by default by default until game is over


    def gameStart(self):
        #store the data from the game and reset it every new game
        self.session_data = []
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
        self.level_start_time = time.time()
        
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
            time.sleep(self.flash_duration)
            
            #Revert the buttons color
            self.buttons[color].configure(bg=color)
            self.root.update() 
           
            time.sleep(self.pause_duration) #pause before next color change
        self.ScreenStatus.config(text=f"Level: {self.level}")
        self.inSequence = False #Let player click

        
    def setDifficulty(self, level):
        self.difficulty = level.capitalize() 

        #updating game speed based on the difficulty that was chosen
        if level == "easy":
            self.flash_duration = 0.9
            self.pause_duration = 0.6
        elif level == "medium":
            self.flash_duration = 0.5
            self.pause_duration = 0.3
        elif level == "hard":
            self.flash_duration = 0.1
            self.pause_duration = 0.1

        #hide the difficulty screen and go back to the gameUI
        self.difficulty_frame.pack_forget()
        self.main_frame.pack() 
        self.ScreenStatus.config(text="Press Start to Begin")
        self.frame.pack()
        self.startButton.config(state=tk.NORMAL) #reset the start button state
        self.startButton.pack(pady=20)


    def retrySameDifficulty(self):
        self.stat_frame.pack_forget()
        self.main_frame.pack()
        self.gameStart()

    def changeDifficulty(self):
        self.stat_frame.pack_forget()
        self.difficulty_frame.pack(pady=100)

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
                #lpg the levels that weere completed
                duration = round(time.time() - self.level_start_time, 2)
                self.session_data.append({
                    "level": self.level,
                    "time": duration,
                    "sequence": self.sequence[:],
                    "player_input": self.playerSequence[:]
                })
                self.inSequence = True
                self.root.after(1000, self.nextRound)
        else:
            self.playSound("")
            #if player is not correct then game is over
            self.ScreenStatus.config(text="Wrong! Game Over.")
            duration = round(time.time() - self.level_start_time, 2)
            #add the failed level to the output.txt also
            self.session_data.append({
                "level": self.level,
                "time": duration,
                "sequence": self.sequence[:],
                "player_input": self.playerSequence[:] 
            })
            self.writeSessionLog()#save to the output file
           
            #set game to over
            self.gamePlaying = False
           
            #Resetting start button
            # Hide game UI
            self.main_frame.pack_forget()

            # Show stat screen
            self.stat_label.config(text=f"Game Over! You reached level {self.level}")
            self.stat_frame.pack(pady=100)
            
            #Set sequence to clear again
            self.sequence.clear()
            
            #Reset level to 0
            self.level = 0

    #writing the stored variables to the output.txt
    def writeSessionLog(self):
        filepath = "output.txt"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filepath, "a") as f:
            f.write(f"\nGAME SESSION ({now}):\n")
            f.write(f"Difficulty: {self.difficulty}\n")
            for entry in self.session_data:
                f.write(f"Level {entry['level']}: {entry['time']} sec\n")
                f.write(f"  Sequence: {entry['sequence']}\n")
                f.write(f"  Player Input: {entry['player_input']}\n")
        

def main():
    #clear the output.txt file
    with open("output.txt", "w") as f:
        f.write("Memory Game Session Info\n")

    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()

main()
