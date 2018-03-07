from collections import defaultdict
import time
import numpy as np

# initialize the board for the gomoko game
gomoku_board = np.array([[0]*7]*7)
# each node represents a different state print the board and the current turn
# class BoardState():
# 	def __init__(self, board, turn):
# 		self.board = board
# 		self.turn = turn
#
# 	def __eq__(self, other):
# 		return self.board == other.board and self.turn == other.turn
#
# 	def __hash__(self):
# 		return hash((self.board, self.turn))
#
# 	def __str__(self):
# 		return "Board: \n" + str(self.board) + "\nTurn: " + str(self.turn)
# red = 1
# blue = 2
# empty = 0

def get_game_status(game_board, player_num):
    player_num = game_board[player_num]
    # check the vertical cases on the gameboard
    for x in range(8):
        for y in range(4):
            vertcheck = 0
            for i in range(5):
                if game_board[x][y+i] == player_num:
                    vertcheck += 1
            if vertcheck == 5:
                return player_num
    # check the horizontal cases on the gameboard
    for x in range(4):
        for y in range(8):
            horizcheck = 0
            for i in range(5):
                if game_board[x+i][y] == player_num:
                    horizcheck += 1
            if horizcheck == 5:
                return player_num
    # check the forward diagonal cases on the gameboard
    for x in range(4):
        for y in range(4):
            diag1, diag2, diag3, diag4 = 0
            for i in range(5):
                if game_board[x+i][y+i+3] == player_num:
                    diag4 += 1
                if game_board[x+i][y+i+2] == player_num:
                    diag3 += 1
                if game_board[x+i][y+i+1] == player_num:
                    diag2 += 1
                if game_board[x+i][y+i] == player_num:
                    diag1 += 1
            if diag1 == 5 or diag2 == 5 or diag3 == 5:
                return player_num
# check the backwards diagonal cases on the gameboard
    for x in range(4):
        for y in range(4):
            diag1, diag2, diag3,diag4 = 0
            for i in range(5):
                if game_board[x+8-i][y+i+3] == player_num:
                    diag4 += 1
                if game_board[x+8-i][y+i+2] == player_num:
                    diag3 += 1
                if game_board[x+8-i][y+i+1] == player_num:
                    diag2 += 1
                if game_board[x+8-i][y+i] == player_num:
                    diag1 += 1
            if diag1 == 5 or diag2 == 5 or diag3 == 5:
                return player_num


def play_game(red, blue):
    game_board = gomoku_board
    while True:
        current_move = red.getMove(game_board)
        # set player to red
        game_board[current_move] = 1
        # check for winner
        game_status = get_game_status(game_board, 1)
        if game_status != 0:
            return game_status
        #check blue move
        current_move = blue.getMove(game_board)
        # set player to blue
        game_board[current_move] = 2
        # check for winner
        game_status = get_game_status(game_board, 2)
        if game_status != 0:
            return game_status


#print("\n current Board is:\n" + str(Node(gomoku_board, 2)))
if __name__ == "__main__":
    print("\n current Board is:\n" + str((gomoku_board, 2)))
