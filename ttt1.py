import random
WIDTH = 600
HEIGHT = 600

ROWS = 3 #rows of the grid
COLS = 3 #cols of the grid

SQUARE_SIZE = WIDTH // COLS #size of one square of the grid - can be height devided by rows
LINE_WIDTH = 15 #width of the lines of the grid

#circle
CIRCLE_WIDTH = 20
RADIUS = SQUARE_SIZE // 3

#cross
CROSS_WIDTH = 20

OFFSET = 50

#define colors
BACKCOLOR = ((random.randint(0,255)), (random.randint(0, 255)), (random.randint(0,255)))
LINE_COLOR = ((random.randint(0,255)), (random.randint(0, 255)), (random.randint(0,255)))
CIRCLE = ((random.randint(0,255)), (random.randint(0, 255)), (random.randint(0,255)))
CROSS = ((random.randint(0,255)), (random.randint(0, 255)), (random.randint(0,255)))