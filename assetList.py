import pygame

CHAR_LEN = 100
CHAR_LEN_HALF = int(CHAR_LEN/2)
CHAR_HITBOX_PERCENT = 0.3
CHAR_HITBOX_LEN = int(CHAR_LEN*CHAR_HITBOX_PERCENT)

CHAR_SPEED = 15

ASSET_INFO_DICT = {
    "Map(v0.1)" : ((0,0), 28, ""), 
    "CharSword1" : ((0,0), 5, "IMMOVE"),
    "Crosshair" : ((0,1000), 5, ""),
    "Star" : ((0,0), 5, "IMMOVE"),
    "Door1" : ((2660-3584,0), 28, "")

}

KEY_COMBOS = {
    (pygame.K_UP, pygame.K_UP) : (0, 0, CHAR_SPEED),
    (pygame.K_DOWN, pygame.K_DOWN) : (180, 0, -CHAR_SPEED),
    (pygame.K_LEFT, pygame.K_LEFT) : (90, CHAR_SPEED, 0),
    (pygame.K_RIGHT, pygame.K_RIGHT) : (270, -CHAR_SPEED, 0),
    (pygame.K_UP, pygame.K_LEFT) : (45, 0, 0),
    (pygame.K_UP, pygame.K_RIGHT) : (315, 0, 0),
    (pygame.K_DOWN, pygame.K_LEFT) : (135, 0, 0),
    (pygame.K_DOWN, pygame.K_RIGHT) : (225, 0, 0)
}

CHAR_HITBOX_COORDS = {
    0 : [-CHAR_LEN_HALF,-CHAR_HITBOX_LEN,CHAR_LEN_HALF,CHAR_HITBOX_LEN*2], 
    1 : [0,-CHAR_HITBOX_LEN,CHAR_LEN_HALF,CHAR_HITBOX_LEN*2],
    2 : [-CHAR_HITBOX_LEN,-CHAR_LEN_HALF,CHAR_HITBOX_LEN*2,CHAR_LEN_HALF],
    3 : [-CHAR_HITBOX_LEN,0,CHAR_HITBOX_LEN*2,CHAR_LEN_HALF]
}

WALL_HITBOXES = {

}

def retrieve_info():
    return ASSET_INFO_DICT

def retrieve_names():
    ASSET_NAMES_LIST = []
    for key in ASSET_INFO_DICT:
        ASSET_NAMES_LIST.append(key)
    return ASSET_NAMES_LIST

def retrieve_key_combos():
    return KEY_COMBOS

def retrieve_char_hitboxes(width_half, height_half):
    CHAR_HITBOXES = []
    for key in CHAR_HITBOX_COORDS:
        CHAR_HITBOX_COORDS[key][0] += width_half
        CHAR_HITBOX_COORDS[key][1] += height_half
        CHAR_HITBOXES.append(pygame.Rect(tuple(CHAR_HITBOX_COORDS[key])))
    return CHAR_HITBOXES

