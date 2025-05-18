# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 17:22:00 2025

@author: martin
"""
import matches.gamemodel
from matches.gamemodel import GameModel, Human, Player
from matches.gamemodel import AI
from matches.gameview import GameView
from matches.gamecontroller import GameController

from cubee.gamemodel import CubeeGameModel, CubeeHuman, CubeeAI
from cubee.gameview import CubeeGameView
from cubee.gamecontroller import CubeeGameController


from pixel_kart.game_controller import GameManager
from pixel_kart.game_model import Game,Circuit, Kart

from pixel_kart.game_view import GameEditor, GameInterface
import random
from tkinter import *
import tkinter as tk



class App(tk.Tk):
    """
    Fenêtre principale de l'application
    Hérite de:
        - tkinter (Tkinter)
    Paramètres:
        - titre de la fenêtre (STRING)
        - taille de la fenêtre (float2)
    Arguments:
        - taille minimale, égale à la taille de la fenêtre en paramètre (float2)
        - possibilité de redimentionner la fenêtre (vrai pour x et y par défaut)(BOOL,BOOL)
        - titre de la fenêtre, égal à celui inséré en paramètre (float2)
    """
    def __init__(self, mainTitle, size):
        super().__init__()
        self.minsize(*size)
        self.resizable(True, True)
        self.title(mainTitle)


class MainFrame(tk.Frame):
    """
    Objet de sélection du jeu
    hérite de:
        - Frame, qui est un widget de tkinter (tkinter)
    Paramètres:
        - container (tk.Tk): fenêtre principale dans laquelle le frame est affiché
    Arguments:
        - texte principal de l'image (STR)
        - cadre contenant les bouttons de sélection des jeux (Widget)
        - les 3 bouttons redirigeant vers les 3 jeux (Widget)
    """
    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.pack()

        # Titre
        self.label = tk.Label(self, text="Projet IA", font=("Arial", 12))
        self.label.pack(pady=10)

        # Frames
        self.play_buttons_frame = tk.Frame(self)
        self.play_buttons_frame.pack()

        # Jeux
        self.games = ["Allumettes", "Cubee", "PixelKart"]
        for game in self.games:
            self.create_game_card(game)

    def create_game_card(self, game_name):
        """
        Création de cards avec bouton "Jouer"
        paramètre:
            - nom du jeu (STR) 
        """
        frame = tk.Frame(self.play_buttons_frame, relief="solid", borderwidth=1)
        frame.pack(side="left", padx=10, pady=10, expand=True, fill="both")

        label = tk.Label(frame, text=game_name, font=("Arial", 12, "bold"))
        label.pack(pady=10)

        # Bouton de lancement du jeu
        button = tk.Button(frame, text="Jouer", bg="lightblue", fg="black", font=("Arial", 12, "bold"),
                           command=lambda: self.launch_game(game_name))
        button.pack(pady=10, padx=10)

    def launch_game(self, game_name):
        """       
        Lance le jeu en fonction du boutton choisi
        paramètre:
            - nom du jeu à lancer (STR) 
        """
        if game_name == "Allumettes":
            self.launch_match_game()
        elif game_name == "Cubee":
            self.launch_cubee()
        elif game_name == "PixelKart":
            self.launch_pixelkart()

    def launch_match_game(self):
        """
        Lance le jeu des allumettes
        Initialise un joueur humain et une IA, puis crée un GameController
        """
        player1 = Human("Jean")
        player2 = AI("Bot")
        controller = GameController(player1, player2, 6)
        print("Allumettes")

    def launch_cubee(self):
        """
        Lance Cubee
        """
        root = tk.Tk()
        root.title("Cubee Game")
        playerA = CubeeAI("Alice",epsilon=0.9)
        playerB = CubeeHuman ("Bob")
        controller = CubeeGameController(root, playerA, playerB)
        print("Cubee")

    def launch_pixelkart(self):
        """
        Lance PixelKart
        """
        print("PixelKart")
        controller = GameManager()


if __name__ == "__main__":
    app = App("Sélection de jeux", [300, 50])
    frame = MainFrame(app)
    app.mainloop()

