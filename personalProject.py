from tkinter import N
import pygame
import time
import assetList, loadAssets, alterAsset
import random

FPS = 30
MAP_DIM_MULT = 28
HUD_PERCENT = 0.2
MOVE_SPEED = 15

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

current_direction = 0

clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

WIDTH, HEIGHT = WINDOW.get_size()
WIDTH_HALF, HEIGHT_HALF = int(WIDTH/2), int(HEIGHT/2)

HUD_HEIGHT = int(HEIGHT*HUD_PERCENT)

ASSET_INFO = assetList.retrieve_asset_info()
ASSET_NAMES = assetList.retrieve_asset_names()
ORIG_ASSETS, ASSET_HITBOXES = loadAssets.load_resources(ASSET_INFO)
KEY_COMBOS = assetList.retrieve_key_combos()
DIRECTION_HITBOXES, DETECTION_HITBOX, STARTING_WALL_HITBOXES = assetList.retrieve_hitboxes(WIDTH_HALF, HEIGHT_HALF)

WALL_HITBOXES = STARTING_WALL_HITBOXES

def get_centered_coords(asset):
    object_width_half = int(asset.get_width()/2)
    object_height_half = int(asset.get_height()/2)
    return (WIDTH_HALF-object_width_half, HEIGHT_HALF-object_height_half)

def check_keys():
    for event in pygame.event.get():
        pass

    keys_pressed = pygame.key.get_pressed()
    return keys_pressed

def alter_map_offset(map_offset, char_direction, colliding_char_hitboxes, keys_pressed):
    for index, key_combo in enumerate(KEY_COMBOS):
        if index not in colliding_char_hitboxes:
            if keys_pressed[key_combo[0]] and keys_pressed[key_combo[1]]:
                char_direction = KEY_COMBOS[key_combo][0]
                map_offset[0] += KEY_COMBOS[key_combo][1]
                map_offset[1] += KEY_COMBOS[key_combo][2]
    
    return map_offset, char_direction

def update_asset_hitbox(asset, hitbox, asset_properties, map_offset):
    centered_coords = get_centered_coords(asset)
    # asset = modify_asset(asset, asset_properties)
    if hitbox.size != asset.get_size():
        hitbox.size = asset.get_size()
    if asset_properties[2]:
        screen_offset = map_offset
    else:
        screen_offset = (0,0)
    new_hitbox = move_hitbox(hitbox, screen_offset, centered_coords)
    return asset, new_hitbox

def modify_asset(asset, index):
    ASSET_INFO[ASSET_NAMES[index]][3]
    
    return asset

def blit_asset(asset, hitbox):
    WINDOW.blit(asset, hitbox.topleft)

def move_hitbox(orig_hitbox, map_offset, additional_offset=(WIDTH_HALF, HEIGHT_HALF)):
    new_hitbox = orig_hitbox.copy()
    new_hitbox.topleft = (orig_hitbox.x + map_offset[0] + additional_offset[0], orig_hitbox.y + map_offset[1] + additional_offset[1])
    return new_hitbox

def draw_rect_list(rect_list, colour):
    for rect in rect_list:
        pygame.draw.rect(WINDOW, colour, rect)

def update_all_resources(assets, map_offset):
    WINDOW.fill(BLACK)
    wall_hitboxes = []
    for wall_hitbox in WALL_HITBOXES:
        wall_hitbox = move_hitbox(wall_hitbox, map_offset)
        wall_hitboxes.append(wall_hitbox)

    for asset, asset_hitbox, index in zip(assets, ASSET_HITBOXES, range(len(assets))):
        asset_properties = ASSET_INFO[ASSET_NAMES[index]]
        asset, asset_hitbox = update_asset_hitbox(asset, asset_hitbox, asset_properties, map_offset)
        blit_asset(asset, asset_hitbox)

    draw_rect_list(wall_hitboxes, BLUE)
    
    # pygame.draw.rect(WINDOW, BLACK, (0,HEIGHT-HUD_HEIGHT,WIDTH,HUD_HEIGHT))

    return wall_hitboxes

def check_collision(hitbox_list1, hitbox_list2):
    colliding_hitboxes = []
    for index, hitbox in enumerate(hitbox_list1):
        if hitbox.collidelistall(hitbox_list2):
            colliding_hitboxes.append(index)

    return colliding_hitboxes

def rect_with_coords(coord_set1, coord_set2):
    coord_diff = (coord_set2[0]-coord_set1[0], coord_set2[1]-coord_set1[1])
    rect = pygame.Rect(coord_set1, coord_diff)
    return rect

def get_wall_hitbox(map_offset, saved_coords, saved_time, keys_pressed):
    if keys_pressed[pygame.K_SPACE] and saved_time + 0.5 < time.time():
        rect_coords = (-map_offset[0], -map_offset[1])
        if saved_coords == 0:
            saved_coords = tuple(rect_coords)
            rect = 0
        else:
            rect = rect_with_coords(saved_coords, rect_coords)
            saved_coords = 0
        saved_time = time.time()
    else:
        rect = 0

    return rect, saved_coords, saved_time

def run_game():
    running = True
    map_offset = [0,0]
    char_direction = 0
    saved_coords = 0
    saved_time = time.time()
    loop_repeat = 0 
    time_taken = []
    wall_hitboxes = []
    wall_hitbox_info = []

    while running:
        time1 = time.time()
        clock.tick(FPS)
        loop_repeat += 1

        assets = ORIG_ASSETS.copy()
        keys_pressed = check_keys()

        colliding_char_hitboxes = check_collision(DIRECTION_HITBOXES, wall_hitboxes)

        map_offset, char_direction = alter_map_offset(map_offset, char_direction, colliding_char_hitboxes, keys_pressed)    

        assets[1] = alterAsset.rotate_asset(ORIG_ASSETS[1], char_direction)

        wall_hitboxes = update_all_resources(assets, map_offset)

        if keys_pressed[pygame.K_ESCAPE]:
            running = False

        pygame.display.update()

        wall_hitbox, saved_coords, saved_time = get_wall_hitbox(map_offset, saved_coords, saved_time, keys_pressed)

        if wall_hitbox != 0:
            WALL_HITBOXES.append(wall_hitbox)
        
        time2 = time.time()
        time_taken.append(time2 - time1)

    for hitbox in WALL_HITBOXES:
        wall_hitbox_info.append((hitbox.x, hitbox.y, hitbox.width, hitbox.height))
    print(wall_hitbox_info)
    print(loop_repeat)
    print("\nSPF = " + str(round(sum(time_taken)/len(time_taken), 7)) + "\n")

def main():
    pygame.display.set_caption("My Personal Project")
    
    run_game()

    pygame.quit()

main()