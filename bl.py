import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Загрузка изображений
game_board_image = pygame.image.load('static/pole.jpg')
black_piece_image = pygame.image.load('static/black.png')
white_piece_image = pygame.image.load('static/white.png')

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


# Функция для проверки победы
def check_win():
    lines = [
        ('A1', 'A4', 'A7'), ('B2', 'B4', 'B6'), ('C3', 'C4', 'C5'),
        ('D1', 'D2', 'D3'), ('D5', 'D6', 'D7'), ('E3', 'E4', 'E5'),
        ('F2', 'F4', 'F6'), ('G1', 'G4', 'G7'),
        ('A1', 'D1', 'G1'), ('B2', 'D2', 'F2'), ('C3', 'D3', 'E3'),
        ('A4', 'B4', 'C4'), ('E4', 'F4', 'G4'), ('C5', 'D5', 'E5'),
        ('B6', 'D6', 'F6'), ('A7', 'D7', 'G7')
    ]
    for line in lines:
        if pieces[line[0]] == pieces[line[1]] == pieces[line[2]] and pieces[line[0]] is not None:
            return True
    return False


# Рисование игрового поля и фишек
def draw_board():
    screen.blit(game_board_image, (0, 0))
    for position, piece in pieces.items():
        if piece == 'black':
            screen.blit(black_piece_image, (position_to_pixel(position)))
        elif piece == 'white':
            screen.blit(white_piece_image, (position_to_pixel(position)))


# Преобразование позиции в координаты на экране
def position_to_pixel(position):
    letters = 'ABCDEFG'
    x = (letters.index(position[0]) + 1) * 100 - 25
    y = int(position[1]) * 100 - 25
    return x, y


def computer_move():
    global turn
    if turn == 'white':  # Ход белых фишек (компьютер)
        available_positions = [pos for pos, piece in pieces.items() if piece is None]
        position = random.choice(available_positions)
        pieces[position] = 'white'
        turn = 'black'

def handle_player_click(mouse_position):
    pixel_position = mouse_position
    x, y = pixel_position
    letters = 'ABCDEFG'
    position = letters[x // 100] + str(y // 100 + 1)
    handle_click(pixel_position)


def check_mill(position):
    # Получаем индексы строки и столбца из позиции
    row = int(position[1]) - 1
    col = ord(position[0]) - ord('A')

    # Горизонтальные линии
    if pieces[f'A{row + 1}'] == pieces[f'B{row + 1}'] == pieces[f'C{row + 1}']:
        return True
    elif pieces[f'D{row + 1}'] == pieces[f'E{row + 1}'] == pieces[f'F{row + 1}']:
        return True
    elif pieces[f'G{row + 1}'] == pieces[f'A{row + 1}'] == pieces[f'D{row + 1}']:
        return True
    elif pieces[f'B{row + 1}'] == pieces[f'D{row + 1}'] == pieces[f'F{row + 1}']:
        return True

    # Вертикальные линии
    if pieces[f'{chr(col + ord("A"))}1'] == pieces[f'{chr(col + ord("A"))}2'] == pieces[f'{chr(col + ord("A"))}3']:
        return True
    elif pieces[f'{chr(col + ord("A"))}4'] == pieces[f'{chr(col + ord("A"))}5'] == pieces[f'{chr(col + ord("A"))}6']:
        return True
    elif pieces[f'{chr(col + ord("A"))}7'] == pieces[f'{chr(col + ord("A"))}4'] == pieces[f'{chr(col + ord("A"))}1']:
        return True

    return False


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

    if piece == turn:  # Проверяем, что выбранная фишка принадлежит текущему игроку
        if selected_piece and selected_piece != position:
            if pieces[position] is None:  # Попытка сделать ход
                if is_valid_move(selected_piece, position):
                    pieces[selected_piece] = None
                    pieces[position] = turn
                    selected_piece = None
                    if not check_mill(position):  # Если был создан мельница, игрок должен убрать фишку соперника
                        change_turn()
            else:  # Выбор другой фишки
                selected_piece = position
        elif selected_piece == position:
            selected_piece = None
        else:  # Выбор фишки
            selected_piece = position
    elif selected_piece and pieces[selected_piece] == turn and piece is None:  # Попытка переместить фишку
        if is_valid_move(selected_piece, position):
            pieces[selected_piece] = None
            pieces[position] = turn
            selected_piece = None
            if not check_mill(position):  # Если был создана мельница, игрок должен убрать фишку соперника
                change_turn()



def handle_game_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if player_turn:  # Если ход игрока
                handle_player_click(mouse_position)  # Функция для обработки клика игрока
            else:  # Если ход компьютера
                # Возможно, здесь потребуется обработка кликов для отображения, что сейчас ходит компьютер
                pass




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

def main_game_loop(game_mode):
    if game_mode == 'vs_computer':
        setup_pieces_human()  # Интерактивная расстановка фишек человеком

    global player_turn
    running = True

    # Остальной код без изменений
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if player_turn:
                    handle_player_click(mouse_position)
                    if game_mode == 'vs_computer' and player_turn:
                        computer_move()
                        change_turn()

        screen.fill(WHITE)
        draw_board()
        pygame.display.flip()

        if check_win():
            print(f'Игрок {turn} выиграл!')
            pygame.time.delay(2000)
            running = False

        pygame.time.Clock().tick(30)


def change_turn():
    global turn
    turn = 'black' if turn == 'white' else 'white'


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
