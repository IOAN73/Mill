import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Загрузка изображений
game_board_image = pygame.image.load('C:/Python_Projects/Mill/static/pole.jpg')
black_piece_image = pygame.image.load('C:/Python_Projects/Mill/static/black.png')
white_piece_image = pygame.image.load('C:/Python_Projects/Mill/static/white.png')

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

# Переменные для хода
selected_piece = None
turn = 'black'


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
    # Добавление счетчиков фишек для каждого игрока
    black_pieces_count = 0
    white_pieces_count = 0

    pixel_position = mouse_position
    for pos, (x, y) in points.items():
        if x - 15 < pixel_position[0] < x + 15 and y - 15 < pixel_position[1] < y + 15:
            if pieces[pos] is None and (turn == 'black' and black_pieces_count < 9 or turn == 'white' and white_pieces_count < 9):
                pieces[pos] = turn
                if turn == 'black':
                    black_pieces_count += 1
                else:
                    white_pieces_count += 1
                change_turn()



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


def is_valid_move(start, end):
    # Получаем индексы строки и столбца из начальной и конечной позиции
    start_row = int(start[1]) - 1
    start_col = ord(start[0]) - ord('A')
    end_row = int(end[1]) - 1
    end_col = ord(end[0]) - ord('A')

    # Проверка допустимости хода (возможно, вам потребуется адаптировать эту логику под вашу игру)
    if pieces[start] == turn and pieces[end] is None:
        # Перемещение на соседнюю клетку
        if abs(start_row - end_row) + abs(start_col - end_col) == 1:
            return True
        # Перемещение на клетку по диагонали
        elif abs(start_row - end_row) == 1 and abs(start_col - end_col) == 1:
            return True
        # Если фишка принадлежит текущему игроку, можно "прыгнуть" через соседнюю фишку
        elif pieces[start] == turn and pieces[end] is None and jump_over_adjacent(start, end):
            return True

    return False


def jump_over_adjacent(start, end):
    # Проверка, можно ли "прыгнуть" через соседнюю фишку
    start_row = int(start[1]) - 1
    start_col = ord(start[0]) - ord('A')
    end_row = int(end[1]) - 1
    end_col = ord(end[0]) - ord('A')

    # Проверка, что начальная и конечная клетки соседние
    if abs(start_row - end_row) + abs(start_col - end_col) != 2:
        return False

    # Определение координат соседней клетки
    adjacent_row = (start_row + end_row) // 2
    adjacent_col = (start_col + end_col) // 2
    adjacent_position = f'{chr(adjacent_col + ord("A"))}{adjacent_row + 1}'

    # Проверка, что соседняя клетка занята фишкой
    return pieces[adjacent_position] and pieces[adjacent_position] != turn


# Обработка кликов мыши
def handle_click(pixel_position):
    global selected_piece, turn
    x, y = pixel_position
    letters = 'ABCDEFG'
    position = letters[x // 100] + str(y // 100 + 1)
    piece = pieces[position]

    if piece == turn:
        if selected_piece and selected_piece != position:
            if pieces[position] is None:
                if is_valid_move(selected_piece, position):
                    pieces[selected_piece] = None
                    pieces[position] = turn
                    selected_piece = None
                    if not get_mill_positions(position):
                        change_turn()
                        # После каждого хода проверяем, возможно удаление фишек противника
                        remove_opponent_piece()
            else:
                selected_piece = position
        elif selected_piece == position:
            selected_piece = None
        else:
            selected_piece = position
    elif selected_piece and pieces[selected_piece] == turn and piece is None:
        if is_valid_move(selected_piece, position):
            pieces[selected_piece] = None
            pieces[position] = turn
            selected_piece = None
            if not get_mill_positions(position):
                change_turn()
                remove_opponent_piece()


# Проверка мельницы и удаление фишек противника
def remove_opponent_piece():
    for pos, piece in pieces.items():
        if piece != turn and get_mill_positions(pos):
            # Определяем координаты фишек мельницы
            mill_positions = [position_to_pixel(position) for pos in [pos[0] for pos in get_mill_positions(pos)]]

            # Отрисовываем линии мельницы
            draw_mill_line(mill_positions)

            # Удаляем одну фишку противника
            remove_piece(pos)
            return

def remove_piece(pos):
    # Удаляем фишку противника
    pieces[pos] = None
    draw_board()  # Обновляем доску после удаления фишки
    pygame.display.flip()  # Обновляем экран


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
                pixel_position = mouse_position
                x, y = pixel_position
                letters = 'ABCDEFG'
                position = letters[x // 100] + str(y // 100 + 1)
                if pieces[position] is None:
                    pieces[position] = turn
                    draw_board()
                    pygame.display.flip()
                    change_turn()
                    print_board()  # Выводим текущее состояние доски


def main_game_loop(game_mode):
    if game_mode == 'two_players':
        setup_pieces_human()
    elif game_mode == 'vs_computer':
        pass

    global player_turn

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
