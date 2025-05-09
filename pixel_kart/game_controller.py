# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 08:41:23 2025

@author: martin
"""
from pixel_kart.game_view import GameEditor, GameInterface
import tkinter as tk
from pixel_kart.game_model import Kart, Circuit, Game
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
        if(self.editor.against_AI):
            self.model.karts.append(Kart())
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
        self.model.karts = [Kart(position=random.choice(self.model.get_finish_lines()))]
        if(self.editor.against_AI.get() != "Human"):
            self.model.karts.append(Kart(position=random.choice(self.model.get_finish_lines())))
        
        self.model.start_game()
    
        # Créer la vue principale de jeu
        self.interface = GameInterface(
            
            controller=self,
            circuit=self.model.circuit,
            loops_count=loops_count,
            against_AI=against_human,
            players=self.model.karts
        )
        
    def move_kart(self, does_accelerate):
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
        if(does_accelerate and kart.speed < 2):
            kart.speed += 1
            # Appliquer les contraintes de mouvement
        self.model.modify_player_movement(self.model.get_current_kart())
        
        next_x, next_y = kart.predict_next_position()
        
        # Vérifier si la case est dans les limites du circuit
        if 0 <= next_x < len(self.model.circuit.grid) and 0 <= next_y < len(self.model.circuit.grid[0]):
            
                # Vérifier que la case est un mur
            if self.model.circuit.grid[next_y][next_x] != "W": 
                
                # Mettre à jour la position
                kart.position = (next_x, next_y)
        
        # Regénérer la grille
        self.interface.draw_grid(self.model.circuit, self.model.karts)

        

if __name__ == "__main__":
    new_manager = GameManager()