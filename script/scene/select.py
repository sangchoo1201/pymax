import json
import os
from dataclasses import dataclass
from typing import List

from script.scene import *
from script.text import TextRender


@dataclass
class Song:
    title: str
    artist: str
    file: str
    preview: str
    bpm: float
    length: float
    vocal: Optional[str] = ""

    def make_image(self) -> pygame.Surface:
        image = pygame.Surface((402, 122))
        image.fill((0, 0, 0))
        rect = image.get_rect()
        render = TextRender(image)

        pygame.draw.rect(image, (255, 255, 255), rect, width=2)
        render(self.title, (20, 20), anchor="topleft")
        render(self.artist, (20, 102), anchor="bottomleft", size=18)

        return image


def get_songs() -> List[Song]:
    li = []
    for folder in (f for f in os.listdir("song") if not os.path.isfile(os.path.join("song", f))):
        folder = os.path.join("song", folder)
        if "data.json" not in os.listdir(folder):
            continue
        with open(os.path.join(folder, "data.json"), "r") as f:
            data = json.load(f)
        song = Song(**data)
        song.file = os.path.join(folder, song.file)
        song.preview = os.path.join(folder, song.preview)
        li.append(song)
    return li


class Select(Scene):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.song_list = get_songs()
        self.song_list.sort(key=lambda x: x.title)
        self.selection = 0

    def get_event(self) -> Optional[callback]:
        key_data = {
            pygame.K_UP: -1, pygame.K_DOWN: 1,
            pygame.K_PAGEUP: -5, pygame.K_PAGEDOWN: 5
        }
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return End, ()
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                from script.scene.title import Title
                return Title, (True,)
            if event.key in key_data:
                self.selection += key_data[event.key]
                self.selection %= len(self.song_list)

    def run(self) -> Optional[callback]:
        result = self.get_event()
        if result is not None:
            return result
        visible_list = [self.song_list[(self.selection + i) % len(self.song_list)] for i in range(-2, 3)]
        for i, song in enumerate(visible_list):
            x = ctx.width + abs(i - 2) * 20 + 2
            y = ctx.height // 2 + (i - 2) * 120
            image = song.make_image()
            rect = image.get_rect(midright=(x, y))
            self.screen.blit(image, rect)
        return
