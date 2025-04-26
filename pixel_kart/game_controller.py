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
        self.root.withdraw()  # cache la fenêtre principale

        self.editor = GameEditor(master = self.root, game_list = self.model.get_all_circuits())
        self.editor.submit_callback = self.receive_editor_data

        self.get_loops_count()
        self.root.mainloop()
        self.interface = GameInterface(circuit=None, loops_count=3, against_human=True, players=[None, None])
        
        self.launch_game()
    def receive_editor_data(self, circuit_name, loops_count, against_human):
        print(f"Circuit choisi: {circuit_name}")
        print(f"Nombre de tours: {loops_count}")
        print(f"Contre humain ?: {against_human}")

        
        self.interface = GameInterface(
            circuit=self.model.get_circuit(circuit_name),
            loops_count=loops_count,
            against_human=against_human,
            players=[None, None]
        )

    def launch_game(self):
        """
        lancer le circuit editor
        proposer le choix du circuit parmi la liste des circuits dispos
        
        """
        self.editor.Toplevel()
    def get_loops_count(self):
        print("test: ", self.editor.loops_entry.get())
        self.editor.loops_count = self.editor.loops_entry.get()
        print(self.editor.loops_count)
        
        

if __name__ == "__main__":
    new_manager = GameManager()