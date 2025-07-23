import constants
import random
import numpy as np
from model import NeuralNetwork
from player import Player

def NewGeneration(saved_players):
    players = calculate_fitness(saved_players)
    
    players.sort(key=lambda p: p.fitness, reverse=True)
    elite = players[:2]
    new_players = elite.copy()
    while len(new_players) < constants.POPULATION_SIZE:
        parent1 = tournament_selection(players)
        parent2 = tournament_selection(players)
        # Crossover
        child_brain = crossover(parent1.brain, parent2.brain)
        new_players.append(Player(child_brain))
    return new_players

def crossover(parent1_brain, parent2_brain):
    """Crossover between two parent brains to create a child brain"""
    genome1 = parent1_brain.get_genome()
    genome2 = parent2_brain.get_genome()
    
    # Simple crossover: take half from each parent
    crossover_point = len(genome1) // 2
    child_genome = np.concatenate((genome1[:crossover_point], genome2[crossover_point:]))
    
    child_brain = NeuralNetwork(parent1_brain.input_nodes, parent1_brain.hidden_nodes, parent1_brain.output_nodes)
    child_brain.set_genome(child_genome)
    return child_brain

def calculate_fitness(players):
    """Calculate fitness based on score and survival time"""
    sum = 0
    for player in players:
        sum += player.score
    for player in players:
        player.fitness = player.score / sum if sum > 0 else 0
    return players

def tournament_selection(players, k = 3):
    tournament = random.sample(players, min(k, len(players)))
    return max(tournament, key=lambda p: p.fitness)