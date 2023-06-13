import pygame

from Rook import Rook
from Bishop import Bishop
from Knight import Knight
from Queen import Queen
from King import King
from Pawn import Pawn


class Board: #класс шахматной доски
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.square_width = width // 8
        self.square_height = height // 8
        self.choose_piece = None
        self.sequence = 'white'

        # шахматная доска
        self.config = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]

        self.playings = self.generate_playings()

        self.location_board()

    def generate_playings(self):
        output = []
        for y in range(8):
            for x in range(8):
                output.append(Playing(x, y, self.square_width, self.square_height))
        return output

    def get_playing_from_pos(self, pos):
        for playing in self.playings:
            if (playing.x, playing.y) == (pos[0], pos[1]):
                return playing

    def get_piece_from_pos(self, pos):
        return self.get_playing_from_pos(pos).location_piece

    def location_board(self): # расположение фигур на доске
        for y, row in enumerate(self.config):
            for x, piece in enumerate(row):
                if piece != '':
                    playing = self.get_playing_from_pos((x, y))
                    if piece[1] == 'R':
                        if piece[0] == 'w':
                            color = 'white'
                        else:
                            color = 'black'
                        playing.location_piece = Rook((x, y), color, self)
                    elif piece[1] == 'N':
                        if piece[0] == 'w':
                            color = 'white'
                        else:
                            color = 'black'
                        playing.location_piece = Knight((x, y), color, self)

                    elif piece[1] == 'B':
                        if piece[0] == 'w':
                            color = 'white'
                        else:
                            color = 'black'
                        playing.location_piece = Bishop((x, y), color, self)

                    elif piece[1] == 'Q':
                        if piece[0] == 'w':
                            color = 'white'
                        else:
                            color = 'black'
                        playing.location_piece = Queen((x, y), color, self)

                    elif piece[1] == 'K':
                        if piece[0] == 'w':
                            color = 'white'
                        else:
                            color = 'black'
                        playing.location_piece = King((x, y), color, self)

                    elif piece[1] == 'P':
                        if piece[0] == 'w':
                            color = 'white'
                        else:
                            color = 'black'
                        playing.location_piece = Pawn((x, y), color, self)

    def mouse_click(self, nx, ny): #щелчок
        x = nx // self.square_width
        y = ny // self.square_height
        clicked_playing = self.get_playing_from_pos((x, y))

        if self.choose_piece is None:
            if clicked_playing.location_piece is not None:
                if clicked_playing.location_piece.color == self.sequence:
                    self.choose_piece = clicked_playing.location_piece

        elif self.choose_piece.move(self, clicked_playing):
            if self.sequence == 'black': #последовательность
                self.sequence = 'white'
            else:
                self.sequence = 'black'

        elif clicked_playing.location_piece is not None:
            if clicked_playing.location_piece.color == self.sequence:
                self.choose_piece = clicked_playing.location_piece

    def in_check(self, color, board_change=None): #проверка
        output = False
        king_pos = None

        changing_piece = None
        old_playing = None
        new_playing = None
        new_playing_old_piece = None

        if board_change is not None:
            for playing in self.playings:
                if playing.pos == board_change[0]:
                    changing_piece = playing.location_piece
                    old_playing = playing
                    old_playing.location_piece = None
            for playing in self.playings:
                if playing.pos == board_change[1]:
                    new_playing = playing
                    new_playing_old_piece = new_playing.location_piece
                    new_playing.location_piece = changing_piece

        pieces = [i.location_piece for i in self.playings if i.location_piece is not None]

        if changing_piece is not None:
            if changing_piece.notation == 'K':
                king_pos = new_playing.pos
        if king_pos is None:
            for piece in pieces:
                if piece.notation == 'K' and piece.color == color:
                    king_pos = piece.pos
        for piece in pieces:
            if piece.color != color:
                for playing in piece.attacking_playings(self):
                    if playing.pos == king_pos:
                        output = True

        if board_change is not None:
            old_playing.location_piece = changing_piece
            new_playing.location_piece = new_playing_old_piece

        return output

    def in_checkmate(self, color): #мат
        output = False

        for piece in [i.location_piece for i in self.playings]:
            if piece is not None:
                if piece.notation == 'K' and piece.color == color:
                    king = piece

        if king.allowed_moves(self) == []:
            if self.in_check(color):
                output = True

        return output

    def draw_board(self, display): #вывод на экран доски
        if self.choose_piece is not None:
            self.get_playing_from_pos(self.choose_piece.pos).highlight = True
            for playing in self.choose_piece.allowed_moves(self):
                playing.highlight = True

        for playing in self.playings:
            playing.draw_playing(display)


class Playing: #класс игровое поле
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.abs_x = x * width
        self.abs_y = y * height
        self.abs_pos = (self.abs_x, self.abs_y)
        self.pos = (x, y)
        if (x + y) % 2 == 0:
            self.draw_color = (255, 240, 245)
            self.highlight_color = (50, 205, 50)
        else:
            self.draw_color = (255, 192, 203)
            self.highlight_color = (127, 247, 159)
        self.location_piece = None #расположение фигуры
        self.coordinates = self.get_coordinates() #координировать
        self.highlight = False
        self.rect = pygame.Rect(self.abs_x, self.abs_y, self.width, self.height) #rect - прямоугольник

    def get_coordinates(self): #получение координат
        col = 'abcdefgh' #col - столбец
        return col[self.x] + str(self.y + 1)

    def draw_playing(self, display): #вывод на экран игровой площади
        if self.highlight:
            pygame.draw.rect(display, self.highlight_color, self.rect)
        else:
            pygame.draw.rect(display, self.draw_color, self.rect)
        if self.location_piece is not None:
            centre_rect = self.location_piece.images.get_rect()
            centre_rect.center = self.rect.center
            display.blit(self.location_piece.images, centre_rect.topleft)


quantity_moves = 0


class Piece: #класс фигур
    def __init__(self, pos, color, board):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.has_moved = False

    def move(self, board, playing, force=False):
        global quantity_moves
        for i in board.playings:
            i.highlight = False

        if playing in self.allowed_moves(board) or force: #начальные позиции фигур
            quantity_moves += 1
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