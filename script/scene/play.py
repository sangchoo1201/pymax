import json
import os
from typing import List, Dict

from script.note import Note
from script.scene import *
from script.song import Song
from script.text import TextRender


class Play(Scene):
    def __init__(self, screen: pygame.Surface, song: Song):
        super().__init__(screen)
        self.song = song
        self.render = TextRender(screen, size=52)
        with open(os.path.join(song.folder, "sheet.json"), "r") as f:
            self.sheet: List[Dict[str, int]] = json.load(f)
        self.counter = -120
        self.note_count = 0
        self.remaining = -1
        self.pause = False
        self.note_group = pygame.sprite.Group()

    def get_event(self) -> Optional[callback]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return End, ()
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                self.pause = not self.pause

    def make_note(self):
        self.counter += 1
        while True:
            if self.note_count >= len(self.sheet):
                self.remaining = 120
                return
            note = self.sheet[self.note_count]
            if note["time"] != self.counter:
                break
            print(note["lane"])  # make note
            x = int((note["lane"] - 2.5) * 50 + ctx.width // 2)
            Note(self.note_group, (x, -20))
            self.note_count += 1

    def run(self) -> Optional[callback]:
        result = self.get_event()
        if result is not None:
            return result
        if self.pause:
            self.render("GAME PAUSED", (ctx.width // 2, ctx.height // 2))
            return
        if self.remaining < 0:
            self.make_note()
        if self.remaining == 0:
            return End, ()
        if self.remaining > 0:
            self.remaining -= 1
            print(self.remaining)

        self.note_group.update()
        self.note_group.draw(self.screen)
