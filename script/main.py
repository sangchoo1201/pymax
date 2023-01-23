import pygame
from script.scene import Scene, End
from script.scene.title import Title
import script.context as ctx

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

scene: Scene = Title(screen)
while True:
    screen.fill((0, 0, 0))

    result = scene.run()
    if result is not None:
        if result[0] == End:
            pygame.quit()
            break
        scene = result[0](screen, *result[1])

    pygame.display.update()
    clock.tick(ctx.fps)
