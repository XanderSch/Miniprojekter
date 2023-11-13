import pygame
import random
import numpy as np
import matplotlib.pyplot as plt
from queue import PriorityQueue

def main():
    pygame.init()
    screen_size = (500, 500)
    screen = pygame.display.set_mode(screen_size)

    grid = make_random_grid(50, 50)
    rect_a = []
    rect_b = []
    path = []

    random.seed(42)

    clock = pygame.time.Clock()
    
    running = True
    while running:
        running = handle_events(running)
        screen.fill((255, 255, 255))

        for x in range(50):
            for y in range(50):
                grid_draw = grid[x][y]
                if grid_draw == 1:
                    # Draw a 10x10 rectangle at the grid position with the value 1
                    pygame.draw.rect(screen, (9, 121, 105), (x * 10, y * 10, 10, 10))
        
        a_to_b(screen, rect_a, rect_b)
        
        clock.tick(60)
        pygame.display.flip()


def a_to_b(screen, rect_a, rect_b) :
    if not rect_a:
        rect_x = random.randint(0, 25) * 10
        rect_y = random.randint(0, 25) * 10
        rect_a.append((rect_x, rect_y))

    if not rect_b:
        rect_x1 = random.randint(25, 49) * 10
        rect_y1 = random.randint(25, 49) * 10
        rect_b.append((rect_x1, rect_y1))
    pygame.draw.rect(screen, (255, 0, 0), (rect_a[0][0], rect_a[0][1], 10, 10))
    pygame.draw.rect(screen, (255, 0, 0), (rect_b[0][0], rect_b[0][1], 10, 10))

def make_random_grid(rows, cols):
    grid = []
    for y in range(rows):
        row = []
        for x in range(cols):
            row.append(1 if random.random() < 1/3 else 0)
        grid.append(row)
    return grid

def path(rect_a, rect_b):
    current = rect_b 
    path = []
    while current != rect_a: 
        path.append(current)
        current = came_from[current]


def bfs(screen, rect_a, rect_b):
    frontier = PriorityQueue()
    frontier.put(rect_a, 0)
    came_from = dict()
    cost_so_far = dict()
    came_from[rect_a] = None
    cost_so_far[rect_a] = 0

    while not frontier.empty():
    current = frontier.get()

    if current == rect_b:
        break
    
    for next in graph.neighbors(current):
        new_cost = cost_so_far[current] + graph.cost(current, next)
        if next not in cost_so_far or new_cost < cost_so_far[next]:
            cost_so_far[next] = new_cost
            priority = new_cost
            frontier.put(next, priority)
            came_from[next] = current


def handle_events(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    return running

if __name__ == "__main__":
    main()