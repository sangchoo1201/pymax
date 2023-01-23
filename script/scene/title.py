from script.scene import *
from script.text import TextRender
import script.context as ctx


class Title(Scene):
    def __init__(self, screen: pygame.Surface, begin: Optional[bool] = False):
        from script.scene.setting import Settings
        from script.scene.select import Select

        super().__init__(screen)
        self.options = ["Play", "Settings", "Quit"]
        self.callbacks = [(Select, ()), (Settings, ()), (End, ())]
        self.selection = 0
        self.begin = begin
        self.render = TextRender(screen, size=52)

    def get_event(self) -> Optional[callback]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return End, ()
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                return End, ()
            if not self.begin:
                self.begin = True
                continue
            if event.key == pygame.K_UP:
                self.selection -= 1
                self.selection %= len(self.options)
            if event.key == pygame.K_DOWN:
                self.selection += 1
                self.selection %= len(self.options)
            if event.key == pygame.K_RETURN:
                return self.callbacks[self.selection]

    def run(self) -> Optional[callback]:
        result = self.get_event()
        if result is not None:
            return result
        if not self.begin:
            center = (ctx.width // 2, ctx.height // 2)
            self.render("아무 키나 눌러서 시작", center)
            return
        for i, option in enumerate(self.options):
            center = (ctx.width // 2, ctx.height // 2 + i * 100)
            color = (255, 255, 63) if i == self.selection else (255, 255, 255)
            self.render(option, center, color=color)
        return
