import random

def checkForHazards(game_state):
    # Initialize all vars
    safe = {"up": True, "down": True, "left": True, "right": True}
    head = game_state['you']['head']
    size = game_state['you']['length']
    eHeads = []
    hazards = []
    
    # Create lists with hazards and heads
    hazards.extend(game_state['board']['hazards'])
    hazards.extend(game_state['you']['body'][1:])
    for snake in game_state['board']['snakes']:
        hazards.extend(snake['body'])
        eHeads.append((snake['head'], snake['length']))

    # Check for nearby hazards
    for hazard in hazards:
        x = head['x'] - hazard['x']
        y = head['y'] - hazard['y']
        if x == 0:
            if y == 1: safe['down'] = False
            if y == -1: safe['up'] = False
        if y == 0:
            if x == 1: safe['left'] = False
            if x == -1: safe['right'] = False

    # Check for boundries
    w, h = game_state['board']['width'], game_state['board']['width']
    if head['x'] == w - 1: safe['right'] = False
    elif head['x'] == 0: safe['left'] = False
    if head['y'] == h - 1: safe['up'] = False
    elif head['y'] == 0: safe['down'] = False

    # Check for nearby heads
    yolo = False
    for eHead in eHeads:
        x = eHead[0]['x'] - head['x']
        y = eHead[0]['y'] - head['y']
        # '>=' to play safe, '>' to be agressive and probably die
        # Only be scared if you have a way out
        if eHead[1] >= size:
            # Diagonal
            if x == -1:
                if y == -1 and (safe['right'] or safe['up']):
                    safe['left'] = False
                    safe['down'] = False
                if y == 1 and (safe['right'] or safe['down']):
                    safe['left'] = False
                    safe['up'] = False
            if x == 1:
                if y == -1 and (safe['left'] or safe['up']):
                    safe['right'] = False
                    safe['down'] = False
                if y == 1 and (safe['left'] or safe['down']):
                    safe['right'] = False
                    safe['up'] = False
            # Horizontal
            if y == 0:
                if x == -2 and (safe['down'] or safe['up'] or safe['right']): safe['left'] = False
                elif x == 2 and (safe['down'] or safe['up'] or safe['left']): safe['right'] = False
                else: yolo = True
            # Vertical
            if x == 0:
                if y == -2 and (safe['right'] or safe['up'] or safe['left']): safe['down'] = False
                elif y == 2 and (safe['right'] or safe['down'] or safe['left']): safe['up'] = False
                else: yolo = True

    return safe, yolo

def moveTowardsFood(game_state, safe, yolo):
    # Initialize all vars
    head = game_state['you']['head']
    food = game_state['board']['food']
    next = None
    
    if len(food) > 0:
        index = -1
        close = 0
        # Find closest food
        for i in range(len(food)):
            dis = abs(head['x'] - food[i]['x']) + abs(head['y'] - food[i]['y'])
            if index == -1 or dis < close:
                index = i
                close = dis

        pellet = food[index]
        # Bad situation abort path to food
        if close == 1 and yolo:
            if head['x'] - pellet['x'] < 0: safe['right'] = False
            elif head['x'] - pellet['x'] > 0: safe['left'] = False
            elif head['y'] - pellet['y'] < 0: safe['up'] = False
            elif head['y'] - pellet['y'] > 0: safe['down'] = False

        # Find safe move towards food
        if head['x'] - pellet['x'] < 0 and safe['right']: next = 'right'
        elif head['x'] - pellet['x'] > 0 and safe['left']: next = 'left'
        if next == None:
            if head['y'] - pellet['y'] < 0 and safe['up']: next = 'up'
            elif head['y'] - pellet['y'] > 0 and safe['down']: next = 'down'

    return next

def moveSnake(game_state):
    next = None
    isSafe, yolo = checkForHazards(game_state)
    next = moveTowardsFood(game_state, isSafe, yolo)

    safe = []
    for move, isSafe in isSafe.items():
        if isSafe:
            safe.append(move)

    if next == None:
        if len(safe) > 0: next = random.choice(safe)
        else: next ="down"

    return next