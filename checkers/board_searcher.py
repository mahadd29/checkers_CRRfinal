from functools import reduce

class BoardSearcher:
	""" find, organize, and return information about a given board"""
	def build(self, board):
		""" 
		
		given a board, initialize lists and dictionaries of categorized positions and pieces, 
		call methods to populate  
		uncaptured pieces is a list of pieces where captured flag is False
		"""
		self.board = board
		self.uncaptured_pieces = list(filter(lambda piece: not piece.captured, board.pieces))
		self.open_positions = []
		self.filled_positions = []
		self.player_positions = {}
		self.player_pieces = {}
		self.position_pieces = {}

		self.build_filled_positions()
		self.build_open_positions()
		self.build_player_positions()
		self.build_player_pieces()
		self.build_position_pieces()

	def build_filled_positions(self):
		""" populate a list of positions that have pieces in them """
		self.filled_positions = reduce((lambda open_positions, piece: open_positions + [piece.position]), self.uncaptured_pieces, [])

	def build_open_positions(self):
		""" populate a list of positions that do not have pieces in them """
		self.open_positions = [position for position in range(1, self.board.position_count) if not position in self.filled_positions]

	def build_player_positions(self):
		""" set player positions to a dictionary with 2 lists of filled positions, 1 list for each player """
		self.player_positions = {
			1: reduce((lambda positions, piece: positions + ([piece.position] if piece.player == 1 else [])), self.uncaptured_pieces, []),
			2: reduce((lambda positions, piece: positions + ([piece.position] if piece.player == 2 else [])), self.uncaptured_pieces, [])
		}

	def build_player_pieces(self):
		""" set player pieces to a dictionary with  2 lists of pieces, 1 list for each player """
		self.player_pieces = {
			1: reduce((lambda pieces, piece: pieces + ([piece] if piece.player == 1 else [])), self.uncaptured_pieces, []),
			2: reduce((lambda pieces, piece: pieces + ([piece] if piece.player == 2 else [])), self.uncaptured_pieces, [])
		}

	def build_position_pieces(self):
		""" set position pieces to a list of pices on the board """
		self.position_pieces = {piece.position: piece for piece in self.uncaptured_pieces}

	def get_pieces_by_player(self, player_number):
		""" given a player id, return a list of their pieces """
		return self.player_pieces[player_number]

	def get_positions_by_player(self, player_number):
		""" given a player id, return a list of the positions of their pieces """
		return self.player_positions[player_number]

	def get_pieces_in_play(self):
		""" return a list of pieces on the board that are not captured or in the proces of cature """
		return self.player_pieces[self.board.player_turn] if not self.board.piece_requiring_further_capture_moves else [self.board.piece_requiring_further_capture_moves]

	def get_piece_by_position(self, position):
		""" get the piece at a given position """
		return self.position_pieces.get(position)