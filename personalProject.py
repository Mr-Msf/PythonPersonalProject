import pygame
import os

FPS = 20
MAP_DIM_MULT = 28

clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

WIDTH, HEIGHT = WINDOW.get_size()
WIDTH_HALF, HEIGHT_HALF = int(WIDTH/2), int(HEIGHT/2)

def get_dimensions(asset):
    return(asset.get_width(), asset.get_height())

def get_centered_coords(asset):
    asset_width_half = int(get_dimensions(asset)[0]/2)
    asset_height_half = int(get_dimensions(asset)[1]/2)
    return (WIDTH_HALF-asset_width_half, HEIGHT_HALF-asset_height_half)

def get_filepath(asset_name, is_picture=True):
    if is_picture:
        return os.path.join("Assets", "Sprite-" + asset_name + ".png")
    else:
        pass

def prepare_file(asset_name, scale_factor=0, rotation_factor=0):
    asset = pygame.image.load(get_filepath(asset_name))
    new_lengths = (get_dimensions(asset)[0]*scale_factor, get_dimensions(asset)[1]*scale_factor)
    asset = pygame.transform.scale(asset, new_lengths)

    return asset

def run_game():
    running = True
    map_offset_x, map_offset_y = 0, 0

    while running:
        
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys_pressed = pygame.key.get_pressed()
        
        if keys_pressed[pygame.K_ESCAPE]:
            running = False
        if keys_pressed[pygame.K_UP]:
            map_offset_y += 15
        if keys_pressed[pygame.K_DOWN]:
            map_offset_y -= 15
        if keys_pressed[pygame.K_RIGHT]:
            map_offset_x -= 15
        if keys_pressed[pygame.K_LEFT]:
            map_offset_x += 15
        
        map_coords = (MAP_CENTER_COORDS[0]+map_offset_x, MAP_CENTER_COORDS[1]+map_offset_y)
        WINDOW.fill((0,0,0))
        WINDOW.blit(MAP, map_coords)
        WINDOW.blit(IMAGE, get_centered_coords(IMAGE))

        pygame.display.update()

def main():
    global MAP, IMAGE, MAP_CENTER_COORDS

    MAP = prepare_file("Map(v0.1)", MAP_DIM_MULT)
    IMAGE = prepare_file("0001", 10)
    MAP_CENTER_COORDS = get_centered_coords(MAP)
    
    pygame.display.set_caption("My Personal Project")
    run_game()
    pygame.quit()

main()