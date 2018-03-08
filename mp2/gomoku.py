from collections import defaultdict
import time
import numpy as np
import reflex
import minimax
import alphabeta

# initialize the board for the gomoko game
gomoku_board = np.array([[0]*7]*7)

# searches the board for a horizontal, vertical, or diagonal section that matches pattern
# returns a tuple containing:
#   the left-most, then top-most position of the found pattern
# 	the position at the opposite end of the pattern
def get_pattern_position(board, pattern):
    size = len(pattern)

    # check horizontal
    for x in range(8 - size):
        for y in range(7):
            good = True
            for i in range(size):
                if board[x+i][y] != pattern[i]:
                    good = False
            if good:
                return ((x, y), (x+size-1, y))

    # vertical
    for x in range(7):
        for y in range(8 - size):
            good = True
            for i in range(size):
                if board[x][y+i] != pattern[i]:
                    good = False
            if good:
                return ((x, y), (x, y+size-1))

    # top-left to bottom-right diagonal
    for x in range(8 - size):
        for y in range(8 - size):
            good = True
            for i in range(size):
                if board[x+i][y+i] != pattern[i]:
                    good = False
            if good:
                return ((x, y), (x+size-1, y+size-1))

    # top-right to bottom-left diagonal
    for x in range(8 - size, 7):
        for y in range(8 - size):
            good = True
            for i in range(size):
                if board[x-i][y+i] != pattern[i]:
                    good = False
            if good:
                return ((x, y), (x-size+1 , y+size-1))

    return 0

# returns 0 if game is not finished
# or 1/2 if that player has won
# or 3 if it is a draw
def get_game_status(game_board):
	p1Win = get_pattern_position(game_board, [1]*5)
	if p1Win:
		return 1

	p2Win = get_pattern_position(game_board, [2]*5)
	if p2Win:
		return 2

	for x in range(7):
		for y in range(7):
			if not game_board[x][y]:
				return 0

	return 3
	

def play_game(red, blue):
    game_board = gomoku_board
    while True:
        current_move = red.getMove(game_board)
        # set player to red
        game_board[current_move] = 1
        print(game_board)
        # check for winner
        game_status = get_game_status(game_board)
        if game_status != 0:
            return game_status
        #check blue move
        current_move = blue.getMove(game_board)
		# set player to blue
        game_board[current_move] = 2
        print(game_board)
        # check for winner
        game_status = get_game_status(game_board)
        if game_status != 0:
            return game_status


#print("\n current Board is:\n" + str(Node(gomoku_board, 2)))
if __name__ == "__main__":
    red = reflex.ReflexAgent(1)
    blue = minimax.MiniMax(2, 3)
    play_game(red, blue)
