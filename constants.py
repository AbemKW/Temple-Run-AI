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
PLAYER_COLOR = [{"fitness": 33, "color": (255, 0, 0,140)},
                {"fitness": 66, "color": (0, 255, 0,140)},
                {"fitness": 100, "color": (0, 0, 255,140)}]
OBSTACLE_COLOR = (0, 255, 0)
LINE_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)

# Difficulty settings
DIFFICULTY_LEVELS = [
    {"threshold": 0, "speed": 3, "multiplier": 1, "spawn_mod": 1},
    {"threshold": 100, "speed": 5, "multiplier": 1.5, "spawn_mod": 3},
    {"threshold": 200, "speed": 10, "multiplier": 2, "spawn_mod": 5}
]

# Population
POPULATION_SIZE = 1000

# Weights for fitness calculation
SCORE_WEIGHT = 0.3
SURVIVAL_WEIGHT = 0.3
OBSTACLE_WEIGHT = 0.2
EFFICIENCY_WEIGHT = 0.1
MOVE_EFFICIENCY_WEIGHT = 0.1