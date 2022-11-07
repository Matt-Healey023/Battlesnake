import random

# TODO: Test if enemy head will cut it off this turn
# Flag direction that was cut off by potential and cut that direction off if you have other directions to go
# Only cut that direction off if you can afford to

DIR = {'up': (0, 1), 'down': (0, -1), 'left': (-1, 0), 'right': (1, 0)}
KEYS = ['up', 'down', 'left', 'right']

def convertGameState(game_state):
    gameState = {
        'width': game_state['board']['width'],
        'height': game_state['board']['height'],
        'food': set(),
        'hazards': { 'real': set(), 'potential': set() },
        'snakes': [],
        'you': {},
        'safe': { 'up': True, 'down': True, 'left': True, 'right': True },
        'zones': { 'up': set(), 'down': set(), 'left': set(), 'right': set() }
    }

    for snake in game_state['board']['snakes']:
        body = {(b['x'], b['y']) for b in snake['body'][1:-1]}
        head = (snake['head']['x'], snake['head']['y'])
        tail = (snake['body'][-1]['x'], snake['body'][-1]['y'])
        length = snake['length']
        new = { 'body': body, 'head': head, 'tail': tail, 'length': length }

        if snake['id'] == game_state['you']['id']: gameState['you'] = new
        else: gameState['snakes'].append(new)

    gameState['food'] = {(f['x'], f['y']) for f in game_state['board']['food']}
    gameState['hazards']['real'] = {(h['x'], h['y']) for h in game_state['board']['hazards']}

    return gameState

def checkZones(gameState):
    def floodFill(current, i=-1):
        if i != -1:
            if current not in gameState['hazards']['real'] and current not in gameState['zones'][KEYS[i]] and 0 <= current[0] < gameState['width'] and 0 <= current[1] < gameState['height']:
                gameState['zones'][KEYS[i]].add(current)
            else:
                return

        section = i
        for j in range(4):
            if i == -1: section = j
            floodFill((current[0] + DIR[KEYS[j]][0], current[1] + DIR[KEYS[j]][1]), section)

    floodFill(gameState['you']['head'])

def checkForHazards(gameState):
    def potentialToKey(origin, coord):
        unit = (coord[0] - origin[0], coord[1] - origin[1])
        for key in KEYS:
            if DIR[key] == unit: return key

    def keyToPotential(coord, key):
        return (coord[0] + DIR[key][0], coord[1] + DIR[key][1])

    # Create list with hazards
    gameState['hazards']['real'].update(gameState['you']['body'])
    gameState['hazards']['real'].add(gameState['you']['head'])
    for snake in gameState['snakes']:
            gameState['hazards']['real'].update(snake['body'])
            gameState['hazards']['real'].add(snake['head'])
            for key in KEYS:
                coord = (keyToPotential(snake['head'], key), snake['length'])
                gameState['hazards']['potential'].add(coord)
                if coord[0] in gameState['food']: gameState['hazards']['real'].add(snake['tail'])

    # Check for nearby hazards
    potential = set()
    for key in KEYS:
        coord = keyToPotential(gameState['you']['head'], key)
        if coord in gameState['food']: gameState['hazards']['real'].add(gameState['you']['tail'])
        if coord in gameState['hazards']['real']: gameState['safe'][key] = False
        else: potential.add(coord)

    # Check for boundries
    toRemove = set()
    for coord in potential:
        if coord[0] < 0:
            gameState['safe']['left'] = False
            toRemove.add(coord)
        elif coord[0] >= gameState['width']:
            gameState['safe']['right'] = False
            toRemove.add(coord)
        if coord[1] < 0:
            gameState['safe']['down'] = False
            toRemove.add(coord)
        elif coord[1] >= gameState['height']:
            gameState['safe']['up'] = False
            toRemove.add(coord)
    potential -= toRemove

    checkZones(gameState)

    # Check if it can fit
    canFit = {'up': True, 'down': True, 'left': True, 'right': True}
    max = 0
    key = ''
    fit = False
    for k in KEYS:
        if len(gameState['zones'][k]) > max:
            key = k
            max = len(gameState['zones'][k])
        if len(gameState['zones'][k]) < gameState['you']['length']: canFit[k] = False
        else: fit = True

    if not fit:
        for k in KEYS:
            gameState['safe'][k] = False
        gameState['safe'][key] = True
        potential = {keyToPotential(gameState['you']['head'], k)}
    else:
        for k in KEYS:
            if not canFit[k] and gameState['safe'][k]:
                gameState['safe'][k] = False
                potential.remove(keyToPotential(gameState['you']['head'], k))

    # Check for nearby heads
    for enemy in gameState['hazards']['potential']:
        if enemy[0] in potential and enemy[1] >= gameState['you']['length'] and len(potential) > 1:
            potential.remove(enemy[0])
            gameState['safe'][potentialToKey(gameState['you']['head'], enemy[0])] = False

def moveTowardsFood(gameState):
    next = None
    if len(gameState['food']) > 0:
        close = -1
        pellet = None
        # Find closest food
        for food in gameState['food']:
            dis = abs(gameState['you']['head'][0] - food[0]) + abs(gameState['you']['head'][1] - food[1])
            if close == -1 or dis < close:
                pellet = food
                close = dis

        # Find safe move towards food
        if gameState['you']['head'][0] - pellet[0] < 0 and gameState['safe']['right']: next = 'right'
        elif gameState['you']['head'][0] - pellet[0] > 0 and gameState['safe']['left']: next = 'left'
        if next == None:
            if gameState['you']['head'][1] - pellet[1] < 0 and gameState['safe']['up']: next = 'up'
            elif gameState['you']['head'][1] - pellet[1] > 0 and gameState['safe']['down']: next = 'down'

    return next

def moveSnake(game_state):
    next = None
    gameState = convertGameState(game_state)
    checkForHazards(gameState)
    next = moveTowardsFood(gameState)

    safe = []
    for move, s in gameState['safe'].items():
        if s:
            safe.append(move)

    if next == None:
        if len(safe) > 0: next = random.choice(safe)
        else: next ="down"

    return next