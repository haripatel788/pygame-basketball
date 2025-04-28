import pygame
import random

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Basketball Catch Game")

WHITE = (255, 255, 255)
RED = (200, 50, 50)
BLUE = (50, 50, 200)
GREEN = (50, 200, 50)
BLACK = (0, 0, 0)

font = pygame.font.Font(None, 48)

hoop_img = pygame.image.load("hoop.png")
original_width, original_height = hoop_img.get_width(), hoop_img.get_height()
scale_factor = WIDTH / 15 / original_width
hoop_width = int(original_width * scale_factor)
hoop_height = int(original_height * scale_factor)
hoop_img = pygame.transform.scale(hoop_img, (hoop_width, hoop_height))

basketball_img = pygame.image.load("basketball.png")
basketball_img = pygame.transform.scale(basketball_img, (25, 25))

obstacle_img = pygame.image.load("obstacle.png")
obstacle_img = pygame.transform.scale(obstacle_img, (25, 25))

hoop_x = WIDTH // 2 - hoop_width // 2
hoop_y = HEIGHT - hoop_height - 20
hoop_speed = WIDTH // 200

balls = []
obstacles = []
ball_speed = HEIGHT // 160
obstacle_speed = HEIGHT // 160

score = 0
game_time = 60

def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h))
    button_text = font.render(text, True, WHITE)
    screen.blit(button_text, (x + (w - button_text.get_width()) // 2, y + (h - button_text.get_height()) // 2))

def show_start_screen():
    screen.fill(BLACK)
    title = font.render("Basketball Catch Game", True, WHITE)
    instructions = font.render("Use WASD or Arrow Keys to move the hoop.", True, WHITE)
    avoid_text = font.render("Avoid obstacles! They reduce your score.", True, WHITE)
    start_x, start_y, start_w, start_h = WIDTH // 2 - 100, HEIGHT // 2, 200, 50

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT // 3))
    screen.blit(avoid_text, (WIDTH // 2 - avoid_text.get_width() // 2, HEIGHT // 2.5))
    draw_button("Start Game", start_x, start_y, start_w, start_h, GREEN)

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if start_x <= mouse_x <= start_x + start_w and start_y <= mouse_y <= start_y + start_h:
                    waiting = False
    return True

def show_game_over_screen():
    screen.fill(BLACK)
    title = font.render("Game Over!", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    replay_x, replay_y, replay_w, replay_h = WIDTH // 2 - 100, HEIGHT // 2, 200, 50

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3))
    draw_button("Play Again", replay_x, replay_y, replay_w, replay_h, GREEN)

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if replay_x <= mouse_x <= replay_x + replay_w and replay_y <= mouse_y <= replay_y + replay_h:
                    return True
    return False

while show_start_screen():
    score = 0
    start_ticks = pygame.time.get_ticks()
    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and hoop_x > 0:
            hoop_x -= hoop_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and hoop_x < WIDTH - hoop_width:
            hoop_x += hoop_speed

        if random.randint(1, 50) == 1:
            balls.append([random.randint(0, WIDTH - 25), 0])

        if random.randint(1, 100) == 1:
            obstacles.append([random.randint(0, WIDTH - 25), 0])

        for ball in balls:
            ball[1] += ball_speed
            if ball[1] > HEIGHT:
                balls.remove(ball)

        for obstacle in obstacles:
            obstacle[1] += obstacle_speed
            if obstacle[1] > HEIGHT:
                obstacles.remove(obstacle)

        for ball in balls:
            if hoop_x < ball[0] < hoop_x + hoop_width and hoop_y < ball[1] < hoop_y + hoop_height:
                balls.remove(ball)
                score += 1

        for obstacle in obstacles:
            if hoop_x < obstacle[0] < hoop_x + hoop_width and hoop_y < obstacle[1] < hoop_y + hoop_height:
                obstacles.remove(obstacle)
                score -= 5

        screen.blit(hoop_img, (hoop_x, hoop_y))
        for ball in balls:
            screen.blit(basketball_img, (ball[0], ball[1]))
        for obstacle in obstacles:
            screen.blit(obstacle_img, (obstacle[0], obstacle[1]))

        elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = max(0, game_time - elapsed_time)

        timer_text = font.render(f"Time: {remaining_time}", True, RED)
        score_text = font.render(f"Score: {score}", True, RED)

        screen.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, HEIGHT // 8))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 6))
        if score < 0:
            running = False
        if remaining_time == 0:
            running = False

        pygame.display.update()

    if not show_game_over_screen():
        break

pygame.quit()
