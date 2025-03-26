import sys
import os
import tkinter as tk
import random
# Importation des modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cubee.gamemodel import CubeeGameModel, CubeePlayer, CubeeHuman
from cubee.gameview import CubeeGameView

"""
La classe GameController fait le lien entre la classe GameModel et la classe GameView
Les fonctions de la classe prennent en compte la logique du jeu et les fonctions d'affichage et les adapte en fonction de l'état du jeu
"""

class CubeeGameController:

    def __init__(self, root,playerA, playerB, dimension=5):
        """
        Constructeur du contrôleur du jeu
        arguments:
            - lecteur d'inputs de tkinter (ROOT)
            - premier joueur(humain) (PLAYER)
            - deuxième joueur(IA) (PLAYER)
            - dimension du plateau de jeu (par défaut: 5) (INT)
                
        attributs:
            - Modèle de la partie (MODEL)
            - Interface graphiue de la partie (VIEW)
        Une fois que toutes les propriétés sont lancées, lance la partie
            
        """
        self.root = root
        self.dimension = dimension
        self.playerA = playerA
        self.playerB = playerB
        self.model = CubeeGameModel(self.dimension, self.playerA, self.playerB)
        self.view = CubeeGameView(root, self, self.dimension)
        self.start_game()


    def start_game(self):
        """
        Démarrage de la partie: si le premier joueur n'est pas humain, lance directement un déplacement de l'IA
        
        """
        if not isinstance(self.model.get_current_player(), CubeeHuman):
            self.handle_random_ai_move()


    def update_view(self):
        """
        Mise à jour du visuel du terrain
        """
        self.view.update_view(self.get_terrain())

    def get_terrain(self):
        """
        Actualise les informations du terrain
        la structure est une matrice contenant soit "P1" ou "P2" en fonction des positions actuelles des joueurs
        retourne:
            - le terrain actualisé ([[STR]])
        """
        grid_display = [["" for _ in range(self.dimension)] for _ in range(self.dimension)]
        grid_display[self.model.player1_pos[0]][self.model.player1_pos[1]] = "P1"
        grid_display[self.model.player2_pos[0]][self.model.player2_pos[1]] = "P2"
        return grid_display
    
    def handle_random_ai_move(self):
        """
        Fait déplacer le joueur IA aléatoire
        Si le déplacement est invalide, lance un appel récursif jusqu'à ce que le choix soit adéquat
        En cas de déplacement valide, le joueur actif est changé et lance une vérification du cas de victoire
        """
        if(self.model.move(self.model.get_current_player(),random.choice(["up","left","down","right"]))):
            self.model.step()
            self.model.switch_player()
          # self.model.enable_locked_cases(self.model.players[self.model.get_current_player()])
            self.update_view()
            if self.model.is_over():  # Vérification si partie terminée
                self.handle_end_game()
        else: 
            self.handle_random_ai_move()
            
    def handle_player_move(self, direction):
        """
        Fait déplacer le joueur humain
        Si le joueur actuel est bien humain, la tentative de mouvement est lancé:
            S'il est valide, le joueur actif est changé
        Ensuite, lance une vérification de fin de partie
        Enfin, change le joueur actif pour donner la main au joueur IA aléatoire
        
        """        
        current_player = self.model.players[self.model.get_current_player()]
        if(type(current_player) == CubeeHuman):

            if(self.model.move(current_player, direction)):
                self.model.switch_player()
            self.model.step()  # changer les valeurs du terrain
            self.update_view()
            #self.model.enable_locked_cases(current_player)
        if self.model.is_over():  # Vérification si partie terminée
            self.handle_end_game()
        current_player = self.model.players[self.model.get_current_player()]
        if(type(current_player) != CubeeHuman):
            self.handle_random_ai_move()
              # Changement de joueur après un tour valide
    
    def handle_ai_move(self):
        """
        Déplacement de l'IA intelligente
        PAS ENCORE IMPLÉMENTÉ
        """
        if self.model.is_ai_turn():
            best_move = self.model.get_best_move()  # Récupération du meilleur coup
            self.handle_player_move(best_move)  # L'IA joue

    def handle_end_game(self):
        """
        Gère la fin de partie et affiche le message du gagnant
        """
        winner = self.model.get_winner()
        message = "It's a draw!" if winner == "it's a draw" else f"{winner} won!"
        self.view.draw_endgame(message)

    def restart_game(self):
        """
        Réinitialisation de la partie
        """
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
