from scene import *


class Title(Scene):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        from setting import Settings
        from select import Select
        self.options = ["Play", "Settings", "Quit"]
        self.callbacks = [(Select, ()), (Settings, ()), (End, ())]
        self.selection = 0

    def get_event(self) -> Optional[callback]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return End, ()
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                return End, ()
            if event.key == pygame.K_UP:
                self.selection = max(0, self.selection - 1)
            if event.key == pygame.K_DOWN:
                self.selection = min(len(self.options) - 1, self.selection + 1)
            if event.key == pygame.K_RETURN:
                return self.callbacks[self.selection]

    def run(self) -> Optional[callback]:
        result = self.get_event()
        if result is not None:
            return result
        return
