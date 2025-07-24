import numpy as np
import pygame
import constants
from model import NeuralNetwork


class Player:
    def __init__(self, brain = None):
        self.score = 0
        self.fitness = 0
        self.player_lane = 1
        self.survival_time = 0
        self.moves_made = 0
        self.passed_obstacles = []
        self.obstacle_avoided = 0
        self.game_over = False
        if(brain is not None):
            self.brain = brain
        else:
            self.brain = NeuralNetwork(8,8,3)
        self.player_rect = pygame.Rect(
            constants.LANE_X[self.player_lane] - constants.PLAYER_WIDTH // 2, 
            constants.PLAYER_Y, 
            constants.PLAYER_WIDTH, 
            constants.PLAYER_HEIGHT
        )

    def think(self, game_state):
        """Move player left (-1) or right (1)"""
        state = np.array(self.get_state(game_state))
        action = self.brain.predict(state)
        # action = np.argmax(1-state)
        # Consider changing action mapping to encourage movement:
        if action == 0:     # Move left
            self.move_player(-1)
        elif action == 1:   # Stay put
            pass
        elif action == 2:   # Move right
            self.move_player(1)

    def move_player(self, direction):
        new_lane = self.player_lane + direction
        if 0 <= new_lane < constants.NUM_LANES:
            self.player_lane = new_lane
            self.moves_made += 1
            self.player_rect.x = constants.LANE_X[self.player_lane] - constants.PLAYER_WIDTH // 2

    def update_score(self):
        """Update score based on survival time and obstacles avoided"""
        self.survival_time += 1
        base_score = self.survival_time // 10
        bonus_score = self.obstacle_avoided * 10
        # difficulty = self.get_difficulty_settings()
        self.score = int((base_score + bonus_score) * 1)

    def get_color(self):
        """Get color based on fitness"""
        if self.fitness < 0.33:
            return constants.PLAYER_COLOR[0]["color"]
        elif self.fitness < 0.66:
            return constants.PLAYER_COLOR[1]["color"]
        elif self.fitness > 0.77:
            return constants.PLAYER_COLOR[2]["color"]
    def draw_player(self, screen):
        """Draw player as a pixelated circle"""
        player_color_fitness = self.get_color()
        
        # Get center position of the player
        center_x = self.player_rect.centerx
        center_y = self.player_rect.centery
        
        # Create a pixelated circle using small squares
        pixel_size = 3
        radius = 8  # Radius in pixels
        
        # Create a darker outline color
        outline_color = tuple(max(0, c - 50) for c in player_color_fitness[:3])
        
        # Draw pixelated circle by drawing squares in a circular pattern
        for y in range(-radius, radius + 1):
            for x in range(-radius, radius + 1):
                # Check if this pixel is within the circle
                distance = (x * x + y * y) ** 0.5
                
                if distance <= radius:
                    pixel_x = center_x + x * pixel_size
                    pixel_y = center_y + y * pixel_size
                    
                    # Draw outline for edge pixels
                    if distance > radius - 1.5:
                        pygame.draw.rect(screen, outline_color, 
                                       pygame.Rect(pixel_x, pixel_y, pixel_size, pixel_size))
                    else:
                        # Draw filled pixels
                        pygame.draw.rect(screen, player_color_fitness,
                                       pygame.Rect(pixel_x, pixel_y, pixel_size, pixel_size))

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
        # info about all lane danger

        # Safety score for staying in current lane
        current_safety = self.calculate_lane_safety(self.player_lane, game_state)
        
        # Safety score for moving left
        left_lane = self.player_lane - 1
        left_safety = self.calculate_lane_safety(left_lane, game_state) if left_lane >= 0 else 0
        
        # Safety score for moving right  
        right_lane = self.player_lane + 1
        right_safety = self.calculate_lane_safety(right_lane, game_state) if right_lane < constants.NUM_LANES else 0

        return one_hot_location + [obstacle_lane, obstacle_distance,current_safety, left_safety, right_safety]

    def calculate_lane_safety(self, lane, game_state):
        """Calculate how safe a lane is (0=dangerous, 1=safe)"""
        if lane < 0 or lane >= constants.NUM_LANES:
            return 0  # Invalid lane
        
        max_danger = 0  # Track the highest danger from any single obstacle
        lane_x = constants.LANE_X[lane]
        
        for obstacle in game_state.obstacles:
            if obstacle['x'] == lane_x:
                # Calculate distance (positive = obstacle is above player, negative = below)
                distance = self.player_rect.y - obstacle['y']
                
                # Only consider obstacles above the player that pose a threat
                if distance > 0 and distance < 300:  # Look ahead 300 pixels up
                    # Closer obstacles are more dangerous (inverse relationship)
                    danger = max(0, (300 - distance) / 300)
                    max_danger = max(max_danger, danger)  # Keep the highest danger
        
        return 1 - max_danger  # Convert danger to safety (1=safe, 0=dangerous)