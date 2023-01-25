from enum import Enum

import script.context as ctx
from script.scene import *
from script.text import TextRender


class Option(Enum):
    music = "Music Volume"
    sfx = "SFX Volume"
    title = "Return to Title"


class Setting(Scene):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.options = [Option.music, Option.sfx, Option.title]
        self.selection = 0
        self.render = TextRender(screen, size=52)

    def get_event(self) -> Optional[callback]:
        key_data = {pygame.K_UP: -1, pygame.K_DOWN: 1}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return End, ()
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                return End, ()
            if event.key in key_data:
                self.selection += key_data[event.key]
                self.selection %= len(self.options)
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                option = self.options[self.selection]
                value = 10 if event.key == pygame.K_RIGHT else -10
                if option == Option.music:
                    ctx.music_volume += value
                    ctx.music_volume = max(0, min(100, ctx.music_volume))
                if option == Option.sfx:
                    ctx.sfx_volume += value
                    ctx.sfx_volume = max(0, min(100, ctx.sfx_volume))
                print(f"{ctx.music_volume = }, {ctx.sfx_volume = }")
            if event.key == pygame.K_RETURN:
                option = self.options[self.selection]
                if option == Option.title:
                    from script.scene.title import Title
                    return Title, (True,)

    def run(self) -> Optional[callback]:
        result = self.get_event()
        if result is not None:
            return result
        for i, option in enumerate(self.options):
            x = ctx.width // 2
            y = ctx.height // 2 + (i - 1) * 100
            color = (255, 255, 63) if i == self.selection else (255, 255, 255)
            anchor = "center" if option == Option.title else "midright"
            self.render(option.value, (x, y), color=color, anchor=anchor)
            if option == Option.music:
                self.render(str(ctx.music_volume), (ctx.width * 3 // 4, y), color=color)
            if option == Option.sfx:
                self.render(str(ctx.sfx_volume), (ctx.width * 3 // 4, y), color=color)
        return
