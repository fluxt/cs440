
import numpy as np
import gomoku
import copy

class AlphaBeta:
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
		elif result == 2:
			return -10000
		return 0

	def getMove(self, game_board_original):
		# make a copy
		game_board = game_board_original[:]
		if not np.any(game_board):
			return (3, 3)
		
		a = float("-inf")
		b = float("inf")
		
		empty_squares = [tuple(e) for e in np.argwhere(game_board==0)]
		if self.color == 1: # maximizing
			best_value = float("-inf")
			for coord in empty_squares:
				game_board[coord] = 1
				value = self.getMoveRecursive(game_board, self.max_depth, a, b, 2)
				if value > best_value:
					best_value = value
					best_coord = coord
				a = max(a, best_value)
				game_board[coord] = 0
		
		else: # minimizing
			best_value = float("inf")
			for coord in empty_squares:
				game_board[coord] = 2
				value = self.getMoveRecursive(game_board, self.max_depth, a, b, 1)
				if value < best_value:
					best_value = value
					best_coord = coord
				b = min(b, best_value)
				game_board[coord] = 0
		
		return best_coord

	def getMoveRecursive(self, game_board, depth, a, b, color):
		if depth == 0 or self.check_end(game_board) != 0:
			return self.heuristic(game_board)

		a_copy = copy.deepcopy(a) # python copies by reference
		b_copy = copy.deepcopy(b)
		empty_squares = [tuple(e) for e in np.argwhere(game_board==0)]
		if color == 1: # maximizing
			best_value = float("-inf")
			for coord in empty_squares:
				game_board[coord] = 1
				best_value = max(best_value, self.getMoveRecursive(game_board, depth-1, a_copy, b_copy, 2))
				a_copy = max(a_copy, best_value)
				if b_copy <= a_copy: break
				game_board[coord] = 0
		else: # minimizing
			best_value = float("inf")
			for coord in empty_squares:
				game_board[coord] = 2
				best_value = min(best_value, self.getMoveRecursive(game_board, depth-1, a_copy, b_copy, 1))
				b_copy = min(b_copy, best_value)
				if b_copy <= a_copy: break
				game_board[coord] = 0
		return best_value

if __name__ == "__main__":
	agent = AlphaBeta(1, 5)
	gomoku_board = np.array([[0]*7]*7)
	gomoku_board[0][3] = 2
	gomoku_board[0][4] = 2
	gomoku_board[0][5] = 2
	gomoku_board[0][6] = 2
	print(gomoku_board)
	print(agent.getMove(gomoku_board))
