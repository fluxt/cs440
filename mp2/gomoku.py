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
    for x in range(7):
        for y in range(3):
            for i in range(5):
                if game_board[x][y+1] == player_num: 




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
