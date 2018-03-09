
import numpy as np
import gomoku

class MiniMax:
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
		ret = 0.0
		end_result = gomoku.get_game_status(game_board)
		if end_result == 3:
			return 0
		elif end_result == 1:
			return 10000
		elif end_result == 2:
			return -10000
		for i in range(7):
			for j in range(7):
				if game_board[i][j] == 1:
					ret += 3-max(abs(i-3), abs(j-3))
				elif game_board[i][j] == 2:
					ret -= 3-max(abs(i-3), abs(j-3))
		return ret

	def getMove(self, game_board_original):
		# make a copy
		game_board = game_board_original.copy()
		# if not np.any(game_board):
		# 	return (3, 3)

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
				best_value = max(best_value, self.getMoveRecursive(game_board, depth-1, 2))
				game_board[coord] = 0
		else: # minimizing
			best_value = float("inf")
			for coord in empty_squares:
				game_board[coord] = 2
				best_value = min(best_value, self.getMoveRecursive(game_board, depth-1, 1))
				game_board[coord] = 0
		return best_value

if __name__ == "__main__":
	agent_red = MiniMax(1, 3)
	agent_blu = MiniMax(2, 3)
	gomoku.play_game(agent_blu, agent_red)
