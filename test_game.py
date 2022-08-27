# This test program draws houses using pygame

import pygame

WIDTH = 800
HEIGHT = 600

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hello World")

def main():
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        WINDOW.fill((50,121,228))

        pygame.draw.rect(WINDOW, (100, 204, 0), (0, 500, 800, 100))
        pygame.draw.rect(WINDOW, (255, 153, 51), (300, 350, 200, 200))
        pygame.draw.rect(WINDOW, (255, 204, 153), (50, 350, 200, 200))
        pygame.draw.rect(WINDOW, (255, 153, 153), (550, 350, 200, 200))
        pygame.draw.polygon(WINDOW, (0,0,153), [(275,350), (525,350), (400, 225)])
        pygame.draw.polygon(WINDOW, (0,0,153), [(25,350), (275,350), (150, 225)])
        pygame.draw.polygon(WINDOW, (0,0,153), [(525,350), (775,350), (650, 225)])
        pygame.draw.rect(WINDOW, (102, 51, 0), (375, 450, 50, 100))
        pygame.draw.rect(WINDOW, (102, 51, 0), (125, 450, 50, 100))
        pygame.draw.rect(WINDOW, (102, 51, 0), (625, 450, 50, 100))   
        
        pygame.display.update()

    pygame.quit()

main()