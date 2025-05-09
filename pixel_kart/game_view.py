# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 08:41:11 2025

@author: martin
"""
import tkinter as tk
from tkinter import Tk, ttk
import pixel_kart.const

class GameEditor(tk.Toplevel):
    """
    Le Game Editor a pour but de paramétrer correctement la partie avec:
        - le choix de l'adversaire (un humain ou une IA)
        - le choix du circuit
        - le nombre de tours à finir avant la fin de la partie
        - le boutton de lanchement de jeu
    Gère aussi le lancement d'une fenêtre supperposée sans casser l'éditeur de partie
    """
    def __init__(self, game_list, master):
        super().__init__(master)
        
    
        self.title("Game Settings")
        self.against_AI = False
        self.loops_count = None
    
        self.all_circuits = game_list
        
        self.circuit_frame = tk.Frame(self)
        self.circuit_frame.pack(pady=5, fill="x")
        self.circuits_text = tk.Label(self.circuit_frame,text="circuits choice:")
        self.circuits_text.pack(side="left")
        self.select_circuit = tk.StringVar()
        
        self.circuit_dropdown = tk.OptionMenu(self.circuit_frame, self.select_circuit, *list(self.all_circuits.keys()))
        self.circuit_dropdown.pack(side="left", padx=5)
        self.select_circuit.set(list(self.all_circuits.keys())[0] if self.all_circuits.keys() else "")
        
        
        
        self.options_frame = tk.Frame(self)
        self.options_frame.pack(pady=5, fill="x")
        
        
        ttk.Label(self.options_frame, text="Play against AI: ").pack(side="left")

        #Passage par un string car tkinter ne gère pas bien un booléen
        self.against_AI = tk.StringVar(value="Human")
        
        C1 = ttk.Radiobutton(
            self.options_frame, 
            text="Human", 
            variable=self.against_AI, 
            value="Human",
            command=self.print_choice
        )
        
        C2 = ttk.Radiobutton(
            self.options_frame, 
            text="AI", 
            variable=self.against_AI, 
            value="AI",
            command=self.print_choice
        )

        C1.pack()
        C2.pack()
        print("button return: ", self.against_AI.get())
        
        ttk.Label(self.options_frame, text="loops count:").pack(side="left", padx=5)
        self.loops_entry = ttk.Entry(self.options_frame, textvariable="3", width=5)
        self.loops_entry.pack(side="left")
        self.submit_callback = None  # le controller pourra donner une fonction
    
   
        launch_frame = tk.Frame(self)
        launch_frame.pack()
        launch_game_button = tk.Button(launch_frame,text="Launch Game", command = self.submit_game_parameters)
        launch_game_button.pack()

    def print_choice(self):
        """
        Fonction de debug, pour vérifier le retour d'un bouton ne fonctionnant pas toujours correctement
        """
        print("button return: ", self.against_AI.get())
    
    def launch_game(self):
        """
        Lance l'interface de la partie, à l'aide des informations du GameEditor lancé
        """
        selected_circuit = self.select_circuit.get()
        print("against AI : ", self.against_AI.get())
        GameInterface(
            circuit=self.all_circuits.get(selected_circuit, None),
            loops_count=self.loops_count,
            against_AI=self.against_AI.get(),
            players=[None]
        ).mainloop()


   
    def submit_game_parameters(self):
        """
        Fonction de callback, convertissant les données nécessaires pour l'interface de jeu
        """

        self.loops_count = int(self.loops_entry.get())
        selected_circuit = self.select_circuit.get()
    
        if self.submit_callback:
            self.submit_callback(selected_circuit, self.loops_count, self.against_AI.get())
    
class GameInterface(tk.Toplevel):

    def __init__(self, controller, loops_count,against_AI,circuit=None,players=[None, None]):
        """
        Interface de jeu, affichant les boutons, les informations de la partie ainsi que le circuit avec les karts joueurs
        hérite de:
            - Toplevel, permet de lancer des fenêtres tkinter superposées
        arguments:
            - gestionnaire de la partie (GAMEMANAGER)
            - nombre de tours (INT)
            - choix du joueur de jouer contre un humain ou une IA (BOOL)
            - circuit choisi par le joueur
            - les deux joueurs dans la partie
        affiche les deux sets de bouttons seulement si le joueur veut joueur contre un humain
        affiche aussi les données de chaque kart (vitesse, orientation, tours restants)
        Dessine la grille de pixels représentant le circuit avec les karts dessus
        """
        
        super().__init__()
        self.controller = controller
        print("kart count: ",len(self.controller.model.karts))

        self.title("Game Interface")
        self.geometry("800x600")  
        self.cells = []

        self.circuit = circuit
        
        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack(side="left")
        
        self.loops_count = loops_count
        self.controller.model.total_laps = loops_count
        self.against_AI = against_AI
        self.players = players


        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill='both', expand=True)


        self.race_frame = tk.Frame(self.main_frame, bg="lightgrey", width=200)
        self.race_frame.pack(side='left', fill='y')

        self.turns_done_text = tk.Label(self.race_frame, text="Time:")
        self.turns_done_text.pack()

        self.loop_to_do_text = tk.Label(self.race_frame, text=f'Turns to do: {self.loops_count}')
        self.loop_to_do_text.pack()

        # Frame pour le joueur 1 (humain)
        self.draw_player_inputs(self.players[0], is_left=False)

        # Frame pour le joueur 2 (humain ou IA)
        if self.against_AI != "Human":
            self.draw_player_infos(self.players[1], is_left=False)

        self.draw_grid(circuit, players)        

        
    def init_cells(self):
        """
        dessine la grille de pixels en fonction des dimensions du circuit
        """
        self.cells = []
        print("rows: ", self.rows, " cols: ", self.cols)
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                cell = tk.Label(self.grid_frame, width=2, height=1, borderwidth=1, relief="solid")
                cell.grid(row=i, column=j)
                row.append(cell)
            self.cells.append(row)

    def draw_player_infos(self, player, is_left=True):
        """
        affiche les informations propre à un joueur
        arguments:
            - le joueur concerné (KART)
            - l'alignement de ses informations sur le canvas (gauche/droite) (BOOL)
        """
        frame = tk.Frame(self.main_frame, bg="white", width=200)
        frame.pack(side='left' if is_left else 'right', fill='y')

        tk.Label(frame, text='Kart').pack()
        tk.Label(frame, text= str(self.controller.model.current_kart))
        tk.Label(frame, text='Direction: ').pack()
        tk.Label(frame, text='Speed: ').pack()
        tk.Label(frame, text='Turns done: ').pack()

    def draw_player_inputs(self, player, is_left=True):

        """
        affiche les bouttons utilisable par le joueur
        arguments:
            - Le joueur concerné (KART)
            - l'alignement de ses bouttons sur le canvas (gauche/droite) (BOOL)
        """

        input_frame = tk.Frame(self.main_frame, bg="lightblue", width=200)
        input_frame.pack(side='left' if is_left else 'right', fill='y')

        tk.Label(input_frame, text="Play").pack()
        tk.Button(input_frame, text="Accelerate", command=lambda: self.controller.move_kart(acceleration = 1), bg="green").pack()
        tk.Button(input_frame, text="Turn left", command=lambda: self.controller.turn_kart(-1), bg="blue").pack()
        tk.Button(input_frame, text="Turn right", command=lambda: self.controller.turn_kart(1), bg="blue").pack()

        tk.Button(input_frame, text="Brake", command=lambda: self.controller.move_kart(acceleration = -1), bg="red").pack()
        tk.Button(input_frame, text="Skip",command=lambda: self.controller.move_kart(acceleration = 0), bg="purple").pack()

        self.draw_player_infos(player, is_left)

                
        
    
    def clear(self):
        """
        Fonction permettant de supprimer tout le contenu dans un canvas
        """
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        self.cells.clear()


    def draw_grid(self, circuit,players):
        """
        Affiche le circuit à partir d'une grille 2D de caractères.
        Chaque caractère représente un type de terrain.
        
        arguments:
            - objet circuit, utilisé pour obtenir sa grille contenant la couleur de toutes les cases (CIRCUIT)
            - liste comprenant les deux joueurs pour pouvoir les afficher (KART)
        """
        if not circuit:
            print("No circuit data")
            return
    
        self.rows = len(circuit.grid)
        self.cols = len(circuit.grid[0]) if circuit.grid else 0
        self.clear()
        self.init_cells()
    
        color_map = dict((v["letter"], v["color"]) for v in pixel_kart.const.PIXEL_TYPES.values())
    
        for i, row in enumerate(circuit.grid):
            for j, char in enumerate(row):
                if i < len(self.cells) and j < len(self.cells[i]):
                    color = color_map.get(char, "grey")  # Si lettre inconnue, met en gris
                    self.cells[i][j].config(bg=color)
         
        # Affiche les karts
        for i, kart in enumerate(self.controller.model.karts):
            print("kart count: ",len(self.controller.model.karts))
            color = "red" if i == 0 else "blue"
            self.cells[kart.position[1]][kart.position[0]].config(bg=color)



    def data_to_dto(self):
        """
        Converti La matrice du circuit en une chaîne de caractères
        """
        export_result = []
        color_map = dict((v["color"], v["letter"]) for v in pixel_kart.const.PIXEL_TYPES.values())
        
        for row in self.cells:
            export_result.append("".join(color_map[cell.cget("bg")] for cell in row))
            
        return ",".join(export_result)
    
    
# if __name__ == '__main__':
#     newEditor = GameEditor()
#     newEditor.mainloop()
    # newGame = GameInterface()
    # newGame.mainloop()