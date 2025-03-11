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
           # self.move(self.current_player, movement)
            self.step()
            if(self.is_over()):
                self.get_winner()
    # def move(self, player, movement):
    #     """
    #     incrémenter player1pos ou player2pos
    #     """
    #     if(player == self.player1):         
    #         if(movement == "up"):
    #         elif(movement == "left"):
    #         elif(movement == "right"):
    #         else:
    #     else:
    #         if(movement == "up"):
    #         elif(movement == "left"):
    #         elif(movement == "right"):
    #         else:
class CubeePlayer():
    def __init__(self, player_name):
        self.player_name = player_name
    def play(self):
        return random.choice([1,2,3,4])        
        

class CubeeHuman(CubeePlayer):
    def __init__(self):
        print()
        

newModel = CubeeGameModel(5, 0, 0)
print(newModel.get_winner())