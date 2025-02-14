import random

class Player:
    def __init__(self, name, game=None):
        """
        Constructeur du profil du joueur:
            
            attributs: 
                - nom du joueur
                - objet de la partie dans laquelle est le joueur
                - nombre de victoires
                - nombres de défaites
            attribut dérivable:
                - nombre de parties jouées
        """
        self.name = name
        self.game = game
        self.nb_wins = 0
        self.nb_loses = 0

    @property
    def nb_games(self): # attribut dérivable
        """
        Renvoie le nombre de parties jouées = nombre de défaites + nombre de victoires
        """
        return self.nb_wins + self.nb_loses

    @staticmethod
    def play():
        """
        Comportement de l'IA à choix aléatoire
        Renvoie le nombre d'allumettes enlevées
        """
        return random.choice([1, 2, 3])

    def win(self):
        """
        Appelée en cas de victoire, augmente le compte de victoires de un

        """
        self.nb_wins += 1

    def lose(self):
        """
        Appelée en cas de défaite, augmente le compte de défaites de un

        """
        self.nb_loses += 1

    def __str__(self):
        """
        Descriptions du joueur
        Renvoie le nom et le nombre de défaites et de victoires en une chaîne de caractères

        """
        return f"{self.name} (Wins: {self.nb_wins}, Losses: {self.nb_loses})"


# Joueur humain
class Human(Player):
    def play(self):
        """
        Seule fonction propre au joueur humain
        Demande un choix entre 1 et 3 et vérifie que le choix soit valide
        Renvoie le nombre choisi

        """
        choice = 0
        while choice not in [1, 2, 3]: #encore important vu qu'on passe par une interface graphique ?
            choice = int(input("Choose 1, 2, or 3 matches to remove: "))
        return choice


# Modèle représentant la logique du jeu
class GameModel:
    def __init__(self, nb_matches, player1, player2):
        """
        Constructeur du comportement d'une partie:
            
            attributs: 
                - nombre d'allumettes en début de partie
                - nombre d'allumettes en cours
                - liste des joueurs engagé dans la partie
                - joueur en cours dans la partie
           
            Rempli aussi la liste des joueurs avec les joueurs inscrits dans la partie
            et choisi aléatoirement un des joueurs inscrits pour commencer la partie

        """
        self.original_nb = self.nb = nb_matches
        self.players = [player1, player2]
        self.current_player = 0  # indique quel joueur joue actuellement
        for player in self.players:
            player.game = self
        self.shuffle()


    def shuffle(self): # mélange l'ordre des joueurs 
        """
        Renvoie la liste des joueurs inscrits avec les éléments dans un ordre aléatoire
        """
        random.shuffle(self.players) 

    def reset(self):
        """
        Modifie les variables de la partie pour repartir de 0:
            - le nombre d'allumettes en jeu retourne à sa valeur originale
            - choix aléatoire du joueur qui commence la partie
            - réinitialise le joueur actuel

        """
        self.nb = self.original_nb # remet la partie à 0
        self.current_player = 0  # réinitialise le joueur actuel
        self.shuffle()

    def switch_player(self):
        """
        Change le joueur actuel en reculant d'une place dans la liste contenant tous les joueurs

        """
        self.current_player = 1 - self.current_player

    def is_game_over(self):
        """
        Vérifie si la partie est fine 
        Renvoie un booléen activé si il reste aucune allumettes

        """
        return self.nb <= 0

    def get_current_player(self):
        """
        Renvoie le joueur actuel dans la liste des joueurs

        """
        return self.players[self.current_player]
    def get_winner(self):
        """
        Renvoie le joueur non-actif au moment où le game_over devient True

        """
    
        return self.players[1- self.current_player] if self.is_game_over() else None

    def get_loser(self):
        """
        Renvoie le joueur actif au moment où le game_over devient True

        """
       
        return self.players[self.current_player] if self.is_game_over() else None

    def step(self, action): # màj de l'état du jeu en modifiant nb matches restants dans le jeu
        """
        Diminue le nombre d'allumettes actuel par le nombre entré par le joueur
        """
        self.nb -= action # action représente le nb de matches retirés