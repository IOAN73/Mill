from httpx import Client
from server.schemas import Game, Trick

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

    def __del__(self):
        self.client.close()
