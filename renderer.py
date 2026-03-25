import pygame

from setting import * 

class GameRenderer:    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("3D Maze Data Vis")
        
        # khởi tạo font an toàn với pathlib
        font_path = r'font\Pixeltype.ttf'
        try:
            self.title_font = pygame.font.Font(font_path, 100)
            self.button_font = pygame.font.Font(font_path, 50)
            self.setup_font = pygame.font.Font(font_path, 200)
            self.main_view_font = pygame.font.Font(font_path, 60)
            self.mini_view_font = pygame.font.Font(font_path, 50)
            self.scoreboard_title_font = pygame.font.Font(font_path, 100)
            self.scoreboard_font = pygame.font.Font(font_path, 40)
        except:
            self.title_font = pygame.font.SysFont('Arial', 100)
            self.button_font = pygame.font.SysFont('Arial', 50)
            self.setup_font = pygame.font.SysFont('Arial', 200)
            self.main_view_font = pygame.font.SysFont('Arial', 60)
            self.mini_view_font = pygame.font.SysFont('Arial', 50)
            self.scoreboard_title_font = pygame.font.SysFont('Arial', 100)
            self.scoreboard_font = pygame.font.SysFont('Arial', 40)

        # Định nghĩa Rect cho các nút bấm để main.py có thể kiểm tra va chạm
        self.play_buttom_rect = pygame.Rect(0, 0, 200, 100)
        self.play_buttom_rect.center = (SCREEN_W // 2, SCREEN_H // 2 - 60)
        
        self.score_buttom_rect = pygame.Rect(0, 0, 200, 100)
        self.score_buttom_rect.center = (SCREEN_W // 2, SCREEN_H // 2 + 60)

        # chuyển maze_cache và last_depth từ main sang đây để tự quản lý
        self.maze_cache = {'XY': None, 'XZ': None, 'YZ': None}
        self.last_depth = {'XY': -1, 'XZ': -1, 'YZ': -1}
        self.axes = ['XY', 'XZ', 'YZ']
        self.last_axis = None

    def clear_screen(self):
        self.screen.fill(COLOR_BACKGORUND)

    def draw_menu(self): # Không cần truyền rect từ ngoài vào nữa
        self.clear_screen()
        title_surf = self.title_font.render('3D MAZE', False, COLOR_TEXT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_W // 2, 150)))
        
        pygame.draw.rect(self.screen, COLOR_TEXT, self.play_buttom_rect)
        play_text = self.button_font.render('PLAY', False, COLOR_START)
        self.screen.blit(play_text, play_text.get_rect(center=self.play_buttom_rect.center))
        
        pygame.draw.rect(self.screen, COLOR_TEXT, self.score_buttom_rect)
        score_text = self.button_font.render('SCOREBOARD', False, COLOR_START)
        self.screen.blit(score_text, score_text.get_rect(center=self.score_buttom_rect.center))

    def draw_setting(self, maze_size):
        self.clear_screen()
        setup_surf = self.setup_font.render(str(maze_size), False, COLOR_TEXT)
        self.screen.blit(setup_surf, setup_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2)))

    def render_maze_surface(self, grid_slice, cell_size):
        rows, cols = grid_slice.shape
        surf = pygame.Surface((rows * cell_size, cols * cell_size))
        for r in range(rows):
            for c in range(cols):
                x = c * cell_size
                y = r * cell_size
                color = COLOR_WALL if grid_slice[r, c] == 1 else COLOR_PATH
                pygame.draw.rect(surf, color, (x, y, cell_size, cell_size))
        return surf

    def draw_entities(self, offset_x, offset_y, cell_size, start_2d, goal_2d, player_2d):
        if start_2d:
            sx, sy = start_2d
            pygame.draw.rect(self.screen, COLOR_START, (offset_x + sx * cell_size, offset_y + sy * cell_size, cell_size, cell_size))
        if goal_2d:
            gx, gy = goal_2d
            pygame.draw.rect(self.screen, COLOR_GOAL, (offset_x + gx * cell_size, offset_y + gy * cell_size, cell_size, cell_size))
        if player_2d:
            px, py = player_2d
            pygame.draw.rect(self.screen, COLOR_PLAYER, (offset_x + px * cell_size, offset_y + py * cell_size, cell_size, cell_size))

    def draw_in_game(self, maze, axis, player_pos, get_slice_func, gizmo):
        self.clear_screen()

        if self.last_axis != axis:
            self.maze_cache = {'XY': None, 'XZ': None, 'YZ': None}
            self.last_axis = axis
        
        actual_size = maze.size
        padding = 50
        
        # logic tính toán offset được đóng gói hoàn toàn tại đây
        main_available_h = SCREEN_H - (padding * 2)
        main_tile_size = main_available_h // actual_size
        main_offset_x = padding
        main_offset_y = (SCREEN_H - (actual_size * main_tile_size)) // 2

        mini_available_h = (SCREEN_H - (padding * 3)) // 2
        mini_tile_size = mini_available_h // actual_size
        mini_offset_x = main_offset_x + (actual_size * main_tile_size) + padding

        # logic cache
        for ax in self.axes:
            grid_slice, p2d, s2d, g2d = get_slice_func(maze, ax, player_pos)
            curr_depth = player_pos[2] if ax == 'XY' else (player_pos[1] if ax == 'XZ' else player_pos[0])

            if self.maze_cache[ax] is None or self.last_depth[ax] != curr_depth:
                cell_size = main_tile_size if ax == axis else mini_tile_size
                self.maze_cache[ax] = self.render_maze_surface(grid_slice, cell_size)
                self.last_depth[ax] = curr_depth

        # vẽ main view
        grid_slice_main, p2d, s2d, g2d = get_slice_func(maze, axis, player_pos)
        self.screen.blit(self.maze_cache[axis], (main_offset_x, main_offset_y))
        self.draw_entities(main_offset_x, main_offset_y, main_tile_size, s2d, g2d, p2d)
        
        main_text_surf = self.main_view_font.render(axis, False, COLOR_PLAYER)
        self.screen.blit(main_text_surf, (main_offset_x, main_offset_y - 30))

        # vẽ mini maps
        curr_mini_offset_y = main_offset_y
        for ax in self.axes:
            if ax == axis: continue
            _, sp2d, ss2d, sg2d = get_slice_func(maze, ax, player_pos)
            self.screen.blit(self.maze_cache[ax], (mini_offset_x, curr_mini_offset_y))
            self.draw_entities(mini_offset_x, curr_mini_offset_y, mini_tile_size, ss2d, sg2d, sp2d)
            
            mini_text_surf = self.mini_view_font.render(ax, False, COLOR_PLAYER)
            self.screen.blit(mini_text_surf, (mini_offset_x, curr_mini_offset_y - 25))
            
            curr_mini_offset_y += (actual_size * mini_tile_size) + 60

        # gọi gizmo
        gizmo.draw(self.screen, axis, player_pos, actual_size, grid_slice_main)

    def draw_ending(self, is_new_highscore, old_score, new_score):
        self.clear_screen()
        if not is_new_highscore:
            old_surf = self.title_font.render(f'HIGHSCORE: {old_score}', False, COLOR_TEXT)
            self.screen.blit(old_surf, old_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 25)))

            new_surf = self.title_font.render(f'YOUR SCORE: {new_score}', False, COLOR_TEXT)
            self.screen.blit(new_surf, new_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 25)))
        else:
            new_high_surf = self.title_font.render(f'NEW HIGHSCORE: {new_score}', False, COLOR_TEXT)
            self.screen.blit(new_high_surf, new_high_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2)))

    def draw_scoreboard(self, highscore_rows):
        self.clear_screen()
        start_line = 120
        line_high = 50
        
        title_surf = self.scoreboard_title_font.render('size : time', False, COLOR_TEXT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_W // 2, start_line - line_high - 20)))
        
        for i, row in enumerate(highscore_rows):
            row_surf = self.scoreboard_font.render(row, False, COLOR_TEXT)
            self.screen.blit(row_surf, row_surf.get_rect(center=(SCREEN_W // 2, start_line + line_high * i)))