from httpx import Client
from server.schemas import Game

URL = 'http://localhost:8000/game'


def get_game() -> Game:
    with Client() as client:
        response = client.get(URL)
        return Game(**response.json())


if __name__ == '__main__':
    game = get_game()
    print(game)
