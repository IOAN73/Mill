import pygame
import sys
import random
from pathlib import Path
from client.client import get_game, set_trick
from server.schemas import Trick, Color

CWD = Path.cwd()
GAME_BOARD_IMAGE_PATH = CWD / 'static' /'pole.jpg'
BLACK_PIECE_IMAGE_PATH = CWD / 'static' / 'black.png'
WHITE_PIECE_IMAGE_PATH = CWD / 'static' / 'white.png'


# Инициализация Pygame
pygame.init()

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

turn = 'black'

# Функция для обработки начального экрана
def handle_start_screen_click(mouse_position, two_players_button, vs_computer_button):
    if two_players_button.collidepoint(mouse_position):
        return 'two_players'
    elif vs_computer_button.collidepoint(mouse_position):
        return 'vs_computer'
    else:
        return None


# Добавление координат точек на игровом поле
points = {'A1': (30, 670), 'A4': (30, 350), 'A7': (30, 30),
          'B2': (135, 560), 'B4': (135, 350), 'B6': (135, 140),
          'C3': (240, 450), 'C4': (240, 350), 'C5': (240, 240),
          'D1': (350, 670), 'D2': (350, 560), 'D3': (350, 450), 'D5': (350, 240), 'D6': (350, 140), 'D7': (350, 30),
          'E3': (450, 450), 'E4': (450, 350), 'E5': (450, 240),
          'F2': (560, 560), 'F4': (560, 350), 'F6': (560, 140),
          'G1': (670, 670), 'G4': (670, 350), 'G7': (670, 30)}

# Расположение фишек
pieces = {'A1': None, 'A4': None, 'A7': None,
          'B2': None, 'B4': None, 'B6': None,
          'C3': None, 'C4': None, 'C5': None,
          'D1': None, 'D2': None, 'D3': None, 'D5': None, 'D6': None, 'D7': None,
          'E3': None, 'E4': None, 'E5': None,
          'F2': None, 'F4': None, 'F6': None,
          'G1': None, 'G4': None, 'G7': None}

# Расположение фишек black
black_pieces = {}

# Расположение фишек white
white_pieces = {}


# Функция отрисовки точек
def draw_points():
    for pos, (x, y) in points.items():
        pygame.draw.circle(screen, BLACK, (x, y), 10)
        font = pygame.font.Font(None, 24)
        text = font.render(pos, True, BLACK)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)


# Преобразование позиции в координаты на экране
def position_to_pixel(position):
    letters = 'ABCDEFG'
    x = (letters.index(position[0]) - 0.4) * 100 + 25
    y = (int(position[1]) - 1.5) * 100 + 25
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


# Функция отрисовки линии мельницы
def draw_mill_line(positions):
    pygame.draw.line(screen, (255, 0, 0), position_to_pixel(positions[0]), position_to_pixel(positions[1]), 2)


# Обработка кликов мыши для расстановки фишек
def handle_player_click_human(mouse_position):
    global black_pieces, white_pieces
    # Добавление счетчиков фишек для каждого игрока
    black_pieces_count = 0
    white_pieces_count = 0

    pixel_position = mouse_position
    for pos, (x, y) in points.items():
        rect = pygame.Rect(x - 35, y - 35, 70, 70)
        if rect.collidepoint(pixel_position) and pieces[pos] is None:
            pieces[pos] = turn
            x, y = position_to_pixel(pos)
            if turn == 'black':
                black_pieces[pos] = (x // 100 + 1, y // 100 + 1)
                black_pieces_count += 1
                trick = Trick(color=Color.black, position=black_pieces[pos])
            else:
                white_pieces[pos] = (x // 100 + 1, y // 100 + 1)
                white_pieces_count += 1
                trick = Trick(color=Color.white, position=white_pieces[pos])
            change_turn()
            set_trick(trick)
            draw_board()
            pygame.display.flip()

    # Выводим словари после каждого хода
    print("Black Pieces:", black_pieces)
    print("White Pieces:", white_pieces)


def get_mill_positions(position):
    # Получаем индексы строки и столбца из позиции
    row = int(position[1]) - 1
    col = ord(position[0]) - ord('A')

    # Горизонтальные линии
    if pieces[f'A{row + 1}'] == pieces[f'B{row + 1}'] == pieces[f'C{row + 1}']:
        return [f'A{row + 1}', f'B{row + 1}', f'C{row + 1}']
    elif pieces[f'D{row + 1}'] == pieces[f'E{row + 1}'] == pieces[f'F{row + 1}']:
        return [f'D{row + 1}', f'E{row + 1}', f'F{row + 1}']
    elif pieces[f'G{row + 1}'] == pieces[f'A{row + 1}'] == pieces[f'D{row + 1}']:
        return [f'G{row + 1}', f'A{row + 1}', f'D{row + 1}']
    elif pieces[f'B{row + 1}'] == pieces[f'D{row + 1}'] == pieces[f'F{row + 1}']:
        return [f'B{row + 1}', f'D{row + 1}', f'F{row + 1}']

    # Вертикальные линии
    if pieces[f'{chr(col + ord("A"))}1'] == pieces[f'{chr(col + ord("A"))}2'] == pieces[f'{chr(col + ord("A"))}3']:
        return [f'{chr(col + ord("A"))}1', f'{chr(col + ord("A"))}2', f'{chr(col + ord("A"))}3']
    elif pieces[f'{chr(col + ord("A"))}4'] == pieces[f'{chr(col + ord("A"))}5'] == pieces[f'{chr(col + ord("A"))}6']:
        return [f'{chr(col + ord("A"))}4', f'{chr(col + ord("A"))}5', f'{chr(col + ord("A"))}6']
    elif pieces[f'{chr(col + ord("A"))}7'] == pieces[f'{chr(col + ord("A"))}4'] == pieces[f'{chr(col + ord("A"))}1']:
        return [f'{chr(col + ord("A"))}7', f'{chr(col + ord("A"))}4', f'{chr(col + ord("A"))}1']

    return []


def setup_pieces_human():
    global turn, player_turn

    player_turn = True
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


def main_game_loop(game_mode):
    if game_mode == 'two_players':
        setup_pieces_human()
    elif game_mode == 'vs_computer':
        pass

    global player_turn

    # Выводим словари перед игровым циклом
    print("Initial Black Pieces:", black_pieces)
    print("Initial White Pieces:", white_pieces)

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

    # Выводим словари после завершения игры
    print("Final Black Pieces:", black_pieces)
    print("Final White Pieces:", white_pieces)


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


# Запуск программы
if __name__ == "__main__":
    running = True
    game_mode = None  # Режим игры: 'two_players' или 'vs_computer'

    start_screen_buttons = draw_start_screen()

    while running and game_mode is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                game_mode = handle_start_screen_click(mouse_position, *start_screen_buttons)

        pygame.display.flip()

    if game_mode:
        main_game_loop(game_mode)

    pygame.quit()
    sys.exit()
