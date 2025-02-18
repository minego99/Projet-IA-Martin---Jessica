import random
"""
La classe GameModel contient toute la logique des règles du jeu des allumettes
Les valeurs renvoyées permettent à GameController de composer le statut du jeu
La classe Player comprend le comportement de l'IA aléatoire, et sa classe héritée celle du joueur humain
"""

class Player:
    def __init__(self, name, game=None):
        """
        Constructeur du profil du joueur:
            argument:
                - nom du joueur(STR)
                - partie dans laquelle est le joueur(GAME)
            attributs: 
                - nom du joueur(STR)
                - objet de la partie dans laquelle est le joueur(GAME)
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
        
        Retourne:
            - le nombre de parties jouées = nombre de défaites + nombre de victoires (INT)
        """
        return self.nb_wins + self.nb_loses

    @staticmethod
    def play():
        """
        Comportement de l'IA à choix aléatoire
        
        Retourne:
            - le nombre d'allumettes enlevées (INT)
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
        Description du joueur
        
        Retourne:
            - le nom et le nombre de défaites et de victoires (STR)

        """
        return f"{self.name} (Wins: {self.nb_wins}, Losses: {self.nb_loses})"


# Joueur humain
class Human(Player):
    def play(self, choice):
        """
        Seule fonction propre au joueur humain
        
        Paramètre: 
            - un choix entre 1 et 3 (INT) 
        Retourne:
            - le nombre choisi (INT)

        """
        return choice

# AI (joueur qui apprend)
class AI(Player):
    def __init__(self, name):
        super().__init__(name)
        self.epsilon = 0.9  # Probabilité d'exploration :  l'IA va choisir 90% du temps une action aléatoire (exploration)
        # α est le coefficient d'ajustement de la value-function.
        # Détermine à quelle vitesse l'IA met à jour ses connaissances en fonction des expériences 
        # Une petite valeur signifie que l'IA apprend lentement. Si α était trop grand, l'IA pourrait trop vite oublier les leçons passées
        self.learning_rate = 0.01 # Taux d'apprentissage : l'IA va choisir  10% du temps la meilleure action connue (exploitation)
        self.history = []  # Historique des transitions : à chaque tour, une transition (s, s') est ajoutée (l'état avant et après que l'adversaire ait joué). Après la partie, l'IA utilise cet historique pour ajuster la value-function (V(s))
        self.previous_state = None  # État précédent
        self.value_function = {"win": 1, "lose": -1}  # Initialisation avec états finaux
    
    def exploit(self, possible_moves):
        """Choisit la meilleure action qui mettra l'adversaire le plus en difficulté."""
        # Choisit l'élément ayant la plus petite valeur selon la fonction de key
        # Pour chaque mouvement possible move, on récupère V(move) -> valeur associée dans self.value_function
        # Si move n'existe pas encore -> valeur 0 (état neutre)
        return min(possible_moves, key=lambda move: self.value_function.get(move, 0)) 
    
    def play(self, game_state, possible_moves):
        """Joue un coup en fonction de l'exploration/exploitation."""
        if self.previous_state is not None:
            self.history.append((self.previous_state, game_state)) #L'IA enregistre les transitions (état précédent -> état actuel) pour pouvoir apprendre plus tard
        
        if random.random() < self.epsilon: # "random.random()" génère un nombre aléatoire entre 0 et 1 et l’IA explore si le nb aléatoire est < que epsilon pcq epsilon représente la probabilité d’exploration
            action = random.choice(possible_moves) # Exploration, l'IA choisit un mouvement aléatoire parmi possible_moves 
        else:
            action = self.exploit(possible_moves)  # Exploitation, pour jouer le meilleur coup
        
        self.previous_state = game_state  # Mise à jour de l'état précédent
        return action
    
    def win(self):
        """Ajoute la dernière transition à l'historique et réinitialise l'état précédent pour préparer une nouvelle partie."""
        if self.previous_state is not None:
            self.history.append((self.previous_state, "win"))
        self.previous_state = None
        super().win()
    
    def lose(self):
        """Ajoute la dernière transition à l'historique et réinitialise l'état précédent pour préparer une nouvelle partie."""
        if self.previous_state is not None:
            self.history.append((self.previous_state, "lose"))
        self.previous_state = None
        super().lose()
    
    def train(self):
        """Entrainement de l'IA : met à jour la value-function en remontant l'historique."""
        # self.history contient la liste des transitions sous forme de tuples (état actuel, état suivant)
        # On remonte l'historique à l'envers car l'IA apprend en backtracking -> en partant de la fin de la partie vers le début
        for state, next_state in reversed(self.history): 
            # valeur de état state ajustée en fonction de la valeur next_state selon la formule V(s)←V(s)+α⋅(V(s ′)−V(s))
            self.value_function[state] = self.value_function.get(state, 0) + self.learning_rate * (self.value_function.get(next_state, 0) - self.value_function.get(state, 0)) # état state à 0 s'il n'a jamais été rencontré
        self.history.clear()  # On vide l'historique après l'entraînement pour partir sur une nouvelle partie "propore"
    
    # factor -> paramètre par défaut 0.95 -> détermine de combien epsilon sera multiplié à chaque appel de la fonction -> chaque fois que la fonction est appelée, epsilon sera réduit à 95 % de sa valeur actuelle 
    # min_epsilon -> valeur minimale par défaut 0.05 que epsilon ne peut pas descendre en dessous -> garantit que l'agent continue d'explorer un peu, même lorsque l'exploitation est privilégiée
    def next_epsilon(self, factor=0.95, min_epsilon=0.05):
        """Diminue epsilon progressivement pour favoriser l'exploitation."""
        # self.epsilon * factor -> diminue epsilon
        # max -> s'assurer que self.epsilon ne descend pas en dessous de min_epsilon. Si self.epsilon * factor est inférieur à min_epsilon, alors self.epsilon prendra la valeur de min_epsilon
        self.epsilon = max(self.epsilon * factor, min_epsilon)

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
        Modifie la liste des joueurs inscrits avec les éléments dans un ordre aléatoire
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
        
        Retourne:
            - un test activé si il reste aucune allumettes (BOOL)

        """
        return self.nb <= 0

    def get_current_player(self):
        """
        Retourne:
            - le joueur actuel dans la liste des joueurs (PLAYER)

        """
        return self.players[self.current_player]
    def get_winner(self):
        """
        Retourne:
            - le joueur non-actif au moment où le game_over devient True (PLAYER)

        """
    
        return self.players[1- self.current_player] if self.is_game_over() else None

    def get_loser(self):
        """
        Retourne:
            - le joueur actif au moment où le game_over devient True (PLAYER)

        """
       
        return self.players[self.current_player] if self.is_game_over() else None

    def step(self, action): # màj de l'état du jeu en modifiant nb matches restants dans le jeu
        """
        Diminue le nombre d'allumettes actuel par le nombre entré par le joueur
        """
        self.nb -= action # action représente le nb de matches retirés