# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 08:41:23 2025

@author: martin
"""
from game_view import GameEditor, GameInterface
import tkinter as tk
# A SUPPRIMER DES QUE LE MODELE EST IMPLEMENTE
from game_model import Kart, Circuit, Game


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
        print(self.model.laps)
        self.root.mainloop()
        

    def receive_editor_data(self, circuit_name, loops_count, against_human):
        print(f"Circuit choisi: {circuit_name}")
        print(f"Nombre de tours: {loops_count}")
        print(f"Contre humain ?: {against_human}")
    
        # Initialiser correctement le modèle !
        circuit = self.model.get_circuit(circuit_name)
        if circuit is None:
            print("Erreur : circuit introuvable")
            return
    
        # Préparer les joueurs
        players = [Kart(), Kart()]  # 2 joueurs par défaut
    
        self.model.circuit = circuit
        self.model.laps = loops_count
        self.model.karts = players
    
        self.model.start_game()
    
        # Créer la vue principale de jeu
        self.interface = GameInterface(
            circuit=circuit,
            loops_count=loops_count,
            against_human=against_human,
            players=players
        )



if __name__ == "__main__":
    new_manager = GameManager()