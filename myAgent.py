import numpy as np
import random
import math

playerName = "myAgent"
nPercepts = 75  #This is the number of percepts
nActions = 7    #This is the number of actionss
chromaLength = 525

# k-way tournament selection to find best parent
def k_way_tournament_selection_best(k, fitness):
    bestparent = random.randint(0,33)
    for i in range(0,k):
        newparent = random.randint(0,33)
        if fitness[newparent] > fitness[bestparent]:
            bestparent = newparent
    return bestparent

# roulette wheel selection to find parent
def roulette_selection(fitness):
    pick = random.uniform(0, sum(fitness))
    current = 0
    for n in range(0,34):
        current += fitness[n]
        if current > pick:
            return n

# This is the class for your creature/agent
class MyCreature:

    def __init__(self):

        # Initializing the chromosome with random genes.
        self.chromosome = []
        for i in range(0, chromaLength):
            self.chromosome.append(random.uniform(-2,2))

    # This is the agent function which takes in input and outputs actions
    def AgentFunction(self, percepts):
        # Uses a 75 perceptron array
        actions = np.zeros((nActions))
        perceptrons = percepts.flatten()
        count = 0
        for action_number in range(0,nActions):
            for percept in range(0,nPercepts):
                # Calculates action
                actions[action_number] += (perceptrons[percept] * self.chromosome[count])
                count += 1
        # Output actions
        return actions

def newGeneration(old_population):

    N = len(old_population)
    fitness = np.zeros((N))
    elitism = 0
    mutation_chance = 700
    size = []
    turn = []

    for n, creature in enumerate(old_population):
        size.append(creature.size)
        turn.append(creature.turn)
    for n, creature in enumerate(old_population):

        # creature.alive - boolean, true if creature is alive at the end of the game
        # creature.turn - turn that the creature lived to (last turn if creature survived the entire game)
        # creature.size - size of the creature
        # creature.strawb_eats - how many strawberries the creature ate
        # creature.enemy_eats - how much energy creature gained from eating enemies

        # Calculate fitness
        fitness[n] = pow(creature.size/max(size)+3 + creature.turn/max(turn)+2 + pow(np.mean(size),2), 3)

        # Change elitism and mutation amount
        if not creature.alive:
            elitism += 0.8
            mutation_chance -= 20

    # Sorts the agent according to fitness and creates a new population
    new_population = list()
    for n in range(N):

        # Create new creature
        new_creature = MyCreature()

        # Selecting parents
        first_parent = roulette_selection(fitness)
        second_parent = roulette_selection(fitness)

        # Random crossover
        for i in range(0, chromaLength):
            if random.randint(0, 1) == 0:
                new_creature.chromosome[i] = (old_population[first_parent].chromosome[i])
            else:
                new_creature.chromosome[i] = (old_population[second_parent].chromosome[i])

        # Mutation
        for i in range(0, chromaLength):
            if random.randint(0,mutation_chance) == 0:
                new_creature.chromosome[i] = random.uniform(-2,2)

        # Add the new agent to the new population
        new_population.append(new_creature)

    # elitism
    if elitism < 3: # min value
        elitism = 3
    elif elitism > 10: # max value
        elitism = 10
    for i in range(0,round(elitism)):
        new_population[i] = old_population[k_way_tournament_selection_best(30,fitness)]

    # At the end you neet to compute average fitness and return it along with your new population
    avg_fitness = np.mean(fitness)

    return (new_population, avg_fitness)