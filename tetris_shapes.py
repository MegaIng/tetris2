from __future__ import annotations

from dataclasses import dataclass
from pprint import pprint


def _rot90(s: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(s[j][i] for j in reversed(range(len(s)))) for i in range(len(s[0]))
    )


@dataclass(frozen=True)
class Shape:
    name: str
    blocks: tuple[tuple[tuple[int, ...], ...], ...]

    @classmethod
    def auto_rotate(cls, name: str, base: tuple[tuple[int, ...], ...]) -> Shape:
        rots = [base]
        for i in range(3):
            rots.append(_rot90(rots[-1]))
        return cls(name, tuple(rots))


SHAPES: tuple[Shape, ...] = (
    Shape.auto_rotate("I", (
        (0, 0, 1, 0, 0),
        (0, 0, 1, 0, 0),
        (0, 0, 1, 0, 0),
        (0, 0, 1, 0, 0),
        (0, 0, 0, 0, 0),
    )), Shape.auto_rotate("O", (
        (1, 1),
        (1, 1),
    )), Shape.auto_rotate("S", (
        (0, 1, 1),
        (1, 1, 0),
        (0, 0, 0)
    )), Shape.auto_rotate("Z", (
        (1, 1, 0),
        (0, 1, 1),
        (0, 0, 0)
    )), Shape.auto_rotate("L", (
        (0, 1, 0),
        (0, 1, 0),
        (0, 1, 1)
    )), Shape.auto_rotate("J", (
        (0, 1, 0),
        (0, 1, 0),
        (1, 1, 0)
    )), Shape.auto_rotate("T", (
        (0, 1, 0),
        (1, 1, 1),
        (0, 0, 0)
    ))
)


def _show_shapes(args):
    import pygame as pg
    from utils import text

    W, H = 600, 480
    BLOCK_SIZE = 60
    BLOCK_START = (BLOCK_SIZE*5//2, H-BLOCK_SIZE*3//2)

    pg.init()

    screen = pg.display.set_mode((W, H))
    clock = pg.time.Clock()
    font = pg.font.SysFont("arial", 30)

    shape_id = 0
    rotate_id = 0

    running = True
    while running:
        dt = clock.tick()
        # EVENTS
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_UP:
                    shape_id = (shape_id - 1) % len(SHAPES)
                elif event.key == pg.K_DOWN:
                    shape_id = (shape_id + 1) % len(SHAPES)
                elif event.key == pg.K_LEFT:
                    rotate_id = (rotate_id + 1) % 4
                elif event.key == pg.K_RIGHT:
                    rotate_id = (rotate_id - 1) % 4

        # LOGIC

        # RENDERING
        screen.fill((0, 0, 0))
        shape = SHAPES[shape_id]
        text(screen, font, (255, 255, 255), [
            f"Shape: {shape_id}=>{shape.name!r}",
            f"Rotation: {rotate_id}"
        ])

        for i, r in enumerate(shape.blocks[rotate_id]):
            y = BLOCK_START[1] - (i+1) * BLOCK_SIZE
            for j, v in enumerate(r):
                x = BLOCK_START[0] + j * BLOCK_SIZE
                if v:
                    print(x,y)
                    screen.fill((255, 0, 0), (x + 1, y + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2))

        pg.display.update()


if __name__ == '__main__':
    import sys

    _show_shapes(sys.argv)
