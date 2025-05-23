# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 08:41:23 2025

@author: martin
"""
from pixel_kart.game_view import GameEditor, GameInterface
import tkinter as tk
from pixel_kart.game_model import Kart, Circuit, Game, AI
import random

class GameManager:

    def __init__(self):
        """
        Constructeur du contrôleur du jeu
    
        attributs:
            - le modèle de la partie, venant de game_model.py (GAME)
            - la source tkinter pour gérer la base de tkinter (TK)
            - l'éditeur de partie, pour paramétrer la partie à lancer (GAMEEDITOR)
            
        Gère aussi le callback, qui va gérer l'échange des données entre l'éditeur et le jeu
        Une fois que toutes les propriétés sont lancées, lance la partie
            
        """       
        self.model = Game()
        self.root = tk.Tk()
        
        # cache la fenêtre principale
        self.root.withdraw() 
        
        self.editor = GameEditor(master = self.root, game_list = self.model.get_all_circuits())
        self.editor.submit_callback = self.receive_editor_data

        #partie éxécutée dès le lancement du jeu
        self.root.mainloop()
        
        
    def receive_editor_data(self, circuit_name, loops_count, against_human):
        """
        Fonction lançant la partie avec les données insérées dans l'éditeur de partie
        arguments:
            - nom du circuit, tel qu'il est dans le fichier les reprenant (STRING)
            - nombre de tours, qui sera inséré par le joueur avant de lancer la partie (INT)
            - choix entre jouer contre une autre personne ou une IA (BOOL)
        attributs:
            - l'objet circuit, récupéré à partir du nom entré en paramètre (CIRCUIT)
            - les joueurs, qui seront placés aléatoirement sur la case de départ ([KART])
            - Interface de jeu, lancé à partir des paramètres/arguments de la fonction (GAMEINTERFACE)
        Assigne aussi une vitesse et orientation par défaut aux joueurs
        """
        print(f"Circuit choisi: {circuit_name}")
        print(f"Nombre de tours: {loops_count}")
        print(f"Contre humain ?: {against_human}")
        

    
        self.model.circuit = self.model.get_circuit(circuit_name)
        self.model.laps = loops_count        
        self.model.karts = [Kart(position=random.choice(self.model.get_finish_lines()), circuit = self.model.circuit)]
        if(self.editor.against_AI == 'AI'):
            self.model.karts.append(AI(position=random.choice(self.model.get_finish_lines()), circuit = self.model.circuit))
            self.model.against_AI = True
         
        self.model.start_game()
    
        # Créer la vue principale de jeu
        self.interface = GameInterface(
            
            controller=self,
            circuit=self.model.circuit,
            loops_count=loops_count,
            against_AI=against_human,
            players=self.model.karts
        )
        
    def move_kart(self, acceleration):
        """
        Gère le déplacement d'un kart
        arguments:
            - choix d'incrémenter ou non la vitesse du kart (BOOL)
        attributs:
            - joueur actuel (implémenter le switch de joueurs) (KART)
        Modifie le déplacement en fonction des cases sur la trajectoire du kart
        Et redessine la grille pour afficher le kart correctement
        """
        kart = self.model.karts[self.model.current_kart]

        if not kart.is_alive:
            return  # Ne pas déplacer un kart mort

        # Ajustement de la vitesse
        kart.speed += acceleration
        if kart.speed > 2:
            kart.speed = 2
        if kart.speed < -1:
            kart.speed = -1

        # Appliquer les contraintes de mouvement
        self.model.modify_player_movement(kart)

        # Vérifier s'il se prend un mur
        x, y = kart.position  # Suppose que position = (x, y)
        if self.model.circuit.grid[y][x] == 'W':
            kart.alive = False
            print(f"Kart {self.model.current_kart} s'est écrasé contre un mur !")

        self.model.time += 1

        # Regénérer la grille
        self.interface.draw_grid(self.model.circuit, self.model.karts)

    def turn_kart(self, movement):
            
        kart = self.model.karts[self.model.current_kart]
        self.model.turn(kart,movement)
        self.move_kart(acceleration = False)
           
                        
    def move_random_AI(self):
        
        print("move AI")
        self.model.current_kart += 1
        random_movement = random.choice([0,1,2,3,4])
        if(random_movement == 0):
            self.move_kart(0)
        elif(random_movement == 1):
            self.move_kart(-1)
        elif(random_movement == 2):
            self.move_kart(-1)
        elif(random_movement == 3):
            self.turn_kart(1)
        elif(random_movement == 4):
            self.turn_kart(-1)
        self.model.current_kart -= 1
        
        
    def move_smart_AI(self):
        """
        déplace le kart en fonction de la q-value la plus élevée pour son état
        """
        actions = ["accelerate","turn_left","turn_right","brake","do_nothing"]
        self.model.current_kart += 1
        action = self.model.get_current_kart().choose_action()
        if(action == "accelerate"):
              self.move_kart(1)
        elif(action == "do_nothing"):
              self.move_kart(0)
        elif(action == "brake"):
              self.move_kart(-1)
        elif(action == "turn_right"):
              self.turn_kart(1)
        elif(action == "turn_left"):
              self.turn_kart(-1)
        self.model.current_kart -= 1