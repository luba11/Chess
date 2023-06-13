import pygame
from turtledemo import clock
from Board import Board

pygame.init()
pygame.mixer.init()
icon = pygame.image.load('chess_icon.png')
pygame.display.set_icon(icon)
display_size = width, height = (512, 512)
display = pygame.display.set_mode(display_size)
pygame.display.set_caption('Chess')
board = Board(display_size[0], display_size[1])
clock = pygame.time.Clock()


class Button: #класс клавиш
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (255, 20, 147)
        self.active_color = (255, 239, 213)

    def draw_button(self, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        self.type_action = action #action отвечает за действие
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(display, self.active_color, (x, y, self.width, self.height))
            if click[0] == 1 and action is not None:
                button_sound = pygame.mixer.Sound('sound.wav')
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()
        else:
            pygame.draw.rect(display, self.inactive_color, (x, y, self.width, self.height))

        text_output(message=message, x=x+10, y=y+10, font_size=font_size)


def main_menu(): #главное меню
    background = pygame.image.load('menu.png')
    start_button = Button(284, 60)
    options_button = Button(150, 60)
    quit_button = Button(330, 60)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        display.blit(background, (0, 0))
        start_button.draw_button(110, 90, 'Начать игру', playing, 38)
        options_button.draw_button(180, 195, 'Опции', options, 38)
        quit_button.draw_button(95, 300, 'Выйти из игры', quit, 38)
        pygame.display.update()
        clock.tick(60)
    quit()


def options():
    options = pygame.image.load('options.png')
    fun = pygame.image.load('fun.png')
    back_button = Button(358, 58)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        display.blit(options, (0, 0))
        display.blit(fun, (55, 230))
        back_button.draw_button(75, 440, 'В главное меню', main_menu, 40)
        text_output('~Обозначение функций~', 10, 20, 37)
        text_output('Стрелки вверх/вниз:', 10, 95, 25)
        text_output('* Регулирование музыки', 240, 135, 20)
        text_output('Клавиша пробел:', 10, 175, 25)
        text_output('* Пауза музыки', 240, 205, 20)
        pygame.display.update()
        clock.tick(60)
    quit()


def text_output(message, x, y, font_size, font_color=(0, 0, 0), font_type='fonts/font.ttf'):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def end_of_the_game():
    background = pygame.image.load('menu.png')
    quit_button = Button(330, 60)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        display.blit(background, (0, 0))
        quit_button.draw_button(95, 225, 'Выйти из игры', quit, 38)
        if board.in_checkmate('black'):
            text_output('Победу одержали Белые', 28, 50, 35)
        elif board.in_checkmate('white'):
            text_output('Победу одержали Черные', 24, 100, 32)
        pygame.display.update()
        clock.tick()
    quit()


def draw(display):
    display.fill('white')
    board.draw_board(display)
    pygame.display.update()


def playing(): #игровой цикл
    flPause = False
    pygame.mixer.music.load("fon_music.mp3")
    pygame.mixer.music.play(-1)
    running_game = True
    while running_game:
        nx, ny = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.mouse_click(nx, ny)
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flPause = not flPause
                    if flPause:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
            if keys[pygame.K_UP]:
                volume = pygame.mixer.music.get_volume() + 0.1
                pygame.mixer.music.set_volume(min(volume, 1.0))
            elif keys[pygame.K_DOWN]:
                volume = pygame.mixer.music.get_volume() - 0.1
                pygame.mixer.music.set_volume(max(volume, 0.0))
        if board.in_checkmate('black'):
            end_of_the_game()
            running_game = False
        elif board.in_checkmate('white'):
            end_of_the_game()
            running_game = False

        pygame.display.update()
        draw(display)
    pygame.mixer.music.stop()


main_menu()
pygame.quit()
quit()