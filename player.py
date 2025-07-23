import pygame
import constants
from model import NeuralNetwork


class Player:
    def __init__(self, brain = False):
        self.score = 0
        self.fitness = 0
        self.player_lane = 1
        self.survival_time = 0
        self.obstacle_avoided = 0
        self.game_over = False
        if(brain):
            self.brain = brain
        else:
            self.brain = NeuralNetwork(5,10,3)
        self.player_rect = pygame.Rect(
            constants.LANE_X[self.player_lane] - constants.PLAYER_WIDTH // 2, 
            constants.PLAYER_Y, 
            constants.PLAYER_WIDTH, 
            constants.PLAYER_HEIGHT
        )

    def think(self, game_state):
        """Move player left (-1) or right (1)"""
        state = self.get_state(game_state)
        action = self.brain.predict(state)
        if action == 1:  # Move left
            self.move_player(-1)
        elif action == 2:  # Move right
            self.move_player(1)

    def move_player(self, direction):
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

    def get_state(self, game_state):
        """Get the current state for AI decision making"""
        player_lane = self.player_lane  # index
        one_hot_location = [0, 0, 0]
        one_hot_location[player_lane] = 1
        
        if game_state.obstacles:
            ahead_obstacles = [o for o in game_state.obstacles if o['y'] < self.player_rect.y]
            if ahead_obstacles:
                closest = max(ahead_obstacles, key=lambda o: o['y'])
                try:
                    obstacle_lane = constants.LANE_X.index(closest['x'])
                except ValueError:
                    obstacle_lane = -1
                obstacle_distance = self.player_rect.y - closest['y']
            else:
                obstacle_lane = -1
                obstacle_distance = 999
        else:
            obstacle_lane = -1
            obstacle_distance = 999

        return one_hot_location + [obstacle_lane, obstacle_distance]