import pytest
import random
import gameDAO
#import gameDAO

"""
La classe GameModel contient toute la logique des règles du jeu cubee
Les valeurs renvoyées permettent à GameController de composer le statut du jeu
La classe CubeePlayer comprend le comportement de l'IA aléatoire, et sa classe héritée celle du joueur humain
La classe CubeeAI est pour l'IA intelligente, qui n'est pas implémentée pour l'instant
"""
class CubeeGameModel():
    def __init__(self,dimension, playerA, playerB, displayable = False):
        """
        Constructeur du comportement d'une partie:
            
            arguments: 
                - dimension du plateau de jeu (INT)
                - premier joueur engagé dans la partie (PLAYER)
                - deuxième joueur engagé dans la partie (PLAYER)
                - test pour décider si la partie doit être affichée par tkinter (BOOL)
           attributs:
                - plateau de jeu, qui est une matrice contenant soit 0,1 ou 2 représentant l'appartenance d'une case([[INT]])
                - le compteur du joueur actuel [INT]
                - la position du premier joueur qui commence toujours en haut à gauche [INT, INT]
                - la position du deuxième joueur qui commence toujours en bas à droite [INT, INT]
                - les deux matrices des enclos, qui indiquent quel joueur a des cases inatteignables [[BOOL]]
                
                
            Rempli aussi la liste des joueurs avec les joueurs inscrits dans la partie
            et choisi aléatoirement un des joueurs inscrits pour commencer la partie
            Les deux cases de départ sont capturées par les deux joueurs

        """
        self.dimension = dimension
        self.grid = [[0] * self.dimension for i in range(self.dimension)]      

        self.grid[0][0] = 1
        self.grid[self.dimension-1][self.dimension-1] = 2
        self.players = [playerA, playerB]
        self.current_player = 0
        self.playerA = playerA
        self.playerB = playerB
        self.player1_pos = [0, 0]
        self.player2_pos = [dimension-1, dimension-1]


        self.displayable = displayable
        self.shuffle_players()
        
    def shuffle_players(self):
        """
        Modifie la liste des joueurs inscrits avec les éléments dans un ordre aléatoire
        """
        random.shuffle(self.players)        
        
    def get_current_player(self):
        """
        renvoie:
            l'indice du joueur ayant la main dans la partie (INT)
        """
        return self.current_player
    def get_score(self):
        player1_score = sum(row.count(1) for row in self.grid)
        player2_score = sum(row.count(2) for row in self.grid)
        return [player1_score, player2_score]

    
    def get_winner(self):
        """
        récupère le score des deux joueurs
        renvoie:
            - Si les deux scores sont égaux, informe que c'est une égalité (INT)
            - Sinon, donne le numéro du joueur gagnant (INT)
        """
        final_score = self.get_score()
        if(final_score[0] == final_score[1]):
            return -1
        else:
            return final_score.index(max(final_score))
        
    def get_loser(self):
        """
        récupère le score des deux joueurs
        renvoie:
            - Si les deux scores sont égaux, informe que c'est une égalité (INT)
            - Sinon, donne le numéro du joueur perdant (INT)
        """
        final_score = self.get_score()
        if(final_score[0] == final_score[1]):
            return -1
        else:
            return final_score.index(min(final_score))     
        
    def is_over(self):
        """
        Vérifie si le plateau de jeu contient encore des cases non-conquises
        retourne:
            - Si il y a une case inocupée, FALSE (BOOL)
            - Sinon, TRUE (BOOL)
        """
        for row in self.grid:
            if(0 in row):
                return False
        print("game over")
        return True
    
    def step(self):
        """
        Modifie les cases où les joueurs se situent par leur valeur respective
        """
        self.grid[self.player1_pos[0]][self.player1_pos[1]] = 1
        self.grid[self.player2_pos[0]][self.player2_pos[1]] = 2
        self.enclosure_search()
     
        
    def reset(self):
        """
        Réinitialise le plateau de jeu, les positions des deux joueurs, le joueur actif et mélange l'ordre des deux joueurs
        """
        self.grid = [[0] * self.dimension for i in range(self.dimension)]
        self.grid[0][0] = 1 
        self.grid[self.dimension-1][self.dimension-1] = 2
        self.current_player = 0
        self.player1_pos = [0, 0]
        self.player2_pos = [self.dimension-1, self.dimension-1]
        self.shuffle_players()
        
    def display(self):
        """
        renvoie:
            - le choix ou non d'afficher le jeu (BOOL)
        Utilisable pour l'entraînement de l'IA sans devoir générer un rendu visuel
        """
        return self.displayable

    def switch_player(self):      
        """
        Change de joueur actif en modifiant l'index de la liste contenant les deux joueurs
        """
        print("SWITCH, joueur actuel: ", self.current_player)
        self.current_player = 1 - self.current_player
        
    def get_movement(self, movement):
        """
        Crée un mouvement instantané vide et le modifie en fonction de l'input
        argument:
            - le mouvement désiré (STR)
        renvoie:
            - Le mouvement joué ([INT, INT])
        """
        position_temp = [0,0]        
        if(movement == "down"):
            position_temp[0] += 1
        elif(movement == "left"):
            position_temp[1] -= 1
        elif(movement == "right"):
            position_temp[1] += 1
        else:
            position_temp[0] -= 1
        
        return position_temp
    
    def is_movement_valid(self, movement):
        """
        Vérifie que le mouvement soit bien valide
        
        argument:
            - le mouvement désiré
            
        renvoie:
            - si le mouvement est entièrement adéquat, TRUE (BOOL)
            - SINON, FALSE (BOOL)
        """
        
        position_temp = self.get_movement(movement)
        
        if(self.players[self.get_current_player()] == self.playerA):
             position_temp[0] += self.player1_pos[0]
             position_temp[1] += self.player1_pos[1]
        else:
             position_temp[0] += self.player2_pos[0]
             position_temp[1] += self.player2_pos[1]
        if(position_temp[0] < self.dimension and position_temp[0] >= 0 and position_temp[1] < self.dimension and position_temp[1] >= 0):     
            return True
        else:
            return False
        
    def move(self, player, movement):
        """
        Teste si le mouvement entré est adéquat, si c'est le cas effectue aussi la vérification du cas de la case conquise par l'adversaire
        arguments:
            - Le joueur actif (PLAYER)
            - Le mouvenement désiré (STR)
            
        renvoie:
            - Si le mouvement est invalide, FALSE (BOOL)
            - Si aucun cas d'erreur n'a été rencontré, TRUE (BOOL)
        """
        
        if not self.is_movement_valid(movement):
            print(f"Le mouvement '{movement}' est invalide.")
            return False
    
        position_temp = self.get_movement(movement)
        dto_id = self.data_to_dto([0,0,0,0]).get('state_id')
        print(dto_id)
        current_state = gameDAO.get_Qline_by_state(dto_id)
        if self.players[self.get_current_player()] == self.playerA:
            new_pos = [self.player1_pos[0] + position_temp[0], self.player1_pos[1] + position_temp[1]]
            if self.grid[new_pos[0]][new_pos[1]] != 2:
                self.player1_pos = new_pos
            else:
                print("Case déjà occupée par l'adversaire")
                return False
        else:
            new_pos = [self.player2_pos[0] + position_temp[0], self.player2_pos[1] + position_temp[1]]
            if self.grid[new_pos[0]][new_pos[1]] != 1:
                self.player2_pos = new_pos
            else:
                print("Case déjà occupée par l'adversaire")
                return False
        self.save_state() 
        return True  # Mouvement effectué avec succès
    
        
    def enclosure_search(self):
        """
        Gère la logique BFS, crée un point de départ (= départ du joueur actif) et active toutes les cases visitables.
        une case visitable rend ses cases adjacentes visitables
        """
        
        enclosure_matrix = [[False] * self.dimension for i in range(0,self.dimension)]
        

        # NE PAS AVOIR D'ATTRIBUTS POUR LES MATRICES
        # RESET LES MATRICES
        # AVOIR LE DEBUT  DE LA QUEUE A LA POSITION DU JOUEUR
        # COMMENCER DEPUIS LA POSITION DU JOUEUR ADVERSE

        if self.players[self.get_current_player()] == self.playerA:
            queue = [(self.player2_pos[0], self.player2_pos[1])]
            claimed_value = 2
            print(len(enclosure_matrix))
            print(self.player2_pos[0],self.player2_pos[1])
            enclosure_matrix[self.player2_pos[0]][self.player2_pos[1]] = True
            
        else:
            queue = [(self.player1_pos[0], self.player1_pos[1])]
            claimed_value = 1
            print(len(enclosure_matrix))
            print(self.player1_pos[0],self.player1_pos[1])

            enclosure_matrix[self.player1_pos[0]][self.player1_pos[1]] = True
        print("matrix before loop:" , enclosure_matrix)
        while queue:
            print("queue len: ", len(queue))
            case = queue.pop()  # Défilement de la file
            x, y = case  # Récupération des coordonnées
    
            print("Processing:", case)
    
            # Vérification des 4 directions
            if y - 1 >= 0:  # LEFT
                self.check_enclosure((x, y - 1), queue, claimed_value, enclosure_matrix)
            if y + 1 < self.dimension:  # RIGHT
                self.check_enclosure((x, y + 1), queue, claimed_value, enclosure_matrix)
            if x - 1 >= 0:  # UP
                self.check_enclosure((x - 1, y), queue, claimed_value, enclosure_matrix)
            if x + 1 < self.dimension:  # DOWN
                self.check_enclosure((x + 1, y), queue, claimed_value, enclosure_matrix)

        #     print("Queue:", queue)
        print("matrix after loop:" , enclosure_matrix)

        if self.players[self.get_current_player()] == self.playerA:
            for i, row in enumerate(enclosure_matrix):
                for j, elem in enumerate(row):
                    if elem == False:
                        print(f"Coordonnées A: ({i}, {j}) - Valeur: {elem}")
                        self.grid[i][j] = 1
        else:
            for i, row in enumerate(enclosure_matrix):
                for j, elem in enumerate(row):
                    if elem == False:
                        print(f"Coordonnées B: ({i}, {j}) - Valeur: {elem}")
                        self.grid[i][j] = 2
    def check_enclosure(self, case, queue, claimed_value, enclosure_matrix):
        """
        Vérification de l'état de la case envoyée en paramètre. Modifie la matrice du joueur adverse et ajoute la case suivante à la file d'attente
        arguments:
            - case à vérifier [INT,INT]
            - file d'attente des cases à vérifier [(INT,INT)]
            - la valeur de l'adversaire sur le plateau (INT)
            - la matrice contenant toutes les cases visitables par le joueur [[BOOL]]
        """
        x, y = case
        print("grid:", self.grid)
        if not enclosure_matrix[x][y] and (self.grid[x][y] == claimed_value or self.grid[x][y] == 0):
            enclosure_matrix[x][y] = True
            queue.append(case)
        if (case in queue):
            print("append hapenned")
        else:
            print("append not hapenned")


    def data_to_dto(self, action_values):
        """
        convertit l'état de la partie et le transforme en une chaîne de caractères
        """
        state_id = ""
        state_id += str(self.player1_pos[0])+str(self.player1_pos[1]) + ";"
        state_id += str(self.player2_pos[0])+str(self.player2_pos[1]) + ";"
        state_id += str(self.current_player) + ";"
        for i, elem in enumerate(self.grid):
            for j, elem in enumerate(self.grid):
                state_id += str(self.grid[i][j])
        return{
        'state_id' : state_id,
        'up_value' : action_values[0],
        'down_value' : action_values[1],
        'left_value' : action_values[2],
        'right_value' : action_values[3]
            }
    
    @staticmethod
    def dto_to_data(data: dict):
        """
        récupère les données du modèle & les valeurs de mouvement et le convertit en dictionnaire pour la database
        """
        return   CubeeGameModel(
            state = data.get('state_id'),
            up_value = data.get('up_value'),
            down_value = data.get('down_value'),
            left_value = data.get('left_value'),
            right_value = data.get('right_value')
            
            )
    
    def save_state(self):
        gameDAO.save_qline(self.data_to_dto([0,0,0,0]))
        
        
class CubeePlayer():
    def __init__(self, player_name):
        """
        Constructeur du profil du joueur:
            argument:
                - nom du joueur(STR)
            attributs: 
                - nom du joueur(STR)
        """
        self.player_name = player_name
        

class CubeeHuman(CubeePlayer):
    def __init__(self, player_name):
        """
        Constructeur du profil du joueur humain:
            hérite de:
                - CubeePlayer
            argument:
                - nom du joueur(STR)
            attributs: 
                - nom du joueur(STR)
        """
        self.player_name = player_name
        
# class CubeeAI(CubeePlayer):
#     def __init__(self, AI_name, qtable, alpha=0.1, gamma=0.9, epsilon=0.1):
#         """
#         Constructeur du profil du joueur IA intelligent.
        
#         arguments:
#             - AI_name: nom de l'IA (STR)
#             - qtable: instance de la QTable pour la gestion des valeurs Q
#             - alpha: taux d'apprentissage (FLOAT)
#             - gamma: importance des récompenses futures (FLOAT)
#             - epsilon: taux d'exploration (FLOAT)
#         """
#     super().__init__(AI_name)  
#     self.qtable = qtable
#     self.alpha = alpha  # Learning rate
#     self.gamma = gamma  # Récompenses futures
#     self.epsilon = epsilon  # Exploration vs exploitation

#     def choose_action(self, state):
#         """Sélectionne l'action en fonction de la Q-table ou exploration."""
#         q_values = self.qtable.get_q_values(state)
#         if random.uniform(0, 1) < self.epsilon:
#             return random.choice(["up", "down", "left", "right"])
#         return max(q_values, key=q_values.get)
    
#     def update_q_table(self, state, action, reward, new_state):
#         """Met à jour la Q-table après un mouvement."""
#         q_values = self.qtable.get_q_values(state)
#         max_future_q = max(self.qtable.get_q_values(new_state).values())
        
#         # Calcul de la nouvelle valeur Q
#         new_q_value = (1 - self.alpha) * q_values[action] + self.alpha * (reward + self.gamma * max_future_q)
#         q_values[action] = new_q_value
        
#         self.qtable.update_q_value(state, q_values)

    def calculate_reward(self, board, player_pos, opponent_pos):
        """
        Calcule la récompense basée sur le mouvement effectué par l'IA.
        """
        reward = 0
        # Pénalité si le mouvement sort des limites
        if player_pos[0] < 0 or player_pos[0] >= len(board) or player_pos[1] < 0 or player_pos[1] >= len(board):
            reward -= 10  # Pénalité pour sortie

        # Récompense pour les cases prises
        player_score = sum(row.count(1) for row in board)  # Nombre de cases du joueur
        opponent_score = sum(row.count(2) for row in board)  # Nombre de cases de l'adversaire
        reward += (player_score - opponent_score)  # Récompense immédiate

        return reward



if(__name__ == '__main__'):
    testmodel = CubeeGameModel(4, "Alice", "Bob")
    testmodel.move("A", "up")
    testmodel.move("A", "left")
    testmodel.move("A", "down")
    testmodel.move("A", "right")