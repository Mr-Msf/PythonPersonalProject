import pygame
import other_functions

FPS = 30
MAP_DIM_MULT = 28
HUD_PERCENT = 0.2
MOVE_SPEED = 15

CHAR_LEN = 112
CHAR_SPEED = 28
CHAR_SPEED_PORT = 0#int(CHAR_SPEED/4)
CHAR_HITBOX_PERCENT = 0.3
CHAR_LEN_HALF = int(CHAR_LEN/2)
CHAR_HITBOX_LEN = int(CHAR_LEN*CHAR_HITBOX_PERCENT)

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

WINDOW = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

WIDTH, HEIGHT = WINDOW.get_size()
WIDTH_HALF, HEIGHT_HALF = int(WIDTH/2), int(HEIGHT/2)

HUD_HEIGHT = int(HEIGHT*HUD_PERCENT)

ASSET_INFO = [
    # (asset_name, (orig_coords), is_movable, is_permeable, is_collectable, init_size_mult, init_rotation)
    ("Map(v0.2)", [(0,0)], [True, True, False], 28), 
    ("Switch1", [(-2128, 1568), (1344, -672), (896, 3136), (-896, 3136), (-1232, 3136), (-1568, 3136), (-3024, -1456)], [True, True, False], 7),
    ("Switch1", [(-1568, -1120), (-1568, -280), (-1344, 560), (1680, 1456), (2912, 896)], [True, True, False], 7, 90),
    ("Switch1", [(-3024, -784), (-3248, 224), (-2800, 224), (1344, -1344)], [True, True, False], 7, 180),
    ("Switch1", [(-1680, 1680), (-3136, 1036), (-3136, 1904), (1232, -1008), (2464, 1232), (1456, 896), (2464, 2576), (2464, 1904)], [True, True, False], 7, 270),
    ("Switch2", [(896, 2128), (1232, 2128), (1568, 2128), (2352, -1456), (2128, -1008), (2576, -784)], [True, True, False], 7),
    ("Door1", [(-924, 0), (-2268, 1008), (-1820, -672), (924, 0), (3164, 0), (1428, 560), (1708, 560), (3164, 0), (1400, 1000000), (1064, 2576), (1400, 3024), (-1064, 1680), (-1848, 3024)], [True, False, False], 28),
    ("Door1", [(0, -924), (0, 924), (-1680, -140), (-1456, 784), (-3024, 1680), (-3024, 924), (-3024, 196), (-3024, 28), (-3024, -504), (-3248, -840), (-2800, -840), (-1680, -1400), (-1680, -840), (-2464, 28), (-2464, 196), (2800, -252), (2800, 252), (1568, 420), (1568, 700), (2800, 700), (2800, 1092), (3360, 1372), (1232, 1848), (896, 2408), (896, 2744), (0, 1876), (0, 3500), (-896, 1848), (1568, 1316), (-896, 1316), (-1568, 1848), (3360, 2016), (0, 1932), (1904, -1344), (2128, -1344), (2352, -1120), (2800, -1344), (2576, -896), (1904, -896), (2128, -1120), (2352, -896), (2576, -1120), (2800, -896), (-3248, -1400), (-2800, -1400), (1232, 2408)], [True, False, False], 28, 90),
    ("Door2", [(2016, -1232), (2240, -1456), (2464, -1232), (2016, -1008), (2240, -1008), (2464, -784), (2688, -784)], [True, False, False], 28),
    ("Door2", [(1904, -1120), (2128, -896), (2800, -1120), (2576, -1344), (2352, -1344)], [True, False, False], 28, 90),
    ("Collectable1", [(-2464, 1008)], [True, True, True], 5),
    ("Collectable2", [(-2464, 560)], [True, True, True], 5),
    ("Collectable3", [(3360, 0)], [True, True, True], 5),
    ("Collectable4", [(1904, -1232)], [True, True, True], 5),
    ("Collectable5", [(1232, 560)], [True, True, True], 5),
    ("Collectable6", [(3052, 2240)], [True, True, True], 5),
    ("Collectable7", [(-896, 1204)], [True, True, True], 5),
    ("Collectable8", [(-3248, 3024)], [True, True, True], 5),
    ("Collectable9", [(-2464, -1120)], [True, True, True], 5),
    ("Collectable10", [(896, 2940)], [True, True, True], 5),
    ("Sword", [(-2016, -1120)], [True, True, True], 5, 180),
    ("Chains", [(3024, 2576)], [True, True, True], 5),
    ("Crown", [(0, 2548)], [True, True, True], 5),
    ("Heart", [(10000,10000)], [False, True, False], 5),
    ("Crosshair", [(0,0)], [False, True, False], 5),
    ("Sword", [(0,0)], [False, True, False], 5)

]

SOUNDTRACK_INFO = [
    ""
]

DIRECTION_HITBOX_COORDS = [
    [(-CHAR_HITBOX_LEN,-CHAR_LEN_HALF,CHAR_HITBOX_LEN*2,CHAR_LEN_HALF), False, -1, True],
    [(-CHAR_HITBOX_LEN,0,CHAR_HITBOX_LEN*2,CHAR_LEN_HALF), False, -1, True],
    [(-CHAR_LEN_HALF,-CHAR_HITBOX_LEN,CHAR_LEN_HALF,CHAR_HITBOX_LEN*2), False, -1, True], 
    [(0,-CHAR_HITBOX_LEN,CHAR_LEN_HALF,CHAR_HITBOX_LEN*2), False, -1, True]
]

DETECTION_HITBOX_COORDS =[
    [(-CHAR_LEN, -CHAR_LEN, CHAR_LEN*2, CHAR_LEN*2), False, -1, True],
    [(-CHAR_LEN_HALF, -CHAR_LEN_HALF, CHAR_LEN, CHAR_LEN), False, -1, True]
]

WALL_HITBOX_COORDS = [
    # 1st section coords
    [(-1568, -896, 672, 784)],
    [(-1568, -1680, 1456, 784)],
    [(-3136, -1456, 224, 112)],
    [(-2688, -1456, 896, 112)], 
    [(-3136, -1344, 224, 560)], 
    [(-2576, -896, 784, 112)], 
    [(-2688, -896, 112, 2016)], 
    [(-2912, 896, 224, 224)], 
    [(-2912, 1120, 672, 224)], 
    [(-2576, 672, 1008, 224)], 
    [(-2016, 112, 672, 336)], 
    [(-2352, -560, 112, 1232)], 
    [(-2240, -560, 448, 448)], 
    [(-2912, 1568, 896, 224)], 
    [(-2688, 1792, 448, 224)], 
    [(-3360, 896, 224, 1344)], 
    [(-3360, 0, 224, 224)], 
    [(-2912, 0, 224, 224)], 
    [(-2912, -560, 224, 112)], 
    [(-3360, -560, 224, 112)], 
    [(-3136, 2016, 224, 224)], 
    [(-2688, 2240, 448, 224)], 
    [(-3136, 2464, 112, 448)], 
    [(-2800, 2688, 224, 224)], 
    [(-2352, 2688, 112, 448)], 
    [(-2016, 1120, 336, 1792)], 
    [(-1680, 1120, 672, 448)], 
    [(-1344, 112, 448, 1008)], 
    [(-896, 896, 784, 224)], 
    [(-784, 1120, 672, 448)],
    [(-2352, -1344, 224, 448), True, 15],
    # 2nd section coords
    [(896, -1344, 336, 672)],
    [(896, -672, 560, 560)], 
    [(896, 112, 560, 336)], 
    [(896, 448, 224, 224)], 
    [(896, 672, 560, 896)], 
    [(112, 896, 784, 672)], 
    [(1680, 224, 1008, 224)], 
    [(2912, 224, 224, 896)], 
    [(3136, 112, 336, 1008)], 
    [(2464, 672, 224, 448)], 
    [(2464, 1344, 224, 448)], 
    [(2912, 1344, 336, 784)], 
    [(2912, 2128, 112, 336)], 
    [(3024, 2352, 560, 112)], 
    [(2464, 2688, 672, 112)], 
    [(2464, 2016, 224, 448)], 
    [(2912, 3136, 224, 448)], 
    [(1680, 672, 784, 2464)], 
    [(3472, -112, 112, 2464)], 
    [(112, -1568, 1708, 224)], 
    [(1680, -700, 1008, 476)], 
    [(2912, -1568, 224, 1344)],
    [(3136, -1568, 448, 1456)],
    [(1680, -1344, 140, 224)],
    [(1680, -896, 140, 224)],
    # 3rd section coords
    [(-1456, 1792, 112, 1344), True, 15], 
    [(-1120, 1792, 112, 1344), True, 15], 
    [(-784, 1792, 112, 1344), True, 15], 
    [(-672, 1792, 560, 224), True, 15], 
    [(112, 1792, 560, 224), True, 15], 
    [(672, 1792, 112, 1344), True, 15], 
    [(112, 2912, 336, 224), True, 15], 
    [(-448, 2912, 336, 224), True, 15], 
    [(1008, 1792, 112, 672), True, 15], 
    [(1008, 2688, 112, 448), True, 15], 
    [(1344, 2240, 112, 672), True, 15], 
    [(1344, 1792, 112, 224), True, 15],
    [(-1680, 1344, 672, 224), True, 15],
    [(-784, 1344, 672, 224), True, 15],
    [(112, 1344, 1344, 224), True, 15],
    [(1344, 2016, 112, 224), True, 15],
    # Outer wall coords
    [(-1120, -3584, 2240, 448)], 
    [(-3584, -2240, 224, 5824)], 
    [(-3360, -2240, 3248, 560)], 
    [(112, -2240, 3472, 672)], 
    [(3136, 2464, 448, 1120)], 
    [(-3360, 3136, 3248, 448)], 
    [(112, 3136, 2576, 448)], 
    [(112, -1344, 784, 448)],
    # Extra wall coords
    [(3220, 1064, 308, 1372), True, 0, True],
]

ALL_HITBOX_COORDS = DIRECTION_HITBOX_COORDS + DETECTION_HITBOX_COORDS + WALL_HITBOX_COORDS

DOORS_PER_SWITCH = [
    [1],
    [46, 51],#
    [45],
    [43],
    [40],
    [12, 38],
    [24, 23, 56],
    [25, 3],
    [15, 2],
    [16],
    [41],
    [32, 33],
    [22, 57, 24],
    [19, 20, 27],
    [20, 26, 27],
    [50, 54],#
    [11, 42],
    [18],
    [17],
    [48, 53],#
    [34],
    [5, 6, 30, 31],
    [14],
    [44],
    [35, 58],
    [36, 37],
    [9, 10],
    [47, 52],#
    [50, 54],
    [49, 55],#
]

STARTING_DOOR_STATES = [
    True,
    False,
    True,
    False,
    False,
    False,
    False,
    False,
    False,
    False,###+
    True,###
    True,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    True,
    False,
    True,#
    False,#
    False,
    False,
    False,
    True,
    True,
    False,
    True,
    True,
    True,
    False,
    False,
    True,###
    True,###
    False,###+
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    True,##
    False,##
    True,##
    True,##
    True,##4
    False,##
    True,##
    False,##
    False,##4
    False,##
    True,#
    False,#
    False,###+
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
]

MESSAGES = [
    ""
]

COLLECTABLE_NEW_COORDS = {
    "Sword" : (-504, -504), 
    "Chains" : (504, -504), 
    "Crown" : (0, -308),
    "Collectable1" : (0,0),
    "Collectable2" : (0,0),
    "Collectable3" : (0,0),
    "Collectable4" : (0,0),
    "Collectable5" : (0,0),
    "Collectable6" : (0,0),
    "Collectable7" : (0,0),
    "Collectable8" : (0,0),
    "Collectable9" : (0,0),
    "Collectable10" : (0,0),
}

KEY_COMBOS = {
    (pygame.K_UP, pygame.K_UP) : (0, 0, CHAR_SPEED),
    (pygame.K_DOWN, pygame.K_DOWN) : (180, 0, -CHAR_SPEED),
    (pygame.K_LEFT, pygame.K_LEFT) : (90, CHAR_SPEED, 0),
    (pygame.K_RIGHT, pygame.K_RIGHT) : (270, -CHAR_SPEED, 0),
    (pygame.K_UP, pygame.K_LEFT) : (45, -CHAR_SPEED_PORT, -CHAR_SPEED_PORT),
    (pygame.K_UP, pygame.K_RIGHT) : (315, CHAR_SPEED_PORT, -CHAR_SPEED_PORT),
    (pygame.K_DOWN, pygame.K_LEFT) : (135, -CHAR_SPEED_PORT, CHAR_SPEED_PORT),
    (pygame.K_DOWN, pygame.K_RIGHT) : (225, CHAR_SPEED_PORT, CHAR_SPEED_PORT)
}