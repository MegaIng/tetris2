from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from tetris_shapes import SHAPES


@dataclass
class Piece:
    x: int
    y: int
    rotation: int
    shape_id: int
    color: int

    @property
    def blocks(self) -> list[list[int]]:
        return [
            [self.color if v else 0 for v in r]
            for r in SHAPES[self.shape_id].blocks
        ]


@dataclass
class TetrisBoard:
    fixed_blocks: list[list[int]]
    current_piece: Optional[Piece]

    @property
    def height(self):
        return len(self.fixed_blocks)

    @property
    def width(self):
        return len(self.fixed_blocks[0])

    @classmethod
    def create(cls, width: int = 10, height: int = 24) -> TetrisBoard:
        return cls([[0] * width for _ in range(height)], None)

    @property
    def blocks(self):
        if self.current_piece is None:
            return self.fixed_blocks
        out = self.fixed_blocks.copy()
        pb = self.current_piece.blocks
        for j, r in enumerate(pb, start=self.current_piece.y):
            out[j] = out[j].copy()
            for i, v in enumerate(r, start=self.current_piece.x):
                out[j][i] = v
        return out

    def fixate_piece(self):
        assert self.current_piece is not None
        self.fixed_blocks = self.blocks
        self.current_piece = None

    def piece_collides(self) -> bool:
        pb = self.current_piece.blocks
        for j, r in enumerate(pb, start=self.current_piece.y):
            for i, v in enumerate(r, start=self.current_piece.x):
                if v and self.fixed_blocks[j][i]:
                    return True
        return False

    def try_move_x(self, dx: int):
        self.current_piece.x += dx
        while self.piece_collides():
            self.current_piece.x += -1 if dx > 0 else 1

    def try_move_y(self, dy: int):
        self.current_piece.y += dy
        while self.piece_collides():
            self.current_piece.y += -1 if dy > 0 else 1

    def try_rotate(self, dr: int):
        self.current_piece.rotation += dr
        self.current_piece.rotation %= 4
        if not self.piece_collides():
            return

        self.current_piece.x -= 1
        if not self.piece_collides():
            return

        self.current_piece.x += 2
        if not self.piece_collides():
            return
        
        self.current_piece.x -= 1
        self.current_piece.rotation += dr
        self.current_piece.rotation %= 4
