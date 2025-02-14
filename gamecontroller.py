from gamemodel import GameModel, Human, Player
from gameview import GameView

import random
import tkinter as tk

# Joueur (en général)



# Vue représentant l'interface graphique du jeu

# Contrôleur qui lie la logique du jeu avec la vue
class GameController:

    def __init__(self, player1, player2, nb_matches):
        """
        Constructeur du contrôleur du jeu
        arguments: 
            - premier joueur(humain)
            - deuxième joueur(IA)
            - nombre d'allumettes pour le début du jeu
        
        """
        # Vérifie qu'au moins un joueur est un humain
        if not (isinstance(player1, Human) or isinstance(player2, Human)):
            raise ValueError("There must be at least one human player.")
        
        # Initialisation des attributs
        self.model = GameModel(nb_matches, player1, player2) # création d'une instance du modèle
        self.view = GameView(self) # création d'une instance de la vue
        
      # Démarre le jeu
        self.start_game()

    def start_game(self):
        """
        Démarre le jeu
        Si l'IA joue en premier, lance d'abord le tour de l'IA
        Sinon, lance la gestion du jeu et des visuels
        """
        # Démarre le jeu, gérant le premier mouvement si c'est l'IA.
        if not isinstance(self.model.get_current_player(), Human):
            self.handle_ai_move()
        self.view.update_view()
        
        # Démarre la boucle principale de la vue
        self.view.mainloop() # gère les événements, maintient l'interface ouverte et permet les màj visuelles 

    def get_nb_matches(self):
        """
        Renvoie le nombre d'allumettes restantes
        """
        # Retourne le nombre restant d'allumettes du jeu
        return self.model.nb

    def get_status_message(self):
        """
        Actualise le message informant le statut de la partie
        Si la partie est finie, 
        Renvoie le nom du joueur gagnant,
        sinon,
        Renvoie le nom du joueur actif
        """
        # Fournit une chaîne de caractères indiquant l'état du jeu
        if self.model.is_game_over():
            winner = self.model.get_winner()
            return f"{winner.name} wins!"
        else:
            current_player = self.model.get_current_player()
            return f"{current_player.name}'s turn."

    def reset_game(self):
        """
        Remet à 0 les paramètres de la partie, et démarre une nouvelle
        Appelle les fonctions de reset du modèle et du visuel
        Génère un joueur actif aléatoirement, si le joueur actif est l'IA, elle joue un tour immédiatement
        Donne ensuite la main à l'humain avec un nouveau layout
        """
        # Réinitialise le jeu
        self.model.reset()
        self.view.reset()
        if not isinstance(self.model.get_current_player(), Human):
            self.handle_ai_move()

    def handle_human_move(self, matches_taken):
        """
        Gestion du mouvement du joueur humain
        argument:
            - nombre d'alumettes enlevées
        actualise le joueur en cours, et s'il est bien humain:
            - fait avancer le calcul du modèle
            - vérifie qu'il reste des allumettes, si c'est le cas change de joueur et si le joueur humain est toujours actif, fais jouer l'IA
            - s'il n'y a plus d'allumettes, lance la fin de partie
        actualise enfin le visuel de la partie 
        """
        # Mouvement humain
        current_player = self.model.get_current_player()
        
        if isinstance(current_player, Human):
            self.model.step(matches_taken)
            if self.model.is_game_over():
                self.handle_end_game()
            else:
                self.model.switch_player()
                if not isinstance(self.model.get_current_player(), Human):
                    self.handle_ai_move()
        
        self.view.update_view()

    def handle_ai_move(self):
        """
        Gestion du mouvement de l'IA
        actualise le joueur en cours, fais jouer l'IA, fais avancer la partie
        S'il ne reste plus d'allumettes, lance la fin de partie, sinon le joueur actif est changé
        actualise enfin le visuel de la partie
        """
        # Mouvement IA
        current_player = self.model.get_current_player()
        matches_taken = current_player.play() # l'IA joue
        self.model.step(matches_taken)
        
        if self.model.is_game_over():
            self.handle_end_game()
        else:
            self.model.switch_player()
        
        self.view.update_view()

    def handle_end_game(self):
        """
        Récupère le gagnant et le perdant
        leur fait augmenter leur score de victoire et de défaite (respectivement)
        Affiche l'écran de fin de partie
        """
        # Fin de la partie
        winner = self.model.get_winner()
        loser = self.model.get_loser()
        winner.win()
        loser.lose()
        self.view.end_game()


if __name__ == "__main__":
    player1 = Human("Jean")
    player2 = Player("Bot")
    controller = GameController(player1, player2, 6)