from typing import Optional, Tuple, Any, Type

import pygame

scene_class = Type["Scene"]
callback = Tuple[scene_class, Tuple[Any, ...]]


class Scene:
    def __init__(self, screen: pygame.Surface, *args):
        self.screen = screen

    def get_event(self) -> Optional[callback]:
        pass

    def run(self) -> Optional[callback]:
        self.get_event()
        return


class End(Scene):
    pass
