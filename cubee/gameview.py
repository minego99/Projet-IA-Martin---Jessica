import tkinter as tk

"""
La classe contient tout le nécessaire pour l'affichage du jeu.
Elle prend en compte les paramètres de la classe gamecontroller pour les interpréter et les appliquer dans le package tkinters
"""
class CubeeGameView:
    
    def __init__(self, root, controller, dimensions=5):
        """
        Constructeur de la gestion graphique du jeu:

            argument:
                - Source de la fenêtre (TKINTER.TK)
                - Game controller de la partie (CONTROLLER)
                - Dimensions du tableau (par défaut =5) (INT)
            attributs: 
                - Plateau de jeu, vide au début mais rempli procéduralement ([[STR]])
                - Positions des deux joueurs en début de partie ({STR : NONE, STR: NONE})
                - canvas du jeu (CANVAS)
            Dessine le plateau de jeus
            Prépare les événements en cas d'inputs du joueur

        """
        self.root = root
        self.controller = controller
        self.dimensions = dimensions
        self.cells = []
        self.player_positions = {"P1": None, "P2": None}  # Stockage des positions actuelles
        
        self.canvas = tk.Frame(root)
        self.canvas.pack()
        
        self.draw_terrain()

        # Association touches directionnelles pour déplacements
        self.root.bind("<Up>", lambda event: self.controller.handle_player_move("up"))
        self.root.bind("<Down>", lambda event: self.controller.handle_player_move("down"))
        self.root.bind("<Left>", lambda event: self.controller.handle_player_move("left"))
        self.root.bind("<Right>", lambda event: self.controller.handle_player_move("right"))
    
    def draw_terrain(self):
        """
        Création du plateau, affiche des cases blanches avec un écart standard en fonction des dimensions insérées dans le constructeur de la partie
        """
        for row in range(self.dimensions):
            row_cells = []
            for col in range(self.dimensions):
                cell_canvas = tk.Canvas(self.canvas, width=60, height=60, bg="white", highlightthickness=1, relief="solid")
                cell_canvas.grid(row=row, column=col, padx=2, pady=2)
                row_cells.append(cell_canvas)
            self.cells.append(row_cells)
    
    def draw_player(self, player, position):
        """
        Affiche l'icône du joueur actif à l'emplacement actuel du joueur actif
        arguments:
            - Le joueur actif
            - La position du joueur actif
        """
        row, col = position
        cell_canvas = self.cells[row][col]
        
        color = "#9b59b6" if player == "P1" else "#3498db"
        
        # Tête
        cell_canvas.create_oval(10, 10, 50, 50, fill=color, outline="black", tags="player")
        
        # Yeux
        cell_canvas.create_oval(22, 22, 26, 28, fill="black", tags="player")  # Œil gauche
        cell_canvas.create_oval(34, 22, 38, 28, fill="black", tags="player")  # Œil droit
        
        # Bouche
        cell_canvas.create_arc(22, 35, 38, 45, start=180, extent=180, style=tk.ARC, outline="black", width=2, tags="player")
    
    def update_view(self, cases):
        """
        Màj du plateau avec personnages et coloriage des cases
        
        argument:
            - plateau de jeu ([[STR]])
            
        Cherche la position des joueurs et colorie la case où ils se situent
        Affiche la position des nouveaux joueurs
        Enlève l'icône des joueurs de leur ancienne positions
        
        """
        new_positions = {"P1": None, "P2": None}
        
        for row in range(self.dimensions):
            for col in range(self.dimensions):
                cell_canvas = self.cells[row][col]
                
                if cases[row][col] == "P1":
                    new_positions["P1"] = (row, col)
                    cell_canvas.config(bg="#9b59b6")  # Coloriage case joueur 1
                elif cases[row][col] == "P2":
                    new_positions["P2"] = (row, col)
                    cell_canvas.config(bg="#3498db")  # Coloriage case joueur 2
                
        # Suppression ancien dessin du joueur
        for player, old_pos in self.player_positions.items():
            if old_pos and old_pos != new_positions[player]:
                self.cells[old_pos[0]][old_pos[1]].delete("player")
        
        # Dessin des joueurs sur leur nouvelle position
        for player, new_pos in new_positions.items():
            if new_pos:
                self.draw_player(player, new_pos)
                
        # Màj positions joueurs
        self.player_positions = new_positions.copy()
    
    def draw_endgame(self, message):
        """
        Message de fin de partie
        argument:
            - message à afficher (STR)
        
        """
        end_label = tk.Label(self.root, text=message, font=("Arial", 14))
        end_label.pack()
    
    def reset_game(self):
        """
        Réinitialisation de l'affichage du plateau
        Les joueurs sont enlevés du plateau
        toutes les cellules du plateau redeviennent blanches
        """
        self.player_positions = {"P1": None, "P2": None}  # Réinitialisation des positions
        for row in range(self.dimensions):
            for col in range(self.dimensions):
                cell_canvas = self.cells[row][col]
                cell_canvas.delete("all")
                cell_canvas.config(bg="white")  # Rétabissemnt du fond blanc
