import random
import pygame
from queue import Queue

class MapGenerator:
    def make_random_grid(rows, cols):
        grid = []
        for y in range(rows):
            row = []
            for x in range(cols):
                row.append(1 if random.random() < 1/10 else 0) #opdeler array hvor 1/10 får værdien 1, og resten værdien 0
            grid.append(row)
        return grid
    
    def get_grid_indices(x, y):
        row = x // 10 
        col = y // 10
        return row, col

    def draw_grid(screen, grid, rect_start, rect_end):
        for y, row in enumerate(grid):
            for x, value in enumerate(row):
                color = (255, 255, 255)  # undlader at farve mulig bevægelses retning 
                if value == 1:
                    color = (0, 0, 0)  # farver væggene sort
                pygame.draw.rect(screen, color, (x * 10, y * 10, 10, 10))

        # Draw rectangles for rect_start and rect_end
        if rect_start:
            pygame.draw.rect(screen, (255, 0, 0), (rect_start[0], rect_start[1], 10, 10))
        if rect_end:
            pygame.draw.rect(screen, (255, 0, 0), (rect_end[0], rect_end[1], 10, 10))

    def a_to_b(grid, rect_start, rect_end):
        if not rect_start: # Laver et random start felt, 
            rect_x =  random.randint(0, 10) * 10  
            rect_y =  random.randint(0, 10) * 10   
            rect_start = (rect_x, rect_y)
            row, col = MapGenerator.get_grid_indices(rect_x, rect_y)
            grid[row][col] = 2

        if not rect_end: # generer en tilfældig slut firkant i 4 kvadrant af array'et
            rect_x1 = random.randint(25, 49) * 10  #34 * 10 
            rect_y1 = random.randint(25, 49) * 10  #30 * 10 
            rect_end = (rect_x1, rect_y1)
            row, col = MapGenerator.get_grid_indices(rect_x1, rect_y1)
            grid[row][col] = 2

        return rect_start, rect_end