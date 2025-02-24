# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 13:04:05 2025

@author: martin
"""


from tkinter import * 
from tkinter import messagebox

from gamecontroller import GameController
from gamemodel import GameModel, Human, Player
from gamemodel import AI
from gameview import GameView 

class App(Tk):
    def __init__(self, mainTitle, size):
        super().__init__()      
        self.minsize(*size)
        self.resizable(True,True) 
        self.title(mainTitle)
class MainFrame(Frame):
    def __init__(self, container):
        super().__init__(container)
        options = {"pady":10}
        self.label = Label(self, text="Entrez votre nom: ")
        self.label.pack(**options)           # place le label dans la fenètre principale
        self.name_entry = Entry(self)
        self.name_entry.pack(**options)
        self.sayHelloButton = Button(self,text= "Dire Bonjour", command= self.play_matches_game(Human(self.name_entry),AI("Bot")))
        self.sayHelloButton.pack(**options)
        self.pack()
    def play_matches_game(self, player1, player2):    
        controller = GameController(player1, player2, 6)
if __name__ == "__main__":
    player1 = Human("Jean")
    player2 = AI("Bot")
    #matches_game = GameController(player1, player2, 6)
    app = App("Game Selection", [600, 300])
    #frame = MainFrame(app)
    #app.mainloop()
    

        