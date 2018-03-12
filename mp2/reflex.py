import gomoku
import numpy as np

class ReflexAgent:
    def __init__(self, player_num):
        self.player_num = player_num

    def getMove(self, game_board):
        move = get_move(game_board, self.player_num)
        return move

# searches the board for a horizontal, vertical, or diagonal section that matches pattern
# returns a list of tuples representing the locations where the pattern was found
def get_pattern_positions(board, pattern, ret_idxs):
    size = len(pattern)
    ret = []
    # check horizontal
    for x in range(8 - size):
        for y in range(7):
            good = True
            for i in range(size):
                if board[x+i][y] != pattern[i]:
                    good = False
            if good:
                for ret_idx in ret_idxs:
                    ret.append((x + ret_idx, y))

    # vertical
    for x in range(7):
        for y in range(8 - size):
            good = True
            for i in range(size):
                if board[x][y+i] != pattern[i]:
                    good = False
            if good:
                for ret_idx in ret_idxs:
                    ret.append((x, y + ret_idx))

    # top-left to bottom-right diagonal
    for x in range(8 - size):
        for y in range(8 - size):
            good = True
            for i in range(size):
                if board[x+i][y+i] != pattern[i]:
                    good = False
            if good:
                for ret_idx in ret_idxs:
                    ret.append((x + ret_idx, y + ret_idx))

    # top-right to bottom-left diagonal
    for x in range(size-1, 7):
        for y in range(8 - size):
            good = True
            for i in range(size):
                if board[x-i][y+i] != pattern[i]:
                    good = False
            if good:
                for ret_idx in ret_idxs:
                    ret.append((x - ret_idx, y + ret_idx))

    return ret

def get_left_bottom(positions):
    left_most_val = 9
    left_most_list = []
    for pos in positions:
        if pos[0] == left_most_val:
            left_most_list.append(pos)
        elif pos[0] < left_most_val:
            left_most_list = [pos]
            left_most_val = pos[0]

    return min(left_most_list, key= lambda x: x[1])

def get_move(board, player_num):
    other_player_num = 1 if player_num == 2 else 2

    winning_positions = get_pattern_positions(board, [0, player_num, player_num, player_num, player_num], [0])
    winning_positions.extend(get_pattern_positions(board, [player_num, 0, player_num, player_num, player_num], [1]))
    winning_positions.extend(get_pattern_positions(board, [player_num, player_num, 0, player_num, player_num], [2]))
    winning_positions.extend(get_pattern_positions(board, [player_num, player_num, player_num, 0, player_num], [3]))
    winning_positions.extend(get_pattern_positions(board, [player_num, player_num, player_num, player_num, 0], [4]))

    if len(winning_positions) > 0:
        return get_left_bottom(winning_positions)


    four_block_positions = get_pattern_positions(board, [0, other_player_num, other_player_num, other_player_num, other_player_num], [0])
    four_block_positions.extend(get_pattern_positions(board, [other_player_num, other_player_num, other_player_num, other_player_num, 0], [4]))

    if len(four_block_positions) > 0:
        return get_left_bottom(four_block_positions)

    three_block_positions = get_pattern_positions(board, [0, other_player_num, other_player_num, other_player_num, 0], [0, 4])
    if len(three_block_positions) > 0:
        return get_left_bottom(three_block_positions)

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
                elif (i > 0 and board[x+i-1][y] == player_num) or (i < 4 and board[x+i+1][y] == player_num):
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
                elif (i > 0 and board[x][y+i-1] == player_num) or (i < 4 and board[x][y+i+1] == player_num):
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
                elif (i > 0 and board[x+i-1][y+i-1] == player_num) or (i < 4 and board[x+i+1][y+i+1] == player_num):
                    valid_positions.append((x+i, y+i))
            if good and mine_count == highest_mine_count:
                best_positions.extend(valid_positions)
            elif good and mine_count > highest_mine_count and len(valid_positions) > 0:
                best_positions = valid_positions
                highest_mine_count = mine_count

    # top-right to bottom-left diagonal
    for x in range(4, 7):
        for y in range(3):
            good = True
            valid_positions = []
            mine_count = 0
            for i in range(5):
                if board[x-i][y+i] == other_player_num:
                    good = False
                elif board[x-i][y+i] == player_num:
                    mine_count += 1
                elif (i > 0 and board[x-i+1][y+i-1] == player_num) or (i < 4 and board[x-i-1][y+i+1] == player_num):
                    valid_positions.append((x-i, y+i))
            if good and mine_count == highest_mine_count:
                best_positions.extend(valid_positions)
            elif good and mine_count > highest_mine_count and len(valid_positions) > 0:
                best_positions = valid_positions
                highest_mine_count = mine_count

    if len(best_positions):
        return get_left_bottom(best_positions)

    empty = [tuple(e) for e in np.argwhere(board==0)]
    return empty[0]

def print_char_board(board):
	print("BOARD:")
	for row in reversed(board.T):
		print("".join(row))

def play_game(red, blue, game_board, alphabet_board, move_number):
	while True:
		#check red move
		current_move = red.getMove(game_board)
		# set player to red
		game_board[current_move] = 1
		alphabet_board[current_move] = chr(ord('a')+ move_number)
		#print("Red's Move " + str(move_number))
		#userplay.print_user_board(game_board)
		# check for winner
		game_status = gomoku.get_game_status(game_board)
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
		game_status = gomoku.get_game_status(game_board)
		if game_status == 2:
			print("BLUE WINS!")
		if game_status == 3:
			print("ITS A TIE!")
		if game_status != 0:
			print_char_board(alphabet_board)
			return game_status

		move_number += 1

if __name__ == "__main__":
    board = gomoku.get_initial_board()
    char_board = gomoku.get_init_alpha_board()
    board[1][1] = 1
    char_board[1][1] = 'a'
    board[5][5] = 2
    char_board[5][5] = 'A'
    reflex_red = ReflexAgent(1)
    reflex_blue = ReflexAgent(2)

    play_game(reflex_red, reflex_blue, game_board=board, alphabet_board=char_board, move_number=1)
