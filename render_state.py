import pygame
import constants

def draw_obstacles(screen, obstacles):
    """Optimized obstacle drawing with batch operations"""
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(
            obstacle['x'] - constants.OBSTACLE_WIDTH // 2, 
            obstacle['y'], 
            constants.OBSTACLE_WIDTH, 
            constants.OBSTACLE_HEIGHT
        )
        pygame.draw.rect(screen, constants.OBSTACLE_COLOR, obstacle_rect)
def show_game_over(screen, score):
    """Optimized game over screen with pre-created surfaces"""
    # Create semi-transparent overlay
    overlay = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    overlay.set_alpha(128) 
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # Use different font sizes for better hierarchy
    title_font = pygame.font.Font(None, 74)
    text_font = pygame.font.Font(None, 48)
    
    # Render text with better positioning
    game_over_text = title_font.render("Game Over", True, (255, 0, 0))
    score_text = text_font.render(f"Your Score: {score}", True, (255, 255, 255))
    restart_text = text_font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    
    # Center text properly
    screen_center_x = constants.SCREEN_WIDTH // 2
    screen.blit(game_over_text, (screen_center_x - game_over_text.get_width() // 2, 200))
    screen.blit(score_text, (screen_center_x - score_text.get_width() // 2, 300))
    screen.blit(restart_text, (screen_center_x - restart_text.get_width() // 2, 400))
    pygame.display.flip()
    
    # Handle game over input
    waiting = True
    clock = pygame.time.Clock()
    while waiting:
        clock.tick(30)  # Lower FPS for game over screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return False
    return False