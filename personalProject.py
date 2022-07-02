import pygame
import os

WIDTH, HEIGHT = 1440, 780
WIDTH_HALF, HEIGHT_HALF = int(WIDTH/2), int(HEIGHT/2)

MAP_DIM_ORIG, MAP_DIM_MULT = 256, 28
MAP_DIM = MAP_DIM_ORIG * MAP_DIM_MULT
MAP_DIM_HALF = int(MAP_DIM/2)
MAP_CENTER_COORDS = (WIDTH_HALF-MAP_DIM_HALF, HEIGHT_HALF-MAP_DIM_HALF)

FPS = 144

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

print(MAP_DIM_HALF)

print(pygame.display.list_modes())

def main():
    MAP = pygame.image.load(join_path("Map(v0.1)"))
    MAP = pygame.transform.scale(MAP, (MAP_DIM, MAP_DIM))
    map_offset_x, map_offset_y = 0, 0

    clock = pygame.time.Clock()
    pygame.display.set_caption("My Personal Project")

    running = True

    while running:
        
        clock.tick(FPS)

        for event in pygame.event.get():
           
            if event.type == pygame.QUIT:
                running = False

        keys_pressed = pygame.key.get_pressed()
        
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

        pygame.display.update()

    pygame.quit()

def join_path(asset_name):
    return os.path.join("Assets", "Sprite-" + asset_name + ".png")

main()