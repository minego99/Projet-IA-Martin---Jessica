# __________________________EXERCISE 4___________________________

import random

class Player:
    def __init__(self, name, game=None):
        self.name = name
        self.game = game
        self.nb_wins = 0
        self.nb_loses = 0

    @property
    def nb_games(self): #attribut dérivable
        return self.nb_wins + self.nb_loses
    
    @staticmethod
    def play(self):
        return random.choice([1, 2, 3])

    def win(self):
        self.nb_wins += 1

    def lose(self):
        self.nb_loses += 1

    def __str__(self):
        return f"{self.name} (Wins: {self.nb_wins}, Losses: {self.nb_loses})"


class Human(Player):
    def play(self):
        choice = 0
        while choice not in [1, 2, 3]:
            choice = int(input("Choose 1, 2, or 3 matches to remove: "))
        return choice


class Game:
    def __init__(self, nb_matches, player1, player2, displayable=True):
        self.original_nb = self.nb = nb_matches
        self.players = [player1, player2]
        self.displayable = displayable
        for player in self.players:
            player.game = self
        self.shuffle()


    def shuffle(self): #mélange l'ordre des joueurs 
        random.shuffle(self.players)

    def reset(self):
        self.nb = self.original_nb #remet la partie à 0
        self.shuffle()

    def display(self): 
        if self.displayable:
            print(f"Current number of matches: {self.nb}")

    def step(self, action): #màj de l'état du jeu en modifiant nb matches restants dans le jeu
        self.nb -= action #action rerpésente le nb de matches restants

    def play(self):
        current_player = 0
        while self.nb > 0:
            self.display()
            action = self.players[current_player].play()
            self.step(action) 
    
            #check si le jeu doit se terminer
            if self.nb <= 0:
                self.players[current_player].win()
                self.players[1 - current_player].lose() #1 - current_player" pour basculer entre deux joueurs où current_player est 0 ou 1. Si current_player = 0, alors 1 - 0 devient 1 et inversement
            else:
                #changez de joueur si le jeu continue
                current_player = 1 - current_player



if __name__ == "__main__":
    player1 = Human("Alice")
    player2 = Player("Random Bot")
    game = Game(6, player1, player2)
    
    game.play()
    print(player1)
    print(player2)


