# Temple Run AI - Neuroevolution Game Agent

A sophisticated AI implementation that learns to play an endless runner game using neuroevolution and genetic algorithms. The project demonstrates advanced machine learning concepts including neural network optimization, population-based learning, and real-time game AI.

## 🚀 Project Overview

This project implements an AI agent capable of learning to navigate a Temple Run-style endless runner game through evolutionary computation. Unlike traditional deep learning approaches, this system uses neuroevolution to evolve neural network weights through genetic algorithms, creating agents that improve over successive generations.

### Key Features

- **Neuroevolutionary Neural Networks**: Custom-built neural networks evolved through genetic algorithms
- **Population-Based Learning**: Simultaneous training of 1000+ AI agents per generation
- **Adaptive Genetic Algorithms**: Dynamic mutation rates and advanced selection mechanisms
- **Real-Time Visualization**: Live gameplay with performance metrics and speed controls
- **Sophisticated Fitness Functions**: Multi-objective optimization balancing survival, score, and movement efficiency

## 🧠 Technical Architecture

### Neural Network Design

The AI brain is implemented as a fully connected neural network with:
- **Input Layer**: 8 neurons processing game state information
- **Hidden Layer**: 4 neurons with tanh activation functions
- **Output Layer**: 3 neurons corresponding to game actions (left, stay, right)

```python
# Network Architecture
Input: [player_position_one_hot(3), obstacle_lane(1), obstacle_distance(1), 
        current_lane_safety(1), left_lane_safety(1), right_lane_safety(1)]
Hidden: 4 neurons (tanh activation)
Output: 3 neurons (argmax for action selection)
```

### Genetic Algorithm Implementation

#### Advanced Selection Mechanisms
- **Nucleus (Top-p) Sampling**: Probabilistic selection focusing on top-performing individuals
- **Temperature Scaling**: Adjustable exploration vs exploitation balance
- **Weighted Selection**: Fitness-proportionate selection with adaptive parameters

#### Adaptive Mutation Strategy
```python
adaptive_rate = base_mutation_rate * (2.0 - population_diversity)
mutation_strength = 0.1 if diversity > 0.5 else 0.3
```

#### Dynamic Elite Preservation
- Adaptive elite percentage based on population diversity
- Elite count varies from 20% to 40% based on genetic diversity metrics

### Game State Representation

The AI processes a sophisticated state representation including:
1. **Positional Encoding**: One-hot representation of current lane position
2. **Obstacle Intelligence**: Distance and lane information for immediate threats
3. **Safety Analysis**: Forward-looking safety scores for all lanes
4. **Predictive Modeling**: Multi-step ahead obstacle avoidance calculations

## 🔥 Technical Challenges and Solutions

### Challenge 1: Population Diversity Management
**Problem**: Genetic algorithms can suffer from premature convergence, where the population becomes too similar and loses diversity.

**Solution**: Implemented adaptive diversity monitoring with dynamic mutation rates:
```python
def calculate_population_diversity(players):
    # Samples subset for performance, calculates genetic distance
    total_distance = 0
    for genome_pair in sampled_combinations:
        distance = np.mean(np.abs(genome1 - genome2))
        total_distance += distance
    return normalized_diversity_score
```

### Challenge 2: Fitness Function Optimization
**Problem**: Balancing multiple objectives (survival time, obstacles avoided, movement efficiency) without causing optimization conflicts.

**Solution**: Developed a composite fitness function with movement efficiency bonuses:
```python
score_component = (player.score / max_score) * 0.8
move_efficiency = min(1.0, obstacles_avoided / moves_made)
efficiency_bonus = move_efficiency * 0.2
player.fitness = (score_component + efficiency_bonus) ** 2
```

### Challenge 3: Real-Time Performance Optimization
**Problem**: Maintaining 60+ FPS while simulating 1000+ AI agents simultaneously.

**Solutions Implemented**:
- **Vectorized Operations**: NumPy-based batch processing for neural network computations
- **Optimized Collision Detection**: Pygame rect-based collision system
- **Memory Management**: Efficient obstacle lifecycle management
- **Selective Rendering**: Only render the best-performing agent to reduce overhead

### Challenge 4: Neural Network Stability
**Problem**: Preventing gradient explosion and ensuring numerical stability in evolution.

**Solution**: Multiple stability mechanisms:
```python
# Numerical clipping in activation functions
def tanh(self, x):
    return np.tanh(np.clip(x, -500, 500))

# Weight clamping during mutation
genome[i] = np.clip(genome[i], -2.0, 2.0)
```

## 🏆 Strong Technical Points

### 1. Advanced Genetic Algorithm Design
- **Nucleus Sampling**: Implementation of cutting-edge selection mechanisms from natural language processing
- **Adaptive Parameters**: Dynamic adjustment of mutation rates based on population metrics
- **Multi-Objective Optimization**: Sophisticated fitness landscapes balancing competing objectives

### 2. Efficient Neural Network Implementation
- **Custom Implementation**: Built from scratch without external ML libraries
- **Optimized Forward Pass**: Vectorized operations for population-scale inference
- **Genome Serialization**: Efficient conversion between network weights and genetic representation

### 3. Real-Time Performance Engineering
- **Concurrent Agent Simulation**: Handling 1000+ agents at 60+ FPS
- **Memory-Efficient Design**: Minimal allocation during gameplay loops
- **Modular Architecture**: Clean separation of concerns for maintainability

### 4. Sophisticated Game AI
- **Predictive State Representation**: Forward-looking obstacle analysis
- **Lane Safety Calculations**: Dynamic safety scoring for decision making
- **Behavioral Emergence**: Complex behaviors emerging from simple rule sets

## 📊 Performance Metrics

### Learning Progression
- **Generation 0**: Random behavior, average survival ~50 frames
- **Generation 5-10**: Basic obstacle avoidance emerges
- **Generation 15+**: Advanced strategies, survival 500+ frames
- **Convergence**: Stable high-performance behavior by generation 20-30

### System Performance
- **Population Size**: 1000 agents per generation
- **Simulation Speed**: 60-600 FPS (user-adjustable)
- **Memory Usage**: ~50MB for full population
- **Evolution Time**: ~30 seconds per generation

## 🛠 Technical Stack

- **Core Language**: Python 3.8+
- **Graphics**: Pygame for real-time rendering
- **Numerical Computing**: NumPy for vectorized operations
- **Architecture**: Object-oriented design with modular components

## 🚀 Installation and Usage

```bash
# Clone the repository
git clone https://github.com/YourUsername/Temple-Run-AI.git
cd Temple-Run-AI

# Install dependencies
pip install pygame numpy

# Run the simulation
python main_game.py
```

### Controls
- **Speed Slider**: Adjust simulation speed (10-600 FPS)
- **Real-time Metrics**: Live population statistics and performance data

## 🔬 Research Applications

This project demonstrates several advanced AI concepts applicable to:
- **Evolutionary Computation Research**: Novel selection and mutation strategies
- **Game AI Development**: Real-time decision making under uncertainty
- **Neural Architecture Search**: Automated network optimization
- **Multi-Agent Systems**: Population-based learning dynamics

## 📈 Future Enhancements

- **Speciation Algorithms**: Implementing NEAT-style species protection
- **Hierarchical Networks**: Multi-level decision architectures
- **Transfer Learning**: Cross-environment skill transfer
- **Parallel Evolution**: GPU-accelerated population simulation

## 🎯 Key Learnings

1. **Population diversity is crucial** for avoiding local optima in evolutionary algorithms
2. **Composite fitness functions** require careful balancing to prevent conflicting objectives
3. **Real-time constraints** demand significant optimization even for "simple" neural networks
4. **Emergent behavior** in neuroevolution can produce surprisingly sophisticated strategies

---

*This project showcases the power of evolutionary computation in creating intelligent game agents, demonstrating that complex behaviors can emerge from simple rules when guided by well-designed selection pressures.*