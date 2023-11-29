import pygame
import random
from map_gen import MapGenerator
from path_find import PathFinder

def handle_events(running, grid, rect_start, rect_end):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # lukker programmmet hvis jeg trykker på "quit(x)"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False # lukker programmet hvis jeg trykker "escape"
            elif event.key == pygame.K_SPACE:
                # ændrer seed og regenerer array samt slut firkant
                random.seed()
                grid = MapGenerator.make_random_grid(50, 50)
                rect_start = (random.randint(0, 25) * 10, random.randint(0, 25) * 10)
                rect_end = (random.randint(26, 49) * 10, random.randint(26, 49) * 10)
                row, col = MapGenerator.get_grid_indices(rect_end[0], rect_end[1])
                grid[row][col] = 2
    return running, grid, rect_start, rect_end

def main():
    pygame.init()

    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Grid Visualization")

    grid = MapGenerator.make_random_grid(50, 50)
    rect_start, rect_end = None, None

    running = True
    while running:
        running, grid, rect_start, rect_end = handle_events(running, grid, rect_start, rect_end)

        rect_start, rect_end = MapGenerator.a_to_b(grid, rect_start, rect_end)

        # Convert rect_start and rect_end to grid indices
        start_indices = MapGenerator.get_grid_indices(rect_start[0], rect_start[1])
        end_indices = MapGenerator.get_grid_indices(rect_end[0], rect_end[1])

        path = PathFinder.bfs(grid, start_indices, end_indices)

        screen.fill((255, 255, 255))  # Fill the screen with a white background
        MapGenerator.draw_grid(screen, grid, rect_start, rect_end)

        # Draw the path as a thin line
        for i in range(len(path) - 1):
            pygame.draw.line(screen, (255, 0, 0), (path[i][0] * 10 + 5, path[i][1] * 10 + 5),
                             (path[i + 1][0] * 10 + 5, path[i + 1][1] * 10 + 5), 2)

        pygame.display.flip()

    pygame.quit()
if __name__ == "__main__":
    main()