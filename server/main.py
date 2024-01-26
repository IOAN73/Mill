from fastapi import FastAPI, HTTPException, Request

from server.exceptions import GameError
from server.schemas import Game, Movement, Position, Trick

app = FastAPI()

game = Game()


@app.get('/game')
async def get_game() -> Game:
    return game


@app.post('/game')
async def set_trick(trick: Trick) -> None:
    game.set_trick(trick)
    return None


@app.patch('/game')
async def move_trick(movement: Movement) -> None:
    game.move_trick(
        from_position=movement.from_position,
        to_position=movement.to_position,
    )


@app.delete('/game')
async def remove_trick(position: Position):
    game.remove_trick(position)


@app.put('/game')
async def restart_game():
    global game
    game = Game()


@app.exception_handler(GameError)
async def game_error_handler(request: Request, error: GameError):
    raise HTTPException(status_code=400, detail=error.__doc__)


if __name__ == '__main__':
    from uvicorn import run

    run('server.main:app')
