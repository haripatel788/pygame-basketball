import pygame
import random

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basketball Catch Game")

# Colors
WHITE = (255, 255, 255)
RED = (200, 50, 50)

# Load assets
try:
    hoop_img = pygame.image.load("hoop.png")
    hoop_img = pygame.transform.scale(hoop_img, (80, 30))  # Resize hoop
except pygame.error:
    print("Failed to load hoop image! Using placeholder.")
    hoop_img = pygame.Surface((80, 30))  # Placeholder rectangle

try:
    basketball_img = pygame.image.load("basketball.png")
    basketball_img = pygame.transform.scale(basketball_img, (25, 25))  # Resize basketball
except pygame.error:
    print("Failed to load basketball image! Using placeholder.")
    basketball_img = pygame.Surface((25, 25))  # Placeholder rectangle

# Set up hoop
hoop_x = WIDTH // 2 - 80 // 2
hoop_y = HEIGHT - 30 - 20
hoop_speed = 10

# Set up balls
balls = []
ball_speed = 5

# Score and timer
score = 0
start_ticks = pygame.time.get_ticks()
game_time = 60  # 60 seconds

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Check for quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move hoop with WASD and arrow keys
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and hoop_x > 0:
        hoop_x -= hoop_speed
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and hoop_x < WIDTH - 80:
        hoop_x += hoop_speed

    # Spawn basketballs
    if random.randint(1, 50) == 1:  # Random chance to spawn
        balls.append([random.randint(0, WIDTH - 25), 0])

    # Move basketballs
    for ball in balls:
        ball[1] += ball_speed
        if ball[1] > HEIGHT:  # Remove balls that fall off screen
            balls.remove(ball)

    # Collision detection
    for ball in balls:
        if hoop_x < ball[0] < hoop_x + 80 and hoop_y < ball[1] < hoop_y + 30:
            balls.remove(ball)
            score += 1

    # Draw hoop and basketballs
    screen.blit(hoop_img, (hoop_x, hoop_y))
    for ball in balls:
        screen.blit(basketball_img, (ball[0], ball[1]))

    # Timer
    elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
    remaining_time = max(0, game_time - elapsed_time)
    font = pygame.font.Font(None, 36)
    timer_text = font.render(f"Time: {remaining_time}", True, RED)
    score_text = font.render(f"Score: {score}", True, RED)
    screen.blit(timer_text, (20, 20))
    screen.blit(score_text, (20, 50))

    # End game when time is up
    if remaining_time == 0:
        running = False

    pygame.display.update()

pygame.quit()
