from collections import defaultdict
import time
import numpy as np
import reflex
import minimax
import userplay
import alphabeta

# initialize the board for the gomoko game
gomoku_board = np.array([[0]*7]*7)
#initialize alphabet array
init_alpha_board = np.chararray((7,7))
init_alpha_board[:] = '.'

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
    for x in range(size-1, 7):
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
    alphabet_board = init_alpha_board
    move_number = 0
    while True:
        #check red move
        current_move = red.getMove(game_board)
        # set player to red
        game_board[current_move] = 1
        alphabet_board[current_move] = chr(ord('a')+ move_number)
        print("Red's Move " + str(move_number))
        userplay.print_user_board(game_board)
        # check for winner
        game_status = get_game_status(game_board)
        if game_status == 1:
            print("RED WINS OHHH YEAHHHH!!")
        if game_status != 0:
            print(alphabet_board)
            return game_status


        #check blue move
        current_move = blue.getMove(game_board)
		# set player to blue
        game_board[current_move] = 2
        alphabet_board[current_move] = chr(ord('A')+ move_number)
        print("Blue's Move " + str(move_number))
        userplay.print_user_board(game_board)
        # check for winner
        game_status = get_game_status(game_board)
        if game_status == 2:
            print("BLUE WINS AWWW YISSSS!!")
        if game_status != 0:
            print(alphabet_board)
            return game_status

        move_number += 1

#print("\n current Board is:\n" + str(Node(gomoku_board, 2)))
if __name__ == "__main__":
    #print("\n current Board is:\n" + str((gomoku_board, 2)))
	agent_red = userplay.UserInterface(1)
	agent_blu = alphabeta.AlphaBeta(2, 3)
	play_game(agent_red, agent_blu)

    # board = np.array([[1, 2, 1, 1, 2, 2, 1],
    #                   [2, 2, 1, 2, 1, 1, 1],
    #                   [2, 1, 2, 1, 2, 2, 1],
    #                   [1, 1, 1, 1, 2, 2, 2],
    #                   [0, 2, 1, 2, 2, 2, 0],
    #                   [0, 2, 1, 2, 1, 1, 0],
    #                   [0, 0, 0, 0, 1, 0, 0]])

    # print(get_game_status(board))
