from fastapi import FastAPI, Request, HTTPException

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
async def kill_trick(position: Position):
    pass


@app.exception_handler(GameError)
async def game_error_handler(request: Request, error: GameError):
    raise HTTPException(status_code=400, detail=error.__doc__)
