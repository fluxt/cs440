import gomoku

class ReflexAgent:
	def __init__(self, player_num):
		self.player_num = player_num

	def getMove(self, game_board):
		move = get_move(game_board, self.player_num)
		return move

def get_four_and_blank_position(board, player_num):
	pos1 = gomoku.get_pattern_position(board, [0, player_num, player_num, player_num, player_num])
	if (pos1):
		return pos1[0]

	pos2 =  gomoku.get_pattern_position(board, [player_num, player_num, player_num, player_num, 0])
	if (pos2):
		return pos2[1]

	return 0

def get_move(board, player_num):
	other_player_num = 1 if player_num == 2 else 2

	winning_position = get_four_and_blank_position(board, player_num)
	if winning_position:
		return winning_position

	blocking_position_1 = get_four_and_blank_position(board, player_num)
	if blocking_position_1:
		return blocking_position_1

	three_block = gomoku.get_pattern_position(board, [0,  player_num, player_num, player_num, 0])
	if three_block:
		return three_block[0]

	best_positions = []
	highest_mine_count = 0

	# check horizontal
	for x in range(3):
		for y in range(7):
			good = True
			valid_positions = []
			mine_count = 0
			for i in range(5):
				if board[x+i][y] == other_player_num:
					good = False
				elif board[x+i][y] == player_num:
					mine_count += 1
				else:
					valid_positions.append((x+i, y))
			if good and mine_count == highest_mine_count:
				best_positions.extend(valid_positions)
			elif good and mine_count > highest_mine_count and len(valid_positions) > 0:
				best_positions = valid_positions
				highest_mine_count = mine_count

	# vertical
	for x in range(7):
		for y in range(3):
			good = True
			valid_positions = []
			mine_count = 0
			for i in range(5):
				if board[x][y+i] == other_player_num:
					good = False
				elif board[x][y+i] == player_num:
					mine_count += 1
				else:
					valid_positions.append((x, y+i))
			if good and mine_count == highest_mine_count:
				best_positions.extend(valid_positions)
			elif good and mine_count > highest_mine_count and len(valid_positions) > 0:
				best_positions = valid_positions
				highest_mine_count = mine_count

	# top-left to bottom-right diagonal
	for x in range(3):
		for y in range(3):
			good = True
			valid_positions = []
			mine_count = 0
			for i in range(5):
				if board[x+i][y+i] == other_player_num:
					good = False
				elif board[x+i][y+i] == player_num:
					mine_count += 1
				else:
					valid_positions.append((x+i, y+i))
			if good and mine_count == highest_mine_count:
				best_positions.extend(valid_positions)
			elif good and mine_count > highest_mine_count and len(valid_positions) > 0:
				best_positions = valid_positions
				highest_mine_count = mine_count

	# top-right to bottom-left diagonal
	for x in range(3, 7):
		for y in range(3):
			good = True
			valid_positions = []
			mine_count = 0
			for i in range(5):
				if board[x-i][y+i] == other_player_num:
					good = False
				elif board[x-i][y+i] == player_num:
					mine_count += 1
				else:
					valid_positions.append((x-i, y+i))
			if good and mine_count == highest_mine_count:
				best_positions.extend(valid_positions)
			elif good and mine_count > highest_mine_count and len(valid_positions) > 0:
				best_positions = valid_positions
				highest_mine_count = mine_count

	print(best_positions)

	left_most_val = 9
	left_most_list = []
	for pos in best_positions:
		if pos[0] == left_most_val:
			left_most_list.append(pos)
		elif pos[0] < left_most_val:
			left_most_list = [pos]
	
	return min(left_most_list, key= lambda x: x[1])
