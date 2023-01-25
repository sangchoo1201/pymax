import json
import os
from typing import List

import script.context as ctx
from script.scene import *
from script.song import Song


def get_songs() -> List[Song]:
    li = []
    for folder in (f for f in os.listdir("song") if not os.path.isfile(os.path.join("song", f))):
        folder = os.path.join("song", folder)
        if not os.path.exists(os.path.join(folder, "data.json")):
            continue
        with open(os.path.join(folder, "data.json"), "r") as f:
            data = json.load(f)
        data["folder"] = folder
        song = Song(**data)
        li.append(song)
    return li


class Select(Scene):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.song_list = get_songs()
        self.song_list.sort(key=lambda x: x.title)
        self.selection = 0

    def get_event(self) -> Optional[callback]:
        from script.scene.play import Play
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
            if event.key == pygame.K_RETURN:
                return Play, (self.song_list[self.selection],)

    def run(self) -> Optional[callback]:
        result = self.get_event()
        if result is not None:
            return result
        visible_list = [self.song_list[(self.selection + i) % len(self.song_list)] for i in range(-2, 3)]
        for i, song in enumerate(visible_list):
            x = ctx.width + abs(i - 2) * 50 + 2
            y = ctx.height // 2 + (i - 2) * 216
            image = song.make_image()
            rect = image.get_rect(midright=(x, y))
            self.screen.blit(image, rect)
        return
