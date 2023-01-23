from typing import Optional, Tuple, Any, Type

import pygame

scene_class = Type["Scene"]
callback = Tuple[scene_class, Tuple[Any, ...]]


class Scene:
    def __init__(self, screen: pygame.Surface, *args):
        self.screen = screen

    def get_event(self) -> Optional[callback]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return End, ()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return End, ()

    def run(self) -> Optional[callback]:
        return self.get_event()


class End(Scene):
    pass
