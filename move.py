import random

def isPosSafe(game_state, zones, pos):
    pellet = (pos['x'], pos['y'])
    for key in zones.keys():
        if pellet in zones[key]:
            if len(zones[key]) > game_state['you']['length']: return True
            else: return False

def checkForHazards(game_state):
    safe = {"up": True, "down": True, "left": True, "right": True}
    head = game_state['you']['head']
    size = game_state['you']['length']
    eHeads = []
    hazards = []
    
    # Create lists with hazards and heads
    hazards.extend(game_state['board']['hazards'])
    hazards.extend(game_state['you']['body'][1:])
    for snake in game_state['board']['snakes']:
        if snake['head']['x'] != head['x'] and snake['head']['y'] != head['y']:
            hazards.extend(snake['body'])
            eHeads.append((snake['head'], snake['length']))

    # Check for nearby hazards
    for hazard in hazards:
        x = head['x'] - hazard['x']
        y = head['y'] - hazard['y']
        if x == 0:
            if y == 1: safe['down'] = False
            elif y == -1: safe['up'] = False
        elif y == 0:
            if x == 1: safe['left'] = False
            elif x == -1: safe['right'] = False

    # Check for boundries
    w, h = game_state['board']['width'], game_state['board']['width']
    if head['x'] == w - 1: safe['right'] = False
    elif head['x'] == 0: safe['left'] = False
    if head['y'] == h - 1: safe['up'] = False
    elif head['y'] == 0: safe['down'] = False

    # Check for nearby heads
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
                elif y == 1 and (safe['right'] or safe['down']):
                    safe['left'] = False
                    safe['up'] = False
            if x == 1:
                if y == -1 and (safe['left'] or safe['up']):
                    safe['right'] = False
                    safe['down'] = False
                elif y == 1 and (safe['left'] or safe['down']):
                    safe['right'] = False
                    safe['up'] = False
            # Horizontal
            if y == 0:
                if x == -2 and (safe['down'] or safe['up'] or safe['right']): safe['left'] = False
                elif x == 2 and (safe['down'] or safe['up'] or safe['left']): safe['right'] = False
            # Vertical
            if x == 0:
                if y == -2 and (safe['right'] or safe['up'] or safe['left']): safe['down'] = False
                elif y == 2 and (safe['right'] or safe['down'] or safe['left']): safe['up'] = False

    zones = smartMove(game_state, hazards)

    # Check if it can fit
    canFit = {'up': True, 'down': True, 'left': True, 'right': True}
    max = 0
    key = ''
    for k in zones.keys():
        if len(zones[k]) > max:
            key = k
            max = len(zones[k])
        if len(zones[k]) < size: canFit[k] = False

    fit = False
    for k in canFit.keys():
        if canFit[k]:
            fit = True
            break

    if not fit:
        for k in safe.keys():
            safe[k] = False
        safe[key] = True
    else:
        for k in safe.keys():
            if not canFit[k]: safe[k] = False

    return safe, hazards, zones

def smartMove(game_state, hazards):
    zones = {'up': set(), 'down': set(), 'left': set(), 'right': set()}
    keys = ['up', 'down', 'left', 'right']

    convertedHazards = [(game_state['you']['head']['x'], game_state['you']['head']['y'])]
    for hazard in hazards:
        convertedHazards.append((hazard['x'], hazard['y']))

    def floodFill(current, i=-1):
        if i != -1:
            if current not in convertedHazards and current not in zones[keys[i]] and 0 <= current[0] < game_state['board']['width'] and 0 <= current[1] < game_state['board']['height']:
                zones[keys[i]].add(current)
            else:
                return

        directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]

        section = i
        for j in range(4):
            if i == -1: section = j
            floodFill((current[0] + directions[j][0], current[1] + directions[j][1]), section)

    floodFill(convertedHazards[0])
    return zones


def moveTowardsFood(game_state, safe, zones):
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

        # Find safe move towards food
        pellet = food[index]
        if head['x'] - pellet['x'] < 0 and safe['right']: next = 'right'
        elif head['x'] - pellet['x'] > 0 and safe['left']: next = 'left'
        if next == None:
            if head['y'] - pellet['y'] < 0 and safe['up']: next = 'up'
            elif head['y'] - pellet['y'] > 0 and safe['down']: next = 'down'

    return next

def moveSnake(game_state):
    next = None
    # TODO: Only go for food if the zone the food is in is larger than the snake's size
    isSafe, hazards, zones = checkForHazards(game_state)
    next = moveTowardsFood(game_state, isSafe, zones)

    safe = []
    for move, s in isSafe.items():
        if s:
            safe.append(move)

    if next == None:
        if len(safe) > 0: next = random.choice(safe)
        else: next ="down"

    return next