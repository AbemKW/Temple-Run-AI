import pygame
from game_state import GameState, check_collision, update_obstacles
from render_state import draw_obstacles
from player import Player
import generation
import constants 

def handle_input( game_state):
    """Handle player input events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state.running = False
            return False
    return True  # Continue running if no quit event


def run_game():
    """Main game loop with optimized structure"""
    pygame.init()
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    pygame.display.set_caption("Temple Run AI")
    clock = pygame.time.Clock()

    players : list[Player] = []
    for i in range(constants.POPULATION_SIZE):
        player = Player()
        players.append(player)
    saved_players = []
    print(f"Game window created successfully! Starting with {constants.POPULATION_SIZE} players")  # Debug output
    print("Look for the 'Temple Run AI' window - it should be visible now!")
    
    # Pre-create font objects to avoid recreation
    score_font = pygame.font.Font(None, 36)
    
    game_state = GameState()
    active_players = players.copy()  # Start with all players active
    print("Starting game loop...")  # Debug output

    while game_state.running:
        # Handle input
        if not handle_input(game_state):
            break
        
        if not active_players:
            print("All players have died")
            players = generation.NewGeneration(saved_players)
            saved_players.clear()  # Clear saved players for the new generation
            game_state.reset()
            
        # Update all players
        active_players = [p for p in players if not p.game_over]

        for player in active_players:
            player.think(game_state)  # AI decision-making
            player.update_score()
            
        if active_players:
            best_player = max(active_players, key=lambda p: p.score)
            # Update obstacles once per frame (using first active player for difficulty)
            update_obstacles(game_state, best_player)
        
        # Check for collisions for all active players
        for player in active_players:
            if check_collision(game_state, player):
                saved_players.append(player)
                player.game_over = True
                print(f"Player died! Score: {player.score}, Active players: {len([p for p in players if not p.game_over])}")
            
        # Render everything
        screen.fill(constants.BACKGROUND_COLOR)
        
        # Draw lanes (static elements)
        for x in constants.LANE_LINES:
            pygame.draw.line(screen, constants.LINE_COLOR, (x, 0), (x, constants.SCREEN_HEIGHT), 2)

        # Draw obstacles
        draw_obstacles(screen, game_state.obstacles)
        
        # Draw all active players
        for player in active_players:
            player.draw_player(screen)

        # Draw UI for the first active player (or best performing player)
        if active_players:
            best_player = max(active_players, key=lambda p: p.score)
            score_text = score_font.render(
                f"Score: {best_player.score}, Obstacles Avoided: {best_player.obstacle_avoided}, Active: {len(active_players)}", 
                True, constants.TEXT_COLOR
            )
            screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(constants.FPS)

    pygame.quit()

# Start the game
if __name__ == "__main__":
    run_game()