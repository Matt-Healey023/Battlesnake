import random
import typing
from move import *

def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "matt-healey023",
        "color": "#EA8C0E",
        "head": "gamer",
        "tail": "hook"
    }

def start(game_state: typing.Dict):
    print("GAME START")

def end(game_state: typing.Dict):
    print("GAME OVER\n")

def move(game_state: typing.Dict) -> typing.Dict:
    next = moveSnake(game_state)

    print(f"MOVE {game_state['turn']}: {next}")
    return {"move": next}

if __name__ == "__main__":
    from server import run_server
    run_server({"info": info, "start": start, "move": move, "end": end})