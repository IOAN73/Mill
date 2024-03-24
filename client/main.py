import sys
from time import time
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

points = {
    (0, 0): (30, 30),
    (3, 0): (350, 30),
    (6, 0): (670, 30),
    (1, 1): (135, 140),
    (3, 1): (350, 135),
    (5, 1): (560, 135),
    (2, 2): (240, 240),
    (3, 2): (350, 240),
    (4, 2): (450, 240),
    (0, 3): (30, 350),
    (1, 3): (140, 350),
    (2, 3): (240, 350),
    (4, 3): (450, 350),
    (5, 3): (560, 350),
    (6, 3): (670, 350),
    (2, 4): (240, 450),
    (3, 4): (350, 450),
    (4, 4): (450, 450),
    (1, 5): (140, 560),
    (3, 5): (350, 560),
    (5, 5): (560, 560),
    (0, 6): (30, 670),
    (3, 6): (350, 670),
    (6, 6): (670, 670),
}

pieces = {(0, 0): None, (3, 0): None, (6, 0): None,
          (1, 1): None, (3, 1): None, (5, 1): None,
          (2, 2): None, (3, 2): None, (4, 2): None,
          (0, 3): None, (1, 3): None, (2, 3): None,
          (4, 3): None, (5, 3): None, (6, 3): None,
          (2, 4): None, (3, 4): None, (4, 4): None,
          (1, 5): None, (3, 5): None, (5, 5): None,
          (0, 6): None, (3, 6): None, (6, 6): None, }


def draw_select_color_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)

    name = font.render("МЕЛЬНИЦА", True, BLACK)
    text_rect = name.get_rect(center=(WIDTH / 2, HEIGHT / 10))
    screen.blit(name, text_rect)

    text = font.render("Выберите цвет фишки", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 4))
    screen.blit(text, text_rect)

    button_font = pygame.font.Font(None, 28)

    black_player_button = pygame.Rect(WIDTH / 4, HEIGHT / 3, WIDTH / 2, 50)
    pygame.draw.rect(screen, BLACK, black_player_button)
    text = button_font.render("Черные фишки", True, WHITE)
    text_rect = text.get_rect(center=black_player_button.center)
    screen.blit(text, text_rect)

    white_player_button = pygame.Rect(WIDTH / 4, HEIGHT * 3 / 6, WIDTH / 2, 50)
    pygame.draw.rect(screen, BLACK, white_player_button)
    text = button_font.render("Белые фишки", True, WHITE)
    text_rect = text.get_rect(center=white_player_button.center)
    screen.blit(text, text_rect)

    # help_button = pygame.Rect(WIDTH / 4, HEIGHT * 5 / 6, WIDTH / 2, 50)
    # pygame.draw.rect(screen, BLACK, help_button)
    # text = button_font.render("Правила игры", True, WHITE)
    # text_rect = text.get_rect(center=help_button.center)
    # screen.blit(text, text_rect)

    return black_player_button, white_player_button


def position_to_pixel(position):
    col, row = int(position[0]), int(position[1])
    x = (col - 0.4) * 100 + 30
    y = (row - 1.4) * 100 + 20
    return x, y


def handle_select_color_screen(
        mouse_position,
        black_player_button,
        white_player_button,
        help_button,
) -> Color | None:
    if black_player_button.collidepoint(mouse_position):
        return Color.black
    elif white_player_button.collidepoint(mouse_position):
        return Color.white
    else:
        return None


color_conv = {Color.white: WHITE,
              Color.black: BLACK,
              }


def draw_tricks(tricks: list[Trick]):
    for trick in tricks:
        pygame.draw.circle(screen, color_conv[trick.color], points[trick.position], 40)


def select_color() -> Color:
    while True:
        select_color_screen_buttons = draw_select_color_screen()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    color_choice = handle_select_color_screen(
                        mouse_position,
                        *select_color_screen_buttons
                    )
                    if color_choice:
                        return color_choice
                    # help()
            pygame.display.flip()


# def help():
#     background_colour = (255, 255, 255)
#     screen = pygame.display.set_mode((300, 300))
#     pygame.display.set_caption('Правила игры')
#     screen.fill(background_colour)
#     pygame.display.flip()
#     running = True
#     while running:
#
#         for event in pygame.event.get():
#
#             if event.type == pygame.QUIT:
#                 running = False


def get_clicked_position(mouse_position):
    for pos, (x, y) in points.items():
        rect = pygame.Rect(x - 35, y - 35, 70, 70)
        if rect.collidepoint(mouse_position) and pieces[pos] is None:
            return pos
    return None


def game(game_client: GameClient):
    player_color = select_color()
    move_pos = []
    while True:
        game = game_client.get_game()
        screen.blit(game_board_image, (0, 0))
        draw_tricks(game.tricks)
        pygame.display.flip()

        if game.need_remove:
            pygame.display.set_caption(f'У игрока {game.turn} образована мельница')
        else:
            pygame.display.set_caption(f'Ход игрока {player_color}, кол-во фишек: {game.free_tricks[player_color]}')

        if game.winner == player_color:
            font = pygame.font.SysFont('Comic Sans MS', 20)
            text_game_over = font.render(f"Игра окончена! Выйграл игрок: {player_color}", True, (255, 0, 0))
            screen.blit(text_game_over, (150, 150))

            print(f"Игра окончена! Выйграл игрок: {player_color}")

        # try:
        #     game_client.move_trick(...)
        # except ValueError:
        #     print(":0")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                clicked_position = get_clicked_position(mouse_position)
                if clicked_position:
                    trick = Trick(color=player_color, position=clicked_position)
                    game_client.set_trick(trick)
                if game.need_remove and game.turn == player_color:
                    game_client.remove_trick(clicked_position)
                if game.free_tricks == 0 and game.turn == player_color:
                    ...


def main_game(game_client: GameClient):
    game(game_client)


@click.command()
@click.option('--host', '-h', default='localhost')
@click.option('--port', '-p', default=8000)
def main(host, port):
    url = f'http://{host}:{port}/game'
    game_client = GameClient(url)
    main_game(game_client)


if __name__ == '__main__':
    main()
