from httpx import Client

from server.schemas import Game, Position, Trick


class GameClient:
    def __init__(self, url: str):
        self._url = url
        self.client = Client()
        self.get_game()

    def get_game(self) -> Game:
        """Получить текущую игру."""
        response = self.client.get(self._url)
        return Game(**response.json())

    def set_trick(self, trick: Trick):
        """Установить фишку на поле."""
        self.client.post(url=self._url, json=trick.model_dump())

    def move_trick(self, from_position: Position, to_position: Position):
        """Переместить фишку"""
        self.client.patch(
            url=self._url,
            json=dict(
                from_position=from_position,
                to_position=to_position,
            ),
        )

    def remove_trick(self, position: Position):
        """Убрать фишку."""
        self.client.request(
            url=self._url,
            method='DELETE',
            json=position,
        )

    def __del__(self):
        self.client.close()
