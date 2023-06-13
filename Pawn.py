import pygame

from Piece import Piece


class Pawn(Piece):
	def __init__(self, pos, color, board):
		super().__init__(pos, color, board)

		images_path = 'images/' + color[0] + 'P.png'
		self.images = pygame.image.load(images_path)
		self.images = pygame.transform.scale(self.images, (board.square_width - 35, board.square_height - 35))

		self.notation = ' '

	def get_possible_moves(self, board):
		output = []
		motion = []

		# move forward
		if self.color == 'white':
			motion.append((0, -1))
			if not self.has_moved:
				motion.append((0, -2))

		elif self.color == 'black':
			motion.append((0, 1))
			if not self.has_moved:
				motion.append((0, 2))

		for move in motion:
			new_pos = (self.x, self.y + move[1])
			if new_pos[1] < 8 and new_pos[1] >= 0:
				output.append(board.get_playing_from_pos(new_pos))
		return output

	def possible_moves(self, board):
		output = []
		for playing in self.get_possible_moves(board):
			if playing.location_piece != None:
				break
			else:
				output.append(playing)
		if self.color == 'white':
			if self.x + 1 < 8 and self.y - 1 >= 0:
				playing = board.get_playing_from_pos((self.x + 1, self.y - 1))
				if playing.location_piece != None and playing.location_piece.color != self.color:
					output.append(playing)
			if self.x - 1 >= 0 and self.y - 1 >= 0:
				playing = board.get_playing_from_pos((self.x - 1, self.y - 1))
				if playing.location_piece != None and playing.location_piece.color != self.color:
					output.append(playing)
		elif self.color == 'black':
			if self.x + 1 < 8 and self.y + 1 < 8:
				playing = board.get_playing_from_pos((self.x + 1, self.y + 1))
				if playing.location_piece != None and playing.location_piece.color != self.color:
					output.append(playing)
			if self.x - 1 >= 0 and self.y + 1 < 8:
				playing = board.get_playing_from_pos((self.x - 1, self.y + 1))
				if playing.location_piece != None and playing.location_piece.color != self.color:
					output.append(playing)
		return output

	def attacking_playings(self, board):
		moves = self.possible_moves(board)
		#диагональные ходы
		return [i for i in moves if i.x != self.x]