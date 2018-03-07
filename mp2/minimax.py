
import numpy as np
import gomoku

class Minimax:
	def __init__(self, color, max_depth):
		self.color = color
		self.max_depth = max_depth

	def getMove(self, game_board_original):
		game_board = game_board_original[:]

		empty_squares = [tuple(e) for e in np.argwhere(game_board==0)]
		if self.color == 1: # maximizing
			best_value = float("-inf")
			for coord in empty_squares:
				game_board[coord] = 1
				value = self.getMoveRecursive(game_board, self.max_depth, 2)
				if value > best_value:
					best_value = value
					best_coord = coord
				game_board[coord] = 0
			return best_coord
		else: # minimizing
			best_value = float("inf")
			for coord in empty_squares:
				game_board[coord] = 2
				value = self.getMoveRecursive(game_board, self.max_depth, 1)
				if value < best_value:
					best_value = value
					best_coord = coord
				game_board[coord] = 0
			return best_coord

	def getMoveRecursive(self, game_board, depth, color):
		if depth == 0 or self.check_win(game_board, 2 if color == 1 else 1):
			return self.heuristic(game_board, color)
		empty_squares = [tuple(e) for e in np.argwhere(game_board==0)]
		if color == 1: # maximizing
			best_value = float("-inf")
			for coord in empty_squares:
				game_board[coord] = 1
				value = self.getMoveRecursive(game_board, depth-1, 2)
				if value > best_value:
					best_value = value
				game_board[coord] = 0
			return best_value
		else: # minimizing
			best_value = float("inf")
			for coord in empty_squares:
				game_board[coord] = 2
				value = self.getMoveRecursive(game_board, depth-1, 1)
				if value < best_value:
					best_value = value
				game_board[coord] = 0
			return best_value

	def check_win(self, game_board, color):
		return 0

	def heuristic(self, game_board, color):
		return 0
	

# function minimax(node, depth, maximizingPlayer)
#     if depth = 0 or node is a terminal node
#         return the heuristic value of node
#     if maximizingPlayer
#         bestValue := −∞
#         for each child of node
#             v := minimax(child, depth − 1, FALSE)
#             bestValue := max(bestValue, v)
#         return bestValue
#     else    (* minimizing player *)
#         bestValue := +∞
#         for each child of node
#             v := minimax(child, depth − 1, TRUE)
#             bestValue := min(bestValue, v)
#         return bestValue
