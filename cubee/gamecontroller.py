#import sys
import os
import tkinter as tk
import random
# Importation des modules
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cubee.gamemodel import CubeeGameModel, CubeePlayer, CubeeHuman
from cubee.gameview import CubeeGameView

class CubeeGameController:
    def __init__(self, root,playerA, playerB, dimension=5):
        self.root = root
        self.dimension = dimension
        self.playerA = playerA
        self.playerB = playerB
        self.model = CubeeGameModel(self.dimension, self.playerA, self.playerB)
        self.view = CubeeGameView(root, self, self.dimension)
        self.start_game()

    def start_game(self):
        """Démarrage de la partie"""
        self.update_view()

    def update_view(self):
        """Màj affichage en fonction du modèle"""
        self.view.update_view(self.get_terrain())

    def get_terrain(self):
        """Retourne l'état actuel du terrain"""
        grid_display = [["" for _ in range(self.dimension)] for _ in range(self.dimension)]
        grid_display[self.model.player1_pos[0]][self.model.player1_pos[1]] = "P1"
        grid_display[self.model.player2_pos[0]][self.model.player2_pos[1]] = "P2"
        return grid_display

    def handle_player_move(self, direction):
        """Déplacement du joueur en cours"""        
        current_player = self.model.players[self.model.get_current_player()]
        if(type(current_player) == CubeeHuman):
            print("Human")
            if self.model.move(current_player, direction):  # Si mouvement est valide
                self.model.step()  # Nouvelle position
                self.update_view()
        else:
            print("BOT")
            if self.model.move(current_player, random.choice(["up","down","left","right"])):
                self.model.step()  # Nouvelle position
                self.update_view()
        if self.model.is_over():  # Vérification si partie terminée
            self.handle_end_game()
        else:
            self.model.switch_player()  # Changement de joueur après un tour valide
    def handle_ai_move(self):
        """Déplacement de l'IA si activée"""
        if self.model.is_ai_turn():
            best_move = self.model.get_best_move()  # Récupération du meilleur coup
            self.handle_player_move(best_move)  # L'IA joue

    def handle_end_game(self):
        """Gère la fin de partie et affiche le message du gagnant"""
        winner = self.model.get_winner()
        message = "It's a draw!" if winner == "it's a draw" else f"{winner} won!"
        self.view.draw_endgame(message)

    def restart_game(self):
        """Réinitialisation de la partie"""
        self.model.reset()
        self.view.reset_game()
        self.update_view()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Cubee Game")
    playerA = CubeePlayer("Alice")
    playerB = CubeeHuman ("Bob")
    controller = CubeeGameController(root, playerA, playerB)
    root.mainloop()
