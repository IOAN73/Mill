from httpx import Client
from server.schemas import Game, Trick

URL = 'http://localhost:8000/game'


def get_game() -> Game:
    """Получить текущую игру."""
    with Client() as client:
        response = client.get(URL)
        return Game(**response.json())


def set_trick(trick: Trick):
    """Установить фишку на поле."""
    with Client() as client:
        client.post(url=URL, json=trick.model_dump())


if __name__ == '__main__':
    game = get_game()
    print(game)
