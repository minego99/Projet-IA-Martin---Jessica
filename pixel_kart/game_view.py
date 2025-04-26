# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 08:41:11 2025

@author: martin
"""
import tkinter as tk
from tkinter import Tk, ttk


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
        C1 = ttk.Checkbutton(self.options_frame, text = "Human", variable = self.against_human, \
           onvalue = self.against_human == True, offvalue=self.against_human == False,  \
           width = 20, )
        C2 = ttk.Checkbutton(self.options_frame, text = "AI", variable = self.against_human, \
           onvalue = self.against_human == False, offvalue =self.against_human == True,  \
           width = 20)
        C1.pack()
        C2.pack()
        
        
        ttk.Label(self.options_frame, text="loops count:").pack(side="left", padx=5)
        self.loops_entry = ttk.Entry(self.options_frame, textvariable="3", width=5)
        self.loops_entry.pack(side="left")
        self.submit_callback = None  # le controller pourra donner une fonction
    
        button= ttk.Button(self.options_frame, text= "Submit game parameter", command=self.submit_game_parameters)
        button.pack(side="left")


        
        launch_frame = tk.Frame(self)
        launch_frame.pack()
        launch_game_button = tk.Button(launch_frame,text="Launch Game", command = self.launch_game)
        launch_game_button.pack()
        
        


    def launch_game(self):
        selected_circuit = self.select_circuit.get()
        is_human = self.against_human
    
        GameInterface(
            circuit=self.all_circuits.get(selected_circuit, None),
            loops_count=self.loops_count,
            against_human=is_human,
            players=[None, None]
        ).mainloop()


   
    def submit_game_parameters(self):
        # Met à jour les attributs
        self.loops_count = int(self.loops_entry.get())
        self.against_human = True if self.against_human else False  # corriger au passage
        selected_circuit = self.select_circuit.get()
    
        if self.submit_callback:
            self.submit_callback(selected_circuit, self.loops_count, self.against_human)
    
        self.destroy()  # ferme la fenêtre une fois validé

class GameInterface(tk.Toplevel):
    def __init__(self, loops_count,circuit=None, against_human=True, players=[None, None]):
        super().__init__()

        self.title("Game Interface")
        self.geometry("800x300")  

        self.circuit = circuit
        self.loops_count = loops_count
        self.against_human = against_human
        self.players = players

        # Frame principale pour contenir tous les panneaux côte à côte
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill='both', expand=True)

        # Frame pour les infos de la course
        self.race_frame = tk.Frame(self.main_frame, bg="lightgrey", width=200)
        self.race_frame.pack(side='left', fill='y')

        self.turns_done_text = tk.Label(self.race_frame, text="Time:")
        self.turns_done_text.pack()

        self.loop_to_do_text = tk.Label(self.race_frame, text=f'Turns to do: {self.loops_count}')
        self.loop_to_do_text.pack()

        # Frame pour le joueur 1 (humain ou IA)
        self.draw_player_inputs(self.players[0], is_left=False)

        # Frame pour le joueur 2 (humain ou IA)
        if self.against_human:
            self.draw_player_inputs(self.players[1], is_left=False)
        else:
            self.draw_player_infos(self.players[1], is_left=False)

    def draw_player_infos(self, player, is_left=True):
        frame = tk.Frame(self.main_frame, bg="white", width=200)
        frame.pack(side='left' if is_left else 'right', fill='y')

        tk.Label(frame, text='Kart').pack()
        tk.Label(frame, text='Direction: ').pack()
        tk.Label(frame, text='Speed: ').pack()
        tk.Label(frame, text='Turns done: ').pack()

    def draw_player_inputs(self, player, is_left=True):


        # Puis les inputs dans une frame séparée
        input_frame = tk.Frame(self.main_frame, bg="lightblue", width=200)
        input_frame.pack(side='left' if is_left else 'right', fill='y')

        tk.Label(input_frame, text="Play").pack()
        tk.Button(input_frame, text="Accelerate", command=None, bg="green").pack()
        tk.Button(input_frame, text="Turn left", command=None, bg="blue").pack()
        tk.Button(input_frame, text="Turn right", command=None, bg="blue").pack()
        tk.Button(input_frame, text="Brake", command=None, bg="red").pack()
        tk.Button(input_frame, text="Skip", command=None, bg="purple").pack()
        # D'abord les infos
        self.draw_player_infos(player, is_left)
        
    def draw_grid(self):
        """
        affiche le terrain sélectionné dans l'éditeur de partie
        le terrain est déjà envoyé dans la view comme une chaîne de caractères (interprétée d'abord par le modèle,
        ensuite envoyé dans le view)
        """
        
        
# if __name__ == '__main__':
#     newEditor = GameEditor()
#     newEditor.mainloop()
    # newGame = GameInterface()
    # newGame.mainloop()