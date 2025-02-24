# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 17:22:00 2025

@author: marti
"""
from gamemodel import GameModel, Human, Player
from gamemodel import AI
from gameview import GameView
from gamecontroller import GameController

import random
from tkinter import *
from tkinter import messagebox
import tkinter as tk


class App(Tk):
    """
    Objet qui sert de template pour le canvas
    
    hérite de:
        - tkinter (Tkinter)
    paramètres:
        - titre de la fenêtre (STRING)
        - taille de la fenêtre (float2)
    arguments:
        - taille minimale, égale à la taille de la fenêtre en paramètre (float2)
        - possibilité de redimentionner la fenêtre (vrai pour x et y par défaut)(BOOL,BOOL)
        - titre de la fenêtre, égal à celui inséré en paramètre (float2)
        - 
    """
    def __init__(self, mainTitle, size):
        super().__init__()      
        self.minsize(*size)
        self.resizable(True,True) 
        self.title(mainTitle)
class MainFrame(Frame):
    """
    Objet de sélection du jeu
    
    hérite de:
        - Frame, qui est un widget de tkinter (tkinter)
    paramètre:
        - template du canvas
    arguments:
        - texte principal de l'image (STR)
        - cadre contenant les bouttons de sélection des jeux (Widget)
        - les 3 bouttons redirigeant vers les 3 jeux (Widget)
    Tous les widgets sont aussi affichés
    
    """
    def __init__(self, container):
        super().__init__(container)
        options = {"pady":10}
        self.label = Label(self, text="Choisissez le jeu: ")
        self.label.pack(**options)
        self.play_buttons_frame = tk.Frame(self) 
        self.play_buttons_frame.pack()
        for i in range(1, 4):
            btn = tk.Button(self.buttons_frame, text=f"Jeu {i}", command=lambda n=i: self.set_controller(n))  
            btn.pack(side=tk.LEFT) 
        self.pack()
    def set_controller(self, choice):
        """
        Lance le jeu en fonction du boutton choisi
        paramètre:
            - choix du joueur (1 à 3)(INT)
        """
        if(choice == 1):
            controller = GameController(player1, player2, 6)
        elif(choice == 2):
         #lancer cubee
             print()
        else:
         #lancer les voitures
             print()
        
if __name__ == "__main__":
    player1 = Human("Jean")
    player2 = AI("Bot")
    app = App("Sélection de jeux", [300, 50])
    frame = MainFrame(app)
    app.mainloop()