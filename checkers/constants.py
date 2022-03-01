#pokud je treba zmenit nejakou konstantu, udelame to tady


import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

CROWN = pygame.transform.scale(pygame.image.load('/home/kate/dev/Checkers/checkers/assets/crown.png'), (44, 25))