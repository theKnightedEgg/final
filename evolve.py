import random, math
import numpy as np
from parsetxt import *

game = "staghunt.game"
population_size = 20
max_epochs = 1000

choices, title, labels, payoffs = parse_game_file(game)
population = [[random.random() for _ in range(choices - 1)] for _ in range(population_size)]
for pop in population:
    pop.sort()

epoch = 0

def do_epoch():
    
    # calculate fitnesses by playing them one on one
    fitnesses = [0] * population_size
    order = [i for i in range(population_size)]
    random.shuffle(order)
    while len(order) > 0:
        # play game
        index_one = order.pop()
        player_one = population[index_one]
        choice_one = 0
        spin_one = random.random()
        for prob in player_one:
            if spin_one > prob:
                choice_one += 1
        
            
        index_two = order.pop()
        player_two = population[index_two]
        choice_two = 0
        spin_two = random.random()
        for prob in player_two:
            if spin_two > prob:
                choice_two += 1
        

        score = payoffs[choice_one][choice_two]
        fitnesses[index_one] = float(score[0])
        fitnesses[index_two] = float(score[1])
        print(f"Player {index_one}, with probability {player_one}, rolled a {spin_one}, so they choose to {labels[choice_one]}. They get a score of {score[0]}")
        print(f"Player {index_two}, with probability {player_two}, rolled a {spin_two}, so they choose to {labels[choice_two]}. They get a score of {score[1]}")


    # use roulette method to decide parents
    parents = []
    while len(parents) < population_size / 2:
        sum = math.fsum(fitnesses)
        for i, fitness in enumerate(fitnesses):
            fitnesses[i] = fitness / sum
        
        roll = random.random()
        pick = 0
        sum = 0

        for i, prob in enumerate(fitnesses):
            sum += prob
            if sum > roll:
                pick = i
                break
        print(f"Player {population[pick]}, who had adusted fitness {fitnesses[pick]}, was chosen as a parent")
        parents.append(population[pick])
        population.pop(pick)
        fitnesses.pop(pick)

    # propogate by taking the average
        
    


        
        
do_epoch()