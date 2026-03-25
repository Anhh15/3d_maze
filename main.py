import pygame
from maze_generator import Maze3D
from sys import exit
import csv
from pathlib import Path

from gizmo_3d import Gizmo3D

from renderer import GameRenderer
from setting import *


# biến chung
maze_size = 0

highscore_fieldnames = ['size', 'time']

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

def save_record(maze_size, time_taken):
    path = Path(HIGHSCORE_FILE)
    rows = []

    if not path.exists():
        for size in range(MAZE_MIN_SIZE, MAZE_MAX_SIZE+ 3):
            if size% 2 == 0: continue
            rows.append({'size': str(size), 'time': "0"})
    else:
        with open(path, 'r', newline= '') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

    update = False
    for row in rows:
        if row['size'] == str(maze_size):
            current_time = float(row['time'])
            if current_time <= 0 or current_time > time_taken:
                row['time'] = time_taken
                update = True
            break
    
    if update or not path.exists():
        with open(path, 'w', newline= '') as f:
            writer = csv.DictWriter(f, fieldnames= highscore_fieldnames)
            writer.writeheader()
            writer.writerows(rows)

def get_current_record(maze_size):
    path = Path(HIGHSCORE_FILE)

    if not path.exists(): return 0.0

    with open(path, 'r', newline= '') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['size'] == str(maze_size):
                return float(row['time'])
    return 0
    
pygame.init()
gizmo = Gizmo3D(*(GIZMO_POS), GIZMO_SIZE)
renderer = GameRenderer()

# game state ------------------------------------------MENU----------------------------------------------------

# game state ------------------------------------------SETTING----------------------------------------------------

# game state ------------------------------------------IN_GAME----------------------------------------------------
axes = ['XY', 'XZ', 'YZ']
curr_axis_idx = 0
axis = axes[curr_axis_idx]

# 3d map state
open_3d_map = False

# game state ------------------------------------------ENDING----------------------------------------------------

# game state ------------------------------------------SCOREBOARD----------------------------------------------------

current_open_file = False

# game state
game_state = 'menu'

# clock
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_state == 'menu':
            if event.type == pygame.MOUSEBUTTONUP:
                if renderer.play_buttom_rect.collidepoint(event.pos):
                    maze_size = 0 
                    game_state = 'setting'

                elif renderer.score_buttom_rect.collidepoint(event.pos):
                    game_state = 'scoreboard'
        
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
                elif keys[pygame.K_BACKSPACE]: maze_size = 0

                elif keys[pygame.K_ESCAPE]: game_state = 'menu'

                if maze_size > 20:
                    maze_size //= 10

                if keys[pygame.K_RETURN]:
                    if maze_size < 4 or maze_size > 20:
                        maze_size = 0
                        continue
                    # process even num
                    if maze_size% 2 == 0: maze_size += 1

                    maze = Maze3D(maze_size)
                    maze.generate()

                    start_time = pygame.time.get_ticks()

                    player_pos = maze.start
                    
                    game_state = 'in_game'
        
        elif game_state == 'in_game':

            gizmo.process_event(event)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    curr_axis_idx = (curr_axis_idx+ 1)% 3
                    axis = axes[curr_axis_idx]
                elif event.key == pygame.K_m:
                    open_3d_map = not open_3d_map

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

                    # calculate time and save record
                    finish_time = pygame.time.get_ticks()- start_time
                    old_highscore = get_current_record(maze_size)

                    is_new_highscore = (old_highscore <= 0 or old_highscore > finish_time)
                    
                    if is_new_highscore: save_record(maze_size, finish_time)

                    # reset setup
                    game_state = 'ending'
    
        elif game_state == 'ending':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    maze_size = 0
                    game_state = 'menu'
        
        elif game_state == 'scoreboard':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    current_open_file = False
                    game_state = 'menu'

    if game_state == 'menu': #--------------------------------------------------------------------------------
        renderer.draw_menu()
    
    elif game_state == 'setting':#--------------------------------------------------------------------------------
        renderer.draw_setting(maze_size)

    elif game_state == 'in_game':#--------------------------------------------------------------------------------
        renderer.draw_in_game(maze, axis, player_pos, get_slice, gizmo)

    elif game_state == 'ending':#--------------------------------------------------------------------------------
        current_record = get_current_record(maze_size)
        renderer.draw_ending(is_new_highscore, current_record, finish_time)

    elif game_state == 'scoreboard': 
        if current_open_file == False:
            highscore_rows = []
            path = Path(HIGHSCORE_FILE)
            if not path.exists():
                rows = []
                for size in range(MAZE_MIN_SIZE, MAZE_MAX_SIZE+ 3):
                    if size% 2 == 0: continue
                    rows.append({'size': str(size), 'time': "0"})

                with open(path, 'w', newline= '') as f:
                    writer = csv.DictWriter(f, fieldnames= highscore_fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)
            
            with open(path, 'r', newline= '') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    highscore_rows.append(f'{row['size']} : {row['time']}')

            current_open_file = True
        
        renderer.draw_scoreboard(highscore_rows)
        
    pygame.display.flip()
