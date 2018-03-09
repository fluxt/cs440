import numpy as np
import gomoku
user_game_board = np.array([[0, 0, 1, 2, 3, 4, 5, 6],
[6,  0, 0, 0, 0, 0, 0 ,0],
[5,  0, 0, 0, 0, 0, 0 ,0],
[4,  0, 0, 0, 0, 0, 0 ,0],
[3,  0, 0, 0, 0, 0, 0 ,0],
[2,  0, 0, 0, 0, 0, 0 ,0],
[1,  0, 0, 0, 0, 0, 0 ,0],
[0,  0, 0, 0, 0, 0, 0 ,0]])

class UserInterface:
    def __init__(self, player_num):
        self.player_num = player_num

    def getMove(self, game_board):
        return get_move(game_board, self.player_num)

#char(ord('a')+move_number)
def print_user_board(game_board):
    print("\n current board is: \n")
    for x in range(1,8):
        for y in range (1,8):
            user_game_board[x][y] = game_board[x-1][y-1]
    print(user_game_board)
    return 0

def get_coordinates(game_board):
    x = int (input("Enter X coordinate for stone (0-6): "))
    y = int (input("Enter Y coordinate for stone (0-6): "))
    pos = (6 - y,x)
    return pos

def get_move(game_board, player_num):
    print_user_board(game_board)
    playerPos = get_coordinates(game_board)
    if game_board[playerPos[0]][playerPos[1]] != 0:
        print("Error Please Try Again, space already taken")
        playerPos = get_coordinates(game_board)
    return playerPos
