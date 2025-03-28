from gamemodel import CubeeGameModel
import pytest
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
def test_enclosure(grid, turn, expected):

		game = CubeeGameModel("P1", "P2", dimension=len(grid))
		game.grid = grid
		game.current_player = turn
		game.check_enclosure()
		assert game.grid == expected, f"{grid} =({turn})=> {game.grid}. But expected : {expected} "
test_check_enclosure_multiple_enclosure()
# newModel = CubeeGameModel(5, 'A', 'B')
