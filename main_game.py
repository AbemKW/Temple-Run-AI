import pygame

def draw_player(screen, lane_X, player_lane, player_Y):
    player_X = lane_X[player_lane]
    pygame.draw.rect(screen, (255, 0, 0), (player_X - 100, player_Y, 50, 50))  # Centered on X

def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()

    Lane_X = [200, 400, 600]
    player_lane = 1
    player_Y = 500

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if player_lane > 0:
                        player_lane -= 1
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if player_lane < 2:
                        player_lane += 1

        screen.fill((150, 245, 255))

        for x in Lane_X:
            pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, 600), 2)

        # Draw player
        draw_player(screen, Lane_X, player_lane, player_Y)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

initialize_game()