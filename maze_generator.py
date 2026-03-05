import numpy as np
import random
import sys

# Recursion limit needs to be increased for larger mazes
sys.setrecursionlimit(2000)

class Maze3D:
    def __init__(self, size=11):
        # Đảm bảo size là số lẻ để tường/đường đồng nhất
        self.size = size if size % 2 != 0 else size + 1
        self.grid = np.ones((self.size, self.size, self.size), dtype=int)
        self.start = None
        self.goal = None

    def generate(self):
        # Chọn điểm bắt đầu (phải là tọa độ lẻ)
        start_node = (1, 1, 1)
        self.grid[start_node] = 0
        
        # Stack lưu trữ các node đã đi qua: [ (x, y, z) ]
        stack = [start_node]
        
        directions = [(2, 0, 0), (-2, 0, 0), (0, 2, 0), (0, -2, 0), (0, 0, 2), (0, 0, -2)]

        while stack:
            curr_x, curr_y, curr_z = stack[-1] # Xem phần tử cuối cùng
            
            # Tìm các láng giềng chưa thăm
            neighbors = []
            for dx, dy, dz in directions:
                nx, ny, nz = curr_x + dx, curr_y + dy, curr_z + dz
                
                if 0 < nx < self.size - 1 and 0 < ny < self.size - 1 and 0 < nz < self.size - 1:
                    if self.grid[nx, ny, nz] == 1:
                        neighbors.append((nx, ny, nz, dx, dy, dz))

            if neighbors:
                # Chọn ngẫu nhiên một hướng và đục tường
                nx, ny, nz, dx, dy, dz = random.choice(neighbors)
                self.grid[curr_x + dx // 2, curr_y + dy // 2, curr_z + dz // 2] = 0
                self.grid[nx, ny, nz] = 0
                stack.append((nx, ny, nz))
            else:
                # Không còn đường đi thì quay lui (Backtrack)
                stack.pop()

        self.set_spawn_and_goal()

    def set_spawn_and_goal(self):
        path_way = np.argwhere(self.grid == 0)
        if len(path_way) < 2: return
        self.start = tuple(path_way[0])
        self.goal = tuple(path_way[-1])


# maze = Maze3D(6)
# maze.generate()

# print(maze.grid)