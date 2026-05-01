import pygame
import random
import math

pygame.init()

# Constants
WIDTH = 600
HEIGHT = 600
CELL = 30
FPS_BASE = 5
FPS_INCREMENT = 2
FOOD_PER_LEVEL = 3
MAX_FOODS_ON_SCREEN = 3   # how many food items can exist simultaneously

#Colors
colorBLACK  = (0, 0, 0)
colorWHITE  = (255, 255, 255)
colorGRAY   = (50, 50, 50)
colorRED    = (220, 50, 50)
colorYELLOW = (240, 200, 50)
colorGREEN  = (50, 200, 80)
colorBLUE   = (50, 120, 220)
colorORANGE = (255, 140, 0)
colorPURPLE = (180, 60, 220)
colorCYAN   = (0, 210, 210)
colorPINK   = (255, 80, 160)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

font_big   = pygame.font.SysFont("monospace", 32, bold=True)
font_small = pygame.font.SysFont("monospace", 20)
font_tiny  = pygame.font.SysFont("monospace", 13, bold=True)


# Food type definitions
# Each entry: (name, points, color, weight, lifetime_ms or None, symbol)
#   weight       – relative probability of being chosen (higher = more common)
#   lifetime_ms  – milliseconds before this food disappears (None = permanent)
FOOD_TYPES = [
    # name       pts  color         weight  lifetime  symbol
    ("Common",    1,  colorGREEN,    50,    None,      "●"),   # always here
    ("Silver",    2,  colorCYAN,     25,    8000,      "★"),   # 8 s
    ("Gold",      3,  colorYELLOW,   12,    6000,      "✦"),   # 6 s
    ("Ruby",      5,  colorRED,       8,    5000,      "♦"),   # 5 s
    ("Amethyst",  8,  colorPURPLE,    4,    4000,      "◆"),   # 4 s
    ("Neon",     15,  colorPINK,      1,    3000,      "⬟"),   # 3 s – rare!
]

# Pre-compute cumulative weights for weighted random selection
_WEIGHTS = [ft[3] for ft in FOOD_TYPES]
_TOTAL_W = sum(_WEIGHTS)


def pick_food_type():
    """Return a random FOOD_TYPES index using weighted probability."""
    r = random.randint(1, _TOTAL_W)
    cumulative = 0
    for i, w in enumerate(_WEIGHTS):
        cumulative += w
        if r <= cumulative:
            return i
    return 0


def draw_grid():
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colorGRAY,
                             (i * CELL, j * CELL, CELL, CELL), 1)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"{self.x}, {self.y}"


class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def is_out_of_bounds(self):
        head = self.body[0]
        return (head.x < 0 or head.x >= WIDTH  // CELL or
                head.y < 0 or head.y >= HEIGHT // CELL)

    def is_self_collision(self):
        head = self.body[0]
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False

    def occupies(self, x, y):
        return any(s.x == x and s.y == y for s in self.body)

    def grow(self):
        tail = self.body[-1]
        self.body.append(Point(tail.x, tail.y))

    def draw(self):
        head = self.body[0]
        # Head: draw with eye details
        hx, hy = head.x * CELL, head.y * CELL
        pygame.draw.rect(screen, colorRED, (hx, hy, CELL, CELL))
        pygame.draw.rect(screen, (255, 100, 100), (hx + 2, hy + 2, CELL - 4, CELL - 4))
        for segment in self.body[1:]:
            sx, sy = segment.x * CELL, segment.y * CELL
            pygame.draw.rect(screen, colorYELLOW, (sx, sy, CELL, CELL))
            pygame.draw.rect(screen, (200, 160, 20), (sx + 3, sy + 3, CELL - 6, CELL - 6))


class Food:
    """
    A single food item.  Each has a type (index into FOOD_TYPES),
    an optional expiry time, and an animated pulse for visibility.
    """

    def __init__(self, snake, existing_foods, type_index=None):
        name, pts, color, weight, lifetime_ms, symbol = FOOD_TYPES[
            type_index if type_index is not None else pick_food_type()
        ]
        self.name       = name
        self.points     = pts
        self.color      = color
        self.lifetime   = lifetime_ms          # None = immortal
        self.symbol     = symbol
        self.spawn_time = pygame.time.get_ticks()
        self.pos        = Point(-1, -1)
        self._place(snake, existing_foods)

    def _place(self, snake, existing_foods):
        occupied = set()
        for s in snake.body:
            occupied.add((s.x, s.y))
        for f in existing_foods:
            occupied.add((f.pos.x, f.pos.y))

        for _ in range(500):                   # max attempts to avoid infinite loop
            x = random.randint(0, WIDTH  // CELL - 1)
            y = random.randint(0, HEIGHT // CELL - 1)
            if (x, y) not in occupied:
                self.pos.x = x
                self.pos.y = y
                return
        # Fallback: just place anywhere not on the snake
        while True:
            x = random.randint(0, WIDTH  // CELL - 1)
            y = random.randint(0, HEIGHT // CELL - 1)
            if not snake.occupies(x, y):
                self.pos.x = x
                self.pos.y = y
                return

    def is_expired(self):
        if self.lifetime is None:
            return False
        return pygame.time.get_ticks() - self.spawn_time >= self.lifetime

    def time_left_ms(self):
        if self.lifetime is None:
            return None
        elapsed = pygame.time.get_ticks() - self.spawn_time
        return max(0, self.lifetime - elapsed)

    def draw(self):
        now   = pygame.time.get_ticks()
        px    = self.pos.x * CELL
        py    = self.pos.y * CELL

        # Determine alpha / urgency
        tl = self.time_left_ms()
        if tl is not None:
            frac = tl / self.lifetime            # 1.0 → 0.0 as it expires
            # Blink fast in the last 1.5 s
            if tl < 1500:
                blink_rate = 150                  # ms per cycle
                if (now // blink_rate) % 2 == 0:
                    return                        # invisible frame
            # Pulse scale
            pulse = 1.0 + 0.12 * math.sin(now / 200.0)
        else:
            pulse = 1.0 + 0.06 * math.sin(now / 400.0)
            frac  = 1.0

        #Draw outer glow
        glow_color = tuple(min(255, int(c * 0.5)) for c in self.color)
        glow_size  = int(CELL * pulse)
        glow_off   = (CELL - glow_size) // 2
        pygame.draw.rect(screen, glow_color,
                         (px + glow_off - 2, py + glow_off - 2,
                          glow_size + 4, glow_size + 4), border_radius=6)

        #Main body
        body_size = int(CELL * 0.82 * pulse)
        body_off  = (CELL - body_size) // 2
        pygame.draw.rect(screen, self.color,
                         (px + body_off, py + body_off, body_size, body_size),
                         border_radius=5)

        # Symbol label
        sym_surf = font_tiny.render(self.symbol, True, colorBLACK)
        sw, sh = sym_surf.get_size()
        screen.blit(sym_surf, (px + (CELL - sw) // 2, py + (CELL - sh) // 2))

        #Timer bar (only for expiring food)
        if tl is not None:
            bar_w   = CELL - 4
            bar_h   = 4
            bar_x   = px + 2
            bar_y   = py + CELL - bar_h - 1
            # background
            pygame.draw.rect(screen, colorGRAY, (bar_x, bar_y, bar_w, bar_h))
            # fill
            fill_w = int(bar_w * frac)
            if fill_w > 0:
                bar_color = (
                    int(255 * (1 - frac)),
                    int(220 * frac),
                    0
                )
                pygame.draw.rect(screen, bar_color,
                                 (bar_x, bar_y, fill_w, bar_h))

    def check_collision(self, snake):
        head = snake.body[0]
        return head.x == self.pos.x and head.y == self.pos.y


def draw_hud(score, level, fps):
    score_surf = font_small.render(f"Score: {score}", True, colorWHITE)
    level_surf = font_small.render(f"Level: {level}", True, colorORANGE)
    speed_surf = font_small.render(f"Speed: {fps} FPS", True, colorBLUE)
    screen.blit(score_surf, (8, 6))
    screen.blit(level_surf, (8, 28))
    screen.blit(speed_surf, (8, 50))


def draw_legend():
    """Show a compact food legend in the bottom-right corner."""
    x0 = WIDTH - 148
    y0 = HEIGHT - len(FOOD_TYPES) * 16 - 8
    bg = pygame.Surface((144, len(FOOD_TYPES) * 16 + 6), pygame.SRCALPHA)
    bg.fill((0, 0, 0, 140))
    screen.blit(bg, (x0 - 2, y0 - 2))
    for i, (name, pts, color, _, lifetime, symbol) in enumerate(FOOD_TYPES):
        t_label = f"{lifetime//1000}s" if lifetime else "∞"
        line = font_tiny.render(
            f"{symbol} {name:8s} +{pts} {t_label}", True, color
        )
        screen.blit(line, (x0, y0 + i * 16))


def draw_floating_score(text, x, y, color, start_time, duration=800):
    """Return True while still active, False when expired."""
    elapsed = pygame.time.get_ticks() - start_time
    if elapsed >= duration:
        return False
    alpha = max(0, 255 - int(255 * elapsed / duration))
    rise  = int(30 * elapsed / duration)
    surf  = font_small.render(text, True, color)
    surf.set_alpha(alpha)
    screen.blit(surf, (x * CELL, y * CELL - rise))
    return True


def draw_message(title, subtitle=""):
    title_surf = font_big.render(title, True, colorRED)
    sub_surf   = font_small.render(subtitle, True, colorWHITE)
    tw = title_surf.get_width()
    sw = sub_surf.get_width()
    screen.blit(title_surf, ((WIDTH - tw) // 2, HEIGHT // 2 - 40))
    screen.blit(sub_surf,   ((WIDTH - sw) // 2, HEIGHT // 2 + 10))
    pygame.display.flip()
    pygame.time.wait(2000)


def main():
    clock = pygame.time.Clock()

    score         = 0
    level         = 1
    food_in_level = 0
    fps           = FPS_BASE

    snake = Snake()

    # Start with one common food on the board
    foods: list[Food] = [Food(snake, [], type_index=0)]

    # Floating score pop-ups: list of (text, grid_x, grid_y, color, start_ms)
    popups = []

    # Timer: when to potentially spawn a new food item
    last_spawn_check = pygame.time.get_ticks()
    SPAWN_INTERVAL   = 3000   # check every 3 s whether to add a food

    running   = True
    game_over = False

    while running:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_RIGHT and snake.dx == 0:
                        snake.dx, snake.dy = 1, 0
                    elif event.key == pygame.K_LEFT and snake.dx == 0:
                        snake.dx, snake.dy = -1, 0
                    elif event.key == pygame.K_DOWN and snake.dy == 0:
                        snake.dx, snake.dy = 0, 1
                    elif event.key == pygame.K_UP and snake.dy == 0:
                        snake.dx, snake.dy = 0, -1
                else:
                    main()
                    return

        if not game_over:
            now = pygame.time.get_ticks()

            # Remove expired foods (keep at least one common food)
            expired = [f for f in foods if f.is_expired()]
            foods   = [f for f in foods if not f.is_expired()]
            if not foods:
                foods.append(Food(snake, [], type_index=0))

            # Periodically spawn extra food
            if now - last_spawn_check >= SPAWN_INTERVAL:
                last_spawn_check = now
                if len(foods) < MAX_FOODS_ON_SCREEN:
                    # Higher chance of a rare food at higher levels
                    foods.append(Food(snake, foods))

            # Move snake
            snake.move()

            if snake.is_out_of_bounds() or snake.is_self_collision():
                draw_message("GAME OVER", f"Score: {score}  |  Press any key")
                game_over = True
                continue

            #Check food collisions
            eaten_indices = []
            for i, f in enumerate(foods):
                if f.check_collision(snake):
                    eaten_indices.append(i)

            for i in sorted(eaten_indices, reverse=True):
                f = foods.pop(i)
                score         += f.points
                food_in_level += 1
                snake.grow()
                # Floating score popup
                popups.append((f"+{f.points}", f.pos.x, f.pos.y, f.color, now))
                # Ensure at least one common food remains
                if not foods:
                    foods.append(Food(snake, foods, type_index=0))

            # Level-up check
            if food_in_level >= FOOD_PER_LEVEL:
                level         += 1
                food_in_level  = 0
                fps           += FPS_INCREMENT
                draw_message(f"LEVEL {level}!", f"Speed up!  FPS → {fps}")

            # Draw
            screen.fill(colorBLACK)
            draw_grid()

            for f in foods:
                f.draw()

            snake.draw()
            draw_hud(score, level, fps)
            draw_legend()

            # Draw & clean up popups
            popups = [p for p in popups
                      if draw_floating_score(p[0], p[1], p[2], p[3], p[4])]

            pygame.display.flip()

        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()