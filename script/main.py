import pygame

import script.context as ctx
from script.scene import Scene, End
from script.scene.title import Title

pygame.init()
screen = pygame.display.set_mode((ctx.width, ctx.height), pygame.FULLSCREEN)
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
