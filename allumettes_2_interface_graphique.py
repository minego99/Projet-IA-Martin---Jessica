import random
import tkinter as tk

# Joueur (en général)
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


# Vue représentant l'interface graphique du jeu
class GameView(tk.Tk):
    def __init__(self, controller):
        """
        Constructeur de la gestion graphique du jeu:
            hérite de:
                - Tkinter.TK
            argument:
                GameController du jeu en cours
            attributs: 
                - comportement de la partie en cours
                - titre de la partie 
                - canvas du jeu (300px sur 300px)
                - chaîne de caractères indiquant le nom du joueur actif 
                - cadre pour les bouttons du jeu
           
            Rempli aussi le cadre de 3 bouttons pour les 3 actions possible
            Tous les widgets Tkinter sont assemblés et le visuel est actualisé

        """
        super().__init__() # héritage de tk.Tk
        
        self.controller = controller
        self.title("Game of Matches")
        
        # Canvas pour afficher les allumettes
        self.canvas = tk.Canvas(self, width=300, height=200)
        self.canvas.pack()
        
        # Label pour afficher l'état du jeu : qui doit jouer + qui a gagné / perdu
        self.message_label = tk.Label(self, text="", font=("Arial", 14))
        self.message_label.pack()
        
        # Frame contenant les boutons
        self.buttons_frame = tk.Frame(self) # Frame -> widget Tkinter pour contenir et organiser d'autre widget, comme Button 
        self.buttons_frame.pack()
        
        # Création des boutons pour retirer de 1 à 3 allumettes
        for i in range(0, 3):
            btn = tk.Button(self.buttons_frame, text=f"Remove {i}", command=lambda n=i: self.controller.handle_human_move(n))  
            btn.pack(side=tk.LEFT) #  place chaque bouton dans la buttons_frame en les disposant horizontalement
        
        self.update_view()

    def update_view(self):
        """
        Actualise l'affichage du jeu:
            - supprime le contenu précédant du canvas
            - actualise le nombre d'allumettes restantes et les dessine
            - actualise le message affichant le joueur actif
        """
        # Met à jour l'affichage du jeu
        # Nécessaire ?
        self.canvas.delete("all")  # efface le canvas avant de redessiner
        nb_matches = self.controller.get_nb_matches()
        self.draw_matches(nb_matches)
        self.message_label.config(text=self.controller.get_status_message()) # méthode config de Tkinter utilisée pour changer le texte dans le Label

    def draw_matches(self, nb):
        """
        Dessine les allumettes en fonction du nombre d'allumettes restantes
        argument:
            - nombre d'allumettes restantes
        Pour chaque allumette restante, dessine une ligne et un oval et les place à des coordonnées fixes par rapport à leur nombre
        (première allumette en position 1, deuxième allumette en position 2, etc...)
        """
        # Dessine le nombre d'allumettes sur le canvas
        for i in range(nb):
            x = 20 + i * 30 # x = poistion horizontale. 20 px depuis le bord gauche puis chaque allumette à 30 px de la précédente
            # Corps de l'allumette
            self.canvas.create_line(x, 50, x, 150, width=5, fill="brown") # (x, 50) : point départ (x position horizontale à 50 px haut) et (x, 150) : point arrivée (x horizontale à 150 px du haut).
            # Tête de l'allumette (oval)
            self.canvas.create_oval(x - 5, 30, x + 5, 50, fill="red", outline="black") # (x - 5, 30) : coin supérieur gauche (5 px à gauche de x et 30 pixels du haut) et (x + 5, 50) : coin inférieur droit (5 px à droite de x et 50 pxdu haut).
    
    def end_game(self):
        """
        Dessine l'écran de fin de partie
        Supprime les bouttons de jeu
        Affiche un bouton capable de recommencer la partie
        """
        # Affiche l'écran de fin de partie
        for widget in self.buttons_frame.winfo_children(): # récupération des éléments de la frame
            widget.destroy() # déstruction de ceux-ci un à un
        reset_btn = tk.Button(self.buttons_frame, text="Recommencer", command=self.controller.reset_game)
        reset_btn.pack()

    def reset(self):
        """
        Permet de recommencer une nouvelle partie
        Supprime tous les widgets dans le canvas
        Actualise l'affichage
        
        """
        # Réinitialise l'affichage pour recommencer une partie
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        for i in range(0, 3):
            btn = tk.Button(self.buttons_frame, text=f"Remove {i}", command=lambda n=i: self.controller.handle_human_move(n))  
            btn.pack(side=tk.LEFT)
        self.update_view()


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

