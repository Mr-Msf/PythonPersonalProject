import pygame
import alterAsset

CHAR_LEN = 112
CHAR_SPEED = 14
CHAR_HITBOX_PERCENT = 0.3
CHAR_LEN_HALF = int(CHAR_LEN/2)
CHAR_HITBOX_LEN = int(CHAR_LEN*CHAR_HITBOX_PERCENT)

FILE_INFO_DICT = {
    # asset_name : ((orig_coords), size_mult, is_movable, is_permeable)
    "Map(v0.1)" : (True, [(0,0)], 28, True, True), 
    "CharSword1" : (True, [(0,1000)], 5, False, False),
    "Star" : (True, [(0,1000)], 5, True, True),
    "Door1" : (True, [(-924, 0), (924, 0)], 28, True, False),
    "Crosshair" : (True, [(0,0)], 5, False, True)

}

DIRECTION_HITBOX_COORDS = [
    (-CHAR_HITBOX_LEN,-CHAR_LEN_HALF,CHAR_HITBOX_LEN*2,CHAR_LEN_HALF),
    (-CHAR_HITBOX_LEN,0,CHAR_HITBOX_LEN*2,CHAR_LEN_HALF),
    (-CHAR_LEN_HALF,-CHAR_HITBOX_LEN,CHAR_LEN_HALF,CHAR_HITBOX_LEN*2), 
    (0,-CHAR_HITBOX_LEN,CHAR_LEN_HALF,CHAR_HITBOX_LEN*2)
]

DETECTION_HITBOX_COORDS = (-CHAR_LEN, -CHAR_LEN, CHAR_LEN*2, CHAR_LEN*2)

WALL_HITBOX_COORDS = [
    # 1st section coords
    (-1568, -896, 672, 784),
    (-1568, -1680, 1456, 784),
    (-3136, -1456, 1344, 112), 
    (-3136, -1344, 224, 560), 
    (-2576, -896, 784, 112), 
    (-2688, -896, 112, 2016), 
    (-2912, 896, 224, 224), 
    (-2912, 1120, 672, 224), 
    (-2576, 672, 1008, 224), 
    (-2016, 112, 672, 336), 
    (-2352, -560, 112, 1232), 
    (-2240, -560, 448, 448), 
    (-2912, 1568, 896, 224), 
    (-2688, 1792, 448, 224), 
    (-3360, 896, 224, 1344), 
    (-3360, 0, 224, 224), 
    (-2912, 0, 224, 224), 
    (-2912, -560, 224, 112), 
    (-3360, -560, 224, 112), 
    (-3136, 2016, 224, 224), 
    (-2688, 2240, 448, 224), 
    (-3136, 2464, 112, 448), 
    (-2800, 2688, 224, 224), 
    (-2352, 2688, 112, 448), 
    (-2016, 1120, 336, 1792), 
    (-1680, 1120, 672, 448), 
    (-1344, 112, 448, 1008), 
    (-896, 896, 784, 224), 
    (-784, 1120, 672, 448),
    # 2nd section coords
    (896, -1344, 336, 672),
    (896, -672, 560, 560), 
    (896, 112, 560, 336), 
    (896, 448, 224, 224), 
    (896, 672, 560, 896), 
    (112, 896, 784, 672), 
    (1680, 224, 1008, 224), 
    (2912, 224, 224, 896), 
    (3136, 112, 336, 1008), 
    (2464, 672, 224, 448), 
    (2464, 1344, 224, 448), 
    (2912, 1344, 336, 784), 
    (2912, 2128, 112, 336), 
    (3024, 2352, 560, 112), 
    (2464, 2688, 672, 112), 
    (2464, 2016, 224, 448), 
    (2912, 3136, 224, 448), 
    (1680, 672, 784, 2464), 
    (3472, -112, 112, 2464), 
    (112, -1568, 1708, 224), 
    (1680, -700, 1008, 476), 
    (2912, -1568, 224, 1344),
    (3136, -1568, 448, 1456),
    # 3rd section coords
    (-1456, 1792, 112, 1344), 
    (-1120, 1792, 112, 1344), 
    (-784, 1792, 112, 1344), 
    (-672, 1792, 560, 224), 
    (112, 1792, 560, 224), 
    (672, 1792, 112, 1344), 
    (112, 2912, 336, 224), 
    (-448, 2912, 336, 224), 
    (1008, 1792, 112, 672), 
    (1008, 2688, 112, 448), 
    (1344, 2240, 112, 672), 
    (1344, 1792, 112, 224),
    # Outer wall coords
    (-1120, -3584, 2240, 448), 
    (-3584, -2240, 224, 5824), 
    (-3360, -2240, 3248, 560), 
    (112, -2240, 3472, 672), 
    (3136, 2464, 448, 1120), 
    (-3360, 3136, 3248, 448), 
    (112, 3136, 2576, 448), 
    (112, -1344, 784, 448)
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

def retrieve_file_info():
    return FILE_INFO_DICT

def retrieve_file_names():
    file_names_list = []
    for key in FILE_INFO_DICT:
        file_names_list.append(key)
    return file_names_list

def retrieve_key_combos():
    return KEY_COMBOS

def retrieve_hitboxes(screen_w_half, screen_h_half):
    direction_hitboxes, wall_hitboxes = [], []
    detection_hitbox = alterAsset.centre_rect(pygame.Rect(DETECTION_HITBOX_COORDS), screen_w_half, screen_h_half)
    for hitbox in DIRECTION_HITBOX_COORDS:
        direction_hitboxes.append(alterAsset.centre_rect(pygame.Rect(hitbox), screen_w_half, screen_h_half))
    for hitbox in WALL_HITBOX_COORDS:
        wall_hitboxes.append(pygame.Rect(hitbox))
    return direction_hitboxes, detection_hitbox, wall_hitboxes