import pygame
import random

def draw_player(screen, lane_X, player_lane, player_Y):
    player_X = lane_X[player_lane]
    pygame.draw.rect(screen, (255, 0, 0), (player_X - 25, player_Y, 50, 50))  # Centered on X

def spawn_obstacles(screen, obstacles):
    # Draw existing obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, (0, 255, 0), (obstacle['x'] - 75, obstacle['y'], 150, 50))

def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((900, 600), pygame.RESIZABLE)
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()

    Lane_X = [150, 450,750]
    lane_Line = [300,600]
    player_lane = 0
    player_Y = 500
    
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

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

initialize_game()