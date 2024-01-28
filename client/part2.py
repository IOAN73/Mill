import sys
from pathlib import Path

import click
import pygame

from client.server_client import GameClient
from server.schemas import Color, Trick

CWD = Path.cwd()

GAME_BOARD_IMAGE_PATH = CWD / 'static' / 'pole.jpg'
BLACK_PIECE_IMAGE_PATH = CWD / 'static' / 'black.png'
WHITE_PIECE_IMAGE_PATH = CWD / 'static' / 'white.png'

# Инициализация Pygame
pygame.init()
client = GameClient()

# Загрузка изображений
game_board_image = pygame.image.load(GAME_BOARD_IMAGE_PATH)
black_piece_image = pygame.image.load(BLACK_PIECE_IMAGE_PATH)
white_piece_image = pygame.image.load(WHITE_PIECE_IMAGE_PATH)

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Установка размеров экрана
WIDTH, HEIGHT = game_board_image.get_width(), game_board_image.get_height()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Мельница")


def draw_start_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)

    text = font.render("Выберите режим игры", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 4))
    screen.blit(text, text_rect)

    button_font = pygame.font.Font(None, 28)

    two_players_button = pygame.Rect(WIDTH / 4, HEIGHT / 2, WIDTH / 2, 50)
    pygame.draw.rect(screen, BLACK, two_players_button)
    text = button_font.render("Игрок vs Игрок", True, WHITE)
    text_rect = text.get_rect(center=two_players_button.center)
    screen.blit(text, text_rect)

    vs_computer_button = pygame.Rect(WIDTH / 4, HEIGHT * 3 / 4, WIDTH / 2, 50)
    pygame.draw.rect(screen, BLACK, vs_computer_button)
    text = button_font.render("Игрок vs Компьютер", True, WHITE)
    text_rect = text.get_rect(center=vs_computer_button.center)
    screen.blit(text, text_rect)

    return two_players_button, vs_computer_button


# Функция для обработки начального экрана
def handle_start_screen_click(mouse_position, two_players_button, vs_computer_button, ):
    if two_players_button.collidepoint(mouse_position):
        return 'two_players'
    elif vs_computer_button.collidepoint(mouse_position):
        return 'vs_computer'
    else:
        return None


# Отрисовка экрана выбора цвета фишек
def draw_select_color_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)

    text = font.render("Выберите цвет фишки", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 4))
    screen.blit(text, text_rect)

    button_font = pygame.font.Font(None, 28)

    black_player_button = pygame.Rect(WIDTH / 4, HEIGHT / 2, WIDTH / 2, 50)
    pygame.draw.rect(screen, BLACK, black_player_button)
    text = button_font.render("Черные фишки", True, WHITE)
    text_rect = text.get_rect(center=black_player_button.center)
    screen.blit(text, text_rect)

    white_player_button = pygame.Rect(WIDTH / 4, HEIGHT * 3 / 4, WIDTH / 2, 50)
    pygame.draw.rect(screen, BLACK, white_player_button)
    text = button_font.render("Белые фишки", True, WHITE)
    text_rect = text.get_rect(center=white_player_button.center)
    screen.blit(text, text_rect)

    return black_player_button, white_player_button


selected_color = None
player_color = None


# Функция для обработки выбора цвета фишек экрана
# @click.command()
# @click.argument('player_color')
def handle_select_color_screen(mouse_position, black_player_button, white_player_button):
    global selected_color, player_color

    if black_player_button.collidepoint(mouse_position):
        selected_color = 'black'
        player_color = 'black'  # цвет другого игрока
        return 'black_player'
    elif white_player_button.collidepoint(mouse_position):
        selected_color = 'white'
        player_color = 'white'  # цвет другого игрока
        return 'white_player'
    else:
        return None


# Добавление координат точек на игровом поле
points = {(0, 0): (30, 30), (3, 0): (30, 350), (6, 0): (30, 670),
          (1, 1): (135, 140), (3, 1): (135, 350), (5, 1): (135, 560),
          (2, 2): (240, 240), (3, 2): (240, 350), (4, 2): (240, 450),
          (0, 3): (350, 30), (1, 3): (350, 140), (2, 3): (350, 240),
          (4, 3): (350, 450), (5, 3): (350, 560), (6, 3): (350, 670),
          (2, 4): (450, 240), (3, 4): (450, 350), (4, 4): (450, 450),
          (1, 5): (560, 140), (3, 5): (560, 350), (5, 5): (560, 560),
          (0, 6): (670, 30), (3, 6): (670, 350), (6, 6): (670, 670),
          }

# Расположение фишек
pieces = {(0, 0): None, (3, 0): None, (6, 0): None,
          (1, 1): None, (3, 1): None, (5, 1): None,
          (2, 2): None, (3, 2): None, (4, 2): None,
          (0, 3): None, (1, 3): None, (2, 3): None,
          (4, 3): None, (5, 3): None, (6, 3): None,
          (2, 4): None, (3, 4): None, (4, 4): None,
          (1, 5): None, (3, 5): None, (5, 5): None,
          (0, 6): None, (3, 6): None, (6, 6): None, }

# Расположение фишек black
black_pieces = {}

# Расположение фишек white
white_pieces = {}


# Функция отрисовки точек
def draw_points():
    for pos, (x, y) in points.items():
        pygame.draw.circle(screen, BLACK, (x, y), 10)
        font = pygame.font.Font(None, 24)
        text = font.render(str(pos), True, BLACK)  # Внесли изменение здесь
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)


# Преобразование позиции в координаты на экране
def position_to_pixel(position):
    col, row = int(position[0]), int(position[1])
    x = (col - 0.4) * 100 + 30
    y = (row - 1.4) * 100 + 20
    return x, y


# Функция для отрисовки игрового поля
def draw_board():
    screen.blit(game_board_image, (0, 0))
    draw_points()
    for position, piece in pieces.items():
        if piece == 'black':
            screen.blit(black_piece_image, (position_to_pixel(position)))
        elif piece == 'white':
            screen.blit(white_piece_image, (position_to_pixel(position)))

    for mill in game.mills:
        for i in range(len(mill.positions) - 1):
            pygame.draw.line(screen, (0, 255, 0), position_to_pixel(mill.positions[i]),
                             position_to_pixel(mill.positions[i + 1]), 3)
        pygame.draw.line(screen, (0, 255, 0), position_to_pixel(mill.positions[-1]),
                         position_to_pixel(mill.positions[0]), 3)


# Функция отрисовки линии мельницы
def draw_mill_line(positions):
    pygame.draw.line(screen, (255, 0, 0), position_to_pixel(positions[0]),
                     position_to_pixel(positions[1]), 2)


# Обработка кликов мыши для расстановки фишек
def handle_player_click_human(mouse_position):
    global black_pieces, white_pieces, turn

    clicked_position = get_clicked_position(mouse_position)

    if clicked_position:
        if turn == player_color:
            trick = Trick(color=Color[turn], position=clicked_position)
            client.set_trick(trick)
            print(f"{turn.capitalize()} player placed a piece at {clicked_position}.")
            change_turn()
        else:
            print("It's not your turn.")

        draw_board()
        pygame.display.flip()

        print_board()

        # Добавим обновление информации о фишках после успешного хода
        update_pieces_from_server(player_color, clicked_position)


turn = 'black'


def get_clicked_position(mouse_position):
    for pos, (x, y) in points.items():
        rect = pygame.Rect(x - 35, y - 35, 70, 70)
        if rect.collidepoint(mouse_position) and pieces[pos] is None:
            return pos
    return None


def get_mill_positions(position):
    # Получаем индексы строки и столбца из позиции
    row = int(position[1]) - 1
    col = ord(position[0]) - ord('A')

    # Горизонтальные линии
    if pieces.get(f'A{row + 1}') == pieces.get(f'B{row + 1}') == pieces.get(f'C{row + 1}'):
        return [f'A{row + 1}', f'B{row + 1}', f'C{row + 1}'], pieces.get(f'A{row + 1}')
    elif pieces.get(f'D{row + 1}') == pieces.get(f'E{row + 1}') == pieces.get(f'F{row + 1}'):
        return [f'D{row + 1}', f'E{row + 1}', f'F{row + 1}'], pieces.get(f'D{row + 1}')
    elif pieces.get(f'G{row + 1}') == pieces.get(f'A{row + 1}') == pieces.get(f'D{row + 1}'):
        return [f'G{row + 1}', f'A{row + 1}', f'D{row + 1}'], pieces.get(f'G{row + 1}')
    elif pieces.get(f'B{row + 1}') == pieces.get(f'D{row + 1}') == pieces.get(f'F{row + 1}'):
        return [f'B{row + 1}', f'D{row + 1}', f'F{row + 1}'], pieces.get(f'B{row + 1}')

    # Вертикальные линии
    if pieces.get(f'{chr(col + ord("A"))}1') == pieces.get(f'{chr(col + ord("A"))}2') == pieces.get(
            f'{chr(col + ord("A"))}3'):
        return [f'{chr(col + ord("A"))}1', f'{chr(col + ord("A"))}2', f'{chr(col + ord("A"))}3'], pieces.get(
            f'{chr(col + ord("A"))}1')
    elif pieces.get(f'{chr(col + ord("A"))}4') == pieces.get(f'{chr(col + ord("A"))}5') == pieces.get(
            f'{chr(col + ord("A"))}6'):
        return [f'{chr(col + ord("A"))}4', f'{chr(col + ord("A"))}5', f'{chr(col + ord("A"))}6'], pieces.get(
            f'{chr(col + ord("A"))}4')
    elif pieces.get(f'{chr(col + ord("A"))}7') == pieces.get(f'{chr(col + ord("A"))}4') == pieces.get(
            f'{chr(col + ord("A"))}1'):
        return [f'{chr(col + ord("A"))}7', f'{chr(col + ord("A"))}4', f'{chr(col + ord("A"))}1'], pieces.get(
            f'{chr(col + ord("A"))}7')

    return [], None


def update_pieces_from_server(color, position):
    global black_pieces, white_pieces

    if color == player_color:
        x, y = position_to_pixel(position)

        pieces[position] = player_color

        draw_board()
        pygame.display.flip()
    elif color == turn:  # Проверка текущего цвета, чтобы избежать дублирования ходов
        trick = Trick(color=Color[color], position=position)
        client.set_trick(trick)


def setup_pieces_human():
    global turn

    screen.fill(WHITE)
    draw_board()
    pygame.display.flip()

    while any(piece is None for piece in pieces.values()):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                handle_player_click_human(mouse_position)

                # Выводим текущее состояние доски
                print_board()

        # Вызываем отрисовку после выбора цвета
        draw_board()
        pygame.display.flip()


def main_game_loop(game_mode):
    global turn, player_color

    if game_mode == 'two_players':
        select_color_screen_buttons = draw_select_color_screen()
        selecting_color = True
        while selecting_color:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    color_choice = handle_select_color_screen(mouse_position, *select_color_screen_buttons)
                    if color_choice:
                        selecting_color = False
                        setup_pieces_human()  # Переносим вызов после успешного выбора цвета
            pygame.display.flip()

    elif game_mode == 'vs_computer':
        select_color_screen_buttons = draw_select_color_screen()
        selecting_color = True
        while selecting_color:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    color_choice = handle_select_color_screen(mouse_position, *select_color_screen_buttons)
                    if color_choice:
                        selecting_color = False
                        # comp master
            pygame.display.flip()

    while True:
        color, position = client.get_game()

        if color and position:
            update_pieces_from_server(color, position)
            draw_board()
            pygame.display.flip()


def change_turn():
    global turn
    turn = 'black' if turn == 'white' else 'white'


def print_board():
    for row in range(1, 8):
        for col in 'ABCDEFG':
            position = f"{col}{row}"
            piece = pieces.get(position, None)
            print(piece or '.', end=' ')
        print()


def main():
    global player_color

    game_mode = None
    start_screen_buttons = draw_start_screen()

    while game_mode is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                game_mode = handle_start_screen_click(mouse_position, *start_screen_buttons)

        pygame.display.flip()

    if game_mode:
        main_game_loop(game_mode)

        while True:
            color, position = client.get_game()

            if color and position:
                update_pieces_from_server(color, position)
                draw_board()
                pygame.display.flip()

    pygame.quit()
    sys.exit()


game = client.get_game()

if __name__ == "__main__":
    main()
