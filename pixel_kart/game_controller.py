# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 08:41:23 2025

@author: martin
"""
from game_view import GameEditor, GameInterface
import tkinter as tk
from game_model import Kart, Circuit, Game
import random

class GameManager:

    def __init__(self):
        """
        Constructeur du contrôleur du jeu
        arguments:
                
        attributs:
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
        print(f"Circuit choisi: {circuit_name}")
        print(f"Nombre de tours: {loops_count}")
        print(f"Contre humain ?: {against_human}")
    
        if circuit_name is None:
            print("Erreur : circuit introuvable")
            return
    
        # Préparer les joueurs
        self.model.circuit = self.model.get_circuit(circuit_name)
        print(type(self.model.circuit))
        self.model.laps = loops_count        
        self.model.karts = [Kart(position=random.choice(self.model.get_finish_lines())), Kart(position=random.choice(self.model.get_finish_lines()))]  # 2 joueurs par défaut


        
        self.model.start_game()
    
        # Créer la vue principale de jeu
        self.interface = GameInterface(
            controller=self,
            circuit=self.model.circuit,
            loops_count=loops_count,
            against_human=against_human,
            players=self.model.karts
        )
        
    def move_kart(self, does_accelerate):
        kart = self.model.karts[self.model.current_kart]
        if(does_accelerate):
            kart.speed += 1
            # Appliquer les contraintes de mouvement
        self.model.modify_player_movement(self.model.get_current_kart())
        
            # Obtenir la position cible
        next_x, next_y = kart.predict_next_position()
        
            # Vérifier si la case est dans les limites du circuit
        if 0 <= next_x < len(self.model.circuit.grid) and 0 <= next_y < len(self.model.circuit.grid[0]):
                # Vérifier que la case est praticable (tu peux ajouter d'autres conditions si besoin)
            if self.model.circuit.grid[next_y][next_x] != "X":  # Supposons que "X" est un mur
                    # Mettre à jour la position
                kart.position = (next_x, next_y)
        
            # Redessiner la grille
        self.interface.draw_grid(self.model.circuit, self.model.karts)

        

if __name__ == "__main__":
    new_manager = GameManager()