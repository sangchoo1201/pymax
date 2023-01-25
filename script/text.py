from typing import Optional, Union, Tuple

import pygame

position_type = Union[pygame.math.Vector2, Tuple[int, int]]
color_type = Union[pygame.color.Color, Tuple[int, int, int], Tuple[int, int, int, int]]


class TextRender:
    def __init__(self, screen: pygame.Surface, size: Optional[int] = 24,
                 color: Optional[color_type] = pygame.color.Color(255, 255, 255),
                 font: Optional[str] = "D2Coding.ttf"):
        self.screen = screen
        self.size = size
        self.color = color
        self.font = font

    def __call__(self, text: str, pos: position_type, alpha: Optional[int] = None,
                 size: Optional[int] = None, color: Optional[color_type] = None,
                 font: Optional[str] = None, anchor: Optional[str] = "center"):
        if size is None:
            size = self.size
        if color is None:
            color = self.color
        if font is None:
            font = self.font

        pos = pygame.math.Vector2(pos)
        color = pygame.color.Color(color)

        text_font = pygame.font.Font(f"resource/font/{font}", size)
        text_image = text_font.render(text, True, color).convert_alpha()
        if alpha is not None:
            text_image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        text_rect = text_image.get_rect(**{anchor: pos})
        self.screen.blit(text_image, text_rect)
