import pygame
import alterAsset

CHAR_LEN = 100
CHAR_SPEED = 10
CHAR_HITBOX_PERCENT = 0.3
CHAR_LEN_HALF = int(CHAR_LEN/2)
CHAR_HITBOX_LEN = int(CHAR_LEN*CHAR_HITBOX_PERCENT)

ASSET_INFO_DICT = {
    # asset_name : ((orig_coords), size_mult, is_movable, is_permeable)
    "Map(v0.1)" : ((0,0), 28, True, True), 
    "CharSword1" : ((0,1000), 5, True, True),
    "Crosshair" : ((0,0), 5, False, True),
    "Star" : ((0,1000), 5, True, True),
    "Door1" : ((2660-3584,0), 28, True, False)

}

DIRECTION_HITBOX_COORDS = [
    (-CHAR_HITBOX_LEN,-CHAR_LEN_HALF,CHAR_HITBOX_LEN*2,CHAR_LEN_HALF),
    (-CHAR_HITBOX_LEN,0,CHAR_HITBOX_LEN*2,CHAR_LEN_HALF),
    (-CHAR_LEN_HALF,-CHAR_HITBOX_LEN,CHAR_LEN_HALF,CHAR_HITBOX_LEN*2), 
    (0,-CHAR_HITBOX_LEN,CHAR_LEN_HALF,CHAR_HITBOX_LEN*2)
]

DETECTION_HITBOX_COORDS = (-CHAR_LEN, -CHAR_LEN, CHAR_LEN*2, CHAR_LEN*2)

WALL_HITBOX_COORDS = [
    (110, -220, 100, 100),
    (410, -170, 190, 190), 
    (180, -10, 250, 710), 

    (120, -520, 280, 270), 
    (-360, 190, 830, 160), 
    (-370, -710, 370, 370), 
    (-470, -370, 120, 520), 
    (-60, -790, 580, 180), 
    (540, -570, 240, 260), 
    (560, -240, 20, 30)

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

def retrieve_asset_info():
    return ASSET_INFO_DICT

def retrieve_asset_names():
    asset_names_list = []
    for key in ASSET_INFO_DICT:
        asset_names_list.append(key)
    return asset_names_list

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