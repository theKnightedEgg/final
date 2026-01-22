from parsetxt import parse_game_file
import random, math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys
import ternary

game = sys.argv[1]
population = 20
epochs = 500   
major_epoch = epochs / 5
learning_factor = 0.01
choices, title, labels, payoffs = parse_game_file(game)


fig, ax = plt.subplots()
if choices == 3:
    fig, ax = ternary.figure()

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
        player[player_choice] = max(0, player[player_choice])
        players[match[0]] = [choice / math.fsum(player) for choice in player]
        enemy[enemy_choice] += (result[1] - average) * learning_factor#*= math.exp((result[1] - average) * learning_factor)
        enemy[enemy_choice] = max(0, enemy[enemy_choice])
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
        size = epoch + major_epoch
        x = []
        y = []
        z = []
        for player in time_averaged_players:
            x.append(player[0])
            y.append(player[1])
        if choices == 3:
            ax.scatter(time_averaged_players, s=size, alpha=0.3, label=f"epoch {epoch}", c="red")
        else:
            ax.scatter(x, y, s=size, alpha=0.3, label=f"epoch {epoch}", c="red")


if choices == 3:
    ax.scatter(time_averaged_players, s=size, alpha=0.3, label=f"epoch {epoch}", c="red")
    ax.set_title("Nash equilibria convergence for " + title)
    ax.boundary(linewidth=2.0)
    ax.gridlines(color="black", multiple=0.5)
    ax.gridlines(color="blue", multiple=0.1, linewidth=0.5)
    ax.left_axis_label(labels[0])
    ax.right_axis_label(labels[1])
    ax.bottom_axis_label(labels[2])
    ax.clear_matplotlib_ticks()
    ax.ticks(axis='lbr')
    ax.legend()
    ternary.plt.show()
else:
    ax.scatter(x, y, s=size, alpha=0.3, label=f"epoch {epoch}", c="red")
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])
    plt.title("Nash equilibria convergence for " + title)
    ax.grid(True)
    ax.legend()
    plt.show()




            
            

