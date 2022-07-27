import pygame
import os

ORIG_IMAGE = [pygame.image.load(os.path.join("Assets", "Sprite-" + "CharSword1" + ".png"))]

WINDOW = pygame.display.set_mode((500, 500))

running = True

coords = (250,250)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    direction = 0

    key_info = pygame.key.get_pressed()

    if key_info[pygame.K_UP]:
        direction = 0
    if key_info[pygame.K_DOWN]:
        direction = 90
    if key_info[pygame.K_LEFT]:
        direction = 270
    if key_info[pygame.K_RIGHT]:
        direction = 180

    WINDOW.fill((50,121,228))

    image = pygame.transform.rotate(ORIG_IMAGE[0], direction)

    WINDOW.blit(image, tuple(coords))
    pygame.display.update()

pygame.quit()