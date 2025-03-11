import random


class CubeeGameModel():
    def __init__(self,dimension, player1, player2):
        self.dimension = dimension
        self.gameboard = [[0] * self.dimension for i in range(self.dimension)]
        self.gameboard[0][0] = 1
        self.gameboard[self.dimension-1][self.dimension-1] = 2
        print(self.gameboard)
        self.players = [player1, player2]
        self.current_player = 0
    def shuffleplayers(self):
        random.shuffle(self.players)        
class CubeePlayer():
    def __init__(self, player_name):
        self.player_name = player_name
    def play(self):
        return random.choice([1,2,3,4])        
        

class CubeeHuman(CubeePlayer):
    def __init__(self):
        print()
        

newModel = CubeeGameModel(5, 0, 0)

