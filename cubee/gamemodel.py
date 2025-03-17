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
                return False
        return False
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
    def move(self, player, movement):
        """
        incrémenter player1pos ou player2pos
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

        if(self.players[self.get_current_player()] == self.playerA):
             position_temp[0] += self.player1_pos[0]
             position_temp[1] += self.player1_pos[1]
        else:
             position_temp[0] += self.player2_pos[0]
             position_temp[1] += self.player2_pos[1]
             #coord X doit être >= 0 et < dimensions
             #coord Y doit être >= 0 et < dimensions
             #vérification pour rester DANS les dimensions du plateau de jeu

        if(position_temp[0] < self.dimension and position_temp[0] >= 0 and position_temp[1] < self.dimension and position_temp[1] >= 0): 
            print("mouvement", position_temp)
            if(self.players[self.get_current_player()] == self.playerA):
                if(self.grid[position_temp[0]][position_temp[1]] != 2):
                    self.player1_pos = position_temp
                else:
                    print("case déjà occupée")
            else:
                if(self.grid[position_temp[0]][position_temp[1]] != 1):
                    self.player2_pos = position_temp
                else:
                    print("case déjà occupée")
            return True
        else:
            #ajouter l'obtention d'un autre mouvement
            if(self.players[self.get_current_player()] == self.playerA):
                print("player1 bloqué: ",  self.player1_pos)
            else:
                print("player2 bloqué: ", self.player2_pos)
            return False
            
class CubeePlayer():
    def __init__(self, player_name):
        self.player_name = player_name
    def play(self):
        return random.choice([1,2,3,4])        
        

class CubeeHuman(CubeePlayer):
    def __init__(self):
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