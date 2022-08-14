import pygame
import time
import assetList, loadAssets, alterAsset
import random

FPS = 20
MAP_DIM_MULT = 28
HUD_PERCENT = 0.2
MOVE_SPEED = 15

BLACK = (0,0,0)

current_direction = 0

clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

WIDTH, HEIGHT = WINDOW.get_size()
WIDTH_HALF, HEIGHT_HALF = int(WIDTH/2), int(HEIGHT/2)

HUD_HEIGHT = int(HEIGHT*HUD_PERCENT)

ASSET_INFO = assetList.retrieve_info()
ASSET_NAMES = assetList.retrieve_names()
ORIG_ASSETS, ASSET_HITBOXES = loadAssets.load_resources(ASSET_INFO)
KEY_COMBOS = assetList.retrieve_key_combos()
CHAR_HITBOXES = assetList.retrieve_char_hitboxes(WIDTH_HALF, HEIGHT_HALF)


RAND_LIST = []
RAND_HITBOXES = []
WALL_HITBOXES = []

for count in range(100):
    RAND_LIST.append(random.randint(-3000,3000))
    RAND_HITBOXES.append(pygame.Rect(0,0,100,100))

def get_centered_coords(object_width, object_height):
    asset_width_half = int(object_width/2)
    asset_height_half = int(object_height/2)
    return (WIDTH_HALF-asset_width_half, HEIGHT_HALF-asset_height_half)

def check_keys():
    for event in pygame.event.get():
        pass

    keys_pressed = pygame.key.get_pressed()
    return keys_pressed

def alter_offset(map_offset, char_direction, colliding_char_hitboxes, keys_pressed):
    for index, key_combo in enumerate(KEY_COMBOS):
        if index not in colliding_char_hitboxes:
            if keys_pressed[key_combo[0]] and keys_pressed[key_combo[1]]:
                char_direction = KEY_COMBOS[key_combo][0]
                map_offset[0] += KEY_COMBOS[key_combo][1]
                map_offset[1] += KEY_COMBOS[key_combo][2]
    
    return map_offset, char_direction

def update_hitbox(asset, hitbox, index, map_offset):
    centered_coords = get_centered_coords(asset.get_width(), asset.get_height())
    if hitbox.size != asset.get_size():
        hitbox.size = asset.get_size()
    asset_offset = ASSET_INFO[ASSET_NAMES[index]][0]
    if ASSET_INFO[ASSET_NAMES[index]][2]:
        coordinates = (centered_coords[0] + asset_offset[0], centered_coords[1] + asset_offset[1])
    else:
        coordinates = (centered_coords[0] + map_offset[0] + asset_offset[0], centered_coords[1] + map_offset[1] + asset_offset[1])
    hitbox.topleft = coordinates
    return hitbox

def update_asset(asset, index):
    ASSET_INFO[ASSET_NAMES[index]][3]
    
    return asset

def blit_asset(asset, hitbox):
    WINDOW.blit(asset, hitbox.topleft)

def move_all_assets(assets, hitboxes, map_offset):
    WINDOW.fill(BLACK)
    e = []
    for rect in WALL_HITBOXES:
        e.append(rect.copy())
    for index, asset in enumerate(assets):
        # asset = update_asset(asset, index)
        hitboxes[index] = update_hitbox(asset, hitboxes[index], index, map_offset)
        for inde, hitbox in enumerate(RAND_HITBOXES):
            hitbox.topleft = (RAND_LIST[inde] + map_offset[0], RAND_LIST[-inde] + map_offset[1])
            pygame.draw.rect(WINDOW, (250,233,89), hitbox)

        blit_asset(asset, hitboxes[index])

    for (hitbox, hitbo) in zip(e, WALL_HITBOXES):

        hitbox.topleft = (hitbo.x + map_offset[0] + WIDTH_HALF, hitbo.y + map_offset[1] + HEIGHT_HALF)
        pygame.draw.rect(WINDOW, (10,233,78), hitbox)

    #for hitbox in CHAR_HITBOXES:
       # pygame.draw.rect(WINDOW, (10,233,78), hitbox)
    
    
    # pygame.draw.rect(WINDOW, BLACK, (0,HEIGHT-HUD_HEIGHT,WIDTH,HUD_HEIGHT))

    return e

def check_collision(hitbox_list1, hitbox_list2):
    colliding_hitboxes = []
    for index, hitbox in enumerate(hitbox_list1):
        if hitbox.collidelistall(hitbox_list2):
            colliding_hitboxes.append(index)

    return colliding_hitboxes

def rect_with_coords(coord_set1, coord_set2):
    coord_diff = (coord_set2[0]-coord_set1[0], coord_set2[1]-coord_set1[1])
    rect = pygame.Rect(coord_set1, coord_diff)
    print("yes")
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
    hitboxes = ASSET_HITBOXES.copy()
    running = True
    map_offset = [0,0]
    char_direction = 0
    saved_coords = 0
    saved_time = time.time()
    loop_repeat = 0 
    time_taken = []
    wall_hitboxes = []

    while running:
        time1 = time.time()
        clock.tick(FPS)
        loop_repeat += 1

        assets = ORIG_ASSETS.copy()
        keys_pressed = check_keys()

        colliding_char_hitboxes = check_collision(CHAR_HITBOXES, wall_hitboxes)

        map_offset, char_direction = alter_offset(map_offset, char_direction, colliding_char_hitboxes, keys_pressed)    

        assets[1] = alterAsset.rotate_asset(ORIG_ASSETS[1], char_direction)

        wall_hitboxes = move_all_assets(assets, hitboxes, map_offset)

        if keys_pressed[pygame.K_ESCAPE]:
            running = False

        pygame.display.update()

        wall_hitbox, saved_coords, saved_time = get_wall_hitbox(map_offset, saved_coords, saved_time, keys_pressed)

        if wall_hitbox != 0:
            WALL_HITBOXES.append(wall_hitbox)
        
        time2 = time.time()
        time_taken.append(time2 - time1)

    print(WALL_HITBOXES)
    print(loop_repeat)
    print("\nSPF = " + str(round(sum(time_taken)/len(time_taken), 7)) + "\n")

def main():
    pygame.display.set_caption("My Personal Project")
    
    run_game()

    pygame.quit()

main()