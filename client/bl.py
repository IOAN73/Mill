import click
import pygame
import sys
from pathlib import Path
from client.server_client import GameClient
from server.schemas import Trick, Color

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


turn = 'black'


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
def handle_select_color_screen(mouse_position, black_player_button, white_player_button):
    global selected_color, player_color

    if black_player_button.collidepoint(mouse_position):
        selected_color = 'black'
        player_color = 'white'  # цвет другого игрока
        return 'black_player'
    elif white_player_button.collidepoint(mouse_position):
        selected_color = 'white'
        player_color = 'black'  # цвет другого игрока
        return 'white_player'
    else:
        return None


# Добавление координат точек на игровом поле
points = {'A1': (30, 30), 'A4': (30, 350), 'A7': (30, 670),
          'B2': (135, 140), 'B4': (135, 350), 'B6': (135, 560),
          'C3': (240, 240), 'C4': (240, 350), 'C5': (240, 450),
          'D1': (350, 30), 'D2': (350, 140), 'D3': (350, 240),
          'D5': (350, 450), 'D6': (350, 560), 'D7': (350, 670),
          'E3': (450, 240), 'E4': (450, 350), 'E5': (450, 450),
          'F2': (560, 140), 'F4': (560, 350), 'F6': (560, 560),
          'G1': (670, 30), 'G4': (670, 350), 'G7': (670, 670),
          }

# Расположение фишек
pieces = {'A1': None, 'A4': None, 'A7': None,
          'B2': None, 'B4': None, 'B6': None,
          'C3': None, 'C4': None, 'C5': None,
          'D1': None, 'D2': None, 'D3': None, 'D5': None, 'D6': None,
          'D7': None,
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
    x = (letters.index(position[0]) - 0.4) * 100 + 30
    y = (int(position[1]) - 1.4) * 100 + 20
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
    pygame.draw.line(screen, (255, 0, 0), position_to_pixel(positions[0]),
                     position_to_pixel(positions[1]), 2)


# Обработка кликов мыши для расстановки фишек
def handle_player_click_human(mouse_position):
    global black_pieces, white_pieces, turn

    # Добавление счетчиков фишек для каждого игрока
    black_pieces_count = sum(1 for piece in pieces.values() if piece == 'black')
    white_pieces_count = sum(1 for piece in pieces.values() if piece == 'white')

    if black_pieces_count < 9 and white_pieces_count < 9:
        # Если еще не все фишки поставлены, ставим фишку в зависимости от текущего хода
        pixel_position = mouse_position
        for pos, (x, y) in points.items():
            rect = pygame.Rect(x - 35, y - 35, 70, 70)
            if rect.collidepoint(pixel_position) and pieces[pos] is None:
                pieces[pos] = turn
                x, y = position_to_pixel(pos)
                if turn == 'black':
                    black_pieces[pos] = (x // 100 + 1, y // 100 + 1)
                    trick = Trick(color=Color.black, position=black_pieces[pos])
                else:
                    white_pieces[pos] = (x // 100 + 1, y // 100 + 1)
                    trick = Trick(color=Color.white, position=white_pieces[pos])

                change_turn()
                client.set_trick(trick)
                draw_board()
                pygame.display.flip()

                # Выводим словари после каждого хода
                print("Black Pieces:", black_pieces)
                print("White Pieces:", white_pieces)

                # Переход хода, если фишки данного цвета уже поставлены
                if (turn == 'black' and black_pieces_count == 9) or (turn == 'white' and white_pieces_count == 9):
                    print(f"All {turn} pieces placed. Switching to moving phase.")
                    turn = 'black' if turn == 'white' else 'white'
                    print(f"Turn: {turn}")

                # Выводим текущее состояние доски
                # print_board()
                return
    else:
        # Если все фишки уже поставлены, начинаем фазу движения
        pass


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

    if color == 'black':
        black_pieces[position] = position_to_pixel(position)
    elif color == 'white':
        white_pieces[position] = position_to_pixel(position)


def setup_pieces_human():
    global turn

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
    global turn, selected_color, player_color

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
                        setup_pieces_human()
            pygame.display.flip()

    elif game_mode == 'vs_computer':
        pass


def change_turn():
    global turn
    turn = 'white' if turn == 'black' else 'black'


def print_board():
    for row in range(1, 8):
        for col in 'ABCDEFG':
            position = f"{col}{row}"
            piece = pieces.get(position, None)
            print(piece or '.', end=' ')
        print()


@click.command()
@click.argument('color')
def main(color):
    running = True
    print(color)
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
        # Запускаем основной игровой цикл
        main_game_loop(game_mode)

        # Получаем информацию о цвете и позиции фишек с сервера и обновляем доску
        while True:
            color, position = client.get_game()
            if color and position:
                update_pieces_from_server(color, position)
                draw_board()
                pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
