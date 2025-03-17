import tkinter as tk

class CubeeGameView:
    def __init__(self, root, controller, dimensions=5):
        self.root = root
        self.controller = controller
        self.dimensions = dimensions
        self.cells = []
        self.initial_positions = {"P1": None, "P2": None}  # Stockage des positions initiales
        
        self.canvas = tk.Frame(root)
        self.canvas.pack()
        
        self.draw_terrain()

        # Association touches directionnelles pour déplacements
        self.root.bind("<Up>", lambda event: self.controller.handle_player_move("up"))
        self.root.bind("<Down>", lambda event: self.controller.handle_player_move("down"))
        self.root.bind("<Left>", lambda event: self.controller.handle_player_move("left"))
        self.root.bind("<Right>", lambda event: self.controller.handle_player_move("right"))
    
    def draw_terrain(self):
        """Création du plateau"""
        for row in range(self.dimensions):
            row_cells = []
            for col in range(self.dimensions):
                cell_canvas = tk.Canvas(self.canvas, width=60, height=60, bg="white", highlightthickness=1, relief="solid")
                cell_canvas.grid(row=row, column=col, padx=2, pady=2)
                row_cells.append(cell_canvas)
            self.cells.append(row_cells)
    
    def draw_player(self, player, position):
        """Dessin du bonhomme joueur uniquement sur la case de départ"""
        row, col = position
        cell_canvas = self.cells[row][col]
        cell_canvas.delete("player")  # Supprimer uniquement le bonhomme
        
        color = "#9b59b6" if player == "P1" else "#3498db"
        
        # Tête
        cell_canvas.create_oval(10, 10, 50, 50, fill=color, outline="black", tags="player")
        
        # Yeux
        cell_canvas.create_oval(22, 22, 26, 28, fill="black", tags="player")  # Œil gauche
        cell_canvas.create_oval(34, 22, 38, 28, fill="black", tags="player")  # Œil droit
        
        # Bouche 
        cell_canvas.create_arc(22, 35, 38, 45, start=180, extent=180, style=tk.ARC, outline="black", width=2, tags="player")
    
    def update_view(self, cases):
        """Màj du plateau avec personnages et coloriage des cases"""
        for row in range(self.dimensions):
            for col in range(self.dimensions):
                cell_canvas = self.cells[row][col]
                
                if cases[row][col] == "P1":
                    if self.initial_positions["P1"] is None:
                        self.initial_positions["P1"] = (row, col)  # Enregistrer la position initiale
                    cell_canvas.config(bg="#9b59b6")  # Colorier la case du joueur 1
                
                elif cases[row][col] == "P2":
                    if self.initial_positions["P2"] is None:
                        self.initial_positions["P2"] = (row, col)  # Enregistrer la position initiale
                    cell_canvas.config(bg="#3498db")  # Colorier la case du joueur 2
                
                elif cell_canvas["bg"] not in ("#9b59b6", "#3498db"):
                    cell_canvas.config(bg="white")  # Garder les cases vides en blanc

        # Dessiner les joueurs uniquement sur leur case initiale
        if self.initial_positions["P1"]:
            self.draw_player("P1", self.initial_positions["P1"])
        if self.initial_positions["P2"]:
            self.draw_player("P2", self.initial_positions["P2"])
    
    def draw_endgame(self, message):
        """Message de fin de partie"""
        end_label = tk.Label(self.root, text=message, font=("Arial", 14))
        end_label.pack()
    
    def reset_game(self):
        """Réinitialisation de l'affichage du plateau"""
        self.initial_positions = {"P1": None, "P2": None}  # Réinitialiser les positions initiales
        for row in range(self.dimensions):
            for col in range(self.dimensions):
                cell_canvas = self.cells[row][col]
                cell_canvas.delete("all")
                cell_canvas.config(bg="white")  # Rétablir le fond blanc




