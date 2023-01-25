from dataclasses import dataclass
from script.text import TextRender
from typing import Optional
import pygame


@dataclass
class Song:
    title: str
    artist: str
    folder: str
    file: str
    preview: str
    bpm: float
    length: float
    vocal: Optional[str] = ""

    def make_image(self) -> pygame.Surface:
        image = pygame.Surface((802, 218))
        image.fill((0, 0, 0))
        rect = image.get_rect()
        render = TextRender(image)

        pygame.draw.rect(image, (255, 255, 255), rect, width=2)
        render(self.title, (20, 20), anchor="topleft", size=80)
        render(self.artist, (20, 216), anchor="bottomleft", size=40)

        return image
