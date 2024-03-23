from httpx import Client, HTTPError

from server.schemas import Game, Position, Trick


class GameClient:
    def __init__(self, url: str):
        self._url = url
        self.client = Client()
        self.get_game()

    def get_game(self) -> Game:
        """Получить текущую игру."""
        try:
            response = self.client.get(self._url)
            return Game(**response.json())
        except HTTPError:
            print('server error')

    def set_trick(self, trick: Trick):
        """Установить фишку на поле."""
        try:
            self.client.post(url=self._url, json=trick.model_dump())
        except HTTPError:
            print('server error')

    def move_trick(self, from_position: Position, to_position: Position):
        """Переместить фишку"""
        try:
            response = self.client.patch(
                url=self._url,
                json=dict(
                    from_position=from_position,
                    to_position=to_position,
                ),
            )
            if response.status_code != 200:
                raise ValueError
        except HTTPError:
            print('server error')

    def remove_trick(self, position: Position):
        """Убрать фишку."""
        try:
            self.client.request(
                url=self._url,
                method='DELETE',
                json=position)
        except HTTPError:
            print('server error')

    def __del__(self):
        self.client.close()
