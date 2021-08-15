import pygame

from tetris_board import TetrisBoard

W, H = 640, 480

pygame.init()

screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

board = TetrisBoard.create()
BLOCK_SIZE = min(H // (board.height - 4), W // board.width)

running = True
while running:
    dt = clock.tick()
    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # LOGIC

    # RENDERING
    screen.fill((0, 0, 0))

    pygame.display.update()
