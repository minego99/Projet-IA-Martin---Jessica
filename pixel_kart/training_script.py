# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 11:35:30 2025

@author: martin
"""
import pixelKart_dao as dao
import gameDAO as AI_dao
import random
import matplotlib.pyplot as plt


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
        """
        renvoie:
            - la nouvelle valeur à assigner à la position du kart en fonction de son orientation ([INT,INT])
        """
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
    
    def reverse_next_position(self):
        """
        renvoie:
            - la nouvelle valeur à assigner à la position du kart lorsqu'il recule en fonction de son orientation ([INT,INT])
        """
        x, y = self.position
        if self.direction == "up":
            return (x, y + 1)
        elif self.direction == "down":
            return (x, y - 1)
        elif self.direction == "left":
            return (x + 1, y)
        elif self.direction == "right":
            return (x - 1, y)
        return self.position
    
    def advance(self):
        """
        modifie la position en fonction du déplacement voulu 
        """
        self.position = self.predict_next_position()


class AI(Kart):
    """
    Classe du Kart agissant automatiquement selon le comportement d'une IA
    Hérite de:
        - Kart
    attributs:
        - epsilon-greedy (FLOAT)
        - alpha ( = learning-rate) (FLOAT)
        - gamma (FLOAT)
    """
    def __init__(self, position=(0,0), speed=0, direction="right", epsilon = 0.9, alpha = 0.1, gamma = 0.9):
     super().__init__(position, speed, direction)
    
     
     self.current_state = None
     self.epsilon = epsilon
     self.alpha = alpha
     self.gamma = gamma
     self.current_state = AI_dao.get_Qline_by_state("0")


    
    def choose_action(self,circuit,actions):
        """Choisit une action selon une stratégie ε-greedy."""
        state_id = AI_dao.encode_state(circuit.grid, self.position[0], self.position[1], self.direction, self.speed)
        q_values =  AI_dao.get_Qline_by_state(state_id)
    
        values = [
            q_values.accelerate,
            q_values.do_nothing,
            q_values.brake,
            q_values.turn_left,
            q_values.turn_right
        ]
 
            # Exploitation : choisir l'action avec la plus grande valeur Q
        max_index = values.index(max(values))
        return actions[max_index]
        
    def data_to_dto(self,circuit):
        """
        convertit l'état de la partie et le transforme en un dictionnaire avec les poids dedans
        """
        
        state_id = AI_dao.encode_state(circuit.grid, self.position[0],self.position[1],self.direction, self.speed)

        return{
        'state_id' : state_id,
        'accelerate': self.current_state.accelerate,
        'brake': self.current_state.brake,
        'turn_left': self.current_state.turn_left,
        'turn_right': self.current_state.turn_right,
        'do_nothing': self.current_state.do_nothing
            }
    

    
    def calculate_reward(self, state, time, actions_per_game, circuit):
        """
        Calcule la récompense basée sur la vitesse, progression, collisions, et distance.
        """
        reward = 0.0
    
        # Récompense de vitesse
        if self.speed == 2:
            reward += 2
        elif self.speed == 1:
            reward += 1
        else:
            reward -= 0.5  # Malus si à l'arrêt
    
        # Récompense de progression dans le temps
        reward += max(0, 2 - (actions_per_game - time) / 10)
    
        # Récompense si tour terminé
        if self.laps_done >= 1:
            reward += 10
        #si le kart est sorti du circuit
        if(self.position not in circuit):
            reward -= 10
        else:
            next_pos = self.predict_next_position()
            #malus s'il y a un mur devant lui
            if(circuit.grid[next_pos[0]][next_pos[1]] == 'W'):
                reward -= 10
            # léger malus s'il y a du gazon devant lui
            elif(circuit.grid[next_pos[0]][next_pos[1]] == 'G'):
                reward -= 1
            # bonus s'il reste sur la route
            elif(circuit.grid[next_pos[0]][next_pos[1]] == 'R'):
                reward += 1

        #second malus s'il est sur le bord de la carte
        if("XXXXXXXXX" in state):
            reward = -20

        return reward

    
    def update_q_table(self, previous_state, action, reward, new_state):
        """
        Met à jour la Q-table après un mouvement.
        sauvegarde le nouvel état avec les nouvelles valeurs dans la DB
        """
    
        # Obtenir les valeurs Q pour l'état suivant
        next_q_values = AI_dao.get_Qline_by_state(new_state)
        max_future_q = max([
            next_q_values.accelerate,
            next_q_values.do_nothing,
            next_q_values.brake,
            next_q_values.turn_left,
            next_q_values.turn_right
        ])
    
        # Obtenir les valeurs Q de l'état précédent
        current_q_values = AI_dao.get_Qline_by_state(previous_state)
    
        # Récupérer la Q-value actuelle selon l'action jouée 
        current_q = getattr(current_q_values, f"{action}")
    
        # Calcul de la nouvelle valeur Q
        new_q = current_q + self.alpha * (reward + self.gamma * max_future_q - current_q)
    
        # Mise à jour de la valeur correspondante
        setattr(current_q_values, f"{action}", new_q)

        AI_dao.save_qline(current_q_values.to_dto())
        
class Circuit:
    """
    Classe représentant le circuit.
    Attributs:
        - grid (list de listes): représentation du circuit avec les types de terrain
    """
    def __init__(self, grid):
        self.grid = grid

    def get_terrain_type(self, position):
        """
        à partir d'une position donnée, permet d'obtenir le caractère inscrit à cette position
        argument:
            - la positon donnée [INT, INT]
        renvoie:
            - le caractère de la position et si la position n'est pas dans le circuit, renvoie le charactère du mur (CHAR)
        """
        x, y = position
        if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0]):
            return self.grid[y][x]
        return "W"  # En dehors de la grille, considéré comme mur
    
    def get_start_positions(self):
        """
        Parcoure l'entièreté du circuit pour obtenir la ligne d'arrivée
        renvoie:
            - les positions des cases de ligne d'arrivée ([(INT,INT)])
        """
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
    def __init__(self,laps = 0,time = 0,circuit = None, karts = None, against_AI = False):
        self.current_player_index = 0  # Joueur 0 commence par défaut
        self.total_laps = laps
        self.time = time
        self.circuit = Circuit(dao.get_circuit_grid("Basic"))
        self.karts = [Kart()]
        self.current_kart = 0
        self.submit_callback = None
        self.against_AI = against_AI
    
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

            if terrain == "R":
                current_player.advance()

            elif terrain == "G" and i % 2 == 0:

                # Si terrain = herbe, et selon la condition, diminuer la vitesse et avancer
                if i % 2 == 0:
                    current_player.advance()
                
            elif terrain == "W":

                # Si terrain = mur, arrêter la voiture
                current_player.speed = 0

            elif terrain == "F" and current_player.direction == 'right' and current_player.speed > 0:

                # Vérifie si on entre sur la ligne d’arrivée par la gauche et validation du tour une seule fois, même si le joueur reste plusieurs pas de vitesse sur la case "finish_line".
                current_player.laps_done += 1
                current_player.advance()  # Avance même sur la ligne

 

            # Vérifier si le joueur a terminé tous ses tours
            if current_player.laps_done >= self.total_laps:
                self.end_game()


        if(current_player.speed == -1):
            #à modifier si on veut de l'évolutivité
            next_pos = current_player.reverse_next_position()
            terrain = self.circuit.get_terrain_type(next_pos)
            if(terrain in ["R","G"]):
                current_player.position = current_player.reverse_next_position()
            elif terrain == "W":
                current_player.speed = 0
            elif terrain == "F":
                current_player.position = current_player.reverse_next_position()

                if current_player.direction == "left":
                    # Vérifie si on entre sur la ligne d’arrivée par la gauche et validation du tour une seule fois, même si le joueur reste plusieurs pas de vitesse sur la case "finish_line".
                    current_player.laps_done += 1
    
    def move_AI(self, action, AI : "AI"):
        
        if(action == 'accelerate'):
            AI.speed += 1
            if(AI.speed > 2):
                AI.speed = 2
            self.modify_player_movement(AI)
        elif(action == 'brake'):
            AI.speed -= 1
            if(AI.speed < -1):
                AI.speed = -1
            self.modify_player_movement(AI)
        elif(action == 'do_nothing'):
            self.modify_player_movement(AI)
        elif(action == 'turn_right'):
            self.turn(AI, 1)
        elif(action == 'turn_left'):
            self.turn(AI, -1)
            
            
    def start_game(self):
        """
        Démarre le jeu avec la voiture à une vitesse de 0 et la direction vers la droite.
        """
        
        for kart in self.karts:
            kart.speed = 0
            kart.direction = "right"
    def end_game(self):
        """
        Déclare la fin de la partie et le gagnant.
        """
        winner = self.karts[self.current_player_index]
             
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
        Retourne le nombre de joueurs dans la partie (INT)
        """
        return len(self.karts)
    
    def get_all_circuits(self):
        """
        renvoie:
            tous les circuits du fichier enregistré ([☺STRING])
        """
        return dao.get_all()
    
    def get_circuit(self, circuit_name):
        """
        renvoie un circuit en fonction de celui intégré au fichier enregistré (CIRCUIT)
        """
        return Circuit(dao.get_circuit_grid(circuit_name))

    def get_finish_lines(self):
        """
        Retourne une liste des positions (x, y) où le circuit contient une case 'F' (finish line).
        """
        finish_lines = []
        for y, row in enumerate(self.circuit.grid):
            for x, char in enumerate(row):
                if char == 'F':
                    finish_lines.append((x, y))
        return finish_lines

        
    def switch_current_kart(self):
        """
        inverse le joueur actuel
        """
        self.current_kart -= 1
    

        
    def get_current_kart(self):
        """
        retourne:
            - le joueur actuel (KART)
        """
        return self.karts[self.current_kart]
    
    def turn(self, current_kart, movement):
        """
        modifie l'orientation du kart, en fonction du mouvement inséré
        arguments:
            - le joueur actuel (KART)
            - le mouvement (1 vers la droite, -1 vers la gauche)(INT)
        utilise une liste reprennant les orientations et décale un index en fonction du mouvement
        """
        new_direction_index = self.get_current_kart().directions.index(self.get_current_kart().direction) + movement
       
        if(new_direction_index >= 4):
            new_direction_index = 0
        current_kart.direction = self.get_current_kart().directions[new_direction_index]
        
        
def train_AI(training_amount, actions_per_game, epsilon_decay):
    AI_player = AI(position=(0,0),speed=0,direction="right")
    training_game = Game(laps=1, karts=[AI_player], circuit=dao.get_by_name("Basic"))
    game_won = 0
    actions = ['accelerate', 'do_nothing', 'turn_left', 'turn_right', 'brake']
    
    min_epsilon = 0.01
    
    for game in range(training_amount):
        training_game.time = 0
        AI_player.position = random.choice(training_game.get_finish_lines())
        AI_player.speed = 0
        AI_player.direction = "right"
        AI_player.laps_done = 0
        
        previous_state = AI_dao.encode_state(training_game.circuit.grid, AI_player.position[0], AI_player.position[1], AI_player.direction, AI_player.speed)
        
        while training_game.time <= actions_per_game:
            print("turn: ", training_game.time, "game: ", game)
            if random.uniform(0, 1) < AI_player.epsilon:
                action = random.choice(actions)
            else:
                action = AI_player.choose_action(training_game.circuit, actions)
            
            training_game.move_AI(action, AI_player)
            
            new_state = AI_dao.encode_state(training_game.circuit.grid, AI_player.position[0], AI_player.position[1], AI_player.direction, AI_player.speed)
            
            reward = AI_player.calculate_reward(previous_state, training_game.time, actions_per_game, training_game.circuit.grid)
            AI_player.update_q_table(previous_state, action, reward, new_state)
            
            training_game.time += 1
            previous_state = new_state

            if AI_player.laps_done >= 1:
                game_won += 1
                training_game.reset()
        
        AI_player.epsilon = max(min_epsilon, AI_player.epsilon * epsilon_decay)
    
    print(f"Nombre de parties gagnées par l'IA : {game_won}/{training_amount}")

    
def plot_training_performance(results):
    """
    Affiche un graphique de l'évolution des performances de l'IA pendant l'entraînement.
    
    :param results: Liste booléenne ou entière (1 pour victoire, 0 pour défaite) représentant les résultats des parties.
    """
    victories = [0]
    for win in results:
        victories.append(victories[-1] + win)

    plt.figure(figsize=(10, 5))
    plt.plot(range(len(victories)), victories, label="Victoires cumulées", color="green")
    plt.xlabel("Nombre de parties jouées")
    plt.ylabel("Nombre de victoires")
    plt.title("Performance de l'IA pendant l'entraînement")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if(__name__ == "__main__"):
    train_AI(training_amount=200, actions_per_game = 75, epsilon_decay=0.00009)