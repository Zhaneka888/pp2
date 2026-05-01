import pygame
import sys
import math

# PYGAME INITIALIZATION
pygame.init()

# CONSTANTS
WIDTH, HEIGHT  = 900, 650
TOOLBAR_HEIGHT = 55
PANEL_WIDTH    = 180

# Rainbow colors (7 colors of the rainbow)
COLORS = [
    (148, 0,   211),  # Violet
    (75,  0,   130),  # Indigo
    (0,   0,   255),  # Blue
    (0,   255, 0  ),  # Green
    (255, 255, 0  ),  # Yellow
    (255, 127, 0  ),  # Orange
    (255, 0,   0  ),  # Red
]

# UI colors
WHITE     = (255, 255, 255)
BLACK     = (0,   0,   0  )
GRAY      = (210, 210, 210)
DARK_GRAY = (90,  90,  90 )
PANEL_BG  = (245, 245, 255)

# WINDOW SETUP
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint App")
screen.fill(WHITE)

# DRAWING STATE
current_color = BLACK
brush_size    = 5
shape_mode    = 'brush'

# FONTS
font_tiny   = pygame.font.SysFont("Arial", 13)
font_small  = pygame.font.SysFont("Arial", 15)
font_medium = pygame.font.SysFont("Arial", 17, bold=True)

# HINT PANEL DATA
# Each entry: (key label, tool name, badge color)
HINT_ITEMS = [
    ("[B]", "Brush",     (80,  140, 255)),
    ("[E]", "Eraser",    (180, 180, 180)),
    ("[R]", "Rectangle", (255, 100, 100)),
    ("[C]", "Circle",    (100, 200, 120)),
    ("[T]", "Triangle",  (255, 180,  60)),
    ("[H]", "Rhombus",   (180,  80, 220)),
    ("[P]", "Clear all", (255,  80,  80)),
    ("[+]", "Brush +",   (60,  180, 120)),
    ("[-]", "Brush -",   (200, 100,  60)),
]

# HELPER — draw a rounded rectangle
def draw_rounded_rect(surface, color, rect, radius=8, border=0, border_color=BLACK):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border:
        pygame.draw.rect(surface, border_color, rect, border, border_radius=radius)

# TOOLBAR
# Draws the top bar: color swatches + active-mode label
def draw_toolbar():
    # Toolbar background
    draw_rounded_rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT), radius=0)

    # Color swatches
    swatch_size = 34
    start_x     = 12
    for i, color in enumerate(COLORS):
        x    = start_x + i * (swatch_size + 6)
        rect = pygame.Rect(x, 10, swatch_size, swatch_size)
        draw_rounded_rect(screen, color, rect, radius=6)
        # White ring highlights the currently selected color
        if color == current_color:
            pygame.draw.rect(screen, WHITE, rect, 3, border_radius=6)

    # Active mode label
    mode_surf = font_small.render(f"Tool:  {shape_mode}", True, DARK_GRAY)
    screen.blit(mode_surf, (WIDTH - PANEL_WIDTH - mode_surf.get_width() - 20, 18))

# RIGHT-SIDE HINT PANEL
# Always visible; shows every keyboard shortcut at a glance
def draw_hint_panel():
    px = WIDTH - PANEL_WIDTH
    py = TOOLBAR_HEIGHT

    # Panel background
    panel_surf = pygame.Surface((PANEL_WIDTH, HEIGHT - TOOLBAR_HEIGHT))
    panel_surf.fill(PANEL_BG)
    screen.blit(panel_surf, (px, py))

    # Left border line separating canvas from panel
    pygame.draw.line(screen, DARK_GRAY, (px, py), (px, HEIGHT), 2)

    # Panel title
    title = font_medium.render("Shortcuts", True, DARK_GRAY)
    screen.blit(title, (px + PANEL_WIDTH // 2 - title.get_width() // 2, py + 10))
    pygame.draw.line(screen, DARK_GRAY,
                     (px + 8, py + 34), (px + PANEL_WIDTH - 8, py + 34), 1)

    # Each shortcut row
    for i, (key, name, badge_col) in enumerate(HINT_ITEMS):
        row_y = py + 44 + i * 30

        # Highlight the row that matches the active tool
        if name.lower().startswith(shape_mode.split('_')[0]):
            highlight = pygame.Surface((PANEL_WIDTH - 4, 26), pygame.SRCALPHA)
            highlight.fill((100, 180, 255, 60))
            screen.blit(highlight, (px + 2, row_y - 2))

        # Colored key badge
        badge = pygame.Rect(px + 8, row_y, 36, 22)
        draw_rounded_rect(screen, badge_col, badge, radius=4)
        key_surf = font_tiny.render(key, True, WHITE)
        screen.blit(key_surf, (badge.centerx - key_surf.get_width() // 2,
                               badge.centery - key_surf.get_height() // 2))

        # Tool name next to the badge
        name_surf = font_small.render(name, True, BLACK)
        screen.blit(name_surf, (px + 52, row_y + 3))

    # Brush-size indicator at the bottom of the panel
    size_txt = font_tiny.render(f"Brush size: {brush_size}", True, DARK_GRAY)
    screen.blit(size_txt, (px + PANEL_WIDTH // 2 - size_txt.get_width() // 2,
                            HEIGHT - 20))

# SHAPE DRAWING HELPERS
def draw_equilateral_triangle(start, end, color):
    """Draws an equilateral triangle; base width = distance between points"""
    side   = int(math.hypot(end[0] - start[0], end[1] - start[1]))
    height = int((math.sqrt(3) / 2) * side)
    p1 = start
    p2 = (start[0] + side,        start[1]         )
    p3 = (start[0] + side // 2,   start[1] - height)
    pygame.draw.polygon(screen, color, [p1, p2, p3], 2)


def draw_rhombus(start, end, color):
    """Draws a rhombus whose bounding box is defined by start and end"""
    w  = abs(end[0] - start[0])
    h  = abs(end[1] - start[1])
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2
    points = [
        (cx,          cy - h // 2),
        (cx + w // 2, cy         ),
        (cx,          cy + h // 2),
        (cx - w // 2, cy         ),
    ]
    pygame.draw.polygon(screen, color, points, 2)

# CANVAS REGION
# The drawable area excludes the toolbar (top) and hint panel (right)
CANVAS_RECT = pygame.Rect(0, TOOLBAR_HEIGHT,
                           WIDTH - PANEL_WIDTH,
                           HEIGHT - TOOLBAR_HEIGHT)


def in_canvas(pos):
    """Returns True if pos is inside the drawable canvas"""
    return CANVAS_RECT.collidepoint(pos)

# MAIN LOOP
clock     = pygame.time.Clock()
running   = True
start_pos = None   # Stores mouse-down position for shape drawing

while running:

    # EVENT HANDLING
    for event in pygame.event.get():

        # Quit the application
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Mouse button pressed
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Click on a color swatch in the toolbar
            if y < TOOLBAR_HEIGHT:
                swatch_size = 34
                idx = (x - 12) // (swatch_size + 6)
                if 0 <= idx < len(COLORS):
                    current_color = COLORS[idx]

            # Start drawing on the canvas
            elif in_canvas(event.pos):
                start_pos = event.pos

        # Switching between shapes and drawing them
        elif event.type == pygame.MOUSEBUTTONUP and start_pos:
            end_pos = event.pos
            if shape_mode == 'rectangle':
                rw = abs(end_pos[0] - start_pos[0])
                rh = abs(end_pos[1] - start_pos[1])
                pygame.draw.rect(screen, current_color,
                                 (min(start_pos[0], end_pos[0]),
                                  min(start_pos[1], end_pos[1]),
                                  rw, rh), 2)
            elif shape_mode == 'circle':
                r  = int(math.hypot(end_pos[0] - start_pos[0],
                                    end_pos[1] - start_pos[1]) / 2)
                cx = (start_pos[0] + end_pos[0]) // 2
                cy = (start_pos[1] + end_pos[1]) // 2
                pygame.draw.circle(screen, current_color, (cx, cy), r, 2)
            elif shape_mode == 'equilateral_triangle':
                draw_equilateral_triangle(start_pos, end_pos, current_color)
            elif shape_mode == 'rhombus':
                draw_rhombus(start_pos, end_pos, current_color)
            start_pos = None

        #Keyboard shortcuts
        elif event.type == pygame.KEYDOWN:
            if   event.key == pygame.K_b: shape_mode = 'brush'
            elif event.key == pygame.K_e: shape_mode = 'eraser'
            elif event.key == pygame.K_r: shape_mode = 'rectangle'
            elif event.key == pygame.K_c: shape_mode = 'circle'
            elif event.key == pygame.K_t: shape_mode = 'equilateral_triangle'
            elif event.key == pygame.K_h: shape_mode = 'rhombus'
            elif event.key == pygame.K_p:
                # Clear the entire canvas by filling it white
                pygame.draw.rect(screen, WHITE, CANVAS_RECT)
            elif event.key == pygame.K_EQUALS:
                brush_size = min(brush_size + 2, 40)   # Increase brush size
            elif event.key == pygame.K_MINUS:
                brush_size = max(brush_size - 2,  2)   # Decrease brush size

    #CONTINUOUS BRUSH / ERASER (held left mouse button)
    if (pygame.mouse.get_pressed()[0]
            and start_pos
            and shape_mode in ('brush', 'eraser')
            and in_canvas(pygame.mouse.get_pos())):
        col = WHITE if shape_mode == 'eraser' else current_color
        pygame.draw.circle(screen, col, pygame.mouse.get_pos(), brush_size)

    #REDRAW UI (always on top of canvas content)
    draw_toolbar()     # Top bar: palette swatches + active tool label
    draw_hint_panel()  # Right panel: shortcut reference + brush size

    pygame.display.flip()
    clock.tick(60)   # Cap at 60 FPS