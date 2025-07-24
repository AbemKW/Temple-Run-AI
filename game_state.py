import random
import pygame
import constants

class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.obstacles = []
        self.obstacle_spawn_timer = 0
        self.running = True
        

    def get_difficulty_settings(self, player):
        """Get current difficulty settings based on score"""
        for i in range(len(constants.DIFFICULTY_LEVELS) - 1, -1, -1):
            if player.score >= constants.DIFFICULTY_LEVELS[i]["threshold"]:
                return constants.DIFFICULTY_LEVELS[i]
        return constants.DIFFICULTY_LEVELS[0]

def check_collision(game_state, player):
    """Optimized collision detection using pygame rects"""
    player_rect = player.player_rect
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
def count_obstacles_passed(game_state, player):
    for obstacle in game_state.obstacles:
        obstacle_id = id(obstacle)  # Use object ID as unique identifier
        
        if (obstacle['y'] > constants.PLAYER_Y + constants.PLAYER_HEIGHT and 
            obstacle_id not in player.passed_obstacles):
            
            player.obstacle_avoided += 1
            player.passed_obstacles.append(obstacle_id)
    
def update_obstacles(game_state, player):
    """Optimized obstacle management"""
    difficulty = game_state.get_difficulty_settings(player)
    obstacle_speed = difficulty["speed"]
    
    # Update obstacle spawn timer
    game_state.obstacle_spawn_timer += difficulty["spawn_mod"]
    
    # Spawn new obstacles
    if game_state.obstacle_spawn_timer > constants.SPAWN_TIMER_BASE:
        random_lane = random.randint(0, constants.NUM_LANES - 1)
        game_state.obstacles.append({
            'x': constants.LANE_X[random_lane],
            'y': -50
        })
        game_state.obstacle_spawn_timer = 0
    
    # Move obstacles and remove off-screen ones (single pass)
    game_state.obstacles = [
        {**obs, 'y': obs['y'] + obstacle_speed} 
        for obs in game_state.obstacles 
        if obs['y'] + obstacle_speed < 650
    ]