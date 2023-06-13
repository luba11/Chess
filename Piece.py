import pygame

num_moves = 0


class Piece: #класс фигур
	def __init__(self, pos, color, board):
		self.pos = pos
		self.x = pos[0]
		self.y = pos[1]
		self.color = color
		self.has_moved = False

	def move(self, board, playing, force=False):
		global num_moves
		for i in board.playings:
			i.highlight = False

		if playing in self.allowed_moves(board) or force: #начальные позиции фигур
			num_moves += 1
			prev_playing = board.get_playing_from_pos(self.pos)
			self.pos, self.x, self.y = playing.pos, playing.x, playing.y

			prev_playing.location_piece = None
			playing.location_piece = self
			board.choose_piece = None
			self.has_moved = True

			if self.notation == ' ':
				if self.y == 0 or self.y == 7:
					from Queen import Queen
					playing.location_piece = Queen((self.x, self.y), self.color, board)

			if self.notation == 'K':
				if prev_playing.x - self.x == 2:
					rook = board.get_piece_from_pos((0, self.y))
					rook.move(board, board.get_playing_from_pos((3, self.y)), force=True)
				elif prev_playing.x - self.x == -2:
					rook = board.get_piece_from_pos((7, self.y))
					rook.move(board, board.get_playing_from_pos((5, self.y)), force=True)

			return True
		else:
			board.choose_piece = None
			return False

	def possible_moves(self, board): #возможные ходы
		output = []
		for direction in self.get_possible_moves(board):
			for playing in direction:
				if playing.location_piece is not None:
					if playing.location_piece.color == self.color:
						break
					else:
						output.append(playing)
						break
				else:
					output.append(playing)
		return output

	def allowed_moves(self, board):#разрешенные ходы
		output = []
		for playing in self.possible_moves(board):
			if not board.in_check(self.color, board_change=[self.pos, playing.pos]):
				output.append(playing)
		return output

	# Верно для всех фигур, кроме пешки
	def attacking_playings(self, board):
		return self.possible_moves(board)