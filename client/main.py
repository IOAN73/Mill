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
    (3, 0): (30, 350),
    (6, 0): (30, 670),
    (1, 1): (135, 140),
    (3, 1): (135, 350),
    (5, 1): (135, 560),
    (2, 2): (240, 240),
    (3, 2): (240, 350),
    (4, 2): (240, 450),
    (0, 3): (350, 30),
    (1, 3): (350, 140),
    (2, 3): (350, 240),
    (4, 3): (350, 450),
    (5, 3): (350, 560),
    (6, 3): (350, 670),
    (2, 4): (450, 240),
    (3, 4): (450, 350),
    (4, 4): (450, 450),
    (1, 5): (560, 140),
    (3, 5): (560, 350),
    (5, 5): (560, 560),
    (0, 6): (670, 30),
    (3, 6): (670, 350),
    (6, 6): (670, 670),
}


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


def handle_select_color_screen(
        mouse_position,
        black_player_button,
        white_player_button,
) -> Color | None:
    if black_player_button.collidepoint(mouse_position):
        return Color.black
    elif white_player_button.collidepoint(mouse_position):
        return Color.white
    else:
        return None


def draw_points(tricks: list[Trick]):
    for trick in tricks:
        pygame.draw.circle(screen, BLACK, points[trick.position], 10)


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
            pygame.display.flip()


def main_game_loop(game_client: GameClient, player_color: Color):
    game = game_client.get_game()
    while True:
        if int(time()) % 5 == 0:
            game = game_client.get_game()
        screen.blit(game_board_image, (0, 0))
        draw_points(game.tricks)
        pygame.display.flip()


def main_game(game_client: GameClient):
    player_color = select_color()
    main_game_loop(game_client, player_color)


@click.command()
@click.option('--host', '-h', default='localhost')
@click.option('--port', '-p', default=8000)
def main(host, port):
    url = f'http://{host}:{port}/game'
    game_client = GameClient(url)
    main_game(game_client)


if __name__ == '__main__':
    main()
