import pygame
from game_state import GameState, check_collision, update_obstacles, count_obstacles_passed
from render_state import draw_obstacles
from player import Player
import generation
import constants 

class SpeedSlider:
    def __init__(self, x, y, width, height, min_val=10, max_val=120, initial_val=60):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.dragging = False
        self.handle_width = 20
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.update_value(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_value(event.pos[0])
    
    def update_value(self, mouse_x):
        # Calculate value based on mouse position
        relative_x = mouse_x - self.rect.x
        relative_x = max(0, min(relative_x, self.rect.width))
        ratio = relative_x / self.rect.width
        self.value = int(self.min_val + ratio * (self.max_val - self.min_val))
    
    def draw(self, screen, font):
        # Draw slider track
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        pygame.draw.rect(screen, (50, 50, 50), self.rect, 2)
        
        # Draw slider handle
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        handle_x = self.rect.x + ratio * (self.rect.width - self.handle_width)
        handle_rect = pygame.Rect(handle_x, self.rect.y - 5, self.handle_width, self.rect.height + 10)
        pygame.draw.rect(screen, (200, 200, 200), handle_rect)
        pygame.draw.rect(screen, (0, 0, 0), handle_rect, 2)
        
        # Draw label and value
        label_text = font.render(f"Speed: {self.value} FPS", True, constants.TEXT_COLOR)
        screen.blit(label_text, (self.rect.x, self.rect.y - 25)) 

def handle_input(game_state, speed_slider):
    """Handle player input events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state.running = False
            return False
        
        # Handle slider events
        speed_slider.handle_event(event)
    
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
    slider_font = pygame.font.Font(None, 24)
    
    # Create speed slider
    speed_slider = SpeedSlider(10, 10, 200, 20, min_val=10, max_val=600, initial_val=constants.FPS)
    
    generation_number = 0
    game_state = GameState()
    active_players = players.copy()  # Start with all players active
    print("Starting game loop...")  # Debug output

    while game_state.running:
        # Handle input (including slider)
        if not handle_input(game_state, speed_slider):
            break
        
        if not active_players:
            print("All players have died")
            players = generation.NewGeneration(saved_players)
            generation_number += 1
            print(f"Generation {generation_number}")
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
        for player in active_players:
            count_obstacles_passed(game_state, player)
        # Check for collisions for all active players
        for player in active_players:
            if check_collision(game_state, player):
                saved_players.append(player)
                player.game_over = True
 
        # Render everything
        screen.fill(constants.BACKGROUND_COLOR)
        
        # Draw speed slider first (on top)
        speed_slider.draw(screen, slider_font)
        
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
            #best_player.draw_player(screen)
            score_text = score_font.render(
                f"Score: {best_player.score}, Obstacles Avoided: {best_player.obstacle_avoided}, Active: {len(active_players)}", 
                True, constants.TEXT_COLOR
            )
            screen.blit(score_text, (10, 50))  # Moved down to avoid slider overlap
        
        pygame.display.flip()
        clock.tick(speed_slider.value)  # Use slider value for FPS

    pygame.quit()

# Start the game
if __name__ == "__main__":
    run_game()