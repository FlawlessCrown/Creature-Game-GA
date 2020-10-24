import numpy as np
import random

playerName = "myAgent"
nPercepts = 75  #This is the number of percepts
nActions = 7    #This is the number of actions
geneLength = 20  #This is the number of genes in the chromosome

# 0 movement type:
#   0: left
#   1: up
#   2: right
#   3: down
# 1 go eat food:
#   0: no
#   1: yes
# 2 random movement:
#   0: no
#   1: yes
# 3 dodge type:
#   0: backwards
#   1: sideways
# 4 dodge:
#   0: no
#   1: yes
# 5 see walls:
#   0: no
#   1: yes
# 6 dodge wall at range 1:
#   0: no
#   1: yes
# 7 dodge wall at range 2:
#   0: no
#   1: yes
# 8 see enemies:
#   0: no
#   1: yes
# 9 dodge large enemies:
#   0: no
#   1: yes
# 10 go after small enemies:
#   0: no
#   1: yes
# 11 see enemies range 1:
#   0: no
#   1: yes
# 12 see enemies range 2:
#   0: no
#   1: yes
# 13 see enemies range 3:
#   0: no
#   1: yes
# 14 see enemies range 4:
#   0: no
#   1: yes
# 15 see food range 1:
#   0: no
#   1: yes
# 16 see food range 2:
#   0: no
#   1: yes
# 17 see food range 3:
#   0: no
#   1: yes
# 18 see food range 4:
#   0: no
#   1: yes

# This is the class for your creature/agent
# Use this class to implement creature behaviour
class MyCreature:

    def __init__(self):
        # You should initialise self.chromosome member variable here (whatever you choose it
        # to be - a list/vector/matrix of numbers - and initialise it with some random
        # values
        
        # creating the chromosome
        # self.chromosome = []
        # for i in range(0, geneLength):
        #     if i == 5:
        #         self.chromosome.append(random.randint(0,2))
        #     elif i == 3 or i == 6 or i == 7 or i == 8 or i == 9 or i == 11:
        #         self.chromosome.append(random.randint(0,1))
                # self.chromosome.append(1)
            # elif i == 4:
            #     self.chromosome.append(2) # movement direction
            # else:
            #     self.chromosome.append(random.randint(0,4))
                # self.chromosome.append(4) # sets the perception to max range
        
        # creating the chromosome
        self.chromosome = []
        for i in range(0, geneLength):
            if i == 1:
                self.chromosome.append(random.randint(0,3))
            else:
                self.chromosome.append(random.randint(0,1))


    def AgentFunction(self, percepts):

        actions = np.zeros((nActions))

        # You should implement a model here that translates from 'percepts' to 'actions'
        # through 'self.chromosome'.
        
        # The 'actions' variable must be returned and it must be a 7-dim numpy vector or a
        # list with 7 numbers.
    
        # The index of the largest numbers in the 'actions' vector/list is the action taken
        # with the following interpretation:
        # 0 - move left
        # 1 - move up
        # 2 - move right
        # 3 - move down
        # 4 - do nothing
        # 5 - eat
        # 6 - move in a random direction
        
        # Different 'percepts' values should lead to different 'actions'.  This way the agent
        # reacts differently to different situations.

        # Percepts are a 5x5x3 tensor, where 5x5 is the region around the creatures
        # that it sees, and 3 corresponds to different maps.  Here's how to
        # extract different maps

        creature_map = percepts[:,:,0]  # 5x5 map with information about creatures and their size
        food_map = percepts[:,:,1]      # 5x5 map with information about strawberries
        wall_map = percepts[:,:,2]      # 5x5 map with information about wallss
        my_size = creature_map[2,2]

        # perceptron range value arrays
        perceptronrange =   [[[1,2],[2,1],[3,2],[2,3]],
                            [[0,2],[1,1],[2,0],[3,1],[4,2],[3,3],[2,4],[1,3]],
                            [[0,1],[1,0],[3,0],[4,1],[4,3],[3,4],[1,4],[0,3]],
                            [[0,0],[4,0],[4,4],[0,4]]]

        # a function which determines which way it moves
        # It checks for walls and friendlies
        def move(direction, count):
            if count >= 3:
                actions[4] = 1
            elif direction == 0:
                if (wall_map[1,2] == 1 and self.chromosome[6] == 1) or (wall_map[0,2] == 1 and self.chromosome[7] == 1) or (creature_map[1,2] > 0 and self.chromosome[11] == 1) or (creature_map[1,3] > 0 or creature_map[0,2] > 0 and self.chromosome[12] == 1):
                    move(1, count+1)
                else:
                    actions[0] = 1
            elif direction == 1:
                if (wall_map[2,1] == 1 and self.chromosome[6] == 1) or (wall_map[2,0] == 1 and self.chromosome[7] == 1) or (creature_map[2,1] > 0 and self.chromosome[11] == 1) or (creature_map[1,1] > 0 or creature_map[2,0] > 0 and self.chromosome[12] == 1):
                    move(2, count+1)
                else:
                    actions[1] = 1
            elif direction == 2:
                if (wall_map[3,2] == 1 and self.chromosome[6] == 1) or (wall_map[4,2] == 1 and self.chromosome[7] == 1) or (creature_map[3,2] > 0 and self.chromosome[11] == 1) or (creature_map[3,1] > 0 or creature_map[4,2] > 0 and self.chromosome[12] == 1):
                    move(3, count+1)
                else:
                    actions[2] = 1
            elif direction == 3:
                if (wall_map[2,3] == 1 and self.chromosome[6] == 1) or (wall_map[2,4] == 1 and self.chromosome[7] == 1) or (creature_map[2,3] > 0 and self.chromosome[11] == 1) or (creature_map[1,3] > 0 or creature_map[2,4] > 0 and self.chromosome[12] == 1):
                    move(0, count+1)
                else:
                    actions[3] = 1
            elif direction == 4:
                actions[4] = 1

        # Different 'self.chromosome' should lead to different 'actions'.  This way different
        # agents can exhibit different behaviour.

        # check for food if on it
        if food_map[2,2] == 1 and self.chromosome[1] == 1:
            actions[5] = 1
            return actions

        # checking range1
        if self.chromosome[11] == 1 or self.chromosome[15] == 1:
            count1 = 0
            for coord in perceptronrange[0]:
                if self.chromosome[8] == 1 and self.chromosome[11] == 1:
                    # check for larger enemies
                    if self.chromosome[9] == 1:
                        if abs(creature_map[coord[0],coord[1]]) > my_size and creature_map[coord[0],coord[1]] < 0:
                            if self.chromosome[3] == 1:
                                if count1+1 >= 4:
                                    move(count1-1,0)
                                else:
                                    move(count1+1,0)
                            else:
                                if count1 >= 2:
                                    move(count1-2,0)
                                else:
                                    move(count1+2,0)
                            return actions
                    # check for smaller enemies
                    if self.chromosome[10] == 1:
                        if abs(creature_map[coord[0],coord[1]]) < my_size and creature_map[coord[0],coord[1]] < 0:
                            move(count1,0)
                            return actions
                # check for food
                if self.chromosome[15] == 1 and self.chromosome[1] == 1:
                    if food_map[coord[0],coord[1]] == 1:
                        move(count1,0)
                        return actions
                count1 += 1

        # checking range2
        if self.chromosome[12] == 1 or self.chromosome[16] == 1:
            count2 = 0
            for coord in perceptronrange[1]:
                if self.chromosome[8] == 1 and self.chromosome[12] == 1:
                    # check for larger enemies
                    if self.chromosome[9] == 1:
                        if abs(creature_map[coord[0],coord[1]]) > my_size and creature_map[coord[0],coord[1]] < 0:
                            if self.chromosome[3] == 1:
                                if int(count2/2) == 0:
                                    move(3,0)
                                elif int(count2/2) == 1:
                                    move(0,0)
                                elif int(count2/2) == 2:
                                    move(1,0)
                                elif int(count2/2) == 3:
                                    move(2,0)
                            else:
                                if int(count2/2) >= 2:
                                    move(int(count2/2)-2,0)
                                else:
                                    move(int(count2/2)+2,0)
                            return actions
                    # check for smaller enemies
                    if self.chromosome[10] == 1:
                        if abs(creature_map[coord[0],coord[1]]) < my_size and creature_map[coord[0],coord[1]] < 0:
                            if (int(count2/2) >= 4):
                                move(0,0)
                            else:
                                move(int(count2/2),0)
                            return actions
                # check for food
                if self.chromosome[16] == 1 and self.chromosome[1] == 1:
                    if food_map[coord[0],coord[1]] == 1 and self.chromosome[2] == 1:
                        if (int(count2/2) >= 4):
                            move(0,0)
                        else:
                            move(int(count2/2),0)
                        return actions
                count2 += 1

        # checking range3
        if self.chromosome[13] == 1 or self.chromosome[17] == 1:
            count3 = 0
            for coord in perceptronrange[2]:
                if self.chromosome[8] == 1 and self.chromosome[13] == 1:
                    # check for larger enemies
                    if self.chromosome[9] == 1:
                        if abs(creature_map[coord[0],coord[1]]) > my_size and creature_map[coord[0],coord[1]] < 0:
                            if self.chromosome[3] == 1:
                                if int(count3/2) == 0:
                                    move(3,0)
                                elif int(count3/2) == 1:
                                    move(0,0)
                                elif int(count3/2) == 2:
                                    move(1,0)
                                elif int(count3/2) == 3:
                                    move(2,0)
                            else:
                                if int(count3/2) >= 2:
                                    move(int(count3/2)-2,0)
                                else:
                                    move(int(count3/2)+2,0)
                            return actions
                    # check for smaller enemies
                    if self.chromosome[10] == 1:
                        if abs(creature_map[coord[0],coord[1]]) < my_size and creature_map[coord[0],coord[1]] < 0:
                            if (int(count3/2) >= 4):
                                move(0,0)
                            else:
                                move(int(count3/2),0)
                            return actions
                # check for food
                if self.chromosome[17] == 1 and self.chromosome[1] == 1:
                    if food_map[coord[0],coord[1]] == 1 and self.chromosome[2] == 1:
                        if (int(count3/2) >= 4):
                            move(0,0)
                        else:
                            move(int(count3/2),0)
                        return actions
                count3 += 1

        # checking range4
        if self.chromosome[14] == 1 or self.chromosome[18] == 1:
            count4 = 0
            for coord in perceptronrange[3]:
                if self.chromosome[8] == 1 and self.chromosome[14] == 1:
                    # check for larger enemies
                    if self.chromosome[9] == 1:
                        if abs(creature_map[coord[0],coord[1]]) > my_size and creature_map[coord[0],coord[1]] < 0:
                            if self.chromosome[3] == 1:
                                if count4+1 >= 4:
                                    move(count4-1,0)
                                else:
                                    move(count4+1,0)
                            elif self.chromosome[3] == 0:
                                if count4 >= 2:
                                    move(count4-2,0)
                                else:
                                    move(count4+2,0)
                            return actions
                    # check for smaller enemies
                    if self.chromosome[10] == 1:
                        if abs(creature_map[coord[0],coord[1]]) < my_size and creature_map[coord[0],coord[1]] < 0:
                            move(count4,0)
                            return actions
                # check for food
                if self.chromosome[18] == 1 and self.chromosome[1] == 1:
                    if food_map[coord[0],coord[1]] == 1 and self.chromosome[2] == 1:
                        move(count4,0)
                        return actions
                count4 += 1

        # move when there is nothing to do
        if self.chromosome[2] == 1:
            actions[6] = 1
        else:
            if self.chromosome[0] == 0 or self.chromosome[0] == 1 or self.chromosome[0] == 2 or self.chromosome[0] == 3:
                move(self.chromosome[0], 0)
            else:
                actions[4] = 1
        return actions
        


def newGeneration(old_population):

    # k-way tournament selection to find parent
    def k_way_tournament_selection_best(k):
        bestparent = 0
        for i in range(0,k):
            parent = random.randint(0,N-1)
            if fitness[parent] > fitness[bestparent]:
                bestparent = parent
        return bestparent

    # roulette wheel selection to find parent
    def roulette_selection():
        max = sum(fitness)
        pick = random.uniform(0, max)
        current = 0
        for n in range(0,N):
            current += fitness[n]
            if current > pick:
                return n

    # rescaling fitness function to normalize the different parameters
    def rescale(m_o):
        return ((m_o - min(m_o))/(max(m_o) - min(m_o)))

    # This function should return a list of 'new_agents' that is of the same length as the
    # list of 'old_agents'.  That is, if previous game was played with N agents, the next game
    # should be played with N agents again.

    # This function should also return average fitness of the old_population
    N = len(old_population)

    # Fitness for all agents
    fitness = np.zeros((N))

    elitism = 0

    mutation_chance = 500

    # mutation
    mutation_chance = 690 # 1/mutation_chance

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


        # This fitness functions just considers length of survival.  It's probably not a great fitness
        # function - you might want to use information from other stats as well


        fitness[n] = round(pow(creature.size,3))
        fitness[n] += round(pow(creature.turn/33,2))

        if not creature.alive:
            # increase the amount of elitists
            elitism += 1
            # increase the mutation chance when more are dead
            mutation_chance -= 10


    # At this point you should sort the agent according to fitness and create new population
    new_population = list()
    for n in range(N):

        # Create new creature
        new_creature = MyCreature()

        # Here you should modify the new_creature's chromosome by selecting two parents (based on their
        # fitness) and crossing their chromosome to overwrite new_creature.chromosome

        # Consider implementing elitism, mutation and various other
        # strategies for producing new creature.

        # This uses tournament selection to find the parents
        # ktimes = 10
        # first_parent = k_way_tournament_selection_best(ktimes)
        # second_parent = k_way_tournament_selection_best(ktimes)
        # while second_parent == first_parent:
        #     if ktimes > 4:
        #         ktimes -= 1
        #     else:
        #         ktimes = 11
        #     second_parent = k_way_tournament_selection_best(ktimes)

        # This uses a selection method uses roulette wheel selection
        first_parent = roulette_selection()
        second_parent = roulette_selection()
        
        
        # crossover
        for i in range(0, geneLength):
            if random.randint(0, fitness[first_parent]+fitness[second_parent]) >= max(fitness[first_parent],fitness[second_parent]):
                new_creature.chromosome[i] = (old_population[first_parent].chromosome[i])
            else:
                new_creature.chromosome[i] = (old_population[second_parent].chromosome[i])

        # mutation
        for i in range(0, geneLength):
            if random.randint(0,100) == 0:
                if i == 1:
                    new_creature.chromosome[i] = (random.randint(0,3))
                else:
                    new_creature.chromosome[i] = (random.randint(0,1))

        # Add the new agent to the new population
        new_population.append(new_creature)

    # elitism
    if elitism < 4: # min
        elitism = 4
    elif elitism > 15: # max
        elitism = 20
    for i in range(0,round(elitism)):
        new_population[i] = old_population[k_way_tournament_selection_best(30)]


    # At the end you need to compute average fitness and return it along with your new population
    avg_fitness = np.mean(fitness)

    return (new_population, avg_fitness)
