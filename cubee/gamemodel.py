import random

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
                
            Rempli aussi la liste des joueurs avec les joueurs inscrits dans la partie
            et choisi aléatoirement un des joueurs inscrits pour commencer la partie
            Les deux cases de départ sont capturées par les deux joueurs

        """
        self.dimension = dimension
        self.grid = [[0] * self.dimension for i in range(self.dimension)]      
        self.enclosure_matrix_A = [[False] * self.dimension for i in range(self.dimension)]
        self.enclosure_matrix_B = [[False] * self.dimension for i in range(self.dimension)]
        self.grid[0][0] = 1
        self.grid[self.dimension-1][self.dimension-1] = 2
        print(self.grid)
        self.players = [playerA, playerB]
        self.current_player = 0
        self.playerA = playerA
        self.playerB = playerB
        self.player1_pos = [0, 0]
        self.player2_pos = [dimension-1, dimension-1]
        self.displayable = displayable
        print(self.player1_pos, self.player2_pos)
        print(self.grid[self.player2_pos[0]][self.player2_pos[1]])
        self.shuffleplayers()
    def shuffleplayers(self):
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
            - Si les deux scores sont égaux, informe que c'est une égalité (STR)
            - Sinon, donne le numéro du joueur gagnant (INT)
        """
        final_score = self.get_score()
        if(final_score[0] == final_score[1]):
            return "it's a draw"
        else:
            return final_score.index(max(final_score))
    def getloser(self):
        """
        récupère le score des deux joueurs
        renvoie:
            - Si les deux scores sont égaux, informe que c'est une égalité (STR)
            - Sinon, donne le numéro du joueur perdant (INT)
        """
        final_score = self.get_score()
        if(final_score[0] == final_score[1]):
            return "it's a draw"
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
                print("game not over")
                return False
        print("game over")
        return True
    def step(self):
        """
        Modifie les cases où les joueurs se situent par leur valeur respective
        """
        print("step")
        self.grid[self.player1_pos[0]][self.player1_pos[1]] = 1
        self.grid[self.player2_pos[0]][self.player2_pos[1]] = 2
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
        self.shuffleplayers()
    def display(self):
        """
        renvoie:
            - le choix ou non d'afficher le jeu (BOOL)
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
    
    def enclosure_search(self):
        queue = []
        if(self.get_current_player() == self.playerA):
            for col,row in self.grid:
                if(self.grid(col) ==  1):
                    queue.append(col)
        print()

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
    def __init__(self, AI_name):
        """
        Constructeur du profil du joueur IA intelligent:
            argument:
                - nom de l'IA (STR)
            attributs: 
                - nom de l'IA (STR)
        """
        self.AI_name = AI_name
def example_movement():
    """
    fonction de test visant à vérifier les tests de validité des déplacement
    """
    playertempA = CubeePlayer("bot")
    playertempB = CubeePlayer("chaussure")
    newModel = CubeeGameModel(5, playertempA, playertempB)
    newModel.move(playertempA, "down")
    newModel.step()
    newModel.move(playertempA, "down")
    newModel.step()
    newModel.move(playertempA, "down")
    newModel.step()
    newModel.move(playertempA, "down")
    newModel.step()
    newModel.move(playertempA, "right")
    newModel.step()
    newModel.move(playertempA, "up")
    newModel.step()
    newModel.move(playertempA, "up")
    newModel.step()
    newModel.move(playertempA, "up")
    newModel.step()
    newModel.move(playertempA, "up")
    newModel.step()
    newModel.move(playertempA, "right")
    newModel.step()
    newModel.move(playertempA, "down")
    newModel.step()
    newModel.move(playertempA, "down")
    newModel.step()
    newModel.move(playertempA, "down")
    newModel.step()
    newModel.move(playertempA, "down")
    newModel.step()
    print(newModel.grid)
    newModel.get_score()
    
if(__name__ == '__main__'):
    example_movement()