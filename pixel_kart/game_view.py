# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 08:41:11 2025

@author: martin
"""
import tkinter as tk
from tkinter import Tk, ttk
import const

class GameEditor(tk.Toplevel):
    """
    Le Game Editor a pour but de paramétrer correctement la partie avec:
        - le choix de l'adversaire (un humain ou une IA)
        - le choix du circuit
        - le nombre de tours à finir avant la fin de la partie
        - le boutton de lanchement de jeu
    """
    def __init__(self, game_list, master):
        super().__init__(master)
        
    
        self.title("Game Settings")
        self.against_human = True
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
        
        
        ttk.Label(self.options_frame, text="Play against human: ").pack(side="left")

        #Passage par un string car tkinter ne gère pas bien un booléen
        self.against_human = tk.StringVar(value="Human")
        
        C1 = ttk.Radiobutton(
            self.options_frame, 
            text="Human", 
            variable=self.against_human, 
            value="Human",
            command=self.print_choice
        )
        
        C2 = ttk.Radiobutton(
            self.options_frame, 
            text="AI", 
            variable=self.against_human, 
            value="AI",
            command=self.print_choice
        )

        C1.pack()
        C2.pack()
        print("button return: ", self.against_human.get())
        
        ttk.Label(self.options_frame, text="loops count:").pack(side="left", padx=5)
        self.loops_entry = ttk.Entry(self.options_frame, textvariable="3", width=5)
        self.loops_entry.pack(side="left")
        self.submit_callback = None  # le controller pourra donner une fonction
    
   
        launch_frame = tk.Frame(self)
        launch_frame.pack()
        launch_game_button = tk.Button(launch_frame,text="Launch Game", command = self.submit_game_parameters)
        launch_game_button.pack()

    def print_choice(self):
        print("button return: ", self.against_human.get())
    
    def launch_game(self):
        selected_circuit = self.select_circuit.get()
        print("is human : ", self.against_human.get())
        GameInterface(
            circuit=self.all_circuits.get(selected_circuit, None),
            loops_count=self.loops_count,
            against_human=self.against_human.get(),
            players=[None, None]
        ).mainloop()


   
    def submit_game_parameters(self):

        self.loops_count = int(self.loops_entry.get())
        selected_circuit = self.select_circuit.get()
    
        if self.submit_callback:
            self.submit_callback(selected_circuit, self.loops_count, self.against_human.get())
    
class GameInterface(tk.Toplevel):
    def __init__(self, controller, loops_count,against_human,circuit=None,players=[None, None]):
        super().__init__()

        self.controller = controller
        self.title("Game Interface")
        self.geometry("800x600")  
        self.cells = []

        self.circuit = circuit
        
        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack(side="left")
        
        self.loops_count = loops_count
        self.against_human = against_human
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
        if self.against_human == "Human":
            self.draw_player_inputs(self.players[1], is_left=False)
        else:
            self.draw_player_infos(self.players[1], is_left=False)

        self.draw_grid(circuit, players)        

        
    def init_cells(self):
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
        frame = tk.Frame(self.main_frame, bg="white", width=200)
        frame.pack(side='left' if is_left else 'right', fill='y')

        tk.Label(frame, text='Kart').pack()
        tk.Label(frame, text= str(self.controller.model.current_kart))
        tk.Label(frame, text='Direction: ').pack()
        tk.Label(frame, text='Speed: ').pack()
        tk.Label(frame, text='Turns done: ').pack()

    def draw_player_inputs(self, player, is_left=True):



        input_frame = tk.Frame(self.main_frame, bg="lightblue", width=200)
        input_frame.pack(side='left' if is_left else 'right', fill='y')

        tk.Label(input_frame, text="Play").pack()
        tk.Button(input_frame, text="Accelerate", command=lambda: self.controller.move_kart(does_accelerate = True), bg="green").pack()
        tk.Button(input_frame, text="Turn left", command=lambda: self.controller.model.turn(self.controller.model.karts[0], -1), bg="blue").pack()
        tk.Button(input_frame, text="Turn right", command=lambda: self.controller.model.turn(self.controller.model.karts[0], 1), bg="blue").pack()

        tk.Button(input_frame, text="Brake", command=lambda: self.controller.model.karts[self.controller.model.current_kart].brake, bg="red").pack()
        tk.Button(input_frame, text="Skip",command=lambda: self.controller.move_kart(does_accelerate = False), bg="purple").pack()

        self.draw_player_infos(player, is_left)

                
        
    
    def clear(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        self.cells.clear()


    def draw_grid(self, circuit,players):
        """
        Affiche le circuit à partir d'une grille 2D de caractères.
        Chaque caractère représente un type de terrain.
        
        Arguments:
            grid (list[list[str]]): Grille du circuit
        """
        if not circuit:
            print("No circuit data")
            return
    
        self.rows = len(circuit.grid)
        self.cols = len(circuit.grid[0]) if circuit.grid else 0
        self.clear()
        self.init_cells()
    
        color_map = dict((v["letter"], v["color"]) for v in const.PIXEL_TYPES.values())
    
        for i, row in enumerate(circuit.grid):
            for j, char in enumerate(row):
                if i < len(self.cells) and j < len(self.cells[i]):
                    color = color_map.get(char, "grey")  # Si lettre inconnue, met en gris
                    self.cells[i][j].config(bg=color)
        
        for elem in players:
            #type(elem) = Kart
            #accéder à la position du kart
            self.cells[elem.position[1]][elem.position[0]].config(bg="red")

    def data_to_dto(self):
        """
        Return the grid as a string look like "rgc,rgc,rgc".
        """
        export_result = []
        color_map = dict((v["color"], v["letter"]) for v in const.PIXEL_TYPES.values())
        for row in self.cells:
            export_result.append("".join(color_map[cell.cget("bg")] for cell in row))
        return ",".join(export_result)
    
    
# if __name__ == '__main__':
#     newEditor = GameEditor()
#     newEditor.mainloop()
    # newGame = GameInterface()
    # newGame.mainloop()