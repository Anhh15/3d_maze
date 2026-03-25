import pygame
from pathlib import Path

# --- Cấu hình màn hình ---
SCREEN_W = 1538
SCREEN_H = 700
FPS = 60

# --- Cấu hình Mê cung ---
MAZE_MIN_SIZE = 5  # Nên là số lẻ
MAZE_MAX_SIZE = 21 # Đã cập nhật để hỗ trợ size 21 của bạn
DEFAULT_TILE_SIZE = 50

# --- Màu sắc (Hệ Hex/RGB) ---
COLOR_BACKGORUND = "#FFFFFF"
COLOR_WALL = "#1A921C"   # Xanh lá (Tường)
COLOR_PATH = "#5E510F"   # Nâu (Đường đi)
COLOR_PLAYER = "#000000" # Đen
COLOR_START = "#FF0000"  # Đỏ
COLOR_GOAL = "#FF00B7"   # Hồng
COLOR_TEXT = "#000000"

# --- Cấu hình Gizmo 3D ---
GIZMO_POS = (1250, 350)
GIZMO_SIZE = 180
GIZMO_SENSITIVITY = 0.005 # Độ nhạy khi xoay chuột
COLOR_AXIS_X = '#FF0000'
COLOR_AXIS_Y = '#00FF00'
COLOR_AXIS_Z = '#0000FF'

# --- Đường dẫn hệ thống ---
FONT_PATH = str(Path('font/Pixeltype.ttf'))
HIGHSCORE_FILE = 'highscore.csv'