from fastapi import FastAPI

from server.schemas import Game, Trick, Color, Movement, Kill

app = FastAPI()

GAME = Game(
    tricks_positions=[
        Trick(
            color=Color.black,
            position=(1, 2)
        ),
        Trick(
            color=Color.white,
            position=(2, 2)
        ),
        Trick(
            color=Color.black,
            position=(1, 4)
        ),
    ]
)


@app.get('/game')
async def get_game() -> Game:
    return GAME


@app.post('/game')
async def create_move(movement: Movement) -> None:
    print(movement)
    return None

@app.delete('/game')
async def delete_trick(deletion: Kill):
    pass
