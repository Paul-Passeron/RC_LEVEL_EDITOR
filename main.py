import pygame
from math import floor
import sys
from random import random

"""Structure of .rcmap files:

#HEADBEGIN
This is a comment describing the map
#HEADEND

#WBEGIN #:Walls
<float p1x> <float p1y> <float p2x> <float p2y> <int textureIdentifier>
#WEND

#IBEGIN #:Items
<flaot px> <float py> <float size> <int textureIdentifire>
#IEND

#PBEGIN #: Player
<float px> <float py>
#PEND
"""

#Global viariables

REG_STDOUT = sys.stdout

RES_X = 12
RES_Y = 12

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

GRID_COLOR  = (255/2, 255/2, 255/2)

LINE_RED = (255*0.7, 0, 0)


TEXTURE_IDS = list(range(9))

text_id = 2

wall_size = 1.0

SCALING_FACTOR = 2

def parse_list(lis, n=3):
    buffer = ""
    for i, w in enumerate(lis):
        for j, token in enumerate(w):
            if j > n:
                buffer += str(token) + " "
            else:
                buffer += str(SCALING_FACTOR*token) + " "
        if i < len(lis)-1:
            buffer+='\n'
    return buffer

def create_rcmap_from_lists(filename, head, wall_list, item_list, player):
    with open(filename, 'w') as f:
        sys.stdout = f
        if len(head) > 0:
            print("#HEADBEGIN")
            print(head)
            print("#HEADEND")
        if len(wall_list) > 0:
            print("#WBEGIN")
            print(parse_list(wall_list))
            print("#WEND")
        if len(item_list) > 0:
            print("#IBEGIN")
            print(parse_list(item_list))
            print("#IEND")
        print("#PBEGIN")
        print(str(player[0]) + " " + str(player[1]))
        print("#PEND")
        f.close()
    sys.stdout = REG_STDOUT

def draw_line(i1, j1, i2, j2, color = GRID_COLOR):
    x1 = SCREEN_WIDTH*i1/RES_X
    x2 = SCREEN_WIDTH*i2/RES_X
    y1 = SCREEN_HEIGHT*j1/RES_Y
    y2 = SCREEN_HEIGHT*j2/RES_Y
    pygame.draw.line(screen, color, (x1, y1), (x2, y2), 3)


def draw_grid():
    for x in range(RES_X):
        draw_line(x, 0, RES_X, 0)
    for y in range(RES_Y):
        draw_line(0, y, 0, RES_Y)
    for x in range(RES_X):
        for y in range(RES_Y):
            j = SCREEN_HEIGHT*y/RES_Y+1
            i = SCREEN_WIDTH*x/RES_X+1
            pygame.draw.circle(screen, GRID_COLOR, (i, j), 5)

def get_closest_grid_point_from_mouse():
    mouseX, mouseY = pygame.mouse.get_pos()
    x = floor((RES_X*(mouseX+SCREEN_WIDTH/RES_X/2))/SCREEN_WIDTH)
    y = floor((RES_Y*(mouseY+SCREEN_HEIGHT/RES_Y/2))/SCREEN_HEIGHT)
    return(x, y)


def get_screen_coords(coords):
    i, j = coords;
    return ((i*SCREEN_WIDTH/RES_X)+1, (j*SCREEN_HEIGHT/RES_Y)+1)

LINES = []

IS_DRAGGING = False
WAS_DRAGGING = False

CURRENT_LINE = []


pygame.init()
pygame.display.set_caption("Raycaster Level Editor")
screen = pygame.display.set_mode((600, 600))

done = False

while not done: #Program Loop

    #Drawing grid lines and dots
    draw_grid()

    #Higlighting closest grid point from mouse
    i, j = get_closest_grid_point_from_mouse()
    pygame.draw.circle(screen, (GRID_COLOR[0], 0, 0), get_screen_coords((i, j)), 5)

    #Handling dragging the mouse
    WAS_DRAGGING = IS_DRAGGING
    IS_DRAGGING = pygame.mouse.get_pressed()[0]

    if len(CURRENT_LINE) >= 4:
        CURRENT_LINE = []
    
    if IS_DRAGGING and len(CURRENT_LINE) == 0:
        CURRENT_LINE = [i, j]

    if not IS_DRAGGING and WAS_DRAGGING and len(CURRENT_LINE) == 2:
        CURRENT_LINE.append(i)
        CURRENT_LINE.append(j)
        CURRENT_LINE.append(1)
        CURRENT_LINE.append(text_id)
        LINES.append(CURRENT_LINE)

    #Drawing lines
    for (i1, j1, i2, j2, _, _) in LINES:
        draw_line(i1, j1, i2, j2, LINE_RED)

    #Handling quitting the window and outputting the .rcmap file when ENTER is rekeased.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER:
            create_rcmap_from_lists("test.rcmap", "", LINES, [], (0, 0))
            print("Map Saved!")

    #Updating the screen
    pygame.display.flip()

