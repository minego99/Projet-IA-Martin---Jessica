import random
import gameDAO

"""
ce script est une copie conforme du modèle de cubee, à l'exception d'un import modifié pour pouvoir lancer une cession d'entraînement pour l'IA par renforcement
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

        self.playerA.model = self
        self.playerB.model = self
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
        Essaye de conquérir les cases enfermées
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
        #print("SWITCH, joueur actuel: ", self.current_player)
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
        Récupère l'état de la partie depuis la base de données avec des poids nulls (pour l'instant)
        Sauvegarde l'état de la partie juste après le mouvement
        renvoie:
            - Si le mouvement est invalide, FALSE (BOOL)
            - Si aucun cas d'erreur n'a été rencontré, TRUE (BOOL)
        """
        
        if not self.is_movement_valid(movement):
           # print(f"Le mouvement '{movement}' est invalide.")
            return False
    
        position_temp = self.get_movement(movement)
        
        if self.players[self.get_current_player()] == self.playerA:
            new_pos = [self.player1_pos[0] + position_temp[0], self.player1_pos[1] + position_temp[1]]
            if self.grid[new_pos[0]][new_pos[1]] != 2:
                self.player1_pos = new_pos
            else:
              #  print("Case déjà occupée par l'adversaire")
                return False
        else:
            new_pos = [self.player2_pos[0] + position_temp[0], self.player2_pos[1] + position_temp[1]]
            if self.grid[new_pos[0]][new_pos[1]] != 1:
                self.player2_pos = new_pos
            else:
              #  print("Case déjà occupée par l'adversaire")
                return False
       
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
            #print(len(enclosure_matrix))
            #print(self.player2_pos[0],self.player2_pos[1])
            enclosure_matrix[self.player2_pos[0]][self.player2_pos[1]] = True
            
        else:
            queue = [(self.player1_pos[0], self.player1_pos[1])]
            claimed_value = 1
           # print(len(enclosure_matrix))
            #print(self.player1_pos[0],self.player1_pos[1])

            enclosure_matrix[self.player1_pos[0]][self.player1_pos[1]] = True
       # print("matrix before loop:" , enclosure_matrix)
        while queue:
          #  print("queue len: ", len(queue))
            case = queue.pop()  # Défilement de la file
            x, y = case  # Récupération des coordonnées

    
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
    #    print("matrix after loop:" , enclosure_matrix)

        if self.players[self.get_current_player()] == self.playerA:
            for i, row in enumerate(enclosure_matrix):
                for j, elem in enumerate(row):
                    if elem == False:
                       # print(f"Coordonnées A: ({i}, {j}) - Valeur: {elem}")
                        self.grid[i][j] = 1
        else:
            for i, row in enumerate(enclosure_matrix):
                for j, elem in enumerate(row):
                    if elem == False:
                    #    print(f"Coordonnées B: ({i}, {j}) - Valeur: {elem}")
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

        #print("grid:", self.grid)
        if not enclosure_matrix[x][y] and (self.grid[x][y] == claimed_value or self.grid[x][y] == 0):
            enclosure_matrix[x][y] = True
            queue.append(case)
        # if (case in queue):
        #     print("append hapenned")
        # else:
        #     print("append not hapenned")


    def create_state (self):
        """
        Crée l'id de la database à partir des données de la partie
        renvoie:
            - l'id de l'état de la partie (STR)
        """
        state_id = ""
        state_id += str(self.player1_pos[0])+str(self.player1_pos[1]) + ";"
        state_id += str(self.player2_pos[0])+str(self.player2_pos[1]) + ";"
        state_id += str(self.current_player) + ";"
        return state_id
    
    
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
    
    def save_state(self, state_values):
        """
        Envoi de l'état avec ses poids vers la base de données
        La Qline sera mise à jour ou créée si elle n'existe pas encore dans la BD
        attributs:
            - valeurs des 4 poids [REEL]
        """
        gameDAO.save_qline(self.data_to_dto())
   
        
class CubeePlayer():
    def __init__(self, player_name, model = None):
        """
        Constructeur du profil du joueur:
            argument:
                - nom du joueur(STR)
            attributs: 
                - nom du joueur(STR)
        """
        self.player_name = player_name
        self.model = model

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
    def __init__(self, AI_name, alpha=0.1, gamma=0.9, epsilon=0.5, min_epsilon=0.01, decay=0.995):
        """
        Initialise l'IA avec les paramètres d'apprentissage.

        Args:
            AI_name (str): Nom de l'IA.
            alpha (float): Taux d'apprentissage.
            gamma (float): Facteur de remise (discount factor).
            epsilon (float): Taux d'exploration initial.
            min_epsilon (float): Taux d'exploration minimum.
            decay (float): Taux de décroissance de epsilon après chaque action.
        """
        super().__init__(AI_name)
        self.alpha = alpha  # taux d'apprentissage
        self.gamma = gamma  # facteur de remise (discount factor)
        self.epsilon = epsilon  # taux d'exploration initial
        self.min_epsilon = min_epsilon  # epsilon minimum
        self.decay = decay  # taux de décroissance de epsilon
        self.actions = ['up', 'down', 'left', 'right']

    def choose_action(self):
        """
        Choisit l'action à effectuer selon la politique epsilon-greedy.

        Retourne une action valide basée sur la Q-table, soit en explorant 
        aléatoirement, soit en exploitant la meilleure action connue.
        """
        state_id = self.model.create_state()
        q_values = gameDAO.get_Qline_by_state(state_id)

        # Récupérer les valeurs Q dans une liste
        values = [
            q_values.up_value,
            q_values.down_value,
            q_values.left_value,
            q_values.right_value
        ]

        # Filtrer les actions invalides pour l'état actuel
        valid_actions = []
        valid_values = []
        for i, action in enumerate(self.actions):
            if self.model.is_move_valid(self, action):
                valid_actions.append(action)
                valid_values.append(values[i])

        if not valid_actions:
            # Aucun mouvement valide, retourner None ou un mouvement par défaut
            return None

        if random.uniform(0, 1) < self.epsilon:
            # Exploration parmi les mouvements valides
            return random.choice(valid_actions)
        else:
            # Exploitation parmi les mouvements valides
            max_index = valid_values.index(max(valid_values))
            return valid_actions[max_index]

    def update_q_table(self, previous_state, action, reward, new_state):
        """
        Met à jour la Q-table selon la formule du Q-learning.

        Args:
            previous_state: état avant action
            action (str): action réalisée
            reward (float): récompense reçue
            new_state: nouvel état après action
        """
        next_q_values = gameDAO.get_Qline_by_state(new_state)
        max_future_q = max([
            next_q_values.up_value,
            next_q_values.down_value,
            next_q_values.left_value,
            next_q_values.right_value
        ])

        current_q_values = gameDAO.get_Qline_by_state(previous_state)
        current_q = getattr(current_q_values, f"{action}_value")

        new_q = (1 - self.alpha) * current_q + self.alpha * (reward + self.gamma * max_future_q)

        setattr(current_q_values, f"{action}_value", new_q)
        gameDAO.save_qline({
            'state_id': previous_state,
            'up_value': current_q_values.up_value,
            'down_value': current_q_values.down_value,
            'left_value': current_q_values.left_value,
            'right_value': current_q_values.right_value
        })

    def calculate_reward(self, player_pos, opponent_pos):
        """
        Calcule la récompense pour l'état donné en fonction de la position des joueurs.

        Args:
            player_pos (tuple): position du joueur IA (x, y)
            opponent_pos (tuple): position de l'adversaire (x, y)

        Returns:
            float: valeur de la récompense
        """
        reward = 0
        grid_size = len(self.model.grid)

        # Pénalité sortie de grille
        if player_pos[0] < 0 or player_pos[0] >= grid_size or player_pos[1] < 0 or player_pos[1] >= grid_size:
            return -10

        player_score = sum(row.count(1) for row in self.model.grid)
        opponent_score = sum(row.count(2) for row in self.model.grid)

        # Récompense principale : différence des scores
        reward += (player_score - opponent_score) * 5

        # Bonus si proche du centre (favoriser le contrôle du centre)
        center = grid_size // 2
        dist_to_center = abs(player_pos[0] - center) + abs(player_pos[1] - center)
        reward += max(0, 3 - dist_to_center)  # plus proche, plus de récompense

        # Pénalité si proche adversaire (ex: éviter d'être enfermé)
        dist_to_opponent = abs(player_pos[0] - opponent_pos[0]) + abs(player_pos[1] - opponent_pos[1])
        if dist_to_opponent == 1:
            reward -= 2  # trop proche = danger

        return reward

    def decay_epsilon(self):
        """
        Décroissance progressive du taux d'exploration epsilon après chaque action.
        """
        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.decay
            if self.epsilon < self.min_epsilon:
                self.epsilon = self.min_epsilon

def training(model, training_amount):
    """
    Fonction d'entraînement de l'IA par auto-jeu contre un adversaire aléatoire.

    Args:
        model: instance du modèle du jeu
        training_amount (int): nombre d'épisodes d'entraînement
    """
    ai = None
    random_ai = None
    
    for player in model.players:
        if isinstance(player, CubeeAI):
            ai = player
        else:
            random_ai = player

    ai_wins = 0
    for episode in range(training_amount):
        model.reset()
        
        while not model.is_over():
            current_player = model.players[model.get_current_player()]
            
            if current_player == ai:
                prev_state = model.create_state()
                action = ai.choose_action()

                if action is None or not model.move(ai, action):
                    # Pas d'action valide ou échec => mouvement aléatoire valide
                    valid_moves = [a for a in ai.actions if model.is_move_valid(ai, a)]
                    if valid_moves:
                        action = random.choice(valid_moves)
                        model.move(ai, action)
                    else:
                        # Aucun mouvement possible
                        break

                model.step()
                new_state = model.create_state()
                reward = ai.calculate_reward(model.player1_pos, model.player2_pos)
                ai.update_q_table(prev_state, action, reward, new_state)

                # Décroissance d'epsilon pour affiner l'exploitation
                ai.decay_epsilon()

            else:
                moved = False
                while not moved:
                    rand_action = random.choice(["up", "down", "left", "right"])
                    moved = model.move(random_ai, rand_action)
                model.step()

            model.switch_player()

        winner = model.get_winner()
        if model.players[winner] == ai:
            ai_wins += 1

        if episode % 1000 == 0:
            print(f"Episode {episode}, Epsilon: {ai.epsilon:.4f}, Win rate: {ai_wins / (episode+1) * 100:.2f}%")

    print("\n=== Résultats de l'entraînement ===")
    print(f"Total de parties : {training_amount}")
    print(f"Victoires de l'IA intelligente : {ai_wins}")
    print(f"Taux de victoire : {ai_wins / training_amount * 100:.2f}%")

class MySmartAI:
    def __init__(self, name):
        self.name = name
    def choose_move(self, game):
        valid_moves = [m for m in ["up", "down", "left", "right"] if game.is_movement_valid(m)]
        if valid_moves:
            return valid_moves[0]  # toujours le premier coup valide
        return None


if(__name__ == '__main__'):
    
    
    playerA = CubeePlayer("Alice")
    playerB = CubeeAI("Bob")
    testmodel = CubeeGameModel(4, playerA, playerB)

def train_and_test(dimension, playerA, playerB, nb_games=100):
    wins = {0:0, 1:0, -1:0}  # 0: joueur A gagne, 1: joueur B gagne, -1: égalité

    for i in range(nb_games):
        game = CubeeGameModel(dimension, playerA, playerB, displayable=False)
        game.reset()

        while not game.is_over():
            current_player = game.get_current_player()
            player = game.players[current_player]

            # L'IA choisit un mouvement valide
            chosen_move = player.choose_move(game)

            # Si pas de coup valide ou coup invalide, on passe le tour
            if chosen_move is None or not game.is_movement_valid(chosen_move):
                game.switch_player()
                continue

            moved = game.move(player, chosen_move)
            if moved:
                game.step()
                game.switch_player()
            else:
                # Mouvement invalide (peu probable si on a vérifié avant), on passe le tour
                game.switch_player()

        winner = game.get_winner()
        wins[winner] += 1

    print(f"Résultats après {nb_games} parties :")
    print(f"Joueur 0 ({playerA.name}) victoires : {wins[0]}")
    print(f"Joueur 1 ({playerB.name}) victoires : {wins[1]}")
    print(f"Égalités : {wins[-1]}")

# Exemple d'IA aléatoire
class RandomPlayer:
    def __init__(self, name):
        self.name = name
    def choose_move(self, game):
        moves = ["up", "down", "left", "right"]
        valid_moves = [m for m in moves if game.is_movement_valid(m)]
        if valid_moves:
            return random.choice(valid_moves)
        else:
            return None

# Exemple d'IA simple qui choisit toujours le premier coup valide
class SmartAI:
    def __init__(self, name):
        self.name = name
    def choose_move(self, game):
        moves = ["up", "down", "left", "right"]
        valid_moves = [m for m in moves if game.is_movement_valid(m)]
        if valid_moves:
            return valid_moves[0]
        else:
            return None

if __name__ == "__main__":
    playerA = SmartAI("SmartAI")
    playerB = RandomPlayer("Random")

    train_and_test(dimension=5, playerA=playerA, playerB=playerB, nb_games=5000)
