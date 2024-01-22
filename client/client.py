from time import sleep

from httpx import Client

URL = 'http://localhost:8000/game'


def main():
    with Client() as client:
        while True:
            # response = client.get(URL)
            # data = response.json()
            # sleep(2)
            response = client.post(
                url=URL,
                json={
                    'from_position': (1, 2),
                    'to_position': (2, 2),
                }
            )
            print(response.status_code)


def get_positions():
    # with Client() as client:
    #     response = client.get(URL)
    #     if response.status_code != 200:
    #         raise ValueError
    #     return response.json()
    return {
        "tricks_positions": [
            {
                "color": "white",
                "position": [1, 2]
            },
            {
                "color": "black",
                "position": [2, 2]
            },
        ],
        "tricks_count": 0
    }

def send_positions(...):
    pass

def delete_trick(): ...