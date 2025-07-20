import pygame
import random

# Game Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 60

# Lane configuration
LANE_X = [150, 450, 750]
LANE_LINES = [300, 600]
NUM_LANES = 3

# Player configuration
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_Y = 500

# Obstacle configuration
OBSTACLE_WIDTH = 150
OBSTACLE_HEIGHT = 20
OBSTACLE_SPEED_BASE = 3
SPAWN_TIMER_BASE = 80

# Colors
BACKGROUND_COLOR = (150, 245, 255)
PLAYER_COLOR = (255, 0, 0)
OBSTACLE_COLOR = (0, 255, 0)
LINE_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)

# Difficulty settings
DIFFICULTY_LEVELS = [
    {"threshold": 0, "speed": 3, "multiplier": 1, "spawn_mod": 1},
    {"threshold": 100, "speed": 5, "multiplier": 1.5, "spawn_mod": 3},
    {"threshold": 200, "speed": 10, "multiplier": 2, "spawn_mod": 5}
]

class GameState:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.player_lane = 0
        self.obstacles = []
        self.score = 0
        self.obstacle_avoided = 0
        self.survival_time = 0
        self.obstacle_spawn_timer = 0
        self.running = True
        
        # Pre-calculate player rect for collision detection
        self.player_rect = pygame.Rect(
            LANE_X[self.player_lane] - PLAYER_WIDTH // 2, 
            PLAYER_Y, 
            PLAYER_WIDTH, 
            PLAYER_HEIGHT
        )
    
    def move_player(self, direction):
        """Move player left (-1) or right (1)"""
        new_lane = self.player_lane + direction
        if 0 <= new_lane < NUM_LANES:
            self.player_lane = new_lane
            self.player_rect.x = LANE_X[self.player_lane] - PLAYER_WIDTH // 2
    
    def get_difficulty_settings(self):
        """Get current difficulty settings based on score"""
        for i in range(len(DIFFICULTY_LEVELS) - 1, -1, -1):
            if self.score >= DIFFICULTY_LEVELS[i]["threshold"]:
                return DIFFICULTY_LEVELS[i]
        return DIFFICULTY_LEVELS[0]
    
    def update_score(self):
        """Update score based on survival time and obstacles avoided"""
        self.survival_time += 1
        base_score = self.survival_time // 10
        bonus_score = self.obstacle_avoided * 10
        difficulty = self.get_difficulty_settings()
        self.score = int((base_score + bonus_score) * difficulty["multiplier"])

def draw_player(screen, game_state):
    """Optimized player drawing using pre-calculated rect"""
    pygame.draw.rect(screen, PLAYER_COLOR, game_state.player_rect)

def draw_obstacles(screen, obstacles):
    """Optimized obstacle drawing with batch operations"""
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(
            obstacle['x'] - OBSTACLE_WIDTH // 2, 
            obstacle['y'], 
            OBSTACLE_WIDTH, 
            OBSTACLE_HEIGHT
        )
        pygame.draw.rect(screen, OBSTACLE_COLOR, obstacle_rect)

def check_collision(game_state):
    """Optimized collision detection using pygame rects"""
    player_rect = game_state.player_rect
    for obstacle in game_state.obstacles:
        obstacle_rect = pygame.Rect(
            obstacle['x'] - OBSTACLE_WIDTH // 2, 
            obstacle['y'], 
            OBSTACLE_WIDTH, 
            OBSTACLE_HEIGHT
        )
        if player_rect.colliderect(obstacle_rect):
            return True
    return False

def show_game_over(screen, score):
    """Optimized game over screen with pre-created surfaces"""
    # Create semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
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
    screen_center_x = SCREEN_WIDTH // 2
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

def update_obstacles(game_state):
    """Optimized obstacle management"""
    difficulty = game_state.get_difficulty_settings()
    obstacle_speed = difficulty["speed"]
    
    # Count obstacles that passed the player (only once per obstacle)
    for obstacle in game_state.obstacles:
        if obstacle['y'] > PLAYER_Y + PLAYER_HEIGHT and not obstacle.get('counted', False):
            game_state.obstacle_avoided += 1
            obstacle['counted'] = True
    
    # Update obstacle spawn timer
    game_state.obstacle_spawn_timer += difficulty["spawn_mod"]
    
    # Spawn new obstacles
    if game_state.obstacle_spawn_timer > SPAWN_TIMER_BASE:
        random_lane = random.randint(0, NUM_LANES - 1)
        game_state.obstacles.append({
            'x': LANE_X[random_lane],
            'y': -50,
            'counted': False
        })
        game_state.obstacle_spawn_timer = 0
    
    # Move obstacles and remove off-screen ones (single pass)
    game_state.obstacles = [
        {**obs, 'y': obs['y'] + obstacle_speed} 
        for obs in game_state.obstacles 
        if obs['y'] + obstacle_speed < 650
    ]

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
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
        screen.fill(BACKGROUND_COLOR)
        
        # Draw lanes (static elements)
        for x in LANE_LINES:
            pygame.draw.line(screen, LINE_COLOR, (x, 0), (x, SCREEN_HEIGHT), 2)
        
        # Draw obstacles
        draw_obstacles(screen, game_state.obstacles)
        
        # Draw player
        draw_player(screen, game_state)
        
        # Draw UI
        score_text = score_font.render(
            f"Score: {game_state.score}, Obstacles Avoided: {game_state.obstacle_avoided}", 
            True, TEXT_COLOR
        )
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

# Start the game
if __name__ == "__main__":
    run_game()