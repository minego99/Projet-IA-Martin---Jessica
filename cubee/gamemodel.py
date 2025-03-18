import random


class CubeeGameModel():
    def __init__(self,dimension, playerA, playerB, displayable = False):
        self.dimension = dimension
        self.grid = [[0] * self.dimension for i in range(self.dimension)]
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
        random.shuffle(self.players)        
    def get_current_player(self):
        return self.current_player
    def get_score(self):
        player1_score = 0
        player2_score = 0
        for i in self.grid:
            player1_score += i.count(1)
            player2_score += i.count(2)
        
        print("player1_score: ",player1_score, "player2_score: ", player2_score)
        return [player1_score, player2_score]
    def get_winner(self):
        
        final_score = self.get_score()
        if(final_score[0] == final_score[1]):
            return "it's a draw"
        else:
            return final_score.index(max(final_score))
    def getloser(self):
       
        final_score = self.get_score()
        if(final_score[0] == final_score[1]):
            return "it's a draw"
        else:
            return final_score.index(min(final_score))        
    def is_over(self):
        for row in self.grid:
            if(0 in row):
                print("game not over")
                return False
        print("game over")
        return True
    def step(self):
        self.grid[self.player1_pos[0]][self.player1_pos[1]] = 1
        self.grid[self.player2_pos[0]][self.player2_pos[1]] = 2
    def reset(self):
        self.grid = [[0] * self.dimension for i in range(self.dimension)]
        self.grid[0][0] = 1 
        self.grid[self.dimension-1][self.dimension-1] = 2
        self.current_player = 0
        self.player1_pos = [0, 0]
        self.player2_pos = [self.dimension-1, self.dimension-1]
        self.shuffleplayers()
    def display(self):
        return self.displayable
    def play(self):
        self.current_player = 0
        while(not self.is_over()):
            self.step()
            if(self.is_over()):
                self.get_winner()
    def  switch_player(self):
        self.current_player = 1 - self.current_player
    def get_movement(self, movement):
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
        Vérifie si le mouvement est valide avant de l'appliquer
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
    
    def move_with_retry(self, player):
        movement = input("Entrez un mouvement (up, down, left, right) : ").strip().lower()
        
        if self.move(player, movement):
            print(f"Mouvement '{movement}' validé !")
        else:
            print("Mouvement invalide, veuillez réessayer.")
            self.move_with_retry(player)  # Récursion si mouvement invalide

class CubeePlayer():
    def __init__(self, player_name):
        self.player_name = player_name
    def play(self):
        return random.choice([1,2,3,4])        
        

class CubeeHuman(CubeePlayer):
    def __init__(self, player_name):
        self.player_name = player_name
        print()
def example_movement():
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