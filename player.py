import pygame
import constants


class Player:
    def __init__(self):
        self.score = 0
        self.player_lane = 1
        self.survival_time = 0
        self.obstacle_avoided = 0
        self.game_over = False
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

    def update_score(self):
        """Update score based on survival time and obstacles avoided"""
        self.survival_time += 1
        base_score = self.survival_time // 10
        bonus_score = self.obstacle_avoided * 10
        # difficulty = self.get_difficulty_settings()
        self.score = int((base_score + bonus_score) * 1)

    def draw_player(self, screen):
        """Optimized player drawing using pre-calculated rect"""
        pygame.draw.rect(screen, constants.PLAYER_COLOR, self.player_rect)