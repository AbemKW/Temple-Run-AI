import pygame
import constants

def draw_player(screen, game_state):
    """Optimized player drawing using pre-calculated rect"""
    pygame.draw.rect(screen, constants.PLAYER_COLOR, game_state.player_rect)

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
