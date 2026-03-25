import pygame
import math

from setting import *

class Gizmo3D:
    def __init__(self, x, y, size):
        self.cx = x
        self.cy = y
        self.size = size
        self.angle_x = math.pi / 6 
        self.angle_y = -math.pi / 4  
        self.dragging = False
        self.last_mouse = (0, 0)
        self.font = None

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.dragging = True
            self.last_mouse = event.pos
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            dx = event.pos[0] - self.last_mouse[0]
            dy = event.pos[1] - self.last_mouse[1]
            self.angle_y -= dx * GIZMO_SENSITIVITY
            self.angle_x -= dy * GIZMO_SENSITIVITY
            self.last_mouse = event.pos

    def project(self, x, y, z, maze_size):
        M = maze_size / 1.5
        dx, dy, dz = x - M, y - M, z - M
        scale = self.size / M
        dx, dy, dz = dx * scale, dy * scale, dz * scale
        # Xoay quanh trục X
        y1 = dy * math.cos(self.angle_x) - dz * math.sin(self.angle_x)
        z1 = dy * math.sin(self.angle_x) + dz * math.cos(self.angle_x)
        # Xoay quanh trục Y
        x1 = dx * math.cos(self.angle_y) + z1 * math.sin(self.angle_y)
        return (self.cx + x1, self.cy + y1)

    def draw(self, surface, axis, player_pos, maze_size, grid_slice):
        if self.font is None:
            try:
                self.font = pygame.font.Font(r'font\Pixeltype.ttf', 30)
            except:
                self.font = pygame.font.SysFont('Arial', 24)

        # Vẽ trục tọa độ XYZ với mũi tên và số
        origin = self.project(0, 0, 0, maze_size)
        axes_info = [
            (maze_size + 2, 0, 0, '#FF0000', 'X'), # Trục X - Đỏ
            (0, maze_size + 2, 0, '#00FF00', 'Y'), # Trục Y - Xanh lá
            (0, 0, maze_size + 2, '#0000FF', 'Z')  # Trục Z - Xanh dương
        ]

        for ax_x, ax_y, ax_z, color, label in axes_info:
            end_point = self.project(ax_x, ax_y, ax_z, maze_size)
            pygame.draw.line(surface, color, origin, end_point, 3)
            # Vẽ mũi tên đơn giản (điểm tròn ở đầu trục)
            pygame.draw.circle(surface, color, (int(end_point[0]), int(end_point[1])), 5)
            # Đánh số tọa độ cực đại và nhãn
            text = self.font.render(f"{label}({maze_size})", True, color)
            surface.blit(text, (end_point[0] + 5, end_point[1] + 5))

        # Vẽ mặt cắt
        px, py, pz = player_pos
        rows, cols = grid_slice.shape
        for r in range(rows):
            for c in range(cols):
                color = "#1A921C" if grid_slice[r, c] == 1 else "#5E510F"
                # Tính toán 4 đỉnh của ô trong không gian 3D dựa trên mặt cắt
                if axis == 'XY':
                    pts = [self.project(c, r, pz, maze_size), self.project(c+1, r, pz, maze_size),
                           self.project(c+1, r+1, pz, maze_size), self.project(c, r+1, pz, maze_size)]
                elif axis == 'XZ':
                    pts = [self.project(c, py, r, maze_size), self.project(c+1, py, r, maze_size),
                           self.project(c+1, py, r+1, maze_size), self.project(c, py, r+1, maze_size)]
                elif axis == 'YZ':
                    pts = [self.project(px, c, r, maze_size), self.project(px, c+1, r, maze_size),
                           self.project(px, c+1, r+1, maze_size), self.project(px, c, r+1, maze_size)]
                
                pygame.draw.polygon(surface, color, pts, 0)
                pygame.draw.polygon(surface, '#000000', pts, 1)

        # Vẽ player
        if axis == 'XY': p_3d = self.project(px + 0.5, py + 0.5, pz, maze_size)
        elif axis == 'XZ': p_3d = self.project(px + 0.5, py, pz + 0.5, maze_size)
        elif axis == 'YZ': p_3d = self.project(px, py + 0.5, pz + 0.5, maze_size)
        pygame.draw.circle(surface, '#FFFFFF', (int(p_3d[0]), int(p_3d[1])), 6) # Viền trắng
        pygame.draw.circle(surface, '#000000', (int(p_3d[0]), int(p_3d[1])), 4) # Nhân đen