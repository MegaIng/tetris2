from __future__ import annotations
import pygame as pg


def text(screen: pg.Surface, font: pg.font.Font, color, lines: list[str] | str, pos: tuple[int, int] = (0, 0)):
    if isinstance(lines, str):
        lines = lines.splitlines(False)
    for line in lines:
        img = font.render(line, True, color)
        rect = img.get_rect(topleft=pos)
        screen.blit(img, rect)
        pos = rect.bottomleft