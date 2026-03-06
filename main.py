import pygame
from maze_generator import Maze3D
from sys import exit

# Cấu hình
main_tile_size = 50

screen_w = 1538
screen_h = 700

maze_size = 0

def render_maze_surface(grid_slice, cell_size):
    rows, cols = grid_slice.shape
    surf = pygame.Surface((rows* cell_size, cols* cell_size))
    for r in range(rows):
        for c in range(cols):
            x = c*cell_size
            y = r*cell_size

            color = "#1A921C" if grid_slice[r, c] == 1 else "#5E510F"
            pygame.draw.rect(surf, color, (x, y, cell_size, cell_size))
    return surf

def draw_entities(surface, off_set_x, off_set_y, cell_size, start_2d, goal_2d, player_2d):
    if start_2d:
        sx, sy = start_2d
        pygame.draw.rect(surface, "#FF0000", (off_set_x+ sx* cell_size, off_set_y+ sy* cell_size, cell_size, cell_size))

    if goal_2d:
        gx, gy = goal_2d
        pygame.draw.rect(surface, "#FF00B7", (off_set_x+ gx* cell_size, off_set_y+ gy* cell_size, cell_size, cell_size))

    if player_2d:
        px, py = player_2d
        pygame.draw.rect(surface, '#000000', (off_set_x+ px* cell_size, off_set_y+ py* cell_size, cell_size, cell_size))

def get_slice(maze, view_axis, player_position):
    px, py, pz = player_position
    sx, sy, sz = maze.start
    gx, gy, gz = maze.goal
    
    if view_axis == 'XY':
        grid_slice = maze.grid[:, :, pz]
        p2d = (px, py)
        g2d = (gx, gy) if gz == pz else None
        s2d = (sx, sy) if sz == pz else None
        return grid_slice.T, p2d, s2d, g2d
        
    elif view_axis == 'XZ':
        grid_slice = maze.grid[:, py, :]
        p2d = (px, pz)
        g2d = (gx, gz) if gy == py else None
        s2d = (sx, sz) if sy == py else None
        return grid_slice.T, p2d, s2d, g2d

    elif view_axis == 'YZ':
        grid_slice = maze.grid[px, :, :]
        p2d = (py, pz)
        g2d = (gy, gz) if gx == px else None
        s2d = (sy, sz) if sx == px else None
        return grid_slice.T, p2d, s2d, g2d
    
pygame.init()

# screen
screen = pygame.display.set_mode((screen_w, screen_h))

# game state ------------------------------------------MENU----------------------------------------------------
# game name text
text_type = pygame.font.Font(r'font\Pixeltype.ttf', 100) 
text_surf = text_type.render('3D MAZE', False, '#000000')
text_rect = text_surf.get_rect(center = (764, 150))

# buttom
play_buttom_rect = pygame.Rect(764, 250, 200, 100)
play_buttom_text_type = pygame.font.Font(r'font\Pixeltype.ttf', 50)
play_buttom_text_surf = play_buttom_text_type.render('PLAY', False, "#CA0E0E")
play_buttom_text_rect = play_buttom_text_surf.get_rect(center= (764, 250))

# game state ------------------------------------------SETTING----------------------------------------------------
setup_text_type = pygame.font.Font(r'font\Pixeltype.ttf', 200)
setup_text_surf = setup_text_type.render('0', False, '#000000')
setup_text_rect = setup_text_surf.get_rect(center= (screen_w// 2, screen_h// 2))

# game state ------------------------------------------IN_GAME----------------------------------------------------
axes = ['XY', 'XZ', 'YZ']
curr_axis_idx = 0
axis = axes[curr_axis_idx]

#cache
maze_cache = {'XY': None, 'XZ': None, 'YZ': None}
last_depth = {'XY': -1, 'XZ': -1, 'YZ': -1}

# text info
main_view_text_type = pygame.font.Font(r'font\Pixeltype.ttf', 60)
mini_view_text_type = pygame.font.Font(r'font\Pixeltype.ttf', 50)

# game state
game_state = 'menu'

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_state == 'menu':
            if event.type == pygame.MOUSEBUTTONUP:
                if play_buttom_rect.collidepoint(event.pos):

                    maze_size = 0

                    game_state = 'setting'
        
        elif game_state == 'setting':
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_1]: maze_size = maze_size* 10 + 1
                elif keys[pygame.K_2]: maze_size = maze_size* 10 + 2
                elif keys[pygame.K_3]: maze_size = maze_size* 10 + 3
                elif keys[pygame.K_4]: maze_size = maze_size* 10 + 4
                elif keys[pygame.K_5]: maze_size = maze_size* 10 + 5
                elif keys[pygame.K_6]: maze_size = maze_size* 10 + 6
                elif keys[pygame.K_7]: maze_size = maze_size* 10 + 7
                elif keys[pygame.K_8]: maze_size = maze_size* 10 + 8
                elif keys[pygame.K_9]: maze_size = maze_size* 10 + 9
                elif keys[pygame.K_0]: maze_size = maze_size* 10

                if maze_size > 20:
                    maze_size //= 10

                setup_text_surf = setup_text_type.render(str(maze_size), False, '#000000')
                setup_text_rect = setup_text_surf.get_rect(center= (screen_w// 2, screen_h// 2))

                if keys[pygame.K_RETURN]:
                    if maze_size < 4 or maze_size > 20:
                        maze_size = 0
                        setup_text_surf = setup_text_type.render('0', False, '#000000')
                        continue
                    # process even num
                    if maze_size% 2 == 0: maze_size += 1

                    maze = Maze3D(maze_size)
                    maze.generate()

                    player_pos = maze.start

                    actual_size = maze.size 

                    padding = 50
                    main_available_h = screen_h - (padding * 2)
                    main_tile_size = main_available_h // actual_size
                    
                    main_offset_x = padding
                    main_offset_y = (screen_h - (actual_size * main_tile_size)) // 2

                    mini_available_h = (screen_h - (padding * 3)) // 2
                    mini_tile_size = mini_available_h // actual_size
                    
                    mini_offset_x = main_offset_x + (actual_size * main_tile_size) + padding
                    
                    game_state = 'in_game'
        
        elif game_state == 'in_game':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    curr_axis_idx = (curr_axis_idx+ 1)% 3
                    axis = axes[curr_axis_idx]

                # dev func --------------------------------------------------------------------------------------
                if event.key == pygame.K_ESCAPE:
                    game_state = 'menu'
                    maze_size = 0
                # dev func --------------------------------------------------------------------------------------

                x, y, z = player_pos
                dx, dy, dz = 0, 0, 0
                axis = axes[curr_axis_idx]
                
                # Logic:
                # XY: W/S -> Y, A/D -> X
                # XZ: W/S -> Z, A/D -> X
                # YZ: W/S -> Z, A/D -> Y
                
                if axis == 'XY':
                    if event.key == pygame.K_w: dy = -1
                    elif event.key == pygame.K_s: dy = 1
                    elif event.key == pygame.K_a: dx = -1
                    elif event.key == pygame.K_d: dx = 1
                elif axis == 'XZ':
                    if event.key == pygame.K_w: dz = -1
                    elif event.key == pygame.K_s: dz = 1
                    elif event.key == pygame.K_a: dx = -1
                    elif event.key == pygame.K_d: dx = 1
                elif axis == 'YZ':
                    if event.key == pygame.K_w: dz = -1
                    elif event.key == pygame.K_s: dz = 1
                    elif event.key == pygame.K_a: dy = -1
                    elif event.key == pygame.K_d: dy = 1
                
                nx, ny, nz = x + dx, y + dy, z + dz
                
                # move logic
                if 0 <= nx < maze_size and 0 <= ny < maze_size and 0 <= nz < maze_size:
                    if maze.grid[nx, ny, nz] == 0:
                        player_pos = [nx, ny, nz]
                
                # win function
                if (nx, ny, nz) == maze.goal:
                    print('win')
                    
                    game_state = 'menu'
                    setup_text_surf = setup_text_type.render('0', False, '#000000')
                    maze_size = 0
    
    if game_state == 'menu':
        # background color
        screen.fill("#FFFFFF")
        # game name text
        screen.blit(text_surf, text_rect)
        pygame.draw.rect(screen, '#000000', rect= play_buttom_rect)
        screen.blit(play_buttom_text_surf, play_buttom_text_rect)
    
    elif game_state == 'setting':
        # background color
        screen.fill('#FFFFFF')
        # maze size custom
        screen.blit(setup_text_surf, setup_text_rect)

    elif game_state == 'in_game':
        # background color
        screen.fill('#FFFFFF')

        # load cache
        for ax in axes:
            grid_slice, p2d, s2d, g2d = get_slice(maze, ax, player_pos)
            curr_depth = player_pos[2] if ax == 'XY' else (player_pos[1] if ax == 'XZ' else player_pos[0])

            if maze_cache[ax] is None or last_depth != curr_depth:
                cell_size = main_tile_size if ax == axis else mini_tile_size
                maze_cache[ax] = render_maze_surface(grid_slice, cell_size)
                last_depth[ax] = curr_depth
        
        # draw main view
        _, p2d, s2d, g2d = get_slice(maze, axis, player_pos)
        screen.blit(maze_cache[axis], (main_offset_x, main_offset_y))
        draw_entities(screen, main_offset_x, main_offset_y, main_tile_size, s2d, g2d, p2d)
        # display main text
        main_view_text_surf = main_view_text_type.render(axis, False, '#000000')
        main_view_text_rect = main_view_text_surf.get_rect(topleft= (main_offset_x, main_offset_y- 30))
        screen.blit(main_view_text_surf, main_view_text_rect)

        # draw minimap
        curr_mini_offset_y = main_offset_y
        for ax in axes:
            if ax == axis: continue

            _, sp2d, ss2d, sg2d = get_slice(maze, ax, player_pos)
            screen.blit(maze_cache[ax], (mini_offset_x, curr_mini_offset_y))
            draw_entities(screen, mini_offset_x, curr_mini_offset_y, mini_tile_size, ss2d, sg2d, sp2d)

            # display text
            mini_view_text_surf = mini_view_text_type.render(ax, False, '#000000')
            mini_view_text_rect = mini_view_text_surf.get_rect(topleft= (mini_offset_x, curr_mini_offset_y- 25))
            screen.blit(mini_view_text_surf, mini_view_text_rect)

            # change offset for other map
            curr_mini_offset_y = curr_mini_offset_y +(maze_size* mini_tile_size)+ 60


    pygame.display.flip()
