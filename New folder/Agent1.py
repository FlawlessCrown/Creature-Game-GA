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
    max = sum(fitness)
    pick = random.uniform(0, max)
    current = 0
    for n in range(0,34):
        current += fitness[n]
        if current > pick:
            return n

# calculates the sigmoid (outputs value in the range of -1 to 1)
def sigmoid(x):
  return 1 / (1 + math.exp(-x))

# This is the class for your creature/agent
class MyCreature:

    def __init__(self):
        # You should initialise self.chromosome member variable here (whatever you choose it
        # to be - a list/vector/matrix of numbers - and initialise it with some random
        # values

        self.chromosome = []
        for i in range(0, chromaLength):
            self.chromosome.append(random.uniform(-2,2))


    def AgentFunction(self, percepts):

        actions = np.zeros((nActions))

        # You should implement a model here that translates from 'percepts' to 'actions'
        # through 'self.chromosome'.
        #
        # The 'actions' variable must be returned and it must be a 7-dim numpy vector or a
        # list with 7 numbers.
        #
        # The index of the largest numbers in the 'actions' vector/list is the action taken
        # with the following interpretation:
        # 0 - move left
        # 1 - move up
        # 2 - move right
        # 3 - move down
        # 4 - do nothing
        # 5 - eat
        # 6 - move in a random direction
        #
        # Different 'percepts' values should lead to different 'actions'.  This way the agent
        # reacts differently to different situations.
        #
        # Different 'self.chromosome' should lead to different 'actions'.  This way different
        # agents can exhibit different behaviour.

        #  uses 75 percepts
        perceptrons = percepts.flatten()
        count = 0
        for i in range(0,7):
            for j in range(0,len(perceptrons)):
                actions[i] += (perceptrons[j] * self.chromosome[count])
                count += 1


        # uses 25 percepts instead of 75
        # creature_map = percepts[:,:,0]  # 5x5 map with information about creatures and their size
        # food_map = percepts[:,:,1]      # 5x5 map with information about strawberries
        # wall_map = percepts[:,:,2]      # 5x5 map with information about wallss
        # my_size = creature_map[2,2]
        # perceptrons = []
        # for i in range(0,5):
        #     for j in range(0,5):
        #         if creature_map[i,j] < 0 and abs(creature_map[i,j]) > my_size:
        #             perceptrons.append(1)
        #         elif (i != 2 and j != 2) and( wall_map[i,j] == 1 or creature_map[i,j] > 0):
        #             perceptrons.append(2)
        #         elif (food_map[i,j] == 1):
        #             perceptrons.append(3)
        #         elif (abs(creature_map[i,j]) < my_size and creature_map[i,j] < 0):
        #             perceptrons.append(4)
        #         else:
        #             perceptrons.append(0)
        # count = 0
        # for i in range(0,7):
        #     for j in range(0,len(perceptrons)):
        #         actions[i] += ( (perceptrons[j] * self.chromosome[count]) )
        #         count += 1

        return actions

def newGeneration(old_population):

    # This function should return a list of 'new_agents' that is of the same length as the
    # list of 'old_agents'.  That is, if previous game was played with N agents, the next game
    # should be played with N agents again.

    # This function should also return average fitness of the old_population
    N = len(old_population)

    # Fitness for all agents
    fitness = np.zeros((N))

    elitism = 0

    mutation_chance = 500

    # This loop iterates over your agents in the old population - the purpose of this boiler plate
    # code is to demonstrate how to fetch information from the old_population in order
    # to score fitness of each agent
    for n, creature in enumerate(old_population):

        # creature is an instance of MyCreature that you implemented above, therefore you can access any attributes
        # (such as `self.chromosome').  Additionally, the objects has attributes provided by the
        # game enginne:
        #
        # creature.alive - boolean, true if creature is alive at the end of the game
        # creature.turn - turn that the creature lived to (last turn if creature survived the entire game)
        # creature.size - size of the creature
        # creature.strawb_eats - how many strawberries the creature ate
        # creature.enemy_eats - how much energy creature gained from eating enemies

        
        fitness[n] = round(pow(creature.size,3))
        fitness[n] += round(pow(creature.turn/35,2))
        

        if not creature.alive:
            # increase the amount of elitists
            elitism += 1
            # increase the mutation chance when more are dead
            mutation_chance -= 10


        # This fitness functions just considers length of survival.  It's probably not a great fitness
        # function - you might want to use information from other stats as well
        # fitness[n] = creature.turn

    # At this point you should sort the agent according to fitness and create new population
    new_population = list()
    for n in range(N):

        # Create new creature
        new_creature = MyCreature()

        # Here you should modify the new_creature's chromosome by selecting two parents (based on their
        # fitness) and crossing their chromosome to overwrite new_creature.chromosome

        first_parent = roulette_selection(fitness)
        second_parent = roulette_selection(fitness)

        # Consider implementing elitism, mutation and various other
        # strategies for producing new creature.

        # crossover
        for i in range(0, chromaLength):
            if random.randint(0, 1) == 0:
                new_creature.chromosome[i] = (old_population[first_parent].chromosome[i])
            else:
                new_creature.chromosome[i] = (old_population[second_parent].chromosome[i])

        # mutation
        for i in range(0, chromaLength):
            if random.randint(0,mutation_chance) == 0:
                new_creature.chromosome[i] = random.uniform(-2,2)

        # Add the new agent to the new population
        new_population.append(new_creature)

    # elitism
    if elitism < 3: # min
        elitism = 3
    elif elitism > 10: # max
        elitism = 10
    for i in range(0,round(elitism)):
        new_population[i] = old_population[k_way_tournament_selection_best(30,fitness)]

    # At the end you neet to compute average fitness and return it along with your new population
    avg_fitness = np.mean(fitness)

    return (new_population, avg_fitness)