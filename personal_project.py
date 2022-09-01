import pygame
import time
import constants, file_preparer, asset_creator, alterAsset
import random

WINDOW = constants.WINDOW

assets = file_preparer.load_assets(constants.ASSET_INFO)
#SOUNDTRACKS = file_preparer.e(constants.SOUNDTRACK_INFO)
other_hitboxes = constants.retrieve_hitboxes()

def check_keys():
    for event in pygame.event.get():
        pass

    keys_pressed = pygame.key.get_pressed()
    return keys_pressed

def draw_rect_list(rect_list, colour):
    for rect in rect_list:
        pygame.draw.rect(WINDOW, colour, rect)

def rect_with_coords(coord_set1, coord_set2):
    coord_diff = (coord_set2[0]-coord_set1[0], coord_set2[1]-coord_set1[1])
    rect = pygame.Rect(coord_set1, coord_diff)
    return rect

def return_opposite_bool(bool_value):
    if bool_value:
        return False
    return True

def alter_map_offset(map_offset, char_direction, colliding_char_hitboxes, keys_pressed):
    for index, key_combo in enumerate(constants.KEY_COMBOS):
        if index not in colliding_char_hitboxes:
            if keys_pressed[key_combo[0]] and keys_pressed[key_combo[1]]:
                char_direction = constants.KEY_COMBOS[key_combo][0]
                map_offset[0] += constants.KEY_COMBOS[key_combo][1]
                map_offset[1] += constants.KEY_COMBOS[key_combo][2]
    
    return map_offset, char_direction

def modify_assets(assets, detection_hitbox, keys_pressed, saved_time):
    collect_items(assets, detection_hitbox, keys_pressed)
    
    #if keys_pressed[pygame.K_a]:
    #    assets[11].rotate(240)

    handle_mechanisms(assets, detection_hitbox, keys_pressed)
    return assets

def check_list_collision(hitbox_list1, hitbox_list2):
    colliding_hitboxes = []
    for index, hitbox in enumerate(hitbox_list1):
        if hitbox.collidelistall(hitbox_list2):
            colliding_hitboxes.append(index)
    return colliding_hitboxes

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

def get_point_coords(map_offset, saved_time):
    if saved_time + 0.5 < time.time():
        point_coords = (-map_offset[0], -map_offset[1])
        saved_time = time.time()
        return point_coords, saved_time
    return 0, saved_time

def get_asset_hitboxes(assets):
    asset_hitboxes = []
    for asset in assets:
        asset_hitboxes.append(asset.detectable_hitbox)
    return asset_hitboxes

def collect_items(assets, detection_hitbox, keys_pressed):
    for asset in assets:
        if asset.check_collision(detection_hitbox) and asset.is_collectable:
            if keys_pressed[pygame.K_f]:
                asset.status_var = True
                asset.orig_hitbox.topleft = (1000000,1000000)

def get_switches_and_doors(assets):
    switches, doors = [], []
    for asset in assets:
        if "Door" in asset.name:
            doors.append(asset)
        if "Switch" in asset.name:
            switches.append(asset)
    return switches, doors

def handle_mechanisms(assets, detection_hitbox, keys_pressed):
    switch_assets, door_assets = get_switches_and_doors(assets)
    for switch_number, switch in enumerate(switch_assets):
        if switch.check_collision(detection_hitbox) and keys_pressed[pygame.K_o]:
            switch.status_var = not switch.status_var
            move_door_assets(door_assets, constants.DOORS_PER_SWITCH[switch_number])
        if switch.status_var:
            switch.rotate(300)
        else:
            switch.rotate(240)

def move_door_assets(door_assets, moving_door_numbers):
    for door_number in moving_door_numbers:
        door_assets[door_number].status_var = not door_assets[door_number].status_var
    for door_asset in door_assets:
        if door_asset.status_var:
            door_asset.orig_hitbox.topleft = (1000000,1000000)
        else:
            door_asset.orig_hitbox.topleft = door_asset.orig_coords

def update_all_resources(assets, other_hitboxes, map_offset, keys_pressed, saved_time):
    WINDOW.fill(constants.BLACK)
    new_wall_hitboxes = []
    for wall_hitbox in other_hitboxes[2]:
        new_wall_hitbox = alterAsset.move_hitbox(wall_hitbox, map_offset)
        new_wall_hitboxes.append(new_wall_hitbox)

    modify_assets(assets, other_hitboxes[1], keys_pressed, saved_time)
    for asset in assets:
        asset.update_position(map_offset)
        asset.blit(WINDOW)

    #draw_rect_list([DETECTION_HITBOX], constants.RED)
    #draw_rect_list(DIRECTION_HITBOXES, constants.GREEN)
    draw_rect_list(new_wall_hitboxes, constants.BLUE)
    
    # pygame.draw.rect(WINDOW, BLACK, (0,HEIGHT-HUD_HEIGHT,WIDTH,HUD_HEIGHT))

    return new_wall_hitboxes

def run_game(assets, other_hitboxes, clock):
    running = True
    map_offset = [0,0]
    char_direction = 0
    saved_time = time.time()
    loop_repeat = 0 
    times_taken = []
    direction_hitboxes, detection_hitbox, orig_wall_hitboxes = other_hitboxes
    wall_hitboxes = orig_wall_hitboxes.copy()
    #wall_hitbox_info = []
    #saved_coords = 0
    object_coords = []
    items_collected = 0
    
    while running:
        time1 = time.time()
        clock.tick(constants.FPS)
        loop_repeat += 1

        keys_pressed = check_keys()
        asset_hitboxes = get_asset_hitboxes(assets)

        colliding_char_hitboxes = check_list_collision(direction_hitboxes, (wall_hitboxes + asset_hitboxes))

        map_offset, char_direction = alter_map_offset(map_offset, char_direction, colliding_char_hitboxes, keys_pressed)    
        
        wall_hitboxes = update_all_resources(assets, other_hitboxes, map_offset, keys_pressed, saved_time)

        if keys_pressed[pygame.K_SPACE]:
            point_coords, saved_time = get_point_coords(map_offset, saved_time)
            if point_coords != 0:
                object_coords.append(point_coords)

        if keys_pressed[pygame.K_ESCAPE]:
            running = False

        pygame.display.update()

        #wall_hitbox, saved_coords, saved_time = get_wall_hitbox(map_offset, saved_coords, saved_time, keys_pressed)

        #if wall_hitbox != 0:
        #    WALL_HITBOXES.append(wall_hitbox)
        
        time2 = time.time()
        times_taken.append(time2 - time1)

    
    #for hitbox in WALL_HITBOXES:
    #    wall_hitbox_info.append((hitbox.x, hitbox.y, hitbox.width, hitbox.height))

    print("\nSPF = " + str(round(sum(times_taken)/len(times_taken), 7)) + "\n")

def main(assets, other_hitboxes):
    clock = pygame.time.Clock()
    pygame.display.set_caption("My Personal Project")
    
    run_game(assets, other_hitboxes, clock)

    pygame.quit()

main(assets, other_hitboxes)