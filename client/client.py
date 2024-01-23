from httpx import Client
from server.schemas import Game, Trick

URL = 'http://localhost:8000/game'


def get_game() -> Game:
    with Client() as client:
        response = client.get(URL)
        return Game(**response.json())


def set_game(trick: Trick):
    with Client() as client:
        client.post(url=URL, json=trick.model_dump_json())


if __name__ == '__main__':
    game = get_game()
    print(game)
