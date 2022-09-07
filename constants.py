import pygame
import other_functions

FPS = 30
MAP_DIM_MULT = 28
HUD_PERCENT = 0.2
MOVE_SPEED = 15

CHAR_LEN = 112
CHAR_SPEED = 28
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
    ("Switch1", [(-2128, 1568), (1344, -672), (896, 3136), (-896, 3136), (-1232, 3136), (-1568, 3136)], [True, False, False], 7),
    ("Switch1", [(-1568, -1120), (-1568, -280), (-1344, 560), (1680, 1456), (2212, -1008), (2912, 896)], [True, False, False], 7, 90),
    ("Switch1", [(-3024, -784), (-3248, 224), (-2800, 224), (1344, -1344)], [True, False, False], 7, 180),
    ("Switch1", [(-1680, 1680), (-3136, 1036), (-3136, 1904), (1232, -896), (1232, -1120), (2492, -784), (2464, 1232), (1456, 896), (2464, 2576), (2464, 1904)], [True, False, False], 7, 270),
    ("Door1", [(-924, 0), (-2268, 1008), (-1820, -672), (924, 0), (3164, 0), (1428, 560), (1708, 560), (3164, 0), (1400, 2128), (1064, 2576), (1400, 3024), (-1064, 1680)], [True, False, False], 28),
    ("Door1", [(-1680, -140), (-1456, 784), (-3024, 1680), (-3024, 924), (-3024, 196), (-3024, 28), (-3024, -504), (-3248, -840), (-2800, -840), (-1680, -1400), (-1680, -840), (2800, -252), (2800, 252), (1568, 420), (1568, 700), (2800, 700), (2800, 1092), (3360, 1372), (1232, 1848), (896, 2408), (896, 2744), (0, 1904), (0, 2968), (-896, 1848), (1568, 1316), (-896, 1316), (-1568, 1848)], [True, False, False], 28, 90),
    ("CharSword1", [(0,0)], [True, True, False], 5),
    ("Star", [(0,1000)], [True, True, True], 5),
    ("Star", [(-2016, -1120),(3024, 2576),(0, 3108)], [True, True, True], 5),
    ("Star", [(-0, -0)], [True, True, True], 5),
    ("Heart", [(644, 378)], [False, True, False], 5),
    ("Crosshair", [(0,0)], [False, True, False], 5)

]

SOUNDTRACK_INFO = [
    ""
]

DIRECTION_HITBOX_COORDS = [
    [(-CHAR_HITBOX_LEN,-CHAR_LEN_HALF,CHAR_HITBOX_LEN*2,CHAR_LEN_HALF), False, -1],
    [(-CHAR_HITBOX_LEN,0,CHAR_HITBOX_LEN*2,CHAR_LEN_HALF), False, -1],
    [(-CHAR_LEN_HALF,-CHAR_HITBOX_LEN,CHAR_LEN_HALF,CHAR_HITBOX_LEN*2), False, -1], 
    [(0,-CHAR_HITBOX_LEN,CHAR_LEN_HALF,CHAR_HITBOX_LEN*2), False, -1]
]

DETECTION_HITBOX_COORDS =[
    [(-CHAR_LEN, -CHAR_LEN, CHAR_LEN*2, CHAR_LEN*2), False, -1],
    [(-CHAR_LEN_HALF, -CHAR_LEN_HALF, CHAR_LEN, CHAR_LEN), False, -1]
]

WALL_HITBOX_COORDS = [
    # 1st section coords
    [(-1568, -896, 672, 784)],
    [(-1568, -1680, 1456, 784)],
    [(-3136, -1456, 1344, 112)], 
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
    # 3rd section coords
    [(-1456, 1792, 112, 1344), True, 10], 
    [(-1120, 1792, 112, 1344), True, 10], 
    [(-784, 1792, 112, 1344), True, 10], 
    [(-672, 1792, 560, 224), True, 10], 
    [(112, 1792, 560, 224), True, 10], 
    [(672, 1792, 112, 1344), True, 10], 
    [(112, 2912, 336, 224), True, 10], 
    [(-448, 2912, 336, 224), True, 10], 
    [(1008, 1792, 112, 672), True, 10], 
    [(1008, 2688, 112, 448), True, 10], 
    [(1344, 2240, 112, 672), True, 10], 
    [(1344, 1792, 112, 224), True, 10],
    # Outer wall coords
    [(-1120, -3584, 2240, 448)], 
    [(-3584, -2240, 224, 5824)], 
    [(-3360, -2240, 3248, 560)], 
    [(112, -2240, 3472, 672)], 
    [(3136, 2464, 448, 1120)], 
    [(-3360, 3136, 3248, 448)], 
    [(112, 3136, 2576, 448)], 
    [(112, -1344, 784, 448)],
]

ALL_HITBOX_COORDS = DIRECTION_HITBOX_COORDS + DETECTION_HITBOX_COORDS + WALL_HITBOX_COORDS

DOORS_PER_SWITCH = [
    [0,1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
]

STARTING_DOOR_STATES = [
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

KEY_COMBOS = {
    (pygame.K_UP, pygame.K_UP) : (0, 0, CHAR_SPEED),
    (pygame.K_DOWN, pygame.K_DOWN) : (180, 0, -CHAR_SPEED),
    (pygame.K_LEFT, pygame.K_LEFT) : (90, CHAR_SPEED, 0),
    (pygame.K_RIGHT, pygame.K_RIGHT) : (270, -CHAR_SPEED, 0),
    #(pygame.K_UP, pygame.K_LEFT) : (45, 0, 0),
    #(pygame.K_UP, pygame.K_RIGHT) : (315, 0, 0),
    #(pygame.K_DOWN, pygame.K_LEFT) : (135, 0, 0),
    #(pygame.K_DOWN, pygame.K_RIGHT) : (225, 0, 0)
}