import pygame
from collections import deque

# initialize font
pygame.font.init()

# screen size
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1000

# screen setup
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BFS Visualizer")

# color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (80, 80, 80)
PURPLE = (76, 0, 153)
ORANGE = (255, 128, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 255, 255)
MAGENTA = (255, 0, 255)

# setup frame rate
FPS = 60
clock = pygame.time.Clock()

# grid variables
ROW = COL = 25

# font setup
#font = pygame.font.SysFont("Comic Sans")

class Spot:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.isStart = False
        self.isEnd = False

    def make_start(self):
        self.color = PURPLE

    def make_end(self):
        self.color = ORANGE

    def make_border(self):
        self.color = GREY

    def make_visited(self):
        self.color = BLUE

    def make_visiting(self):
        self.color = LIGHT_BLUE

    def make_path(self):
        self.color = MAGENTA

    def resetColor(self):
        self.color = WHITE

    def drawSpot(self, screen, x, y, width, height, color):
        pygame.draw.rect(screen, color, (x, y, width, height), width=0)  # fill the spot


# bfs implementation
def BFS(queue, row, col, grid):
    foundEnd = False
    while queue:
        if foundEnd:
            break

        x, y, curPath = queue.popleft()
        spot = grid[x][y]

        # if spot is not a starting spot, make it visited
        if not spot.isStart:
            spot.make_visited()
            spot.drawSpot(SCREEN, spot.x, spot.y, spot.width, spot.height, spot.color)

        for nx, ny in [[x+1,y], [x-1,y], [x,y+1], [x,y-1]]:
            if 0<=nx<col and 0<=ny<row and (nx,ny) not in curPath:
                newSpot = grid[nx][ny]

                if newSpot.color == WHITE: # make it the currently visiting spot
                    newSpot.make_visiting()
                    newSpot.drawSpot(SCREEN, newSpot.x, newSpot.y, newSpot.width, newSpot.height, newSpot.color)
                    queue.append((nx,ny,curPath | {(nx,ny)}))

                elif newSpot.isEnd:
                    for (col, row) in curPath:
                        curSpot = grid[col][row]
                        if curSpot.isStart is not True:
                            curSpot.make_path()
                            curSpot.drawSpot(SCREEN, curSpot.x, curSpot.y, curSpot.width, curSpot.height, curSpot.color)

                        foundEnd = True

# function to get clicking position of the mouse
def get_clicked_pos(screenWidth, screenHeight, col, row):
    # get coordinates of the mouse
    x_pos, y_pos = pygame.mouse.get_pos()

    # get the spot width and height
    spotWidth = screenWidth / col
    spotHeight = screenHeight / row

    # calculate the index of row and column for the grid
    x = x_pos // spotWidth
    y = y_pos // spotHeight

    return int(x), int(y)

# function to build the grid in a 2D array
def createGrid(row, col, screenWidth, screenHeight):
    grid = []
    y_pos = 0
    x_pos = 0

    spotWidth = screenWidth / col
    spotHeight = screenHeight / row

    for y in range(row):
        temp_list = []
        for x in range(col):
            spot = Spot(x_pos, y_pos, spotWidth, spotHeight, WHITE)
            temp_list.append(spot)
            x_pos = x_pos + spotWidth

        grid.append(temp_list)
        y_pos = y_pos + spotHeight
        x_pos = 0

    return grid

# function to draw the lines for the grid
def drawLines(screen, screenWidth, screenHeight, row, col):
    count_x = 0
    count_y = 0

    spotWidth = screenWidth / col
    spotHeight = screenHeight / row

    # draw horizontal lines
    for _ in range(row):
        pygame.draw.line(screen, BLACK, (0, count_y), (screenWidth, count_y), width=1)
        count_y += spotHeight

    # draw vertical lines
    for _ in range(col):
        pygame.draw.line(screen, BLACK, (count_x, 0), (count_x, screenHeight), width=1)
        count_x += spotWidth

# function to draw background
def drawBG(screen):
    screen.fill(WHITE)

# main game loop
def main():
    grid = createGrid(ROW, COL, SCREEN_WIDTH, SCREEN_HEIGHT)
    #print(grid)

    # main game loop variables
    Start = False
    End = False
    run = True
    queue = deque([])

    # draw background
    drawBG(SCREEN)

    while run:
        clock.tick(FPS)

        # draw lines
        drawLines(SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT, ROW, COL)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed(num_buttons=3)[0]: # left click
                row, col = get_clicked_pos(SCREEN_WIDTH, SCREEN_HEIGHT, ROW, COL)
                spot = grid[col][row]

                #print(spot.isStart, spot.isEnd)
                if Start == False: # make starting position
                    spot.make_start()
                    Start = True
                    spot.isStart = True
                    queue.append((col, row, set([(col, row)])))

                elif End == False and Start == True and not spot.isStart: # make ending position
                    spot.make_end()
                    End = True
                    spot.isEnd = True

                else: # make border
                    if spot.isStart:
                        spot.make_start()

                    elif spot.isEnd: # if the spot is CURRENTLY a start or end position
                        spot.make_end()

                    else:
                        spot.make_border()

                spot.drawSpot(SCREEN, spot.x, spot.y, spot.width, spot.height, spot.color)

            if pygame.mouse.get_pressed(num_buttons=3)[2]: # right click
                row, col = get_clicked_pos(SCREEN_WIDTH, SCREEN_HEIGHT, ROW, COL)
                spot = grid[col][row]

                if spot.isStart:
                    Start = False
                    spot.isStart = False

                elif spot.isEnd:
                    End = False
                    spot.isEnd = False

                spot.resetColor()
                spot.drawSpot(SCREEN, spot.x, spot.y, spot.width, spot.height, spot.color)

            keys_pressed = pygame.key.get_pressed()

            if keys_pressed[pygame.K_SPACE]: # reset the grid
                # redraw the background
                drawBG(SCREEN)
                drawLines(SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT, ROW, COL)

                # reset Start and End variables
                Start = False
                End = False

                # reset the queue and target
                queue = deque([])

                # reset the grid
                grid = createGrid(ROW, COL, SCREEN_WIDTH, SCREEN_HEIGHT)

            if keys_pressed[pygame.K_c]: # start BFS algorithm
                if Start and End: # if we have a start and end position
                    BFS(queue, ROW, COL, grid)

                    # reset the deque when the path is found
                    queue = deque([])

        pygame.display.update()

if __name__ == "__main__":
    main()