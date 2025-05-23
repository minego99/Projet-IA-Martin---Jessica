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
        self.loops_count = None
    
        self.all_circuits = game_list
        
        self.circuit_frame = tk.Frame(self)
        self.circuit_frame.pack(pady=5, fill="x")
        self.circuits_text = tk.Label(self.circuit_frame,text="circuits choice:")
        self.circuits_text.pack(side="left")
        self.select_circuit = tk.StringVar()
        
        self.circuit_dropdown = tk.OptionMenu(self.circuit_frame, self.select_circuit, *list(self.all_circuits.keys()))
        self.circuit_dropdown.pack(side="left", padx=5)
        self.select_circuit.set(list(self.all_circuits.keys())[0] if self.all_circuits.keys() else "Basic")
        
        
        self.options_frame = tk.Frame(self)
        
        
        ttk.Label(self.options_frame, text="Play against AI: ").pack(side="left")

        #Passage par un string car tkinter ne gère pas bien un booléen
        self.against_AI = tk.StringVar(value="Human")
        self.options_frame.pack(pady=5, fill="x")
                
        ttk.Label(self.options_frame, text="loops count:").pack(side="left", padx=5)
        self.loops_var = tk.StringVar(value="3")
        self.loops_entry = ttk.Entry(self.options_frame, textvariable=self.loops_var, width=5)

        self.loops_entry.pack(side="left")
        self.submit_callback = None  # le controller pourra donner une fonction
        
        launch_frame = tk.Frame(self)
        launch_frame.pack()
        launch_game_button = tk.Button(launch_frame,text="Launch Game without AI", command = self.submit_game_parameters_without_AI)
        launch_game_AI_button = tk.Button(launch_frame, text= "Launch Game with AI", command= self.submit_game_parameters_with_AI)

        launch_game_button.pack()
        launch_game_AI_button.pack()
        
        
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
        self.print_choice()
        GameInterface(
            circuit=self.all_circuits.get(selected_circuit, None),
            loops_count=self.loops_count,
            against_AI=self.against_AI,
            players=[None]
        ).mainloop()


   
    def submit_game_parameters_without_AI(self):
        """
        Fonction de callback, convertissant les données nécessaires pour l'interface de jeu
        """

        self.against_AI = "Human"
        self.loops_count = int(self.loops_entry.get())
        selected_circuit = self.select_circuit.get()
    
        if self.submit_callback:
            self.submit_callback(selected_circuit, self.loops_count, self.against_AI)
   
    def submit_game_parameters_with_AI(self):
        """
        Même fonctionnement que submit_game_parameters_without_AI, hormis le booléen modifié
        C'est de la duplication de code, c'est vraiment pas bien dans l'idée, mais les bouttons de sélection tkinter font vraiment n'importe quoi.
        C'est donc une mauvaise solution, mais au moins elle fonctionne'
        """

        self.against_AI = "AI"
        self.loops_count = int(self.loops_entry.get())
        selected_circuit = self.select_circuit.get()
    
        if self.submit_callback:
            self.submit_callback(selected_circuit, self.loops_count, self.against_AI)
    
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

        self.loop_to_do_text = tk.Label(self.race_frame, text=f'Turns to do: {self.loops_count}')
        self.loop_to_do_text.pack()

        # Frame pour le joueur 1 (humain)
        self.draw_player_inputs(self.players[0], is_left=False)

        # Frame pour le joueur 2 (humain ou IA)

        self.draw_grid(circuit, players)        

        
    def init_cells(self):
        """
        dessine la grille de pixels en fonction des dimensions du circuit
        """
        self.cells = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                cell = tk.Label(self.grid_frame, width=2, height=1, borderwidth=1, relief="solid")
                cell.grid(row=i, column=j)
                row.append(cell)
            self.cells.append(row)

    def draw_player_infos(self, player, is_left=True):
        """
        Affiche les informations propre à un joueur
        """
        frame = tk.Frame(self.main_frame, bg="white", width=200)
        frame.pack(side='left' if is_left else 'right', fill='y')
        if(player == self.controller.model.karts[1]):
            self.controller.model.current_kart +=1
            print("IA INFO")
        # Stocke la frame dans un attribut pour pouvoir la supprimer ensuite
        if is_left:
            self.player_info_frame_left = frame
        else:
            self.player_info_frame_right = frame
    
        tk.Label(frame, text='Kart').pack()
        tk.Label(frame, text='Player').pack()
    
        tk.Label(frame, text=str(self.controller.model.current_kart)).pack()
        tk.Label(frame, text='Direction: ').pack()
        tk.Label(frame, text=self.controller.model.get_current_kart().direction).pack()
    
        tk.Label(frame, text='Speed: ').pack()
        tk.Label(frame, text=self.controller.model.get_current_kart().speed).pack()
    
        tk.Label(frame, text='Turns done: ').pack()
        tk.Label(frame, text=self.controller.model.get_current_kart().laps_done).pack()

        tk.Label(frame, text='Time: ').pack()
        tk.Label(frame, text=self.controller.model.time).pack()

        if(player == self.controller.model.karts[1]):
            self.controller.model.current_kart -=1
            
    def remove_player_infos(self, is_left=True):
        if is_left and hasattr(self, 'player_info_frame_left') and self.player_info_frame_left:
            self.player_info_frame_left.destroy()
            self.player_info_frame_left = None
        elif not is_left and hasattr(self, 'player_info_frame_right') and self.player_info_frame_right:
            self.player_info_frame_right.destroy()
            self.player_info_frame_right = None

        

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
        tk.Button(input_frame, text="Accelerate", command=self.on_accelerate,bg="green").pack()
        tk.Button(input_frame, text="Turn left", command= self.play_turn_left, bg="blue").pack()
        tk.Button(input_frame, text="Turn right", command=self.play_turn_right, bg="blue").pack()

        tk.Button(input_frame, text="Brake", command=self.play_brake, bg="red").pack()
        tk.Button(input_frame, text="Skip",command= self.play_skip, bg="purple").pack()

        #self.draw_player_infos(player, is_left)
        
    def on_accelerate(self):
        
        self.remove_player_infos(is_left=True)
        self.remove_player_infos(is_left=False)

        self.controller.move_kart(acceleration=1)
        if(self.controller.model.against_AI):
            self.controller.move_smart_AI()
        self.draw_player_infos(self.players[0], is_left=False)
        self.draw_player_infos(self.players[1], is_left=True)

        
                
    def play_turn_left(self):
        self.remove_player_infos(is_left=True)
        self.remove_player_infos(is_left=False)

        self.controller.turn_kart(-1)
        if(self.controller.model.against_AI):
            self.controller.move_smart_AI()
        self.draw_player_infos(self.players[0], is_left=False)
        self.draw_player_infos(self.players[1], is_left=True)

    def play_turn_right(self):
        
        self.remove_player_infos(is_left=True)
        self.remove_player_infos(is_left=False)

        self.controller.turn_kart(1)
        if(self.controller.model.against_AI):
            self.controller.move_smart_AI()
        self.draw_player_infos(self.players[0], is_left=False)
        self.draw_player_infos(self.players[1], is_left=True)
             
    def play_brake(self):
        self.remove_player_infos(is_left=True)
        self.remove_player_infos(is_left=False)

        self.controller.move_kart(acceleration=-1)
        if(self.controller.model.against_AI):
            self.controller.move_smart_AI()
        self.draw_player_infos(self.players[0], is_left=False)
        self.draw_player_infos(self.players[1], is_left=True)

    def play_skip(self):
        self.remove_player_infos(is_left=True)
        self.remove_player_infos(is_left=False)

        self.controller.move_kart(acceleration=0)
        if(self.controller.model.against_AI):
            self.controller.move_smart_AI()
        self.draw_player_infos(self.players[0], is_left=False)
        self.draw_player_infos(self.players[1], is_left=True)

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
    