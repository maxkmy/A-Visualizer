import pygame 
import math
from queue import PriorityQueue

WIDTH = 650
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Path Finding Visualizer")

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (173,216,230)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQUOISE = (64,224,208)

class Node:
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def getPosition(self):
        return self.row, self.col

    def isClosed(self):
        return self.color == RED

    def isOpen(self):
        return self.color == GREEN

    def isBarrier(self):
        return self.color == BLACK

    def isStart(self):
        return self.color == ORANGE

    def isEnd(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def setClosed(self):
        self.color = RED

    def setOpen(self):
        self.color = GREEN

    def setBarrier(self):
        self.color = BLACK

    def setEnd(self):
        self.color = TURQUOISE

    def setStart(self):
        self.color = ORANGE 

    def setPath(self):
        self.color = PURPLE

    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))

    def addNeighbor(self,grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].isBarrier():  #down
            self.neighbors.append(grid[self.row+1][self.col])
            
        if self.row > 0 and not grid[self.row-1][self.col].isBarrier():  #up
            self.neighbors.append(grid[self.row-1][self.col])
            
        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].isBarrier():  #right 
            self.neighbors.append(grid[self.row][self.col+1])
            
        if self.col > 0 and not grid[self.row][self.col-1].isBarrier():  #left
            self.neighbors.append(grid[self.row][self.col-1])

def h(p1,p2):
    distance = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    return distance

def reconstructPath(predecessor,current,draw):
    while current in predecessor:
        current = predecessor[current]
        current.setPath()
        draw()

def algorithm(draw,grid,start,end):
    count = 0
    openSet = PriorityQueue()
    openSet.put((0,count,start))
    predecessor = {}
    g_score = {node: float("inf") for row in grid for node in row}
    f_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score[start] = h(start.getPosition(),end.getPosition())

    openSetHash = {start}

    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = openSet.get()[2]
        openSetHash.remove(current)

        #make path
        if current == end:
            end.setEnd()
            reconstructPath(predecessor,end,draw)
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1  #assume an unweighted graph
            if temp_g_score < g_score[neighbor]:
                g_score[neighbor] = temp_g_score
                predecessor[neighbor] = current
                f_score[neighbor] = temp_g_score + h(neighbor.getPosition(),end.getPosition())
                if neighbor not in openSetHash:
                    count += 1
                    openSet.put((f_score[neighbor],count,neighbor))
                    openSetHash.add(neighbor)
                    neighbor.setOpen()
        draw()

        if current != start:
            current.setClosed()

    return False 
            
def makeGrid(rows,width):
    grid = []
    gap = width // rows
    for i in range (rows):
        grid.append([])
        for j in range (rows):
            node = Node(i,j,gap,rows)
            grid[i].append(node)
            
    return grid

def drawGrid(win,rows,width):
    gap = width // rows
    for i in range (rows):
        pygame.draw.line(win,GREY,(0,i * gap),(width,i * gap))
        for j in range (rows):
            pygame.draw.line(win,GREY,(j * gap,0),(j*gap,width))

def draw(win,grid,rows,width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    drawGrid(win,rows,width)
    pygame.display.update()


def getClickedPosition(pos,rows,width):
    gap = width // rows
    y,x = pos

    row = y // gap
    col = x // gap

    return row, col

def main(win,width):
    ROWS = 50
    grid = makeGrid(ROWS,width)

    start = None
    end = None

    run = True
    
    while (run):
        draw(win,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  #left mouse
                pos = pygame.mouse.get_pos()
                row,col = getClickedPosition(pos,ROWS,width)
                node = grid[row][col]
                
                if not start and node != end:
                    start = node
                    start.setStart()

                elif not end and node != start:
                    end = node
                    end.setEnd()

                elif node != end and node != start:
                    node.setBarrier()

            elif pygame.mouse.get_pressed()[2]:  #right mouse
                pos = pygame.mouse.get_pos()
                row,col = getClickedPosition(pos,ROWS,width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None

                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.addNeighbor(grid)
                    algorithm(lambda: draw(win,grid,ROWS,width),grid,start,end)

                if event.key == pygame.K_c:
                    start = None
                    end = None 
                    grid = makeGrid(ROWS,width)
                            
    pygame.quit()

main(WIN,WIDTH)
