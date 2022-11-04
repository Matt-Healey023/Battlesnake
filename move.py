# is_move_safe = {"up": True, "down": True, "left": True, "right": True}

# # Body check
# head = game_state['you']['head']
# body = game_state['you']['body'][1:]

# for i in range(len(body)):
#     x = head['x'] - body[i]['x']
#     y = head['y'] - body[i]['y']
#     if y == 0:
#         if x == 1:
#             is_move_safe['left'] = False
#         if x == -1:
#             is_move_safe['right'] = False

#     if x == 0:
#         if y == 1:
#             is_move_safe['down'] = False
#         if y == -1:
#             is_move_safe['up'] = False

#     # print(f"({head['x']}, {head['y']}) - ({body[i]['x']}, {body[i]['y']}) = ({x}, {y})")

# # Out-of-bounds
# width = game_state['board']['width']
# height = game_state['board']['height']

# if head['x'] == 0:
#     is_move_safe['left'] = False
# elif head['x'] == width - 1:
#     is_move_safe['right'] = False

# if head['y'] == height - 1:
#     is_move_safe['up'] = False
# elif head['y'] == 0:
#     is_move_safe['down'] = False

# # Basic enemy avoidance
# for snake in game_state['board']['snakes']:
#     for i in range(len(snake['body'])):
#         x = head['x'] - snake['body'][i]['x']
#         y = head['y'] - snake['body'][i]['y']
#         if y == 0:
#             if x == 1:
#                 is_move_safe['left'] = False
#             if x == -1:
#                 is_move_safe['right'] = False

#         if x == 0:
#             if y == 1:
#                 is_move_safe['down'] = False
#             if y == -1:
#                 is_move_safe['up'] = False

# # Are there any safe moves left?
# safe_moves = []
# for move, isSafe in is_move_safe.items():
#     if isSafe:
#         safe_moves.append(move)

# # if len(safe_moves) == 0:
# #     print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
# #     return {"move": "down"}

# # Get move to closest food
# next_move = None
# food = game_state['board']['food']
# if len(food) > 0:
#     index = -1
#     close = 0
#     for i in range(len(food)):
#         dis = math.sqrt((head['x'] - food[i]['x']) ** 2 + (head['y'] - food[i]['y']) ** 2)
#         if index == -1 or dis < close:
#             index = i
#             close = dis
    
#     pellet = food[index]
#     if abs(pellet['x'] - head['x']) > abs(pellet['y'] - head['y']):
#         if head['x'] - pellet['x'] < 0 and is_move_safe['right']:
#             next_move = 'right'
#         elif is_move_safe['left']:
#             next_move = 'left'

#         if next_move == None:
#             if head['y'] - pellet['y'] < 0 and is_move_safe['up']:
#                 next_move = 'up'
#             elif is_move_safe['down']:
#                 next_move = 'down'
#     else:
#         if head['y'] - pellet['y'] < 0 and is_move_safe['up']:
#             next_move = 'up'
#         elif is_move_safe['down']:
#             next_move = 'down'

#         if next_move == None:
#             if head['x'] - pellet['x'] < 0 and is_move_safe['right']:
#                 next_move = 'right'
#             elif is_move_safe['left']:
#                 next_move = 'left'

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

    # Check for neaby heads
    for eHead in eHeads:
        x = eHead[0]['x'] - head['x']
        y = eHead[0]['y'] - head['y']
        # '>=' to play safe, '>' to be agressive
        if eHead[1] >= size:
            if x == -1:
                if y == -1:
                    safe['left'] = False
                    safe['down'] = False
                if y == 1:
                    safe['left'] = False
                    safe['up'] = False
            if x == 1:
                if y == -1:
                    safe['right'] = False
                    safe['down'] = False
                if y == 1:
                    safe['right'] = False
                    safe['up'] = False

    # Check for boundries
    w, h = game_state['board']['width'], game_state['board']['width']
    if head['x'] == w - 1: safe['right'] = False
    elif head['x'] == 0: safe['left'] = False
    if head['y'] == h - 1: safe['up'] = False
    elif head['y'] == 0: safe['down'] = False

    return safe

def moveTowardsFood(game_state, safe):
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
    isSafe = checkForHazards(game_state)
    next = moveTowardsFood(game_state, isSafe)

    safe = []
    for move, isSafe in isSafe.items():
        if isSafe:
            safe.append(move)

    if next == None:
        if len(safe) > 0: next = random.choice(safe)
        else: next ="down"

    return next