import json
import os
from typing import List, Dict, cast

import script.context as ctx
from script.note import Note
from script.scene import *
from script.song import Song
from script.text import TextRender, color_type

lane_y = ctx.height - 200
note_speed = 10


def draw_gradient(image: pygame.Surface, rect: pygame.rect.Rect,
                  top_color: color_type, bottom_color: color_type):
    color_image = pygame.Surface((2, 2)).convert_alpha()
    pygame.draw.line(color_image, top_color, (0, 0), (1, 0))
    pygame.draw.line(color_image, bottom_color, (0, 1), (1, 1))
    color_image = pygame.transform.smoothscale(color_image, (rect.width, rect.height))
    image.blit(color_image, color_image.get_rect())


class Play(Scene):
    def __init__(self, screen: pygame.Surface, song: Song):
        super().__init__(screen)
        self.song = song
        self.render = TextRender(screen, size=100)
        with open(os.path.join(song.folder, "sheet.json"), "r") as f:
            self.sheet: List[Dict[str, float]] = json.load(f)
        self.counter = 0
        self.note_count = 0
        self.remaining = -1
        self.pause = False
        self.note_group = pygame.sprite.Group()
        self.judgement = ""
        self.judgement_time = 0

    def get_event(self) -> Optional[callback]:
        from script.scene.select import Select
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return End, ()
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                self.pause = not self.pause
                return Select, ()
            if event.key in ctx.key_setting and not self.pause:
                lane = ctx.key_setting.index(event.key) + 1
                self.lane_input(lane)

    def lane_input(self, lane: int):
        from script.note import Judgement
        sprites = cast(List[Note], self.note_group.sprites())
        lane_notes = [sprite for sprite in sprites if sprite.lane == lane]
        if not lane_notes:
            return
        nearest_note = min(lane_notes)
        judgement = nearest_note.judgement(lane_y)
        if judgement == Judgement.far:
            return
        if judgement == Judgement.miss and nearest_note.rect.y > lane_y:
            return
        self.judgement = judgement.name
        self.judgement_time = 40
        nearest_note.kill()

    def draw_keybeam(self):
        keys = pygame.key.get_pressed()
        for i, key in enumerate(ctx.key_setting):
            if not keys[key]:
                continue
            image = pygame.Surface((100, lane_y)).convert_alpha()
            rect = image.get_rect(topleft=(ctx.width // 2 + (i - 2) * 100, 0))
            draw_gradient(image, rect, (0, 0, 0, 0), (0, 0, 63, 255))
            self.screen.blit(image, rect)

    def draw_judgement(self):
        if self.judgement_time == 0:
            return
        alpha = self.judgement_time / 20 if self.judgement_time <= 20 else 1
        self.render(self.judgement, (ctx.width // 2, ctx.height // 2), int(alpha * 255))
        self.judgement_time -= 1

    def make_note(self):
        self.counter += 1
        while True:
            if self.note_count >= len(self.sheet):
                self.remaining = 180
                return
            note = self.sheet[self.note_count]
            if note["time"] > self.counter:
                break
            x = int((note["lane"] - 2.5) * 100 + ctx.width // 2)
            y = int(lane_y - (note_speed * 100) + (note["time"] % 1) * note_speed)
            Note(self.note_group, (x, y), int(note["lane"]), note_speed)
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
            pass  # ends the song
        if self.remaining > 0:
            self.remaining -= 1

        pygame.draw.line(self.screen, (255, 255, 255), (0, lane_y), (ctx.width, lane_y), width=2)

        self.draw_keybeam()

        self.note_group.update()
        self.note_group.draw(self.screen)

        self.draw_judgement()
