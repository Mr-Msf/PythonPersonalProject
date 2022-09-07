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

def modify_assets(assets, other_objects, other_hitboxes, keys_pressed, saved_time):
    if saved_time + 0.5 < time.time():
        saved_time = collect_items(assets, other_hitboxes[4].hitbox, keys_pressed, saved_time)
    
        #if keys_pressed[pygame.K_a]:
        #    assets[11].rotate(240)

        handle_mechanisms(other_objects, other_hitboxes[4].hitbox, keys_pressed)
    return saved_time

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

def get_non_permeable_hitboxes(assets, hitboxes):
    non_permeable_hitboxes = []
    for object in assets + hitboxes:
        if not object.is_permeable:
            non_permeable_hitboxes.append(object.hitbox)
    return non_permeable_hitboxes

def get_hitboxes_from_list(object_list):
    hitboxes = []
    for object in object_list:
        hitboxes.append(object.hitbox)
    return hitboxes

def collect_items(assets, detection_hitbox, keys_pressed, saved_time):
    for asset in assets:
        if asset.check_collision(detection_hitbox) and asset.is_collectable:
            if keys_pressed[pygame.K_f]:
                asset.status_var = True
                asset.orig_hitbox.topleft = (1000000,1000000)
                saved_time = time.time()
    return saved_time

def handle_mechanisms(other_objects, detection_hitbox, keys_pressed):
    for switch in other_objects[0]:
        if keys_pressed[pygame.K_o]:
            switch.flip(detection_hitbox, other_objects[1])
    for door in other_objects[1]:
        door.update()

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
    if char_health > 500:
        char_health = 500
    return char_health

def handle_health_system(assets, other_hitboxes, char_health):
    char_health = take_damage(other_hitboxes, char_health)
    hearts = char_health//5
    for count in range(hearts):
        heart_spacing = count * 100
        WINDOW.blit(assets[-2].image, (constants.WIDTH - heart_spacing, constants.HEIGHT - 100))
    return char_health

def update_all_positions(assets, other_hitboxes, map_offset):
    WINDOW.fill(constants.BLACK)
    for object in assets + other_hitboxes:
        object.update_position(map_offset)

    for asset in assets:
        asset.blit(WINDOW)

    for hitbox in other_hitboxes:
        break
        #other_functions.draw_rect_list(WINDOW, [all_hitboxes[1]], constants.RED)
        #draw_rect_list(DIRECTION_HITBOXES, constants.GREEN)
        pygame.draw.rect(WINDOW, constants.BLUE, hitbox.hitbox)
    #pygame.draw.rect(WINDOW, constants.RED, other_hitboxes[5].hitbox)
        
    
    # pygame.draw.rect(WINDOW, BLACK, (0,HEIGHT-HUD_HEIGHT,WIDTH,HUD_HEIGHT))

def run_game(assets, other_hitboxes, clock):
    running = True
    map_offset = [0,0]
    char_direction = 0
    char_health = 500
    saved_time = time.time()
    times_taken = []
    #wall_hitbox_info = []
    #saved_coords = 0
    object_coords = []
    items_collected = 0
    asset_list_indices = []
    other_objects = file_preparer.get_switches_and_doors(assets)
    
    #sans_font = pygame.font.SysFont("sans", 40)

    while running:
        time1 = time.time()
        clock.tick(constants.FPS)

        keys_pressed = check_keys()
        non_permeable_hitboxes = get_non_permeable_hitboxes(assets, other_hitboxes)
        
        print(char_health)
        #message = sans_font.render("LOL", 1, constants.BLACK)
        #coords = other_functions.get_centered_coords(message, (constants.WIDTH_HALF, constants.HEIGHT_HALF))
        
        colliding_char_hitboxes = check_list_collision(get_hitboxes_from_list(other_hitboxes[:4]), non_permeable_hitboxes)

        map_offset, char_direction = alter_map_offset(map_offset, char_direction, colliding_char_hitboxes, keys_pressed)    
        
        saved_time = modify_assets(assets, other_objects, other_hitboxes, keys_pressed, saved_time)
        
        update_all_positions(assets, other_hitboxes, map_offset)

        #WINDOW.blit(message, coords)

        if keys_pressed[pygame.K_SPACE]:
            point_coords, saved_time = get_point_coords(map_offset, saved_time)
            if point_coords != 0:
                object_coords.append(point_coords)

        if keys_pressed[pygame.K_i]:
            touching_asset_index = get_touching_asset_index(other_objects, other_hitboxes[4].hitbox)
            if touching_asset_index != "lol" and saved_time + 0.3 < time.time():
                asset_list_indices.append(touching_asset_index)
                saved_time = time.time()

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
    print(asset_list_indices)
    print(object_coords)

    print("\nSPF = " + str(round(sum(times_taken)/len(times_taken), 7)) + "\n")

def main(assets, other_hitboxes):
    clock = pygame.time.Clock()
    pygame.display.set_caption("My Personal Project")
    
    run_game(assets, other_hitboxes, clock)

    pygame.quit()

main(assets, other_hitboxes)