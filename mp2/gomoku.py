import time
import numpy as np
import reflex
import minimax
import userplay
import alphabeta


def get_initial_board():
	return np.array([[0]*7]*7)

def get_init_alpha_board():
	return np.array([['.']*7]*7)

def has_pattern_position(board, pattern):
	size = len(pattern)

	# check horizontal
	for x in range(8 - size):
		for y in range(7):
			good = True
			for i in range(size):
				if board[x+i][y] != pattern[i]:
					good = False
			if good:
				return True

	# vertical
	for x in range(7):
		for y in range(8 - size):
			good = True
			for i in range(size):
				if board[x][y+i] != pattern[i]:
					good = False
			if good:
				return True

	# top-left to bottom-right diagonal
	for x in range(8 - size):
		for y in range(8 - size):
			good = True
			for i in range(size):
				if board[x+i][y+i] != pattern[i]:
					good = False
			if good:
				return True

	# top-right to bottom-left diagonal
	for x in range(size-1, 7):
		for y in range(8 - size):
			good = True
			for i in range(size):
				if board[x-i][y+i] != pattern[i]:
					good = False
			if good:
				return True

	return 0

# returns 0 if game is not finished
# or 1/2 if that player has won
# or 3 if it is a draw
def get_game_status(game_board):
	p1Win = has_pattern_position(game_board, [1]*5)
	if p1Win:
		return 1

	p2Win = has_pattern_position(game_board, [2]*5)
	if p2Win:
		return 2

	for x in range(7):
		for y in range(7):
			if not game_board[x][y]:
				return 0

	return 3

def print_char_board(board):
	print("BOARD:")
	for row in reversed(board.T):
		print("".join(row))

def play_game(red, blue):
	game_board = get_initial_board()
	alphabet_board = get_init_alpha_board()
	move_number = 0

	while True:
		#check red move
		current_move = red.getMove(game_board)
		# set player to red
		game_board[current_move] = 1
		alphabet_board[current_move] = chr(ord('a')+ move_number)
		#print("Red's Move " + str(move_number))
		#userplay.print_user_board(game_board)
		# check for winner
		game_status = get_game_status(game_board)
		if game_status == 1:
			print("RED WINS!")
		if game_status == 3:
			print("ITS A TIE!")
		if game_status != 0:
			print_char_board(alphabet_board)
			return game_status


		#check blue move
		current_move = blue.getMove(game_board)
		# set player to blue
		game_board[current_move] = 2
		alphabet_board[current_move] = chr(ord('A')+ move_number)
		#print("Blue's Move " + str(move_number))
		#userplay.print_user_board(game_board)
		# check for winner
		game_status = get_game_status(game_board)
		if game_status == 2:
			print("BLUE WINS!")
		if game_status == 3:
			print("ITS A TIE!")
		if game_status != 0:
			print_char_board(alphabet_board)
			return game_status

		move_number += 1

if __name__ == "__main__":
	alpha_beta_red = alphabeta.AlphaBeta(1,3)
	alpha_beta_blue = alphabeta.AlphaBeta(2,3)
	minimax_red = minimax.MiniMax(1,3)
	minimax_blue = minimax.MiniMax(2,3)
	reflex_red = reflex.ReflexAgent(1)
	reflex_blue = reflex.ReflexAgent(2)

	print ("Alpha-Beta vs MiniMax")
	start_1 = time.time()
	play_game(alpha_beta_red, minimax_blue)
	end_1 = time.time()
	print("total runtime : {0:.3f} seconds".format(end_1-start_1))
	print("Red nodes expanded: " + str(alpha_beta_red.get_nodes_expanded()))
	alpha_beta_red.reset()
	print("Blue nodes expanded: " + str(minimax_blue.get_nodes_expanded()))
	minimax_blue.reset()

	print ("MiniMax vs Alpha-Beta")
	start_2 = time.time()
	play_game(minimax_red, alpha_beta_blue)
	end_2 = time.time()
	print("total runtime : {0:.3f} seconds".format(end_2-start_2))
	print("Red nodes expanded: " + str(minimax_red.get_nodes_expanded()))
	minimax_red.reset()
	print("Blue nodes expanded: " + str(alpha_beta_blue.get_nodes_expanded()))
	alpha_beta_blue.reset()

	print("Alpha-Beta vs Reflex")
	start_3 = time.time()
	play_game(alpha_beta_red, reflex_blue)
	end_3 = time.time()
	print("total runtime : {0:.3f} seconds".format(end_3-start_3))
	print("Red nodes expanded: " + str(alpha_beta_red.get_nodes_expanded()))
	alpha_beta_red.reset()

	print("Reflex vs Alpha-Beta")
	start_4 = time.time()
	play_game(reflex_red, alpha_beta_blue)
	end_4 = time.time()
	print("total runtime : {0:.3f} seconds".format(end_4-start_4))
	print("Blue nodes expanded: " + str(alpha_beta_blue.get_nodes_expanded()))
	alpha_beta_blue.reset()

	print("Reflex vs MiniMax")
	start_5 = time.time()
	play_game(reflex_red, minimax_blue)
	end_5 = time.time()
	print("total runtime : {0:.3f} seconds".format(end_5-start_5))
	print("Blue nodes expanded: " + str(minimax_blue.get_nodes_expanded()))
	minimax_blue.reset()

	print("MiniMax vs Reflex")
	start_6 = time.time()
	play_game(minimax_red, reflex_blue)
	end_6 = time.time()
	print("total runtime : {0:.3f} seconds".format(end_6-start_6))
	print("Red nodes expanded: " + str(minimax_red.get_nodes_expanded()))
	minimax_red.reset()
