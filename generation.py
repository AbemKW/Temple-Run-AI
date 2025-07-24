import constants
import random
import numpy as np
from model import NeuralNetwork
from player import Player

def NewGeneration(saved_players):
    # Handle edge case where no players survived
    if not saved_players:
        print("No players survived! Creating new random population.")
        new_players = []
        for i in range(constants.POPULATION_SIZE):
            new_players.append(Player())
        return new_players
    
    players = calculate_fitness(saved_players)
    
    players.sort(key=lambda p: p.fitness, reverse=True)
    
    # Take top 30% as elite
    elite_count = int(constants.POPULATION_SIZE * 0.3)  # 30% of population
    elite = players[:elite_count]
    
    # Reset elite players for new generation
    new_players = []
    for elite_player in elite:
        # Create new player with same brain but reset state
        new_player = Player(elite_player.brain)
        new_players.append(new_player)
    
    while len(new_players) < constants.POPULATION_SIZE:
        parent1 = weighted_selection(players)
        parent2 = weighted_selection(players)
        # Crossover
        child_brain = crossover(parent1.brain, parent2.brain)
        child_brain.set_genome(mutate_genome(child_brain.get_genome()))
        new_players.append(Player(child_brain))
        
    return new_players

def crossover(parent1_brain, parent2_brain):
    """Crossover between two parent brains to create a child brain"""
    genome1 = parent1_brain.get_genome()
    genome2 = parent2_brain.get_genome()

    # Blend crossover: create child genome by blending parent genes
    child_genome = np.zeros_like(genome1)
    for i in range(len(genome1)):
        # For each gene, select random value between the two parent values
        min_val = min(genome1[i], genome2[i])
        max_val = max(genome1[i], genome2[i])
        child_genome[i] = np.random.uniform(min_val, max_val)
    child_genome = mutate_genome(child_genome)
    child_brain = NeuralNetwork(parent1_brain.input_nodes, parent1_brain.hidden_nodes, parent1_brain.output_nodes)
    child_brain.set_genome(child_genome)
    return child_brain

def mutate_genome(genome, mutation_rate=0.01):
    """Mutate the genome with a given mutation rate"""
    for i in range(len(genome)):
        if random.random() < mutation_rate:
            mutation_value = np.random.uniform(-0.5, 0.5)  # Small mutation
            genome[i] += mutation_value
    return genome

def calculate_fitness(players):
    
    """Calculate fitness based on score and survival time"""
    max_score = max((player.score for player in players), default=1)
    max_obstacle_avoided = max((player.obstacle_avoided for player in players), default=1)
    max_survival_time = max((player.survival_time for player in players), default=1)  
    max_moves_made = max((player.moves_made for player in players), default=1)
    
    # Additional safety: ensure no zero divisions
    max_score = max(max_score, 1)
    max_obstacle_avoided = max(max_obstacle_avoided, 1)
    max_survival_time = max(max_survival_time, 1)
    max_moves_made = max(max_moves_made, 1)
    for player in players:
        player.fitness = player.score ** 3

    # Normalize fitness values
    max_fitness = sum(player.fitness for player in players) if players else 1
    for player in players:
        player.fitness /= max_fitness
    # Debug info
    print(f"Generation stats - Max score: {max_score}, Max obstacles avoided: {max_obstacle_avoided}")
    print(f"Best player fitness: {max(p.fitness for p in players)}")
        
    return players

def weighted_selection(players, temp=0.2, p_value=0.5):
    """Select a player based on weighted probabilities with nucleus (top-p) sampling"""
    total_fitness = sum(player.fitness for player in players)
    if total_fitness == 0:
        return random.choice(players)  # Avoid division by zero

    probabilities = [player.fitness / total_fitness for player in players]

    # Apply temperature scaling
    scaled_probabilities = [p ** (1 / temp) for p in probabilities]
    total_scaled = sum(scaled_probabilities)
    if total_scaled == 0:
        return random.choice(players)  # Avoid division by zero

    scaled_probabilities = [p / total_scaled for p in scaled_probabilities]

    # Nucleus (top-p) sampling
    sorted_indices = np.argsort(scaled_probabilities)[::-1]
    sorted_probs = np.array(scaled_probabilities)[sorted_indices]
    cumulative_probs = np.cumsum(sorted_probs)
    cutoff = np.searchsorted(cumulative_probs, p_value) + 1

    # Select top-p players and normalize their probabilities
    top_indices = sorted_indices[:cutoff]
    top_probs = sorted_probs[:cutoff]
    top_probs /= top_probs.sum()

    selected_index = np.random.choice(top_indices, p=top_probs)
    return players[selected_index]