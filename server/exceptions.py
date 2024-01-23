class GameError(Exception):
    """Игровая ошибка."""


class TurnError(GameError):
    """Сейчас ход другого игрока."""


class TrickSetError(GameError):
    """Вы не можете поставить фишку сюда."""


class TrickNotFound(GameError):
    """В этой позиции нет фишки."""
