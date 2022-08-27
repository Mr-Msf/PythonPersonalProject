import pygame
import time
import constants, file_preparer, asset_creator, alterAsset
import random

WINDOW = constants.WINDOW

ASSETS = file_preparer.load_assets(constants.ASSET_INFO)
#SOUNDTRACKS = file_preparer.e(constants.SOUNDTRACK_INFO)
DIRECTION_HITBOXES, DETECTION_HITBOX, ORIG_WALL_HITBOXES = constants.retrieve_hitboxes()

WALL_HITBOXES = ORIG_WALL_HITBOXES

def check_keys():
    for event in pygame.event.get():
        pass

    keys_pressed = pygame.key.get_pressed()
    return keys_pressed

def alter_map_offset(map_offset, char_direction, colliding_char_hitboxes, keys_pressed):
    for index, key_combo in enumerate(constants.KEY_COMBOS):
        if index not in colliding_char_hitboxes:
            if keys_pressed[key_combo[0]] and keys_pressed[key_combo[1]]:
                char_direction = constants.KEY_COMBOS[key_combo][0]
                map_offset[0] += constants.KEY_COMBOS[key_combo][1]
                map_offset[1] += constants.KEY_COMBOS[key_combo][2]
    
    return map_offset, char_direction

def modify_asset(asset, colliding_asset_hitboxes, asset_properties):
    E = asset_properties[3]
    
    return asset

def blit_asset(asset, hitbox):
    WINDOW.blit(asset, hitbox.topleft)

def draw_rect_list(rect_list, colour):
    for rect in rect_list:
        pygame.draw.rect(WINDOW, colour, rect)

def update_all_resources(assets, colliding_asset_hitboxes, map_offset):
    WINDOW.fill(constants.BLACK)
    wall_hitboxes = []
    for wall_hitbox in WALL_HITBOXES:
        wall_hitbox = alterAsset.move_hitbox(wall_hitbox, map_offset)
        wall_hitboxes.append(wall_hitbox)

    for asset in assets:
        #asset = modify_asset(asset, colliding_asset_hitboxes, asset_properties)
        asset.update_position(map_offset)
        asset.blit(WINDOW)

    #draw_rect_list([DETECTION_HITBOX], constants.RED)
    #draw_rect_list(DIRECTION_HITBOXES, constants.GREEN)
    draw_rect_list(wall_hitboxes, constants.BLUE)
    
    # pygame.draw.rect(WINDOW, BLACK, (0,HEIGHT-HUD_HEIGHT,WIDTH,HUD_HEIGHT))

    return assets, wall_hitboxes

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
    if keys_pressed[pygame.K_q] and saved_time + 0.5 < time.time():
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

def get_asset_hitboxes(assets):
    asset_hitboxes = []
    for asset in assets:
        asset_hitboxes.append(asset.detectable_hitbox)
    return asset_hitboxes

def run_game(assets, clock):
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
        clock.tick(constants.FPS)
        loop_repeat += 1

        keys_pressed = check_keys()
        asset_hitboxes = get_asset_hitboxes(assets)

        colliding_char_hitboxes = check_collision(DIRECTION_HITBOXES, (wall_hitboxes + asset_hitboxes))
        colliding_asset_hitboxes = 0#check_collision(asset_hitboxes, [DETECTION_HITBOX])

        map_offset, char_direction = alter_map_offset(map_offset, char_direction, colliding_char_hitboxes, keys_pressed)    

        assets[1].rotate(char_direction)

        assets, wall_hitboxes = update_all_resources(assets, colliding_asset_hitboxes, map_offset)

        if keys_pressed[pygame.K_SPACE]:
            print((-map_offset[0], -map_offset[1]))

        if keys_pressed[pygame.K_ESCAPE]:
            running = False

        pygame.display.update()

        wall_hitbox, saved_coords, saved_time = get_wall_hitbox(map_offset, saved_coords, saved_time, keys_pressed)

        if wall_hitbox != 0:
            WALL_HITBOXES.append(wall_hitbox)
        
        time2 = time.time()
        time_taken.append(time2 - time1)


    wall_hitbox_info = []
    for hitbox in WALL_HITBOXES:
        wall_hitbox_info.append((hitbox.x, hitbox.y, hitbox.width, hitbox.height))

    print("\nSPF = " + str(round(sum(time_taken)/len(time_taken), 7)) + "\n")

def main():
    clock = pygame.time.Clock()
    assets = ASSETS
    
    pygame.display.set_caption("My Personal Project")
    
    run_game(assets, clock)

    pygame.quit()

main()