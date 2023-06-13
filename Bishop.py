import pygame


from Piece import Piece


class Bishop(Piece):
	def __init__(self, pos, color, board):
		super().__init__(pos, color, board)

		images_path = 'images/' + color[0] + 'B.png'
		self.images = pygame.image.load(images_path)
		self.images = pygame.transform.scale(self.images, (board.square_width - 20, board.square_height - 20))

		self.notation = 'B'

	def get_possible_moves(self, board):
		output = []

		movement_ne = []
		for i in range(1, 8):
			if self.x + i > 7 or self.y - i < 0:
				break
			movement_ne.append(board.get_playing_from_pos((self.x + i, self.y - i)))
		output.append(movement_ne)

		movement_se = []
		for i in range(1, 8):
			if self.x + i > 7 or self.y + i > 7:
				break
			movement_se.append(board.get_playing_from_pos((self.x + i, self.y + i)))
		output.append(movement_se)

		movement_sw = []
		for i in range(1, 8):
			if self.x - i < 0 or self.y + i > 7:
				break
			movement_sw.append(board.get_playing_from_pos((self.x - i, self.y + i)))
		output.append(movement_sw)

		movement_nw = []
		for i in range(1, 8):
			if self.x - i < 0 or self.y - i < 0:
				break
			movement_nw.append(board.get_playing_from_pos((self.x - i, self.y - i)))
		output.append(movement_nw)
		return output