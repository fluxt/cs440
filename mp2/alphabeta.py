
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
		# if not np.any(game_board):
		# 	return (3, 3)
		
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

		empty_squares = [tuple(e) for e in np.argwhere(game_board==0)]
		if color == 1: # maximizing
			best_value = float("-inf")
			for coord in empty_squares:
				game_board[coord] = 1
				best_value = max(best_value, self.getMoveRecursive(game_board, depth-1, a, b, 2))
				a = max(a, best_value)
				game_board[coord] = 0
				if b <= a: break
		else: # minimizing
			best_value = float("inf")
			for coord in empty_squares:
				game_board[coord] = 2
				best_value = min(best_value, self.getMoveRecursive(game_board, depth-1, a, b, 1))
				b = min(b, best_value)
				game_board[coord] = 0
				if b <= a: break
		return best_value

if __name__ == "__main__":
	agent_red = AlphaBeta(1, 3)
	agent_blu = AlphaBeta(2, 3)
	gomoku.play_game(agent_blu, agent_red)