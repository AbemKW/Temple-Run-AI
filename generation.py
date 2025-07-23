import constants
from player import Player

def NewGeneration(saved_players):
    players = calculate_fitness(saved_players)
    
    for i in range(5):
        player = Player()
        players.append(player)
    return players

def calculate_fitness(players):
    """Calculate fitness based on score and survival time"""
    sum = 0
    for player in players:
        sum += player.score
    for player in players:
        player.fitness = player.score / sum if sum > 0 else 0
    return players