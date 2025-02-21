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
    def play(possible_moves = [1,2,3]):
        """
        Comportement de l'IA à choix aléatoire
        
        argument:
            - nombre de coups possibles selon les règles, nécessaire pour supporter le polymorphisme avec la fonction AI.play (liste de INT)
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
        hérite de :
            - Player
        Paramètre: 
            - un choix entre 1 et 3 (INT) 
        Retourne:
            - le nombre choisi (INT)

        """
        return choice

# AI (joueur qui apprend)
class AI(Player):
    def __init__(self, name):
        """
        Constructeur de l'Intelligence artificielle avec renforcement:
        
        hérite de:
            - Player (Player)
        Argument:
            - nom de l'IA (STR)
        Attributs:
            - epsilon, représente la probabilité entre l'exploitation et l'exploration (Réel)
            - learning_rate, réprésente l'importance donnée à l'apprentissage acquis après une étape (Réel)
            - history, liste reprenant toutes les transitions d'états parcourues par les IA (liste de tuple contenant chacun un INT)
            - previous_state, reprend l'état précédent dans lequel était le joueur lors de son tour précédent (INT)
            - value_function, contient toutes les possibilités dans lesquelles peut se retrouver l'IA, avec la pondération de l'état (dictionnaire: clé en STR ou INT valeurs: Réel)
        
        """
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
        """"""
        # Choisit l'élément ayant la plus petite valeur selon la fonction de key
        # Pour chaque mouvement possible move, on récupère V(move) -> valeur associée dans self.value_function
        # Si move n'existe pas encore -> valeur 0 (état neutre)
        
        #get sur le résultat du move, et pas sur le move en soi
        """
        Choisit la meilleure action qui mettra l'adversaire le plus en difficulté.
        
        argument:
            - actions possible selon les règles du jeu (1, 2 ou 3 allumettes retirées) (liste de INT)
            
        renvoie:
            - valeur choisie parmis les 3 choix, choisi en fonction du poids le plus petit au sein de la value_function de l'IA (INT)
        """
        return min(possible_moves, key=lambda move: self.value_function.get(move, 0)) 

    
    def play(self, game_state, possible_moves = [1,2,3]):
        """"""
        """
        adaptation de la fonction selon le comportement de l'IA: joue le coup en fonction de l'exploration/exploitation.
        Gère aussi l'ajout de l'état précedent dans l'historique des états
        argument:
            - nombre d'allumettes restantes au début du tour (INT)
            - nombre d'actions permises par les règles du jeu (liste de INT)
        """
        if self.previous_state is not None:
            self.history.append((self.previous_state, game_state)) #L'IA enregistre les transitions (état précédent -> état actuel) pour pouvoir apprendre plus tard
        
        if random.random() < self.epsilon: # "random.random()" génère un nombre aléatoire entre 0 et 1 et l’IA explore si le nb aléatoire est < que epsilon pcq epsilon représente la probabilité d’exploration
            action = random.choice(possible_moves) # Exploration, l'IA choisit un mouvement aléatoire parmi possible_moves 
        else:
            action = self.exploit(possible_moves)  # Exploitation, pour jouer le meilleur coup
        
        self.previous_state = game_state  # Mise à jour de l'état précédent
        return action
    
    def win(self):
        """
        Ajoute la dernière transition à l'historique et réinitialise l'état précédent pour préparer une nouvelle partie.
        Appelle ensuite le comportement de base de la fonction win
        
        """
        if self.previous_state is not None:
            self.history.append((self.previous_state, "win"))
        self.previous_state = None
        super().win()
    
    def lose(self):
        """
        Ajoute la dernière transition à l'historique et réinitialise l'état précédent pour préparer une nouvelle partie.
        Appelle ensuite le comportement de base de la fonction lose
        
        """
        if self.previous_state is not None:
            self.history.append((self.previous_state, "lose"))
        self.previous_state = None
        super().lose()
    
    def train(self):
        """
        Entrainement de l'IA : met à jour la value-function en remontant l'historique.
        Application de la V-function sur l'état actuel avec tous les états précédents de l'historique
        Nettoyage de l'historique pour ne pas garder un environnement obsolète. Les poids gardés dans la value function représentent déjà l'apprentissage passé
        
        """
        # self.history contient la liste des transitions sous forme de tuples (état actuel, état suivant)
        # On remonte l'historique à l'envers car l'IA apprend en backtracking -> en partant de la fin de la partie vers le début
        for state, next_state in reversed(self.history): 
            # valeur de état state ajustée en fonction de la valeur next_state selon la formule V(s)←V(s)+α⋅(V(s ′)−V(s))
            self.value_function[state] = self.value_function.get(state, 0) + self.learning_rate * (self.value_function.get(next_state, 0) - self.value_function.get(state, 0)) # état state à 0 s'il n'a jamais été rencontré
        self.history.clear()  # On vide l'historique après l'entraînement pour partir sur une nouvelle partie "propre"
    
    # factor -> paramètre par défaut 0.95 -> détermine de combien epsilon sera multiplié à chaque appel de la fonction -> chaque fois que la fonction est appelée, epsilon sera réduit à 95 % de sa valeur actuelle 
    # min_epsilon -> valeur minimale par défaut 0.05 que epsilon ne peut pas descendre en dessous -> garantit que l'agent continue d'explorer un peu, même lorsque l'exploitation est privilégiée
    def next_epsilon(self, factor=0.95, min_epsilon=0.05):
        """
        Diminue epsilon progressivement pour favoriser l'exploitation.
        
        arguments:
            - facteur d'adaptation de l'epsilon (Réel)
            - valeur minimale de l'epsilon (Réel)
            
        """
        # self.epsilon * factor -> diminue epsilon
        # max -> s'assurer que self.epsilon ne descend pas en dessous de min_epsilon. Si self.epsilon * factor est inférieur à min_epsilon, alors self.epsilon prendra la valeur de min_epsilon
        self.epsilon = max(self.epsilon * factor, min_epsilon)

def training(ai1, ai2, nb_games, nb_epsilon):
    """
    Lance une séance d'entainement entre deux joueurs
    
    arguments:
        - première intelligence artificielle à entraîner (PLAYER)
        - deuxième intelligence artificielle à entraîner (PLAYER)
        - nombre de parties de l'entraînement (INT)
        - fréquence d'actualisation de l'epsilon (INT)
        
    Crée un modèle pour l'entraînement
    Lance autant de parties que demandé, entraîne les deux IA si possible après chaque partie
    Et clôture les scores aorès chaque partie
    """
    # Train the AIs @ai1 and @ai2 during @nb_games games
    # epsilon decrease every @nb_epsilon games
    training_game = GameModel(12, ai1, ai2)
    for i in range(0, nb_games):
        if i % nb_epsilon == 0:
            if type(ai1)==AI : ai1.next_epsilon()
            if type(ai2)==AI : ai2.next_epsilon()

        training_game.play()
        if type(ai1)==AI : ai1.train()
        if type(ai2)==AI : ai2.train()

        training_game.reset()
        
def compare_ai(*ais):
    # Print a comparison between the @ais
    """
    Affiche les résultats de l'entraînement entre 2 IA
    
    arguement:
        - Toutes les IA qui ont été entraînées (*PLAYER)
        
    affiche:
        - le nom des joueurs
        - le nombre de victoires de chaque joueur sur le nombre total de parties 
        - la valeur de chaque poids pour chaque élément pour chaque IA
    """
    names = f"{'':4}"
    stats1 = f"{'':4}"
    stats2 = f"{'':4}"

    for ai in ais :
        names += f"{ai.name:^15}"
        stats1 += f"{str(ai.nb_wins)+'/'+str(ai.nb_games):^15}"
        stats2 += f"{f'{ai.nb_wins/ai.nb_games*100:4.4}'+'%':^15}"

    print(names)
    print(stats1)
    print(stats2)
    print(f"{'-'*4}{'-'*len(ais)*15}")

    all_v_dict = {key : [ai.value_function.get(key,0) for ai in ais] for key in ais[0].value_function.keys()}
    sorted_v = lambda v_dict : sorted(filter(lambda x : type(x[0])==int ,v_dict.items()))
    for state, values in sorted_v(all_v_dict):
        print(f"{state:2} :", end='')
        for value in values:
            print(f"{value:^15.3}", end='')
        print()
# Modèle représentant la logique du jeu
class GameModel:
    def __init__(self, nb_matches, player1, player2, displayable = False):
        """
        Constructeur du comportement d'une partie:
            
            attributs: 
                - nombre d'allumettes en début de partie (INT)
                - nombre d'allumettes en cours (INT)
                - liste des joueurs engagé dans la partie (PLAYER)
                - joueur en cours dans la partie (PLAYER)
                - test pour décider si la partie doit être affichée par tkinter (BOOL)
           
            Rempli aussi la liste des joueurs avec les joueurs inscrits dans la partie
            et choisi aléatoirement un des joueurs inscrits pour commencer la partie

        """
        
        self.original_nb = self.nb = nb_matches
        self.players = [player1, player2]
        self.current_player = 0  # indique quel joueur joue actuellement
        self.displayable = displayable
        for player in self.players:
            player.game = self
        self.shuffle()
    def display(self): 
        """
        Si la partie doit être affichée, affiche le nombre actuel d'allumettes
        """
        if self.displayable:
            print(f"Current number of matches: {self.nb}")
    def play(self):
        """
        Lance la partie, et répète l'algorithme tant qu'il reste une allumette:
            - Choisis le premier joueur à jouer (assigné aléatoirement), le fait jouer et fait avancer la partie
            - Vérifie ensuite si la partie n'est pas finie. Dans ce cas-là, décide du gagnant et perdant
            - sinon, change de joueur actif
        """
        current_player = 0
        while self.nb > 0:
            self.display()
            action = self.players[current_player].play(self.nb)
            self.step(action) 
    
            #check si le jeu doit se terminer
            if self.nb <= 0:
                self.players[current_player].win()
                self.players[1 - current_player].lose() #1 - current_player" pour basculer entre deux joueurs où current_player est 0 ou 1. Si current_player = 0, alors 1 - 0 devient 1 et inversement
            else:
                #changez de joueur si le jeu continue
                current_player = 1 - current_player
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
        
        argument:
            - nombre d'allumettes enlevées (INT)
        """
        self.nb -= action # action représente le nb de matches retirés
        
if( __name__ == '__main__'):
    player1= AI("Alice")
    player2= AI("Bob")
    player3= AI("Randy")
    player4 = Player("Basique")
    training(player1, player2,10000000, 10)
    training(player3, player4, 10000000, 10)
    compare_ai(player1,player2,player3)