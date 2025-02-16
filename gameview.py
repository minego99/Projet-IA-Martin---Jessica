import tkinter as tk

"""
La classe contient tout le nécessaire pour l'affichage du jeu.
Elle prend en compte les paramètres de la classe gamecontroller pour les interpréter et les appliquer dans le package tkinters
"""

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
        for i in range(1, 4):
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
        for i in range(1, 4):
            btn = tk.Button(self.buttons_frame, text=f"Remove {i}", command=lambda n=i: self.controller.handle_human_move(n))  
            btn.pack(side=tk.LEFT)
        self.update_view()

