import pytest
import random
import sqlite3
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
        self.enclosure_matrix_A = [[False] * self.dimension for i in range(self.dimension)]
        self.enclosure_matrix_B = [[False] * self.dimension for i in range(self.dimension)]
        # self.enclosure_matrix_A[0][0] = True
        # self.enclosure_matrix_B[self.dimension-1][self.dimension-1] = True

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
        """
        Calcule le nombre de cases capturées par le joueur A et B
        renvoie:
            - la somme des cases capturées par le joueur 1 et par le joueur 2 ([INT, INT])
        """
        player1_score = 0
        player2_score = 0
        for i in self.grid:
            player1_score += i.count(1)
            player2_score += i.count(2)
        
        print("player1_score: ",player1_score, "player2_score: ", player2_score)
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
    
        return True  # Mouvement effectué avec succès
    
    # def enable_locked_cases(self, current_player):
    #     """
        
    #     Bloque les cases inaccessibles pour le joueur adverse
    #     argument:
    #         - le joueur actuel (PLAYER)
    #     SI le joueur actif est le joueur A, donne toutes les cases inaccessibles au joueur B
    #     Et inversément si le joueur actif est le joueur Bs
    #     """
    #     # if(current_player == self.playerA):
    #     #     for i, row in enumerate(self.enclosure_matrix_A):
    #     #         for j, elem in enumerate(row):
    #     #             if elem == False:
    #     #                 print(f"Coordonnées A: ({i}, {j}) - Valeur: {elem}")
    #     #                 self.grid[i][j] = 2
    #     # else:
    #     #     for i, row in enumerate(self.enclosure_matrix_B):
    #     #         for j, elem in enumerate(row):
    #     #             if elem == False:
    #     #                 print(f"Coordonnées B: ({i}, {j}) - Valeur: {elem}")
    #     #                 self.grid[i][j] = 1
    #     # print("wip function")
        
    def enclosure_search(self):
        """
        Gère la logique BFS, crée un point de départ (= départ du joueur actif) et active toutes les cases visitables.
        une case visitable rend ses cases adjacentes visitables
        """
        if self.players[self.get_current_player()] == self.playerA:
            queue = [(0, 0)]
            temp_matrix = self.enclosure_matrix_A
            claimed_value = 1
        else:
            queue = [(self.dimension - 1, self.dimension - 1)]
            temp_matrix = self.enclosure_matrix_B
            claimed_value = 2
    
        while queue:
            case = queue.pop()  # Défilement de la file
            x, y = case  # Récupération des coordonnées
    
           # print("Processing:", case)
    
            # Vérification des 4 directions
            if y - 1 >= 0:  # LEFT
                self.check_enclosure((x, y - 1), queue, claimed_value, temp_matrix)
            if y + 1 < self.dimension:  # RIGHT
                self.check_enclosure((x, y + 1), queue, claimed_value, temp_matrix)
            if x - 1 >= 0:  # UP
                self.check_enclosure((x - 1, y), queue, claimed_value, temp_matrix)
            if x + 1 < self.dimension:  # DOWN
                self.check_enclosure((x + 1, y), queue, claimed_value, temp_matrix)
    
        #     print("Queue:", queue)
        print("matrix_A:" , self.enclosure_matrix_A)
        print("matrix_B:" , self.enclosure_matrix_B)

        if self.players[self.get_current_player()] == self.playerA:
            for i, row in enumerate(self.enclosure_matrix_A):
                for j, elem in enumerate(row):
                    if elem == False:
                        print(f"Coordonnées A: ({i}, {j}) - Valeur: {elem}")
                        self.grid[i][j] = 2
        else:
            for i, row in enumerate(self.enclosure_matrix_B):
                for j, elem in enumerate(row):
                    if elem == False:
                        print(f"Coordonnées B: ({i}, {j}) - Valeur: {elem}")
                        self.grid[i][j] = 1
                        
    def check_enclosure(self, case, queue, claimed_value, temp_matrix):
        """
        Vérification de l'état de la case envoyée en paramètre. Modifie la matrice du joueur adverse et ajoute la case suivante à la file d'attente
        arguments:
            - case à vérifier [INT,INT]
            - file d'attente des cases à vérifier [(INT,INT)]
            - la valeur de l'adversaire sur le plateau (INT)
            - la matrice contenant toutes les cases visitables par le joueur
        """
        x, y = case
        if not temp_matrix[x][y] and (self.grid[x][y] == claimed_value or self.grid[x][y] == 0):
            temp_matrix[x][y] = True
            queue.append(case)

    # def data_to_dto(self, action_values):
    #     temp = 0
    #     state_id = ""
    #     state_id += str(self.player1_pos[0])+str(self.player1_pos[1]) + ";"
    #     state_id += str(self.player2_pos[0])+str(self.player2_pos[1]) + ";"
    #     state_id += str(self.current_player) + ";"
    #     for i, elem in enumerate(self.grid):
    #         for j, elem in enumerate(self.grid):
    #             state_id += str(self.grid[i][j])
    #     return{
    #     'state_id' : state_id,
    #     'up_value' : action_values[0],
    #     'down_value' : action_values[1],
    #     'left_value' : action_values[2],
    #     'right_value' : action_values[3]
    #         }
    # @staticmethod
    # def dto_to_data(data: dict):
    #     return   CubeeGameModel(
    #         state = data.get('state_id'),
    #         up_value = data.get('up_value'),
    #         down_value = data.get('down_value'),
    #         left_value = data.get('left_value'),
    #         right_value = data.get('right_value')
    #         )

class QTable:
    def __init__(self, db_path="qtable.db"): # Initialise l'objet QTable avec un fichier de base de données SQLite 
        """
        Gestion de la base de données pour la Q-table.
        """
        self.conn = sqlite3.connect(db_path) #  Établit une connexion avec la base de données SQLite (qtable.db)
        self.cursor = self.conn.cursor() # Crée un curseur permettant d'exécuter des requêtes SQL
        self.create_table() #  Appelle une méthode qui crée la table qtable si elle n'existe pas encore
    
    def create_table(self):
        """
        Création de la table si elle n'existe pas.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS qtable (
                # Définition de state (état du jeu) comme clé primaire :
                state TEXT PRIMARY KEY,
                # Initialisation des valeurs Q pour chaque action (up, down, left, right) à 0 :
                up REAL DEFAULT 0,
                down REAL DEFAULT 0,
                left REAL DEFAULT 0,
                right REAL DEFAULT 0
            )
        ''')
        self.conn.commit() # Applique la modification en enregistrant la création de la table
    
    def get_q_values(self, state):
        """
        Récupération des valeurs Q pour un état donné.
        """
        self.cursor.execute("SELECT * FROM qtable WHERE state = ?", (state,)) # Cherche l’état state dans la table qtable
        row = self.cursor.fetchone() # Récupère la première ligne trouvée (ou None si l’état n’existe pas
        if row: # Si état trouvé (row existe), on retourne les valeurs up, down, left, right sinon on retourne des valeurs Q initialisées à 0
            return {"up": row[1], "down": row[2], "left": row[3], "right": row[4]}
        else:
            return {"up": 0, "down": 0, "left": 0, "right": 0}
    
    def update_q_value(self, state, action, new_value):
        """
        Mise à jour de la valeur Q.
        """
        # INSERT INTO qtable (state, up, down, left, right) VALUES (?, 0, 0, 0, 0) → Insère un nouvel état avec des valeurs Q à 0 si l’état n’existe pas encore
        # ON CONFLICT(state) DO UPDATE SET {} = ?.format(action) → Si l’état existe déjà, met à jour l’action spécifiée (up, down, left, right) avec new_value
        self.cursor.execute("INSERT INTO qtable (state, up, down, left, right) VALUES (?, 0, 0, 0, 0) ON CONFLICT(state) DO UPDATE SET {} = ?".format(action), (state, new_value))
        self.conn.commit() #  Sauvegarde la modification dans la base de données
    
    def close(self):
        """
        Fermeture de la connextion à la BDD et libération des ressources liées à la connexion SQLite
        """
        self.conn.close()        
        
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

class CubeeAI(CubeePlayer):
    def __init__(self, AI_name, qtable, alpha=0.1, gamma=0.9, epsilon=0.1):
        """
        Constructeur du profil du joueur IA intelligent.
        
        arguments:
            - AI_name: nom de l'IA (STR)
            - qtable: instance de la QTable pour la gestion des valeurs Q
            - alpha: taux d'apprentissage (FLOAT)
            - gamma: importance des récompenses futures (FLOAT)
            - epsilon: taux d'exploration (FLOAT)
        """
    super().__init__(AI_name)  
    self.qtable = qtable
    self.alpha = alpha  # Learning rate
    self.gamma = gamma  # Récompenses futures
    self.epsilon = epsilon  # Exploration vs exploitation

    def choose_action(self, state):
        """Sélectionne l'action en fonction de la Q-table ou exploration."""
        q_values = self.qtable.get_q_values(state)
        if random.uniform(0, 1) < self.epsilon: # si nombre entre 0 et 1 est inférieur à epsilon, l'IA prend une action au hasard
            return random.choice(["up", "down", "left", "right"])
        return max(q_values, key=q_values.get) # sinon, l'IA exploite la Q-table et choisit l'action avec la plus haute valeur Q
    
    def update_q_table(self, state, action, reward, new_state):
        """Met à jour la Q-table après un mouvement."""
        q_values = self.qtable.get_q_values(state)
        max_future_q = max(self.qtable.get_q_values(new_state).values()) # cherche la meilleure valeur Q de l'état suivant new_state : représente l'estimation de la meilleure récompense future
        
        # Calcul de la nouvelle valeur Q
        # Met à jour la valeur Q avec l'équation du Q-learning :
        # (1 - alpha) * q_values[action] : ancienne valeur légèrement diminuée
        # reward + gamma * max_future_q : nouvelle estimation de la récompense
        # alpha : contrôle l'importance de l'ancienne valeur vs la nouvelle estimation
        new_q_value = (1 - self.alpha) * q_values[action] + self.alpha * (reward + self.gamma * max_future_q)
        q_values[action] = new_q_value
        # Màj BDD avec nouvelle valeur Q
        self.qtable.update_q_value(state, q_values)

    def calculate_reward(self, board, player_pos, opponent_pos):
        """
        Calcule la récompense basée sur le mouvement effectué par l'IA.
        """
        reward = 0
        # Pénalité si le mouvement sort des limites
        # 0 : lignes (haut - bas) et 1 : colonnes (gauche - droite)
        # player_pos[0] < 0 → Le joueur dépasse la limite haute (-1)
        # player_pos[0] >= len(board) → Le joueur dépasse la limite basse (5 si le tableau fait 5 lignes)
        # player_pos[1] < 0 → Le joueur dépasse la limite gauche (-1)
        # player_pos[1] >= len(board[0]) → Le joueur dépasse la limite droite (5 si le tableau fait 5 colonnes)
        if player_pos[0] < 0 or player_pos[0] >= len(board) or player_pos[1] < 0 or player_pos[1] >= len(board):
            reward -= 10  # Pénalité pour sortie

        # Récompense pour les cases prises
        player_score = sum(row.count(1) for row in board)  # Nombre de cases du joueur
        opponent_score = sum(row.count(2) for row in board)  # Nombre de cases de l'adversaire
        reward += (player_score - opponent_score)  # Récompense immédiate

        return reward


def test_check_enclosure_empty_board():
    game = CubeeGameModel(3,"P1","P2")
    game.board = [[0,0,0],
                  [0,0,0],
                  [0,0,2]]
    game.player_turn = 1
    game.enclosure_search()
    assert game.board == [[0,0,0],
                         [0,0,0],
                         [0,0,2]]

def test_check_enclosure_simple_case():
    game = CubeeGameModel(3,"P1", "P2")
    game.grid = [[1,1,0],
                  [1,1,1],
                  [1,2,2]]
    game.player_turn = 1
    game.enclosure_search()
    
    print(game.grid)
    assert game.grid == [[1,1,1],
                         [1,1,1],
                         [1,2,2]]

def test_check_enclosure_no_enclosed_area():
    game = CubeeGameModel(3,"P1", "P2")
    game.grid = [[1,1,1],
                  [1,0,0],
                  [1,1,2]]
    game.player_turn = 1
    game.enclosure_search()
    assert game.grid == [[1,1,1],
                         [1,0,0],
                         [1,1,2]]

def test_check_enclosure_multiple_spaces():
    game = CubeeGameModel(4,"P1", "P2")
    game.grid = [[1,1,1,1],
                  [1,0,0,1],
                  [1,0,1,1],
                  [1,1,2,2]]
    game.player_turn = 1
    game.enclosure_search()
    assert game.grid == [[1,1,1,1],
                         [1,1,1,1],
                         [1,1,1,1],
                         [1,1,2,2]]

def test_check_enclosure_multiple_enclosure():
    game = CubeeGameModel(4,"P1", "P2")
    game.grid = [[1,1,0,0],
                  [1,1,0,1],
                  [0,1,1,2],
                  [1,1,2,2]]
    game.player_turn = 1
    game.enclosure_search()
  
    assert game.grid == [[1,1,1,1],
                         [1,1,1,1],
                         [1,1,1,2],
                         [1,1,2,2]]

                         
tests = [
    ([[1,1,1],[1,2,1],[1,2,2]],
     1,
     [[1,1,1],[1,2,1],[1,2,2]]),

    ([[1,0,0],[1,1,1],[1,2,2]],
     1,
     [[1,1,1],[1,1,1],[1,2,2]]),

    ([[1,1,1],[1,0,2],[1,1,2]],
     1,
     [[1,1,1],[1,0,2],[1,1,2]]),

    ([[1,2,0],[1,2,0],[1,2,2]],
     2,
     [[1,2,2],[1,2,2],[1,2,2]]),

    ([[1,0,1,1],[1,0,0,1],[1,1,1,2],[1,1,1,2]],
     1,
     [[1,1,1,1],[1,1,1,1],[1,1,1,2],[1,1,1,2]]),

    ([[1,0,1,1],[1,0,0,1],[1,1,0,1],[1,1,2,2]],
     2,
     [[1,0,1,1],[1,0,0,1],[1,1,0,1],[1,1,2,2]]),

    ([[1,1,0,0],[1,1,0,1],[0,1,2,2],[1,1,2,2]],
     1,
     [[1,1,0,0],[1,1,0,1],[1,1,2,2],[1,1,2,2]]),
]   

@pytest.mark.parametrize("board,turn,expected", tests)
def test_enclosure(board, turn, expected):
		game = CubeeGameModel("P1", "P2", size=len(board))
		game.board = board
		game.player_turn = turn
		game.check_enclosure()
		assert game.board == expected, f"{board} =({turn})=> {game.board}. But expected : {expected} "
if(__name__ == '__main__'):
    #example_movement()
    testmodel = CubeeGameModel(4, "Alice", "Bob")
   # testmodel.data_to_dto()
    test_check_enclosure_multiple_enclosure()