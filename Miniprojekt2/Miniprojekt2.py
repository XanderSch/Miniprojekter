import pygame
import random
import numpy as np
import matplotlib.pyplot as plt
from queue import Queue
import heapq

# laver et tilfældigt array med x antal 0'er, alt efter hvor mange rows,cols der bliver valgt
def make_random_grid(rows, cols):
    grid = []
    for y in range(rows):
        row = []
        for x in range(cols):
            row.append(1 if random.random() < 1/10 else 0) #opdeler array i 1/5 1 taller hvor resten forbliver 0
        grid.append(row)
    return grid
# fortæller at hver enkelte firkant med (x,y) koordinat er 10x10 pixels
# i et grid med 2500 koordinater, er der 50 rækker og 50 kolonner
def get_grid_indices(x, y):
    row = y // 10 
    col = x // 10
    return row, col
# laver 2 firkanter, et start firkant og en slut firkant
def a_to_b(grid, rect_start, rect_end):
    if not rect_start: # laver en start firkant i koordinatet (10, 10)
        rect_x = 0 #random.randint(0, 10) * 10
        rect_y = 0 #random.randint(0, 10) * 10
        rect_start = (rect_x, rect_y)
        row, col = get_grid_indices(rect_x, rect_y)
        grid[row][col] = 2

    if not rect_end: # generer en tilfældig slut firkant i 4 kvadrant af array'et
        rect_x1 = random.randint(25, 49) * 10
        rect_y1 = random.randint(25, 49) * 10
        rect_end = (rect_x1, rect_y1)
        row, col = get_grid_indices(rect_x1, rect_y1)
        grid[row][col] = 2

    return rect_start, rect_end
# funktion til håndtere programmet
def handle_events(running, grid, rect_end):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # lukker programmmet hvis jeg trykker på "quit(x)"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False # lukker programmet hvis jeg trykker "escape"
            # elif event.key == pygame.K_SPACE:
            #     # ændrer seed og regenerer array samt slut firkant
            #     random.seed()
            #     grid = make_random_grid(50, 50)
            #     rect_end = (random.randint(25, 49) * 10, random.randint(25, 49) * 10)
            #     row, col = get_grid_indices(rect_end[0], rect_end[1])
            #     grid[row][col] = 2
            #     print(grid)
    return running, grid, rect_end

# funktion for at tegne grid, tegner noget forskelligt alt efter om værdien i array er "0", "1" eller "2"
def draw_grid(screen, grid, rect_start, rect_end):
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            color = (255, 255, 255)  # undlader at farve mulig bevægelses retning 
            if value == 1:
                color = (0, 0, 0)  # farver væggene sort
            elif value == 2:
                color = (255, 0, 0)  # farver start firkant og slut firkant rød

            pygame.draw.rect(screen, color, (x * 10, y * 10, 10, 10))

    # Draw rectangles for rect_start and rect_end
    if rect_start:
        pygame.draw.rect(screen, (255, 0, 0), (rect_start[0], rect_start[1], 10, 10))
    if rect_end:
        pygame.draw.rect(screen, (255, 0, 0), (rect_end[0], rect_end[1], 10, 10))

def bfs(grid, rect_start, rect_end):
    visited = set()
    predecessors = {}  # Dictionary to store predecessors
    q = Queue()
    q.put(rect_start)

    while not q.empty():
        current = q.get()
        if current == rect_end:
            break

        for neighbor in get_neighbors(current[0], current[1], grid):
            if neighbor not in visited:
                q.put(neighbor)
                visited.add(neighbor)
                predecessors[neighbor] = current  # Store predecessor

    path = reconstruct_path(rect_start, rect_end, predecessors)
    return path

def get_neighbors(x, y, grid):
    neighbors = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != 1:
            neighbors.append((nx, ny))
    
    return neighbors

def reconstruct_path(start, end, predecessors):
    path = []
    current = end

    while current != start:
        path.append(current)
        # Check if the current node is in the predecessors dictionary
        if current not in predecessors:
            break
        current = predecessors[current]

    # If the loop terminated without reaching the start, there's no path
    if current != start:
        return []

    path.append(start)
    path.reverse()
    return path

def main():
    pygame.init()

    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Path finding from a to b")

    grid = make_random_grid(50, 50)
    rect_start, rect_end = None, None
    
    running = True
    while running:
        running, grid, rect_end = handle_events(running, grid, rect_end)

        rect_start, rect_end = a_to_b(grid, rect_start, rect_end)

        # Convert rect_start and rect_end to grid indices
        start_indices = get_grid_indices(rect_start[0], rect_start[1])
        end_indices = get_grid_indices(rect_end[0], rect_end[1])

        path = bfs(grid, start_indices, end_indices)

        screen.fill((255, 255, 255))  # Fill the screen with a white background
        draw_grid(screen, grid, rect_start, rect_end)

        # Draw the path as a thin line
        for i in range(len(path) - 1):
            pygame.draw.line(screen, (255, 0, 0), (path[i][0] * 10 + 5, path[i][1] * 10 + 5),
                             (path[i + 1][0] * 10 + 5, path[i + 1][1] * 10 + 5), 2)
    
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()