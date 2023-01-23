import pygame
from scene import Scene, End
from title import Title

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

scene: Scene = Title(screen)
while True:
    result = scene.run()
    if result is not None:
        if result[0] == End:
            pygame.quit()
            break
        scene = result[0](screen, *result[1])
