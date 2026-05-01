import pygame
import math


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Paint App")
    clock = pygame.time.Clock()

    
    radius = 15          # Brush radius / shape border thickness
    # Available tools (keys 1-9 cycle through them)
    tool = 'brush'       # Active tool name

    colors = [
        (0,   0,   255),  # 0 Blue
        (255, 0,   0),    # 1 Red
        (0,   255, 0),    # 2 Green
        (255, 255, 255),  # 3 White
        (255, 255, 0),    # 4 Yellow
        (255, 128, 0),    # 5 Orange
        (180, 0,   255),  # 6 Purple
        (0,   255, 255),  # 7 Cyan
    ]
    color_index = 0      # Index of the currently selected color

    # Every finished shape/stroke is stored here and re-drawn every frame.
    objects = []

    current_shape_start = None   # Mouse position where the drag began
    drawing = False              # True while left mouse button is held

    while True:
        # Clear the canvas with black each frame
        screen.fill((0, 0, 0))

        # Event handling
        for event in pygame.event.get():

            # ---- Quit ----
            if event.type == pygame.QUIT:
                return

            # ---- Keyboard ----
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                # Color shortcuts
                if   event.key == pygame.K_r: color_index = 1   # Red
                elif event.key == pygame.K_g: color_index = 2   # Green
                elif event.key == pygame.K_b: color_index = 0   # Blue

                # Cycle through all colors with '0'
                elif event.key == pygame.K_0:
                    color_index = (color_index + 1) % len(colors)

                # Tool shortcuts (1–9)
                if   event.key == pygame.K_1: tool = 'brush'
                elif event.key == pygame.K_2: tool = 'rectangle'
                elif event.key == pygame.K_3: tool = 'circle'
                elif event.key == pygame.K_4: tool = 'eraser'
                elif event.key == pygame.K_5: tool = 'square'
                elif event.key == pygame.K_6: tool = 'right_triangle'
                elif event.key == pygame.K_7: tool = 'equilateral_triangle'
                elif event.key == pygame.K_8: tool = 'rhombus'

                # Undo last stroke / shape with Ctrl+Z
                elif event.key == pygame.K_z and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    if objects:
                        objects.pop()

            # ---- Mouse button down ----
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:          # Left click → start drawing
                    drawing = True
                    current_shape_start = event.pos
                    active_color = (0, 0, 0) if tool == 'eraser' else colors[color_index]

                    # Brush and eraser draw continuously, so start a stroke now
                    if tool in ('brush', 'eraser'):
                        objects.append({
                            'type':   'line',
                            'points': [event.pos],
                            'color':  active_color,
                            'radius': radius,
                        })

                elif event.button == 4:        # Scroll up  increase radius
                    radius = min(200, radius + 2)
                elif event.button == 5:        # Scroll down  decrease radius
                    radius = max(1,   radius - 2)

            #  Mouse button up
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    active_color = (0, 0, 0) if tool == 'eraser' else colors[color_index]

                    # All shape tools: record the final object on mouse release
                    if tool not in ('brush', 'eraser'):
                        objects.append({
                            'type':   tool,
                            'start':  current_shape_start,
                            'end':    event.pos,
                            'color':  active_color,
                            'radius': radius,
                        })

                    drawing = False
                    current_shape_start = None

            #Mouse motion 
            if event.type == pygame.MOUSEMOTION and drawing:
                # Brush/eraser: keep appending points to the current stroke
                if tool in ('brush', 'eraser'):
                    objects[-1]['points'].append(event.pos)

        # Render all committed objects
        for obj in objects:
            draw_object(screen, obj)

        # Live preview: show shape while the user is still dragging
        if drawing and current_shape_start and tool not in ('brush', 'eraser'):
            mouse_pos    = pygame.mouse.get_pos()
            active_color = colors[color_index]
            temp_obj = {
                'type':   tool,
                'start':  current_shape_start,
                'end':    mouse_pos,
                'color':  active_color,
                'radius': radius,
            }
            draw_object(screen, temp_obj)

        # HUD overlay
        display_info(screen, tool, colors[color_index], radius)

        pygame.display.flip()
        clock.tick(60)


# Shape drawing dispatcher
def draw_object(screen, obj):
    """
    Dispatch to the correct drawing routine based on obj['type'].
    Every object dict contains at minimum: type, color, radius.
    Shape objects also have: start, end.
    Brush/eraser objects have: points (list of (x,y)).
    """
    t = obj['type']

    if t == 'line':
        draw_line(screen, obj)
    elif t == 'rectangle':
        draw_rectangle(screen, obj)
    elif t == 'circle':
        draw_circle(screen, obj)
    elif t == 'square':
        draw_square(screen, obj)
    elif t == 'right_triangle':
        draw_right_triangle(screen, obj)
    elif t == 'equilateral_triangle':
        draw_equilateral_triangle(screen, obj)
    elif t == 'rhombus':
        draw_rhombus(screen, obj)


# Individual shape renderers

def draw_line(screen, obj):
    """
    Render a freehand brush / eraser stroke.
    Connects consecutive points with lines and caps each joint with a circle
    so the stroke looks smooth and continuous.
    """
    pts    = obj['points']
    color  = obj['color']
    r      = obj['radius']

    for i in range(len(pts) - 1):
        pygame.draw.line(screen, color, pts[i], pts[i + 1], r * 2)
        pygame.draw.circle(screen, color, pts[i], r)   # smooth joint
    # Cap the very last point
    if pts:
        pygame.draw.circle(screen, color, pts[-1], r)


def draw_rectangle(screen, obj):
    """
    Draw an axis-aligned rectangle outline.
    start and end are opposite corners dragged by the user.
    Border thickness = obj['radius'].
    """
    x1, y1 = obj['start']
    x2, y2 = obj['end']
    rect = pygame.Rect(
        min(x1, x2), min(y1, y2),
        abs(x1 - x2), abs(y1 - y2)
    )
    pygame.draw.rect(screen, obj['color'], rect, max(1, obj['radius']))


def draw_circle(screen, obj):
    """
    Draw a circle whose center is 'start' and radius is the
    Euclidean distance from start to end (the drag endpoint).
    """
    x1, y1 = obj['start']
    x2, y2 = obj['end']
    dist = int(math.hypot(x2 - x1, y2 - y1))
    if dist > 0:
        pygame.draw.circle(screen, obj['color'], (x1, y1), dist, max(1, obj['radius']))


def draw_square(screen, obj):
    """
    Draw an axis-aligned square.
    The side length is determined by the LARGER of Δx or Δy so the shape
    always stays perfectly square regardless of drag direction.
    The square grows from 'start' toward 'end', preserving sign.
    """
    x1, y1 = obj['start']
    x2, y2 = obj['end']

    dx = x2 - x1
    dy = y2 - y1

    # Use the larger delta for the side so the square fills the drag nicely
    side = max(abs(dx), abs(dy))

    # Preserve the drag direction on each axis
    sx = side if dx >= 0 else -side
    sy = side if dy >= 0 else -side

    # Build a normalised pygame.Rect (handles negative width/height)
    rect = pygame.Rect(
        min(x1, x1 + sx), min(y1, y1 + sy),
        side, side
    )
    pygame.draw.rect(screen, obj['color'], rect, max(1, obj['radius']))


def draw_right_triangle(screen, obj):
    """
    Draw a right-angled triangle.
    The right angle is always at 'start'.
    The three vertices are:
      A = start                 (right-angle corner)
      B = (end_x, start_y)     (horizontal leg endpoint)
      C = end                   (hypotenuse corner / diagonal vertex)
    This gives a classic right triangle that follows the drag box.
    """
    x1, y1 = obj['start']
    x2, y2 = obj['end']

    A = (x1, y1)   # right-angle vertex
    B = (x2, y1)   # horizontal leg endpoint
    C = (x2, y2)   # vertical leg / hypotenuse endpoint

    pygame.draw.polygon(screen, obj['color'], [A, B, C], max(1, obj['radius']))


def draw_equilateral_triangle(screen, obj):
    """
    Draw an equilateral triangle (all sides equal, all angles 60°).
    The base runs horizontally from start to end (projected onto x-axis).
    The apex is placed above / below the midpoint of the base at the
    mathematically correct height h = side * sqrt(3) / 2.
    The apex leans toward end_y so the user can flip it by dragging up or down.
    """
    x1, y1 = obj['start']
    x2, y2 = obj['end']

    # Base goes from start to (end_x, start_y) — always horizontal
    base_len = abs(x2 - x1)
    if base_len == 0:
        return  # Nothing to draw yet

    # Height of an equilateral triangle with the given base
    height = int(base_len * math.sqrt(3) / 2)

    # Mid-point of the base
    mid_x = (x1 + x2) // 2

    # Apex direction: above base if user drags upward, below if downward
    apex_y = y1 - height if y2 < y1 else y1 + height

    A = (x1, y1)         # left  base vertex
    B = (x2, y1)         # right base vertex
    C = (mid_x, apex_y)  # apex

    pygame.draw.polygon(screen, obj['color'], [A, B, C], max(1, obj['radius']))


def draw_rhombus(screen, obj):
    """
    Draw a rhombus (diamond) defined by its two diagonals.
    The bounding box is the rectangle from start to end.
    The four vertices sit at the midpoints of each side of that box:
      Top    = (mid_x, top_y)
      Right  = (right_x, mid_y)
      Bottom = (mid_x, bottom_y)
      Left   = (left_x, mid_y)
    This ensures all four sides are equal in length (true rhombus).
    """
    x1, y1 = obj['start']
    x2, y2 = obj['end']

    # Bounding-box extents
    left_x   = min(x1, x2)
    right_x  = max(x1, x2)
    top_y    = min(y1, y2)
    bottom_y = max(y1, y2)

    # Midpoints
    mid_x = (left_x + right_x) // 2
    mid_y = (top_y  + bottom_y) // 2

    top    = (mid_x,   top_y)
    right  = (right_x, mid_y)
    bottom = (mid_x,   bottom_y)
    left   = (left_x,  mid_y)

    pygame.draw.polygon(screen, obj['color'],
                        [top, right, bottom, left], max(1, obj['radius']))


# HUD / info bar

# Human-readable labels for each tool key
TOOL_KEYS = {
    'brush':                '1',
    'rectangle':            '2',
    'circle':               '3',
    'eraser':               '4',
    'square':               '5',
    'right_triangle':       '6',
    'equilateral_triangle': '7',
    'rhombus':              '8',
}

def display_info(screen, tool, color, radius):
    """
    Render a two-line HUD at the top-left corner showing:
      Line 1 – active tool, current color RGB, brush radius
      Line 2 – quick reference for all tool shortcuts
    A small color swatch is drawn next to the tool name.
    """
    font      = pygame.font.SysFont("Consolas", 16)
    font_hint = pygame.font.SysFont("Consolas", 13)

    # Line 1: current settings
    line1 = (f"Tool: {tool.upper()} [{TOOL_KEYS.get(tool,'?')}]"
             f"  |  Color: {color}  |  Radius: {radius}"
             f"  |  Ctrl+Z: Undo  |  0: Cycle color")
    img1  = font.render(line1, True, (255, 255, 255))
    screen.blit(img1, (50, 8))   # leave 50 px for the color swatch

    # Color swatch
    pygame.draw.rect(screen, color,        (10, 8,  34, 18))
    pygame.draw.rect(screen, (200,200,200),(10, 8,  34, 18), 1)  # border

    # Line 2: shortcut hint
    hint = ("1:Brush  2:Rect  3:Circle  4:Eraser  "
            "5:Square  6:RightTri  7:EqTri  8:Rhombus"
            "  |  R/G/B: color  |  Scroll: size")
    img2 = font_hint.render(hint, True, (180, 180, 180))
    screen.blit(img2, (10, 28))


if __name__ == "__main__":
    main()