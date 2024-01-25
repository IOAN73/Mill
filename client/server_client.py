from httpx import Client
from server.schemas import Game, Trick, Position

URL = 'http://localhost:8000/game'


class GameClient:
    def __init__(self):
        self.client = Client()
        self.get_game()

    def get_game(self) -> Game:
        """Получить текущую игру."""
        response = self.client.get(URL)
        return Game(**response.json())

    def set_trick(self, trick: Trick):
        """Установить фишку на поле."""
        self.client.post(url=URL, json=trick.model_dump())

    def move_trick(self, from_position: Position, to_position: Position):
        """Переместить фишку"""
        self.client.patch(
            url=URL,
            json=dict(
                from_position=from_position,
                to_position=to_position,
            ),
        )

    def __del__(self):
        self.client.close()
