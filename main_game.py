import pygame
import random

def draw_player(screen, lane_X, player_lane, player_Y):
    player_X = lane_X[player_lane]
    pygame.draw.rect(screen, (255, 0, 0), (player_X - 25, player_Y, 50, 50))  # Centered on X

def spawn_obstacles(screen, obstacles):
    # Draw existing obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, (0, 255, 0), (obstacle['x'] - 75, obstacle['y'], 150, 50))
def check_collision(player_lane,player_Y,obstacles, Lane_X):
    player_rect = pygame.Rect(Lane_X[player_lane] - 25, player_Y, 50, 50)
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle['x'] - 75, obstacle['y'], 150, 50)
        if player_rect.colliderect(obstacle_rect):
            return True
    return False

def show_game_over(screen,score):
    overlay = pygame.Surface((900, 600))
    overlay.fill((0, 0, 0, 128))  # Semi-transparent black
    screen.blit(overlay, (0, 0))
    
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Your Score: {score}", True, (255, 255, 255))
    restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    
    screen.blit(game_over_text,(900//2 - game_over_text.get_width()//2, 200))
    screen.blit(score_text,(900//2 - score_text.get_width()//2, 300))
    screen.blit(restart_text,(900//2 - restart_text.get_width()//2, 400))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return False

def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((900, 600), pygame.RESIZABLE)
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()

    Lane_X = [150, 450,750]
    lane_Line = [300,600]
    player_lane = 0
    player_Y = 500
    
    score = 0
    font = pygame.font.Font(None, 36)
    # Obstacle management
    obstacles = []
    obstacle_spawn_timer = 0
    obstacle_speed = 3

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if player_lane > 0:
                        player_lane -= 1
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if player_lane < 2:
                        player_lane += 1

        screen.fill((150, 245, 255))

        score+=1
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        # Spawn new obstacles periodically
        obstacle_spawn_timer += 1
        if obstacle_spawn_timer > 80:
            random_lane = random.randint(0, 2)
            obstacles.append({
                'x': Lane_X[random_lane],
                'y': -50  # Start above the screen
            })
            obstacle_spawn_timer = 0

        # Move obstacles down and remove off-screen ones
        obstacles = [obs for obs in obstacles if obs['y'] < 650]  # Remove obstacles that are off-screen
        for obstacle in obstacles:
            obstacle['y'] += obstacle_speed

        for x in lane_Line:
            pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, 600), 2)

        # Draw obstacles
        spawn_obstacles(screen, obstacles)

        # Draw player
        draw_player(screen, Lane_X, player_lane, player_Y)
        
        if check_collision(player_lane, player_Y, obstacles, Lane_X):
            print("Collision detected!")
            if show_game_over(screen, score):
                initialize_game()
            else:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

initialize_game()