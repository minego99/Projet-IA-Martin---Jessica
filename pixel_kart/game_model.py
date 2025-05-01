# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 11:35:30 2025

@author: martin
"""

import pixelKart_dao as dao

class Kart:
    """
    Classe représentant un kart dans le jeu.
    Attributs:
        - position (tuple): position actuelle du kart (x, y)
        - speed (int): vitesse actuelle du kart
        - direction (str): direction actuelle ('up', 'down', 'left', 'right')
        - laps_done (int): nombre de tours effectués
        - has_crossed_line (bool): flag pour éviter d'ajouter plusieurs tours sur la ligne d'arrivée
    """
    def __init__(self, position=(0,0), speed=0, direction="right"):
        self.position = position
        self.speed = speed
        self.laps_done = 0
        self.has_crossed_line = False
        self.directions = ["left","up","right","down"]
        
        # la gestion de la direction se fait par l'index de la liste de la direction (0 pour la gauche, 1 pour le haut, 2 pour la droite et 3 pour le bas)
        self.direction = direction

    def predict_next_position(self):
        x, y = self.position
        if self.direction == "up":
            return (x, y - 1)
        elif self.direction == "down":
            return (x, y + 1)
        elif self.direction == "left":
            return (x - 1, y)
        elif self.direction == "right":
            return (x + 1, y)
        return self.position

    def advance(self):
        self.position = self.predict_next_position()

    def decide_action(self):
        pass  # À définir par l'IA ou les contrôles joueur

    def update_position(self):
        pass  # Peut inclure des animations, effets, etc.

    def brake(self):
        self.speed = 0


class Circuit:
    """
    Classe représentant le circuit.
    Attributs:
        - grid (list de listes): représentation du circuit avec les types de terrain
    """
    def __init__(self, grid):
        self.grid = grid

    def get_terrain_type(self, position):
        x, y = position
        if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0]):
            return self.grid[y][x]
        return "wall"  # En dehors de la grille, considéré comme mur
    
    def get_start_positions(self):
        finish_cells = []
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 'F':
                    finish_cells.append((x, y))

        return finish_cells
        

class Game():
    """
    Classe reprennant la logique de l'interaction entre le circuit et un kart.
    arguments:
        - le nombre de tours pour gagner la partie(INT)
        - le nombre de tours déjà écoulés (INT)
    """
    def __init__(self,laps = 0,time = 0,circuit = None, karts = None):
        self.laps = laps
        self.time = time
        self.circuit = dao.get_circuit_grid("Basic")
        self.karts = karts
        self.current_kart = 0
        self.submit_callback = None
        
    
    def modify_player_movement(self, current_player: 'Kart'):
        """
        adapte le mouvement du joueur qui vient de se déplacer en fonction de la case sur laquelle il arrive
        arguments:
            - le joueur actuel (PLAYER)
        Si le joueur est sur une route, il continue à avancer en fonction de sa vitesse
        Si le joueur est sur de l'herbe, diminue la vitesse pour ce déplacement de 1
        Si le joueur est devant un mur, sa vitesse est fixée à 0
        Si le joueur atteind une case de ligne d'arrivée par la gauche, augmente le nombre de tour de 1
        
        "has_crossed_line" est un drapeau booléen (flag) : 
            False -> le joueur n’a pas encore franchi la ligne depuis la dernière fois qu’il l’a quittée, on peut ajouter un tour
            True -> le joueur a déjà validé un tour en étant sur la ligne : on n'ajoute plus rien tant qu’il ne quitte pas la ligne
        """
        # Vérifie la direction et la vitesse du joueur
        print("test terrain 1")

        for i in range(self.get_current_kart().speed):
            # Prévoir la prochaine position
            print("test terrain 2")
            next_pos = current_player.predict_next_position()
            print("test terrain 3")

            terrain = self.circuit.get_terrain_type(next_pos)
            print("terrain: ",terrain)
            if terrain == "road":
                current_player.advance()

            if terrain == "grass" and i % 2 == 0:
                # Si terrain = herbe, et selon la condition, diminuer la vitesse et avancer
                if i % 2 == 0:
                    current_player.advance()
                
            elif terrain == "wall":
                # Si terrain = mur, arrêter la voiture
                current_player.speed = 0
                continue # On vérifie les autres cases mais sans avancer

            elif terrain == "finish_line":
                # Vérifie si on entre sur la ligne d’arrivée par la gauche et validation du tour une seule fois, même si le joueur reste plusieurs pas de vitesse sur la case "finish_line".
                if current_player.direction == "right" and not current_player.has_crossed_line:
                   current_player.laps_done += 1
                   current_player.has_crossed_line = True
                current_player.advance()  # Avance même sur la ligne
            else:
                current_player.advance()
    
            # Si le joueur quitte la ligne d’arrivée, on réinitialise le flag
            if terrain != "finish_line":
                current_player.has_crossed_line = False

    
    def start_game(self):
        """
        Démarre le jeu avec la voiture à une vitesse de 0 et la direction vers la droite.
        """
        for kart in self.karts:
            kart.speed = 0
            kart.direction = "right"
    
    def step(self):
        """
        Avance d’un pas dans le temps. Chaque kart avance automatiquement à la vitesse qu'il a,
        même si aucun input n'est donné.

        À chaque tick (seconde), on appelle:
        - decide_action() pour voir s’il y a une action du joueur
        - modify_player_movement() pour adapter en fonction du terrain (vitesse, mur, herbe, ligne d’arrivée)
        """
        self.time += 1
        for kart in self.karts:
            kart.decide_action() # Le joueur peut changer de direction ou accélérer
            self.modify_player_movement(kart) # Avance automatiquement à sa vitesse actuelle
            kart.update_position()

    def stop(self):
        """
        Arrête les karts en appelant la méthode brake()
        """
        for kart in self.karts:
            kart.brake()

    def number_laps(self):
        """
        renvoie le nombre de tours à faire pour qu'un joueur soit considéré comme gagnant
            renvoie: 
                - si il y a un joueur qui a un nombre de tours égal au nombre de tours fixés par la partie, True (BOOL)
                - Sinon, False
        """
        for kart in self.karts:
            if kart.laps_done >= self.laps:
                return True
        return False
    
    def reset(self):
        """
        Réinitialise le temps et les karts pour une nouvelle partie.
        """
        self.time = 0
        for kart in self.karts:
            kart.laps_done = 0
            kart.position = (0, 0)
            kart.speed = 0
            kart.has_crossed_line = False
    
    def player_count(self):
        """
        Retourne le nombre de joueurs dans la partie.
        """
        return len(self.karts)
    
    def get_all_circuits(self):
        return dao.get_all()
    
    def get_circuit(self, circuit_name):
        return dao.get_circuit_grid(circuit_name)

    def get_finish_lines(self):
        """
        Retourne une liste des positions (x, y) où le circuit contient une case 'F' (finish line).
        """
        finish_lines = []
        for y, row in enumerate(self.circuit):
            for x, char in enumerate(row):
                if char == 'F':
                    finish_lines.append((x, y))
        print("finish line debug: ", finish_lines)
        return finish_lines

    def accelerate(self, current_kart):
        current_kart.speed += 1
        
    def switch_current_kart(self):
        self.current_kart -= 1
        
    def get_current_kart(self):
        return self.karts[self.current_kart]
    
    def turn(self, current_kart, movement):
       new_direction_index = self.get_current_kart().directions.index(self.get_current_kart().direction) + movement
       
       if(new_direction_index >= 4):
            new_direction_index = 0
       current_kart.direction = self.get_current_kart().directions[new_direction_index]
       print(current_kart.direction)