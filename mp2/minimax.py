
import numpy as np
import gomoku

class Minimax:
	def __init__(self, color, max_depth):
		self.color = color
		self.max_depth = max_depth-1


# 0 if didn't end
# 1 if red won
# 2 if blue won
# 3 if draw
	def check_end(self, game_board):
		return gomoku.get_game_status(game_board)

	def heuristic(self, game_board):
		result = gomoku.get_game_status(game_board)
		if result == 1:
			return 10000
		if result == 2:
			return -10000
		return 0

	def getMove(self, game_board_original):
		# make a copy
		game_board = game_board_original[:]
		if not np.any(game_board):
			return (3, 3)

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
		if depth == 0 or self.check_end(game_board) != 0:
			return self.heuristic(game_board)

		empty_squares = [tuple(e) for e in np.argwhere(game_board==0)]
		if color == 1: # maximizing
			best_value = float("-inf")
			for coord in empty_squares:
				game_board[coord] = 1
				value = self.getMoveRecursive(game_board, depth-1, 2)
				best_value = max(best_value, value)
				game_board[coord] = 0
		else: # minimizing
			best_value = float("inf")
			for coord in empty_squares:
				game_board[coord] = 2
				value = self.getMoveRecursive(game_board, depth-1, 1)
				best_value = max(best_value, value)
				game_board[coord] = 0
		return best_value

if __name__ == "__main__":
	minimax = Minimax(1, 3)
	gomoku_board = np.array([[0]*7]*7)
	gomoku_board[0][2] = 2
	gomoku_board[0][3] = 2
	gomoku_board[0][4] = 2
	print(gomoku_board)
	print(minimax.getMove(gomoku_board))