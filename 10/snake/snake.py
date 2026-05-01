import pygame
import sys
import random
# PYGAME INITIALIZATION
pygame.init()

# CONSTANTS
CELL      = 20
COLS      = 30
ROWS      = 28
WIDTH     = CELL * COLS
HEIGHT    = CELL * ROWS
UI_HEIGHT = 50
WIN_W     = WIDTH
WIN_H     = HEIGHT + UI_HEIGHT

#BG,snake and other stuffs color
GRASS_BG   = (34,  139, 34 )   # Forest green background
GRASS_ALT  = (44,  160, 44 )   # Slightly lighter green for checker pattern
UI_BG      = (0,   100, 0  )   # Dark green UI bar
UI_BORDER  = (0,   80,  0  )   # UI bar bottom border
WALL_COL   = (20,  80,  20 )   # Dark green walls

SNAKE_HEAD = (220, 30,  30 )   # Bright red head
SNAKE_BODY = (180, 20,  20 )   # Darker red body

FOOD_COL   = (255, 255, 0  )   # Yellow food (stands out on green)
TEXT_COL   = (255, 255, 255)   # White text
GOLD       = (255, 220, 50 )   # Gold for level-up flash

# Level settings
LEVELS = [
    (3,  8 ),
    (6,  10),
    (10, 13),
    (15, 16),
    (21, 20),
    (28, 25),
    (36, 30),
]
MAX_LEVEL = len(LEVELS)

# WINDOW
screen = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# FONTS
font_big    = pygame.font.SysFont("Consolas", 36, bold=True)
font_medium = pygame.font.SysFont("Consolas", 22, bold=True)
font_small  = pygame.font.SysFont("Consolas", 17)


# HELPER — grid cell to pixel rect
def cell_rect(col, row):
    """Returns the pygame.Rect for a grid cell at (col, row)"""
    return pygame.Rect(col * CELL, UI_HEIGHT + row * CELL, CELL, CELL)


# DRAW BACKGROUND
# Simple checkerboard pattern in two shades of grass green
def draw_background():
    for c in range(COLS):
        for r in range(ROWS):
            # Alternate between two green shades like a grass field
            color = GRASS_BG if (c + r) % 2 == 0 else GRASS_ALT
            pygame.draw.rect(screen, color, cell_rect(c, r))


# DRAW WALLS
# Solid dark green border around the play area
def draw_walls():
    for c in range(COLS):
        pygame.draw.rect(screen, WALL_COL, cell_rect(c, 0))
        pygame.draw.rect(screen, WALL_COL, cell_rect(c, ROWS - 1))
    for r in range(ROWS):
        pygame.draw.rect(screen, WALL_COL, cell_rect(0, r))
        pygame.draw.rect(screen, WALL_COL, cell_rect(COLS - 1, r))


# DRAW SNAKE
# Red head, darker red body — plain filled rectangles
def draw_snake(snake):
    for i, (c, r) in enumerate(snake):
        color = SNAKE_HEAD if i == 0 else SNAKE_BODY
        # Fill the full cell with a tiny margin so segments look separate
        rect = cell_rect(c, r).inflate(-2, -2)
        pygame.draw.rect(screen, color, rect, border_radius=3)


# DRAW FOOD
# Yellow circle centered in the cell
def draw_food(food):
    c, r   = food
    rect   = cell_rect(c, r)
    pygame.draw.circle(screen, FOOD_COL, rect.center, CELL // 2 - 3)


# DRAW UI BAR
# Dark green bar at the top showing score, level and progress
def draw_ui(score, level, food_eaten, level_up_timer):
    # Bar background
    pygame.draw.rect(screen, UI_BG, (0, 0, WIN_W, UI_HEIGHT))
    # Bottom border line
    pygame.draw.line(screen, UI_BORDER, (0, UI_HEIGHT), (WIN_W, UI_HEIGHT), 3)

    # Score (left)
    score_surf = font_medium.render(f"SCORE: {score}", True, TEXT_COL)
    screen.blit(score_surf, (16, 13))

    # Level (center) — flashes gold on level-up
    col      = GOLD if level_up_timer > 0 else TEXT_COL
    lvl_text = f"LEVEL: {level}" if level < MAX_LEVEL else f"LEVEL: {level} MAX"
    lvl_surf = font_medium.render(lvl_text, True, col)
    screen.blit(lvl_surf, (WIN_W // 2 - lvl_surf.get_width() // 2, 13))

    # Progress to next level (right)
    if level < MAX_LEVEL:
        needed   = LEVELS[level - 1][0]
        progress = f"Next: {food_eaten}/{needed}"
    else:
        progress = "Max level!"
    prog_surf = font_small.render(progress, True, TEXT_COL)
    screen.blit(prog_surf, (WIN_W - prog_surf.get_width() - 16, 16))


# SPAWN FOOD
# Random cell that is not a wall and not on the snake
def spawn_food(snake):
    while True:
        col = random.randint(1, COLS - 2)
        row = random.randint(1, ROWS - 2)
        if (col, row) not in snake:
            return (col, row)


# WALL COLLISION CHECK
def hit_wall(head):
    """Returns True if head is on a border wall cell"""
    c, r = head
    return c <= 0 or c >= COLS - 1 or r <= 0 or r >= ROWS - 1


# GAME OVER SCREEN
def game_over_screen(score, level):
    # Semi-transparent dark overlay
    overlay = pygame.Surface((WIN_W, WIN_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    go   = font_big.render("GAME  OVER", True, (220, 50, 50))
    sc   = font_medium.render(f"Score: {score}     Level: {level}", True, TEXT_COL)
    hint = font_small.render("SPACE — restart       ESC — quit", True, TEXT_COL)

    screen.blit(go,   (WIN_W // 2 - go.get_width()   // 2, WIN_H // 2 - 70))
    screen.blit(sc,   (WIN_W // 2 - sc.get_width()   // 2, WIN_H // 2 - 10))
    screen.blit(hint, (WIN_W // 2 - hint.get_width() // 2, WIN_H // 2 + 40))
    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:  return True
                if e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()


# LEVEL-UP SCREEN
# Brief pause showing the new level number
def level_up_screen(new_level):
    overlay = pygame.Surface((WIN_W, WIN_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 130))
    screen.blit(overlay, (0, 0))

    title = font_big.render(f"LEVEL  {new_level}!", True, GOLD)
    sub   = font_medium.render("Speed increased!", True, TEXT_COL)
    screen.blit(title, (WIN_W // 2 - title.get_width() // 2, WIN_H // 2 - 40))
    screen.blit(sub,   (WIN_W // 2 - sub.get_width()   // 2, WIN_H // 2 + 20))
    pygame.display.flip()
    pygame.time.wait(1200)


# NEW GAME STATE
def new_game():
    start_col = COLS // 2
    start_row = ROWS // 2
    snake = [
        (start_col,     start_row),
        (start_col - 1, start_row),
        (start_col - 2, start_row),
    ]
    return {
        "snake":      snake,
        "direction":  (1, 0),
        "next_dir":   (1, 0),
        "food":       spawn_food(snake),
        "score":      0,
        "level":      1,
        "food_eaten": 0,
        "speed":      LEVELS[0][1],
        "lvl_timer":  0,
    }


# GAME LOOP
def main():
    state = new_game()

    while True:

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                dc, dr = state["direction"]
                # Arrow keys — prevent reversing into itself
                if event.key == pygame.K_UP    and dr != 1:  state["next_dir"] = (0, -1)
                if event.key == pygame.K_DOWN  and dr != -1: state["next_dir"] = (0,  1)
                if event.key == pygame.K_LEFT  and dc != 1:  state["next_dir"] = (-1, 0)
                if event.key == pygame.K_RIGHT and dc != -1: state["next_dir"] = (1,  0)
                # WASD alternative controls(Because i am used to WASD and arrow keys are small on laptop)
                if event.key == pygame.K_w and dr != 1:  state["next_dir"] = (0, -1)
                if event.key == pygame.K_s and dr != -1: state["next_dir"] = (0,  1)
                if event.key == pygame.K_a and dc != 1:  state["next_dir"] = (-1, 0)
                if event.key == pygame.K_d and dc != -1: state["next_dir"] = (1,  0)

        # Apply direction
        state["direction"] = state["next_dir"]
        dc, dr = state["direction"]

        # New head position
        hc, hr   = state["snake"][0]
        new_head = (hc + dc, hr + dr)

        # Wall collision -> game over
        if hit_wall(new_head):
            if game_over_screen(state["score"], state["level"]):
                state = new_game()
            continue

        # Self collision -> game over
        if new_head in state["snake"]:
            if game_over_screen(state["score"], state["level"]):
                state = new_game()
            continue

        # Move: add new head
        state["snake"].insert(0, new_head)

        # Food eaten
        if new_head == state["food"]:
            state["score"]      += 10
            state["food_eaten"] += 1
            state["food"]        = spawn_food(state["snake"])  # Respawn food

            # Level-up check
            lvl = state["level"]
            if lvl < MAX_LEVEL:
                if state["food_eaten"] >= LEVELS[lvl - 1][0]:
                    state["level"]    += 1
                    state["speed"]     = LEVELS[state["level"] - 1][1]
                    state["lvl_timer"] = 60
                    level_up_screen(state["level"])
            # Tail NOT removed -> snake grows by 1
        else:
            # No food -> remove tail to keep length constant
            state["snake"].pop()

        # Level-up flash timer countdown
        if state["lvl_timer"] > 0:
            state["lvl_timer"] -= 1

        # Draw everything
        draw_background()                  # Green checkerboard grass
        draw_walls()                       # Dark green border
        draw_food(state["food"])           # Yellow circle
        draw_snake(state["snake"])         # Red snake
        draw_ui(state["score"],            # Green UI bar on top
                state["level"],
                state["food_eaten"],
                state["lvl_timer"])

        pygame.display.flip()
        clock.tick(state["speed"])


# ENTRY POINT
if __name__ == "__main__":
    main()