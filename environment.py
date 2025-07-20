from game_state import GameState, check_collision, update_obstacles
import constants

class Environment:
    def __init__(self):
        self.game_state = GameState()
    
    def reset(self):
        """Reset the game state for a new episode"""
        self.game_state.reset()
    
    def step(self, action):
        """Execute an action and return the next state, reward, and done flag"""
        if action == 1:  # Move left
            self.game_state.move_player(-1)
        elif action == 2:  # Move right
            self.game_state.move_player(1)
        update_obstacles(self.game_state)
        
        if check_collision(self.game_state):
            reward = -10  # Penalty for collision
            done = True
        else:
            reward = 1  # Reward for survival
            done = False

        return self.get_state(), reward, done

    def get_state(self):
        player_lane = self.game_state.player_lane #index
        one_hot_location = [0 , 0, 0]
        one_hot_location[player_lane] = 1
        
        if self.game_state.obstacles:
            ahead_obstacles = [o for o in self.game_state.obstacles if o['y'] < self.game_state.player_rect.y]
            if ahead_obstacles:
                closest = max(ahead_obstacles, key=lambda o: o['y'])
                obstacle_lane = constants.LANE_X.index(closest['x'])
                obstacle_distance = self.game_state.player_rect.y - closest['y']
            else:
                obstacle_lane = -1
                obstacle_distance = 999
        else:
            obstacle_lane = -1
            obstacle_distance = 999

        return one_hot_location + [obstacle_lane, obstacle_distance]