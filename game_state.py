import random
import pygame
import constants

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
            constants.LANE_X[self.player_lane] - constants.PLAYER_WIDTH // 2, 
            constants.PLAYER_Y, 
            constants.PLAYER_WIDTH, 
            constants.PLAYER_HEIGHT
        )
        
    def move_player(self, direction):
        """Move player left (-1) or right (1)"""
        new_lane = self.player_lane + direction
        if 0 <= new_lane < constants.NUM_LANES:
            self.player_lane = new_lane
            self.player_rect.x = constants.LANE_X[self.player_lane] - constants.PLAYER_WIDTH // 2

    def get_difficulty_settings(self):
        """Get current difficulty settings based on score"""
        for i in range(len(constants.DIFFICULTY_LEVELS) - 1, -1, -1):
            if self.score >= constants.DIFFICULTY_LEVELS[i]["threshold"]:
                return constants.DIFFICULTY_LEVELS[i]
        return constants.DIFFICULTY_LEVELS[0]

    def update_score(self):
        """Update score based on survival time and obstacles avoided"""
        self.survival_time += 1
        base_score = self.survival_time // 10
        bonus_score = self.obstacle_avoided * 10
        difficulty = self.get_difficulty_settings()
        self.score = int((base_score + bonus_score) * difficulty["multiplier"])

def check_collision(game_state):
    """Optimized collision detection using pygame rects"""
    player_rect = game_state.player_rect
    for obstacle in game_state.obstacles:
        obstacle_rect = pygame.Rect(
            obstacle['x'] - constants.OBSTACLE_WIDTH // 2, 
            obstacle['y'], 
            constants.OBSTACLE_WIDTH, 
            constants.OBSTACLE_HEIGHT
        )
        if player_rect.colliderect(obstacle_rect):
            return True
    return False

def update_obstacles(game_state):
    """Optimized obstacle management"""
    difficulty = game_state.get_difficulty_settings()
    obstacle_speed = difficulty["speed"]
    
    # Count obstacles that passed the player (only once per obstacle)
    for obstacle in game_state.obstacles:
        if obstacle['y'] > constants.PLAYER_Y + constants.PLAYER_HEIGHT and not obstacle.get('counted', False):
            game_state.obstacle_avoided += 1
            obstacle['counted'] = True
    
    # Update obstacle spawn timer
    game_state.obstacle_spawn_timer += difficulty["spawn_mod"]
    
    # Spawn new obstacles
    if game_state.obstacle_spawn_timer > constants.SPAWN_TIMER_BASE:
        random_lane = random.randint(0, constants.NUM_LANES - 1)
        game_state.obstacles.append({
            'x': constants.LANE_X[random_lane],
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