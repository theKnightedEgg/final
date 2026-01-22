from parsetxt import parse_game_file
import random, math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

game = "rps.game"
population = 20
major_epoch = 100
epochs = 500    
learning_factor = 0.01
choices, title, labels, payoffs = parse_game_file(game)


fig, ax = plt.subplots()

time_averaged_players = [[0.0] * choices for _ in range(population)]
players = [np.random.dirichlet(np.ones(choices)).tolist() for _ in range(population)] # seed randomly


for epoch in range(epochs):
    # do round robin
    round_robin_matches = []
    for i, player in enumerate(players):
        for j, enemy in enumerate(players[i+1:], i+1):
            round_robin_matches.append([i, j])
    random.shuffle(round_robin_matches)

    for match in round_robin_matches:
        player = players[match[0]]
        enemy = players[match[1]]
        # make player choice
        player_roll = random.random()
        player_choice = 0
        sum = 0
        for choice, prob in enumerate(player):
            sum += prob
            if player_roll < sum:
                player_choice = choice
                break
        # make enemy choice
        enemy_roll = random.random()
        enemy_choice = 0
        sum = 0
        for choice, prob in enumerate(enemy):
            sum += prob
            if enemy_roll < sum:
                enemy_choice = choice
                break
        # play game
        result = payoffs[player_choice][enemy_choice]
        #print(f"Player {i} played {labels[player_choice]}. They scored {result[0]}. Player {j} played {labels[enemy_choice]}. They scored {result[1]}")
        # update scores
        average = (result[0] + result[1]) / 2
        player[player_choice] += (result[0] - average) * learning_factor#*= math.exp((result[0] - average) * learning_factor)
        players[match[0]] = [choice / math.fsum(player) for choice in player]
        enemy[enemy_choice] += (result[1] - average) * learning_factor#*= math.exp((result[1] - average) * learning_factor)
        players[match[1]] = [choice / math.fsum(enemy) for choice in enemy]
        # print(math.fsum(player))
        # print(math.fsum(enemy))

    # update time averages
    for i, player in enumerate(time_averaged_players):
        for j, weight in enumerate(player):
            player[j] = (weight * epoch + players[i][j]) / (epoch + 1)
        time_averaged_players[i] = player
    print(time_averaged_players)

    if epoch % major_epoch == 0:
        x = []
        y = []
        for player in time_averaged_players:
            x.append(player[0])
            y.append(player[1])
        ax.scatter(x, y, s=epoch, alpha=0.3, c="red")


plt.xlabel(labels[0])
plt.ylabel(labels[1])

plt.show()


            
            

