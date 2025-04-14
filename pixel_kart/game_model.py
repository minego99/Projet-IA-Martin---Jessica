# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 11:35:30 2025

@author: martin
"""
from model.kart import Kart
from model.circuit import Circuit

class game():
    """
    Classe reprennant la logique de l'interaction entre le circuit et un kart.
    arguments:
        - le nombre de tours pour gagner la partie(INT)
        - le nombre de tours déjà écoulés (INT)
    """
    def __init__(self,laps,time,circuit = None, karts = None):
        self.laps = laps
        self.time = time
        self.circuit = circuit
        self.karts = karts
        
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
        for i in range(current_player.speed):
            # Prévoir la prochaine position
            next_pos = current_player.predict_next_position()
            terrain = self.circuit.get_terrain_type(next_pos)

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
