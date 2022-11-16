import numpy as np


def result_probabilities(xg_home, xg_away):
    num_sim = 100000

    homeSimulatedScore = np.random.poisson(np.sum(xg_home), num_sim)
    awaySimulatedScore = np.random.poisson(np.sum(xg_away), num_sim)

    homeWins = 0
    awayWins = 0
    draws = 0

    for i in range(num_sim):
        if homeSimulatedScore[i] > awaySimulatedScore[i]:
            homeWins = homeWins + 1
        elif homeSimulatedScore[i] < awaySimulatedScore[i]:
            awayWins = awayWins + 1
        else:
            draws = draws + 1

    perc_home = homeWins / num_sim * 100
    perc_away = awayWins / num_sim * 100
    perc_draw = draws / num_sim * 100

    return perc_home, perc_away, perc_draw