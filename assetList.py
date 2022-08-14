import pygame

CHAR_LEN = 100
CHAR_LEN_HALF = int(CHAR_LEN/2)
CHAR_HITBOX_PERCENT = 0.3
CHAR_HITBOX_LEN = int(CHAR_LEN*CHAR_HITBOX_PERCENT)

CHAR_SPEED = 10

ASSET_INFO_DICT = {
    # asset_name : ((orig_coords), size_mult, is_immovable, is_)
    "Map(v0.1)" : ((0,0), 28, False), 
    "CharSword1" : ((0,1000), 5, True),
    "Crosshair" : ((0,0), 5, True),
    "Star" : ((0,1000), 5, True),
    "Door1" : ((2660-3584,0), 28, False)

}

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

CHAR_HITBOX_COORDS = {
    "top" : [-CHAR_HITBOX_LEN,-CHAR_LEN_HALF,CHAR_HITBOX_LEN*2,CHAR_LEN_HALF],
    "bottom" : [-CHAR_HITBOX_LEN,0,CHAR_HITBOX_LEN*2,CHAR_LEN_HALF],
    "left" : [-CHAR_LEN_HALF,-CHAR_HITBOX_LEN,CHAR_LEN_HALF,CHAR_HITBOX_LEN*2], 
    "right" : [0,-CHAR_HITBOX_LEN,CHAR_LEN_HALF,CHAR_HITBOX_LEN*2]
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

