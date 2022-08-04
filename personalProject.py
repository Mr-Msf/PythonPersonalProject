import pygame
import assetList, loadAssets, alterAsset

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

WALL_HITBOXES = pygame.Rect(1000,600,100,100)

def get_centered_coords(asset):
    asset_width_half = int(asset.get_width()/2)
    asset_height_half = int(asset.get_height()/2)
    return (WIDTH_HALF-asset_width_half, HEIGHT_HALF-asset_height_half)

def check_keys():
    for event in pygame.event.get():
        pass

    keys_pressed = pygame.key.get_pressed()
    return keys_pressed

def alter_offset(map_offset, char_direction, keys_pressed):
    for key_combo in KEY_COMBOS:
        if keys_pressed[key_combo[0]] and keys_pressed[key_combo[1]]:
            char_direction = KEY_COMBOS[key_combo][0]
            map_offset[0] += KEY_COMBOS[key_combo][1]
            map_offset[1] += KEY_COMBOS[key_combo][2]
    
    return map_offset, char_direction

def update_hitbox(hitbox, index, map_offset):
    asset_offset = ASSET_INFO[ASSET_NAMES[index]][0]
    if ASSET_INFO[ASSET_NAMES[index]][2] == "IMMOVE":
        coordinates = asset_offset
    else:
        coordinates = (map_offset[0]+asset_offset[0], map_offset[1]+asset_offset[1])
    hitbox.center = coordinates
    return hitbox

def update_asset(asset, index):
    return asset

def blit_asset(asset, hitbox):
    centered_coords = get_centered_coords(asset)
    
    WINDOW.blit(asset, hitbox.topleft)

def move_all_assets(assets, hitboxes, map_offset):
    WINDOW.fill(BLACK)
    for index, asset in enumerate(assets):
        hitboxes[index] = update_hitbox(hitboxes[index], index, map_offset)
        asset = update_asset(asset, index)
        blit_asset(asset, hitboxes[index])

    for hitbox in CHAR_HITBOXES:
        pygame.draw.rect(WINDOW, (10,233,78), hitbox)
    
    pygame.draw.rect(WINDOW, (10,233,250), WALL_HITBOXES)
    
    # pygame.draw.rect(WINDOW, BLACK, (0,HEIGHT-HUD_HEIGHT,WIDTH,HUD_HEIGHT))

def function(hitbox_list):
    for rect in hitbox_list:
        pass

def run_game():
    hitboxes = ASSET_HITBOXES.copy()
    running = True
    map_offset = [0, 0]
    char_direction = 0

    while running:
        clock.tick(FPS)

        assets = ORIG_ASSETS.copy()
        keys_pressed = check_keys()

        map_offset, char_direction = alter_offset(map_offset, char_direction, keys_pressed)
        


        

        hitboxes = move_all_assets(assets, hitboxes, map_offset)

        if keys_pressed[pygame.K_ESCAPE]:
            running = False

        pygame.display.update()

def main():
    pygame.display.set_caption("My Personal Project")
    
    run_game()

    pygame.quit()

main()