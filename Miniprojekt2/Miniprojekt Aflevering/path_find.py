from queue import Queue
import random



class PathFinder:
    def bfs(grid, rect_start, rect_end):
        visited = set()
        predecessors = {}  # Dictionary to store predecessors
        q = Queue()
        q.put(rect_start)

        while not q.empty():
            current = q.get()
            if current == rect_end:
                break

            for neighbor in PathFinder.get_neighbors(current[0], current[1], grid):

                if neighbor not in visited:
                    q.put(neighbor)
                    visited.add(neighbor)
                    predecessors[neighbor] = current  # Store predecessor

        path = PathFinder.reconstruct_path(rect_start, rect_end, predecessors)
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