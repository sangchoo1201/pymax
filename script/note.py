import pygame
from typing import Tuple
import script.context as ctx
from enum import Enum


class Judgement(Enum):
    perfect = 0
    great = 1
    good = 2
    miss = 3
    far = 4


class Note(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, pos: Tuple[int, int], lane: int, speed: int):
        super().__init__(group)
        self.image = pygame.Surface((100, 40))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=pos)
        self.lane = lane
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > ctx.height:
            self.kill()

    def __lt__(self, other: "Note") -> bool:
        return self.rect.y > other.rect.y

    def judgement(self, lane_y: int) -> Judgement:
        diff = abs(self.rect.centery - lane_y) // self.speed
        if -2 <= diff <= 2:
            return Judgement.perfect
        elif -4 <= diff <= 4:
            return Judgement.great
        elif -7 <= diff <= 7:
            return Judgement.good
        elif -15 <= diff <= 15:
            return Judgement.miss
        else:
            return Judgement.far
