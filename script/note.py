import pygame
from typing import Tuple
import script.context as ctx


class Note(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, pos: Tuple[int, int]):
        super().__init__(group)
        self.image = pygame.Surface((50, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=pos)

    def update(self) -> None:
        self.rect.y += 20
        if self.rect.top > ctx.height:
            self.kill()
