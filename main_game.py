import pygame
from game_state import GameState, check_collision, show_game_over, update_obstacles
from render_state import draw_player, draw_obstacles
import constants 




def handle_input(game_state):
    """Handle player input events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state.running = False
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                game_state.move_player(-1)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                game_state.move_player(1)
    return True

def run_game():
    """Main game loop with optimized structure"""
    pygame.init()
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    pygame.display.set_caption("Temple Run - Optimized")
    clock = pygame.time.Clock()
    
    # Pre-create font objects to avoid recreation
    score_font = pygame.font.Font(None, 36)
    
    game_state = GameState()
    
    while game_state.running:
        # Handle input
        if not handle_input(game_state):
            break
        
        # Update game state
        game_state.update_score()
        update_obstacles(game_state)
        
        # Check collision
        if check_collision(game_state):
            if show_game_over(screen, game_state.score):
                game_state.reset()  # Restart game
            else:
                break  # Quit game
        
        # Render everything
        screen.fill(constants.BACKGROUND_COLOR)
        
        # Draw lanes (static elements)
        for x in constants.LANE_LINES:
            pygame.draw.line(screen, constants.LINE_COLOR, (x, 0), (x, constants.SCREEN_HEIGHT), 2)

        # Draw obstacles
        draw_obstacles(screen, game_state.obstacles)
        
        # Draw player
        draw_player(screen, game_state)
        
        # Draw UI
        score_text = score_font.render(
            f"Score: {game_state.score}, Obstacles Avoided: {game_state.obstacle_avoided}", 
            True, constants.TEXT_COLOR
        )
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(constants.FPS)

    pygame.quit()

# Start the game
if __name__ == "__main__":
    run_game()