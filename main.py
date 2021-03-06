import pygame
import math
from queue import PriorityQueue

pygame.init()

WIDTH = 800
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinding Algorithm")

# Colors
RED = (255,0,0)
GREEN = (0,255,2)
BLUE = (1,1,230)
WHITE = (255,255,255)
YELLOW = (240,240,0)
BLACK =  (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQUOISE = (64, 224 ,208)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return  self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_start(self):
        self.color = ORANGE

    def make_path(self):
        self.color = PURPLE

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # Down
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0  and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # Right
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # Left
            self.neighbours.append(grid[self.row][self.col - 1])




    def __lt__(self, other):
        return False

def H(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    
    return grid

def draw_grid(screen, rows, width):
    gap  = width // rows
    for i in range(rows):
        pygame.draw.line(screen, GREY, (0, i*gap), (width, i*gap))
    for j in range(rows):
        pygame.draw.line(screen, GREY, (j* gap, 0), (j * gap, width))

def draw(screen, grid, rows, width):
    screen.fill(WHITE)
    
    for row in grid:
        for spot in row:
            spot.draw(screen)

    draw_grid(screen, rows, width)
    pygame.display.update()

def get_pos_clicked(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap

    return row, col

def reconstruct_path(parent, current, draw):
    while current in parent:
        current = parent[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    parent = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = H(start.get_pos(), end.get_pos())

    open_set_hash = {start}
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end: # Found path 
            reconstruct_path(parent, end, draw)
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                parent[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + H(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
            
        draw()

        if current != start:
            current.make_closed()

    path = False
    no_path()
    return path

def no_path():
    font = pygame.font.SysFont("Arial", 32)
    no_path = font.render("NO PATH FOUND", True, BLUE, GREY)
    rect = no_path.get_rect()
    rect.center = (300,400)
    screen.blit(no_path, rect)




def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None
    running = True
    started = False
    path = None

    while running:
        draw(screen, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
 
            if pygame.mouse.get_pressed()[0]: # Pressing left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_pos_clicked(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                
                elif spot != end and spot != start:
                    spot.make_barrier()
                
            elif pygame.mouse.get_pressed()[2]: # Presiing right mouse buttom
                pos = pygame.mouse.get_pos()
                row, col = get_pos_clicked(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)

                    path = algorithm(lambda: draw(screen, grid, ROWS, width), grid, start, end)
    
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)


    pygame.quit() 

main(screen, WIDTH)