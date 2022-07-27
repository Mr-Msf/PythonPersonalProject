import pygame
import assetList, loadAssets, alterAsset

FPS = 20
MAP_DIM_MULT = 28
HUD_PERCENTAGE = 0.2
MOVE_SPEED = 15

BLACK = (0,0,0)

current_direction = 0

ASSET_INFO = assetList.retrieve_info()
ASSET_NAMES = assetList.retrieve_names()
ORIG_ASSETS = loadAssets.load_assets(ASSET_INFO)

clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

WIDTH, HEIGHT = WINDOW.get_size()
WIDTH_HALF, HEIGHT_HALF = int(WIDTH/2), int(HEIGHT/2)

HUD_HEIGHT = int(HEIGHT*HUD_PERCENTAGE)

def get_centered_coords(asset):
    asset_width_half = int(alterAsset.get_dimensions(asset)[0]/2)
    asset_height_half = int(alterAsset.get_dimensions(asset)[1]/2)

    return (WIDTH_HALF-asset_width_half, HEIGHT_HALF-asset_height_half)

def move_map(assets, map_offset, keys_pressed):
    direction = 0

    if "UP" in keys_pressed:
        map_offset[1] += MOVE_SPEED
    if "DOWN" in keys_pressed:
        direction = 180
        map_offset[1] -= MOVE_SPEED
    if "LEFT" in keys_pressed:
        direction = 90
        map_offset[0] += MOVE_SPEED
    if "RIGHT" in keys_pressed:
        direction = 270
        map_offset[0] -= MOVE_SPEED

    assets[1] = alterAsset.rotate_asset(ORIG_ASSETS[1], direction)

    return assets, map_offset

def blit_asset(asset, index, map_offset):
    centered_coords = get_centered_coords(asset)
    asset_offset = ASSET_INFO[ASSET_NAMES[index]][0]
    coordinates = (centered_coords[0]+map_offset[0]+asset_offset[0], centered_coords[1]+map_offset[1]+asset_offset[1])
    WINDOW.blit(asset, coordinates)

def display_all_assets(assets, map_offset):
    WINDOW.fill(BLACK)
    for index, asset in enumerate(assets):
        blit_asset(asset, index, map_offset)
    
    # pygame.draw.rect(WINDOW, BLACK, (0,HEIGHT-HUD_HEIGHT,WIDTH,HUD_HEIGHT))

print

def check_keys():
    key_info = pygame.key.get_pressed()
    keys_pressed = []
        
    for event in pygame.event.get():
        pass
    
    if key_info[pygame.K_ESCAPE]:
        keys_pressed.append("ESC")
    if key_info[pygame.K_UP]:
        keys_pressed.append("UP")
    if key_info[pygame.K_DOWN]:
        keys_pressed.append("DOWN")
    if key_info[pygame.K_LEFT]:
        keys_pressed.append("LEFT")
    if key_info[pygame.K_RIGHT]:
        keys_pressed.append("RIGHT")

    return keys_pressed

def get_hixbox(asset):
    dimensions = alterAsset.get_dimensions(asset[0])
    hitbox = pygame.Rect(asset[1], dimensions)
    return hitbox


def function():
    for rect in hitbox_list:
        pass


def run_game():
    running = True
    
    map_offset = [0, 0]

    while running:
        clock.tick(FPS)

        assets = ORIG_ASSETS.copy()

        keys_pressed = check_keys()

        assets, map_offset = move_map(assets, map_offset, keys_pressed)

        display_all_assets(assets, map_offset)

        if "ESC" in keys_pressed:
            running = False

        pygame.display.update()

def main():
    pygame.display.set_caption("My Personal Project")
    
    run_game()

    pygame.quit()

main()