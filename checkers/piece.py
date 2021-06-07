from math import ceil
from argparse import ArgumentParser

class Piece:
	"""
	pieces are kept in lists in BOARDS
	individual checkers piece.  
	each piece has an associated BOARD, a position on that BOARD, and a player  
	pieces can find possible moves, move on the BOARD, and capture enemy pieces

	"""

	def __init__(self):
		""" initialize a new piece object.  set values to none/false/empty/zero"""
		self.player = None
		self.other_player = None
		self.king = False
		self.captured = False
		self.position = None
		self.board = None
		self.capture_move_enemies = {}
		self.reset_for_new_board()

	def reset_for_new_board(self):
		""" set lists of possible moves to None in a new board """
		self.possible_capture_moves = None
		self.possible_positional_moves = None

	def is_movable(self):
		""" return True if piece has possible moves and has not been captured """
		return (self.get_possible_capture_moves() or self.get_possible_positional_moves()) and not self.captured

	def capture(self):
		""" indicate capture and remove piece from board by setting position to None """
		self.captured = True
		self.position = None

	def move(self, new_position):
		""" change position to new position, king piece if at enemy side of board """
		self.position = new_position
		self.king = self.king or self.is_on_enemy_home_row()

	def get_possible_capture_moves(self):
		""" if the list of capture moves is empty, call method to build a list of possible capture moves """
		if self.possible_capture_moves == None:
			self.possible_capture_moves = self.build_possible_capture_moves()

		return self.possible_capture_moves

	def build_possible_capture_moves(self):
		""" 
		
		build a list of possible capture moves  
		capture move defined as moves to positions that are behind an enemy piece and open
		create a list of positions and call method which returns list of moves based on those positions  
		
		"""
		adjacent_enemy_positions = list(filter((lambda position: position in self.board.searcher.get_positions_by_player(self.other_player)), self.get_adjacent_positions()))
		capture_move_positions = []

		for enemy_position in adjacent_enemy_positions:
			enemy_piece = self.board.searcher.get_piece_by_position(enemy_position)
			position_behind_enemy = self.get_position_behind_enemy(enemy_piece)

			if (position_behind_enemy != None) and self.board.position_is_open(position_behind_enemy):
				capture_move_positions.append(position_behind_enemy)
				self.capture_move_enemies[position_behind_enemy] = enemy_piece

		return self.create_moves_from_new_positions(capture_move_positions)

	def get_position_behind_enemy(self, enemy_piece):
		""" find and return board positions behind and enemy piece """
		current_row = self.get_row()
		current_column = self.get_column()
		enemy_column = enemy_piece.get_column()
		enemy_row = enemy_piece.get_row()
		if current_row % 2 == 0: column_adjustment = -1
		else: column_adjustment = 1
		if current_column == enemy_column: column_behind_enemy = current_column + column_adjustment
		else: column_behind_enemy = enemy_column
		row_behind_enemy = enemy_row + (enemy_row - current_row)

		return self.board.position_layout.get(row_behind_enemy, {}).get(column_behind_enemy)

	def get_possible_positional_moves(self):
		""" if the list of positional (non-capture) moves is empty, call method to build a list of possible positional moves """
		if self.possible_positional_moves == None:
			self.possible_positional_moves = self.build_possible_positional_moves()

		return self.possible_positional_moves

	def build_possible_positional_moves(self):
		""" build a list of possible new positions, call method to return moves to those positions """
		new_positions = list(filter((lambda position: self.board.position_is_open(position)), self.get_adjacent_positions()))

		return self.create_moves_from_new_positions(new_positions)

	def create_moves_from_new_positions(self, new_positions):
		""" given a list of positions, create a list of moves from the current position to each new position """
		return [[self.position, new_position] for new_position in new_positions]

	def get_adjacent_positions(self):
		""" 
		
		create and return a list of positions adjacent to the current position  
		king pieces get a list of all positions, non-king pieces get only positions in front of them  
		
		"""
		adjacent_positions = self.get_directional_adjacent_positions(forward = True) 
		if self.king: 
			adjacent_positions = adjacent_positions + self.get_directional_adjacent_positions(forward = False)
		return adjacent_positions

	def get_column(self):
		""" return the column index of the piece's position """
		return (self.position - 1) % self.board.width

	def get_row(self):
		""" return the row index of the piece's position """ 
		return self.get_row_from_position(self.position)

	def is_on_enemy_home_row(self):
		""" return True if row index is 1 and the other player is 1, or if row index is width of the board and other player is not 1 """
		if self.other_player == 1: position = 1
		else: position = self.board.position_count
		return self.get_row() == self.get_row_from_position(position)

	def get_row_from_position(self, position):
		""" return row index based on board width and position in 1D board list """
		return ceil(position / self.board.width) - 1

	def get_directional_adjacent_positions(self, forward):
		""" get a list of positions adjacent to the piece, only forward positions if forward is True """
		positions = []
		current_row = self.get_row()
		
		if self.player == 1: player_val = 1
		else: player_val = -1
		if forward: forward_val = 1
		else: forward_val = -1
		next_row = current_row + player_val * forward_val

		if not next_row in self.board.position_layout:
			return []

		next_column_indexes = self.get_next_column_indexes(current_row, self.get_column())

		for column_index in next_column_indexes:
			positions.append(self.board.position_layout[next_row][column_index])
		return positions

	def get_next_column_indexes(self, current_row, current_column):
		""" get a list of column indices for columns adjacent to current position, based on position in 1D board list """
		if current_row % 2 == 0:
			column_indexes = [current_column, current_column + 1]
		else: column_indexes = [current_column - 1, current_column]

		return filter((lambda column_index: column_index >= 0 and column_index < self.board.width), column_indexes)

	def __setattr__(self, name, value):
		""" define piece player and value attributes """
		super(Piece, self).__setattr__(name, value)

		if name == 'player':
			self.other_player = 1 if value == 2 else 2