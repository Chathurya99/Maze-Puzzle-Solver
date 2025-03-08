import numpy as np
import random
import time
from queue import Queue
import heapq

# Function to create a maze
def create_maze(dim):
    maze = np.ones((dim * 2 + 1, dim * 2 + 1))
    x, y = (0, 0)
    maze[2 * x + 1, 2 * y + 1] = 0
    stack = [(x, y)]
    while len(stack) > 0:
        x, y = stack[-1]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < dim and 0 <= ny < dim and maze[2 * nx + 1, 2 * ny + 1] == 1:
                maze[2 * nx + 1, 2 * ny + 1] = 0
                maze[2 * x + 1 + dx, 2 * y + 1 + dy] = 0
                stack.append((nx, ny))
                break
        else:
            stack.pop()
    maze[1, 0] = 0
    maze[-2, -1] = 0
    return maze

# BFS Algorithm
def bfs(maze, start, end):
    start_time = time.time()
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    visited = np.zeros_like(maze, dtype=bool)
    visited[start] = True
    queue = Queue()
    queue.put((start, []))
    while not queue.empty():
        (node, path) = queue.get()
        for dx, dy in directions:
            next_node = (node[0] + dx, node[1] + dy)
            if next_node == end:
                return path + [next_node], time.time() - start_time
            if 0 <= next_node[0] < maze.shape[0] and 0 <= next_node[1] < maze.shape[1] and maze[next_node] == 0 and not visited[next_node]:
                visited[next_node] = True
                queue.put((next_node, path + [next_node]))
    return None, time.time() - start_time

# A* Algorithm
def a_star(maze, start, end):
    start_time = time.time()
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    def heuristic(node):
        return abs(node[0] - end[0]) + abs(node[1] - end[1])
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start), start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start)}
    while open_set:
        current_fscore, current = heapq.heappop(open_set)
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], time.time() - start_time
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < maze.shape[0] and 0 <= neighbor[1] < maze.shape[1] and maze[neighbor] == 0:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return None, time.time() - start_time

# DFS Algorithm
def dfs(maze, start, end):
    start_time = time.time()
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    stack, visited, path = [start], set(), {}
    visited.add(start)
    while stack:
        node = stack.pop()
        if node == end:
            final_path = []
            while node in path:
                final_path.append(node)
                node = path[node]
            return final_path[::-1], time.time() - start_time
        for dx, dy in directions:
            next_node = (node[0] + dx, node[1] + dy)
            if 0 <= next_node[0] < maze.shape[0] and 0 <= next_node[1] < maze.shape[1] and maze[next_node] == 0 and next_node not in visited:
                visited.add(next_node)
                stack.append(next_node)
                path[next_node] = node
    return None, time.time() - start_time
