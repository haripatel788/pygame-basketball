
`import pygame`  
`import random`  

that brings in pygame for visuals and random numbers

---

getting screen size  

`info = pygame.display.Info()`  
`WIDTH, HEIGHT = info.current_w, info.current_h`  
`screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)`  
`pygame.display.set_caption("Basketball Catch Game")`  

this makes it fullscreen so it fits your screen size, no matter the user's window res



colors and fonts  

`WHITE = (255, 255, 255)`  
`RED = (200, 50, 50)`  
`BLUE = (50, 50, 200)`  
`GREEN = (50, 200, 50)`  
`BLACK = (0, 0, 0)`  

`font = pygame.font.Font(None, 48)`  

colors so we don't play in black layout, and a font for the score + timer  



loading pics  

`hoop_img = pygame.image.load("hoop.png")`  
`basketball_img = pygame.image.load("basketball.png")`  
`obstacle_img = pygame.image.load("obstacle.png")`  

grabbing the hoop, ball, and obstacles  

---

making sure hoop isnt stretched based on user's screen width + height

`original_width, original_height = hoop_img.get_width(), hoop_img.get_height()`  
`scale_factor = WIDTH / 15 / original_width`  
`hoop_width = int(original_width * scale_factor)`  
`hoop_height = int(original_height * scale_factor)`  
`hoop_img = pygame.transform.scale(hoop_img, (hoop_width, hoop_height))`  

resizes while keeping the original proportions so it doesn't look stretched or compressed  

---

resetting game  

`def reset_game():`  
`global hoop_x, hoop_y, hoop_speed, balls, obstacles, score, start_ticks, running`  
`hoop_x = WIDTH // 2 - hoop_width // 2`  
`hoop_y = HEIGHT - hoop_height - 20`  
`hoop_speed = WIDTH // 200`  
`balls.clear()`  
`obstacles.clear()`  
`score = 0`  
`start_ticks = pygame.time.get_ticks()`  
`running = True`  

whenever you restart, wipes everything clean  

---

game over screen  

`def show_game_over_screen():`  
`screen.fill(BLACK)`  
`title = font.render("Game Over!", True, RED)`  
`score_text = font.render(f"Final Score: {score}", True, WHITE)`  
`replay_x, replay_y, replay_w, replay_h = WIDTH // 2 - 100, HEIGHT // 2, 200, 50`  

makes the “Game Over” message pop up and a replay button  

---

game loop  

`while running:`  
`screen.fill(WHITE)`  

`for event in pygame.event.get():`  
`if event.type == pygame.QUIT:`  
`running = False`  

keeps the game running till you quit  

---

hoop movement  

`keys = pygame.key.get_pressed()`  
`if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and hoop_x > 0:`  
`hoop_x -= hoop_speed`  
`if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and hoop_x < WIDTH - hoop_width:`  
`hoop_x += hoop_speed`  

lets you move the hoop left and right  

---

spawning stuff  

`if random.randint(1, 50) == 1:`  
`balls.append([random.randint(0, WIDTH - 25), 0])`  

`if random.randint(1, 100) == 1:`  
`obstacles.append([random.randint(0, WIDTH - 25), 0])`  

balls spawn faster than obstacles, gotta keep the game fair  

---

moving objects down  

`for ball in balls:`  
`ball[1] += HEIGHT // 160`  
`if ball[1] > HEIGHT:`  
`balls.remove(ball)`  

same thing happens for obstacles but with a different list  

---

scoring system  

`for ball in balls:`  
`if hoop_x < ball[0] < hoop_x + hoop_width and hoop_y < ball[1] < hoop_y + hoop_height:`  
`balls.remove(ball)`  
`score += 1`  

catch a ball -> get a point  

`for obstacle in obstacles:`  
`if hoop_x < obstacle[0] < hoop_x + hoop_width and hoop_y < obstacle[1] < hoop_y + hoop_height:`  
`obstacles.remove(obstacle)`  
`score -= 5`  

catch an obstacle score -> -5 points  

---

displaying stuff  

`elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000`  
`remaining_time = max(0, 60 - elapsed_time)`  
`screen.blit(font.render(f"Time: {remaining_time}", True, RED), (20, 20))`  
`screen.blit(font.render(f"Score: {score}", True, RED), (20, 50))`  

puts score and time on the screen  

---

ending game  

`if remaining_time == 0:`  
`if not show_game_over_screen():`  
`break`  

when the timer hits zero or score hits zero game over  

