import random
import typing

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
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # Body check
    head = game_state["you"]["body"][0]
    body = game_state['you']['body'][1:]

    for i in range(len(body)):
        x = head['x'] - body[i]['x']
        y = head['y'] - body[i]['y']
        if y == 0:
            if x == 1:
                is_move_safe['left'] = False
            if x == -1:
                is_move_safe['right'] = False

        if x == 0:
            if y == 1:
                is_move_safe['down'] = False
            if y == -1:
                is_move_safe['up'] = False

        # print(f"({head['x']}, {head['y']}) - ({body[i]['x']}, {body[i]['y']}) = ({x}, {y})")

    # Out-of-bounds
    width = game_state['board']['width']
    height = game_state['board']['height']

    if head['x'] == 0:
        is_move_safe['left'] = False
    elif head['x'] == width - 1:
        is_move_safe['right'] = False

    if head['y'] == height - 1:
        is_move_safe['up'] = False
    elif head['y'] == 0:
        is_move_safe['down'] = False

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

if __name__ == "__main__":
    from server import run_server
    run_server({"info": info, "start": start, "move": move, "end": end})