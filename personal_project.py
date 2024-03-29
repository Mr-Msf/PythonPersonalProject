import pygame
import time
import constants, file_preparer, other_functions

pygame.font.init()

WINDOW = constants.WINDOW

assets = file_preparer.load_assets(constants.ASSET_INFO)
other_hitboxes = file_preparer.get_hitboxes(constants.ALL_HITBOX_COORDS)
#SOUNDTRACKS = file_preparer.e(constants.SOUNDTRACK_INFO)

def check_keys():
    for event in pygame.event.get():
        pass

    keys_pressed = pygame.key.get_pressed()
    return keys_pressed

def rect_with_coords(coord_set1, coord_set2):
    coord_diff = (coord_set2[0]-coord_set1[0], coord_set2[1]-coord_set1[1])
    rect = pygame.Rect(coord_set1, coord_diff)
    return rect

def alter_map_offset(map_offset, char_direction, colliding_char_hitboxes, keys_pressed):
    for index, key_combo in enumerate(constants.KEY_COMBOS):
        if index not in colliding_char_hitboxes:
            if keys_pressed[key_combo[0]] and keys_pressed[key_combo[1]]:
                char_direction = constants.KEY_COMBOS[key_combo][0]
                map_offset[0] += constants.KEY_COMBOS[key_combo][1]
                map_offset[1] += constants.KEY_COMBOS[key_combo][2]
    
    return map_offset, char_direction

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

def get_non_permeable_hitboxes(objects):
    non_permeable_hitboxes = []
    for object in objects:
        if not object.is_permeable:
            non_permeable_hitboxes.append(object.hitbox)
    return non_permeable_hitboxes

def get_hitboxes_from_list(object_list):
    hitboxes = []
    for object in object_list:
        hitboxes.append(object.hitbox)
    return hitboxes

def collect_items(assets, detection_hitbox, items_collected, keys_pressed, saved_time):
    for index, asset in enumerate(assets):
        if asset.check_collision(detection_hitbox) and asset.is_collectable:
            if keys_pressed[pygame.K_SPACE]:
                asset.status_var = True
                asset.orig_hitbox.topleft = (1000000,1000000)
                saved_time = time.time()
                items_collected.append(index)
    return items_collected, saved_time

def handle_mechanisms(other_objects, detection_hitbox, keys_pressed):
    for switch in other_objects[0]:
        if keys_pressed[pygame.K_SPACE]:
            switch.flip(detection_hitbox, other_objects[1])
    for door in other_objects[1]:
        door.reverse()

def get_touching_asset_index(other_objects, detection_hitbox):
    for index, switch in enumerate(other_objects[0]):
        if switch.asset.check_collision(detection_hitbox):
            return index
    for index, door in enumerate(other_objects[1]):
        if door.asset.check_collision(detection_hitbox):
            return index
    return "lol"

def take_damage(hitboxes, char_health):
    for hitbox in hitboxes:
        if hitbox.check_collision(hitboxes[5].hitbox):
            char_health -= hitbox.dmg_amount
    if char_health > 1000:
        char_health = 1000
    elif char_health < 0:
        char_health = 0
    return char_health

def handle_health_system(assets, other_hitboxes, char_health):
    char_health = take_damage(other_hitboxes, char_health)
    hearts = int(char_health/200)
    for count in range(hearts):
        heart_spacing = count * 100 + 100
        WINDOW.blit(assets[-3].image, (constants.WIDTH - heart_spacing, constants.HEIGHT - 100))
    return char_health

def handle_collected_items(assets, words, items_collected):
    collectable_info = constants.COLLECTABLE_INFO
    for item in items_collected:
        asset = assets[item]
        coords = collectable_info[asset.name][0]
        words[collectable_info[asset.name][1]].is_visible = True
        asset.orig_hitbox.topleft = (coords)

def open_collectable_doors(assets, doors, items_collected):
    major_collectable_num = 0
    minor_collectable_num = 0
    omega_collectable_num = 0
    for item_index in items_collected:
        if item_index in constants.MAJOR_COLLECTABLE_ASSET_INDICES:
            major_collectable_num += 1
        if item_index in constants.MINOR_COLLECTABLE_ASSET_INDICES:
            minor_collectable_num += 1
        if item_index in constants.OMEGA_COLLECTABLE_ASSET_INDICES:
            omega_collectable_num += 1
    if major_collectable_num == 3:
        doors[13].state = True
    if minor_collectable_num == 10:
        doors[59].state = True
        doors[39].state = True
    if omega_collectable_num == 1:
        assets[14].is_movable = False

def handle_projectiles(projectiles, collidable_hitboxes, char_health):

    for projectile in projectiles:
        projectile.update_position()

        if projectile.check_all_collision(collidable_hitboxes):

            if projectile.asset.check_collision(collidable_hitboxes[-1]):
                char_health -= projectile.dmg_amount
            projectile.reset_position()
    return char_health

def modify_assets(assets, other_objects, other_hitboxes, items_collected, char_health, keys_pressed, saved_time):
    if saved_time + 0.5 < time.time():
        items_collected, saved_time = collect_items(assets, other_hitboxes[4].hitbox, items_collected, keys_pressed, saved_time)

        handle_collected_items(assets, other_objects[3], items_collected)

        char_health = handle_projectiles(other_objects[2], get_non_permeable_hitboxes(assets + other_hitboxes) + [other_hitboxes[5].hitbox], char_health)

        handle_mechanisms(other_objects, other_hitboxes[4].hitbox, keys_pressed)

    open_collectable_doors(assets, other_objects[1], items_collected)
    
    return items_collected, char_health, saved_time

def update_all_positions(assets, other_hitboxes, map_offset):
    WINDOW.fill(constants.BLACK)
    for object in assets + other_hitboxes:
        object.update_position(map_offset)

    for asset in assets:
        asset.blit(WINDOW)

    pygame.draw.rect(WINDOW, constants.BLACK, other_hitboxes[-1].hitbox)

    for hitbox in other_hitboxes:
        break
        #other_functions.draw_rect_list(WINDOW, [all_hitboxes[1]], constants.RED)
        #draw_rect_list(DIRECTION_HITBOXES, constants.GREEN)
        pygame.draw.rect(WINDOW, constants.BLUE, hitbox.hitbox)
    #pygame.draw.rect(WINDOW, constants.RED, other_hitboxes[5].hitbox)
        
    
    # pygame.draw.rect(WINDOW, BLACK, (0,HEIGHT-HUD_HEIGHT,WIDTH,HUD_HEIGHT))

def draw_game_gui(assets, other_hitboxes, char_health):
    char_health = handle_health_system(assets, other_hitboxes, char_health)
    
    return char_health

def run_game(assets, other_hitboxes, clock):
    running = True
    map_offset = [0, -224]
    char_direction = 180
    char_health = 1000
    saved_time = time.time()
    times_taken = []
    object_coords = []
    wall_hitbox_list = []
    asset_list_indices = []
    other_objects = file_preparer.get_switches_and_doors(assets)
    saved_coords = 0
    items_collected = []

    while running:
        time1 = time.time()
        
        keys_pressed = check_keys()
        non_permeable_hitboxes = get_non_permeable_hitboxes(assets + other_hitboxes)
    
        if keys_pressed[pygame.K_1] and keys_pressed[pygame.K_3] and keys_pressed[pygame.K_m] and not keys_pressed[pygame.K_2]:
            colliding_char_hitboxes = []
        else:
            colliding_char_hitboxes = check_list_collision(get_hitboxes_from_list(other_hitboxes[:4]), non_permeable_hitboxes)
        
        map_offset, char_direction = alter_map_offset(map_offset, char_direction, colliding_char_hitboxes, keys_pressed)    
        
        assets[-1].rotate(char_direction)

        for word in other_objects[3]:
            word.check_collision(other_hitboxes[4].hitbox)
            word.update(map_offset)

        items_collected, char_health, saved_time = modify_assets(assets, other_objects, other_hitboxes, items_collected, char_health, keys_pressed, saved_time)

        update_all_positions(assets, other_hitboxes, map_offset)
        
        char_health = draw_game_gui(assets, other_hitboxes, char_health)

        #if keys_pressed[pygame.K_o]:
        #    point_coords, saved_time = get_point_coords(map_offset, saved_time)
        #    if point_coords != 0:
        #        object_coords.append(point_coords)

        if keys_pressed[pygame.K_i]:
            touching_asset_index = get_touching_asset_index(other_objects, other_hitboxes[4].hitbox)
            if touching_asset_index != "lol" and saved_time + 0.3 < time.time():
                asset_list_indices.append(touching_asset_index)
                saved_time = time.time()

        if keys_pressed[pygame.K_ESCAPE]:    
            running = False

        if char_health <= 0:
            map_offset = [0,0]

        pygame.display.update()

        wall_hitbox, saved_coords, saved_time = get_wall_hitbox(map_offset, saved_coords, saved_time, keys_pressed)
        
        if wall_hitbox != 0:
            wall_hitbox_list.append(wall_hitbox)
        
        time2 = time.time()
        times_taken.append(time2 - time1)
    
    print(wall_hitbox_list)
    print(items_collected)
    print(asset_list_indices)
    print(object_coords)

    print("\nSPF = " + str(round(sum(times_taken)/len(times_taken), 7)) + "\n")

def main(assets, other_hitboxes):
    clock = pygame.time.Clock()
    pygame.display.set_caption("My Personal Project")
    
    run_game(assets, other_hitboxes, clock)

    pygame.quit()

main(assets, other_hitboxes)