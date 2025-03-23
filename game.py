sadsadsaddsadimport pygames
import random
import math

pygame.init()

# Set up display
width, height = 600, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pacman Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
pink = (255, 192, 203)
orange = (255, 165, 0)
blue = (0, 0, 255)
green = (0, 255, 0)  # For stun projectiles

# Game variables
block_size = 20
score = 0
high_score = 0

# Ammo variables
max_ammo = 10
ammo = max_ammo
ammo_recharge_score = 50  # Score needed to recharge 1 ammo
last_recharge_score = 0

# Invincibility variables
invincible = False
invincibility_duration = 3  # seconds
invincibility_start_time = 0

# Font
font = pygame.font.SysFont("Courier", 24)

# Pacman
pacman_pos = [width / 2, height / 2]
pacman_direction = "STOP"
pacman_speed = 300  # Increased to 300 pixels per second

# Projectile settings
projectile_speed = 250  # pixels per second
projectile_radius = 5
projectile_color = blue
projectiles = []  # List to hold all active projectiles

# Stun Projectile settings
stun_projectile_speed = 300
stun_projectile_radius = 7
stun_projectile_color = green
stun_projectiles = []

# Gun cooldown
gun_cooldown = 0.5  # seconds
last_shot_time = 0

# Ghosts with different personalities and speeds
ghosts = [
    {"pos": [100.0, 100.0], "color": red, "speed": 150, "personality": "chase", "last_shot_time": 0, "stunned": False, "stun_end_time": 0},
    {"pos": [500.0, 100.0], "color": pink, "speed": 110, "personality": "ambush", "last_shot_time": 0, "stunned": False, "stun_end_time": 0},
    {"pos": [500.0, 500.0], "color": orange, "speed": 100, "personality": "scatter", "last_shot_time": 0, "stunned": False, "stun_end_time": 0}
]

# Food
food = (
    random.randint(0, (width - block_size) // block_size) * block_size,
    random.randint(0, (height - block_size) // block_size) * block_size
)

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 120

# Functions
def draw_pacman(pos):
    pygame.draw.circle(win, yellow, (int(pos[0]), int(pos[1])), block_size // 2)

def draw_ghosts(ghosts):
    for ghost in ghosts:
        if ghost["stunned"]:
            color = white  # Change color when stunned
        else:
            color = ghost["color"]
        pygame.draw.circle(win, color, (int(ghost["pos"][0]), int(ghost["pos"][1])), block_size // 2)

def draw_food(food):
    pygame.draw.rect(win, white, (*food, block_size, block_size))

def draw_projectiles(projectiles, color):
    for proj in projectiles:
        pygame.draw.circle(win, color, (int(proj['x']), int(proj['y'])), proj['radius'])

def move_pacman(pos, direction, delta_time):
    if direction == "UP":
        pos[1] -= pacman_speed * delta_time
    elif direction == "DOWN":
        pos[1] += pacman_speed * delta_time
    elif direction == "LEFT":
        pos[0] -= pacman_speed * delta_time
    elif direction == "RIGHT":
        pos[0] += pacman_speed * delta_time

    # Keep Pacman within bounds
    pos[0] = max(0, min(width - block_size, pos[0]))
    pos[1] = max(0, min(height - block_size, pos[1]))

def move_ghosts(ghosts, pacman_pos, pacman_direction, delta_time):
    for ghost in ghosts:
        if ghost["stunned"]:
            if pygame.time.get_ticks() / 1000.0 >= ghost["stun_end_time"]:
                ghost["stunned"] = False
            else:
                continue  # Skip movement if stunned

        if ghost["personality"] == "chase":
            # Move towards Pacman
            direction = get_direction_vector(ghost["pos"], pacman_pos)
            ghost["pos"][0] += direction[0] * ghost["speed"] * delta_time
            ghost["pos"][1] += direction[1] * ghost["speed"] * delta_time

        elif ghost["personality"] == "ambush":
            # Target a position ahead of Pacman
            offset = block_size * 2
            target_x = pacman_pos[0] + (offset if pacman_direction == "RIGHT" else -offset if pacman_direction == "LEFT" else 0)
            target_y = pacman_pos[1] + (offset if pacman_direction == "DOWN" else -offset if pacman_direction == "UP" else 0)
            target_x = max(0, min(width - block_size, target_x))
            target_y = max(0, min(height - block_size, target_y))

            direction = get_direction_vector(ghost["pos"], [target_x, target_y])
            ghost["pos"][0] += direction[0] * ghost["speed"] * delta_time
            ghost["pos"][1] += direction[1] * ghost["speed"] * delta_time

        elif ghost["personality"] == "scatter":
            # Move towards a corner
            if ghost["color"] == orange:
                corner = [0, 0]
            else:
                corner = [width - block_size, height - block_size]
            
            direction = get_direction_vector(ghost["pos"], corner)
            ghost["pos"][0] += direction[0] * ghost["speed"] * delta_time
            ghost["pos"][1] += direction[1] * ghost["speed"] * delta_time

def get_direction_vector(src, dest):
    dx = dest[0] - src[0]
    dy = dest[1] - src[1]
    distance = math.hypot(dx, dy)
    if distance == 0:
        return (0, 0)
    return (dx / distance, dy / distance)

def shoot_projectiles(ghosts, current_time):
    shot_cooldown = random.randint(1, 7)  # seconds between shots
    for ghost in ghosts:
        if current_time - ghost["last_shot_time"] >= shot_cooldown and not ghost["stunned"]:
            direction = get_direction_vector(ghost["pos"], pacman_pos)
            projectile = {
                "x": ghost["pos"][0],
                "y": ghost["pos"][1],
                "dx": direction[0],
                "dy": direction[1],
                "speed": projectile_speed,
                "radius": projectile_radius
            }
            projectiles.append(projectile)
            ghost["last_shot_time"] = current_time

def move_projectiles(projectiles, delta_time):
    for proj in projectiles[:]:
        proj["x"] += proj["dx"] * proj["speed"] * delta_time
        proj["y"] += proj["dy"] * proj["speed"] * delta_time

        # Remove projectile if it goes out of bounds
        if proj["x"] < 0 or proj["x"] > width or proj["y"] < 0 or proj["y"] > height:
            projectiles.remove(proj)

def check_projectile_collision(projectiles, pacman_pos):
    pac_rect = pygame.Rect(pacman_pos[0], pacman_pos[1], block_size, block_size)
    for proj in projectiles:
        proj_rect = pygame.Rect(proj["x"] - proj["radius"], proj["y"] - proj["radius"], proj["radius"] * 2, proj["radius"] * 2)
        if pac_rect.colliderect(proj_rect):
            return True
    return False

def check_stun_collision(stun_projectiles, ghosts):
    for stun_proj in stun_projectiles:
        stun_rect = pygame.Rect(stun_proj['x'] - stun_proj['radius'], stun_proj['y'] - stun_proj['radius'], stun_proj['radius'] * 2, stun_proj['radius'] * 2)
        for ghost in ghosts:
            ghost_rect = pygame.Rect(ghost["pos"][0], ghost["pos"][1], block_size, block_size)
            if ghost_rect.colliderect(stun_rect) and not ghost["stunned"]:
                ghost["stunned"] = True
                ghost["stun_end_time"] = pygame.time.get_ticks() / 1000.0 + 5  # Stunned for 5 seconds
                if stun_proj in stun_projectiles:
                    stun_projectiles.remove(stun_proj)

def check_collision(pacman_pos, ghosts):
    if invincible:
        return False  # Ignore collisions if invincible
    pac_rect = pygame.Rect(pacman_pos[0], pacman_pos[1], block_size, block_size)
    for ghost in ghosts:
        ghost_rect = pygame.Rect(ghost["pos"][0], ghost["pos"][1], block_size, block_size)
        if pac_rect.colliderect(ghost_rect):
            return True
    return False

def display_score(score, high_score, ammo):
    text = font.render(f"Score: {score}  High Score: {high_score}  Ammo: {ammo}", True, white)
    win.blit(text, [0, 0])

# Main game loop
running = True
while running:
    delta_time = clock.tick(FPS) / 1000.0  # Time in seconds since last tick
    current_time = pygame.time.get_ticks() / 1000.0  # Current time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                pacman_direction = "UP"
            elif event.key == pygame.K_s:
                pacman_direction = "DOWN"
            elif event.key == pygame.K_a:
                pacman_direction = "LEFT"
            elif event.key == pygame.K_d:
                pacman_direction = "RIGHT"
            elif event.key == pygame.K_SPACE:
                if ammo > 0 and current_time - last_shot_time >= gun_cooldown:
                    # Shoot stun projectile
                    direction = get_direction_vector(pacman_pos, pacman_pos)  # Placeholder, set actual direction
                    # For simplicity, shoot upwards
                    stun_direction = (0, -1)
                    stun_proj = {
                        "x": pacman_pos[0],
                        "y": pacman_pos[1],
                        "dx": stun_direction[0],
                        "dy": stun_direction[1],
                        "speed": stun_projectile_speed,
                        "radius": stun_projectile_radius,
                        "color": stun_projectile_color
                    }
                    stun_projectiles.append(stun_proj)
                    ammo -= 1
                    last_shot_time = current_time

    # Move Pacman
    if pacman_direction != "STOP":
        move_pacman(pacman_pos, pacman_direction, delta_time)

    # Move ghosts
    move_ghosts(ghosts, pacman_pos, pacman_direction, delta_time)

    # Ghosts shoot projectiles
    shoot_projectiles(ghosts, current_time)

    # Move projectiles
    move_projectiles(projectiles, delta_time)

    # Move stun projectiles
    for stun_proj in stun_projectiles[:]:
        stun_proj['x'] += stun_proj['dx'] * stun_proj['speed'] * delta_time
        stun_proj['y'] += stun_proj['dy'] * stun_proj['speed'] * delta_time
        # Remove if out of bounds
        if stun_proj['x'] < 0 or stun_proj['x'] > width or stun_proj['y'] < 0 or stun_proj['y'] > height:
            stun_projectiles.remove(stun_proj)

    # Check collision with ghosts
    if check_collision(pacman_pos, ghosts):
        time.sleep(1)
        pacman_pos = [width / 2, height / 2]
        pacman_direction = "STOP"
        score = 0
        projectiles.clear()
        stun_projectiles.clear()
        # Reset ghosts positions and states
        ghosts = [
            {"pos": [100.0, 100.0], "color": red, "speed": 150, "personality": "chase", "last_shot_time": 0, "stunned": False, "stun_end_time": 0},
            {"pos": [500.0, 100.0], "color": pink, "speed": 110, "personality": "ambush", "last_shot_time": 0, "stunned": False, "stun_end_time": 0},
            {"pos": [500.0, 500.0], "color": orange, "speed": 100, "personality": "scatter", "last_shot_time": 0, "stunned": False, "stun_end_time": 0}
        ]
        invincible = False

    # Check collision with projectiles
    if check_projectile_collision(projectiles, pacman_pos) and not invincible:
        time.sleep(1)
        pacman_pos = [width / 2, height / 2]
        pacman_direction = "STOP"
        score = 0
        projectiles.clear()
        stun_projectiles.clear()
        # Reset ghosts positions and states
        ghosts = [
            {"pos": [100.0, 100.0], "color": red, "speed": 150, "personality": "chase", "last_shot_time": 0, "stunned": False, "stun_end_time": 0},
            {"pos": [500.0, 100.0], "color": pink, "speed": 110, "personality": "ambush", "last_shot_time": 0, "stunned": False, "stun_end_time": 0},
            {"pos": [500.0, 500.0], "color": orange, "speed": 100, "personality": "scatter", "last_shot_time": 0, "stunned": False, "stun_end_time": 0}
        ]
        invincible = False

    # Check collision of stun projectiles with ghosts
    check_stun_collision(stun_projectiles, ghosts)

    # Check if Pacman eats food
    pac_rect = pygame.Rect(pacman_pos[0], pacman_pos[1], block_size, block_size)
    food_rect = pygame.Rect(food[0], food[1], block_size, block_size)
    if pac_rect.colliderect(food_rect):
        score += 10
        # Handle high score
        if score > high_score:
            high_score = score
        # Recharge ammo based on score
        if score - last_recharge_score >= ammo_recharge_score:
            ammo = min(max_ammo, ammo + 1)
            last_recharge_score = score
        # Start invincibility
        invincible = True
        invincibility_start_time = current_time
        food = (
            random.randint(0, (width - block_size) // block_size) * block_size,
            random.randint(0, (height - block_size) // block_size) * block_size
        )

    # Handle invincibility duration
    if invincible and current_time - invincibility_start_time >= invincibility_duration:
        invincible = False

    # Draw everything
    win.fill(black)
    draw_pacman(pacman_pos)
    draw_ghosts(ghosts)
    draw_food(food)
    draw_projectiles(projectiles, projectile_color)
    draw_projectiles(stun_projectiles, stun_projectile_color)
    display_score(score, high_score, ammo)
    pygame.display.flip()

pygame.quit()