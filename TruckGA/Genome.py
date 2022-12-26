import math
import time
import random

import Items
import g


def rnd(rng, lo, hi):
    """ return a random real number in the range [a, b) """
    return (hi - lo) * rng.random() + lo;


def rndInt(rng, lo, hi):
    """ retun a random number in the range [a, b) """
    return rng.randrange(lo, hi)


class Genome(object):
    genes = []
    score = 0;
    generation = 0;
    mutations = 0;

    def __init__(self, rng):
        """ populates the new genome with random numbers """
        self.genes = [rndInt(rng, 0, g.NUM_OF_TRUCKS + 1) for i in range(g.NUM_OF_ITEMS)]
        self.score = g.marker
        self.generation = 0
        self.mutations = 0

    def calcScore(self, itemList: [Items.Item]) -> float:  # ItemList lst
        """ return the genome score """
        if self.score != g.marker:
            return self.score  # already scored
        self.score = 0
        trucks = [[] for i in range(g.NUM_OF_TRUCKS)]
        loaded_items = []
        for item_idx in range(g.NUM_OF_ITEMS):
            if self.genes[item_idx] > 0:
                truck_id = self.genes[item_idx] - 1
                trucks[truck_id].append(itemList.lst[item_idx])
                loaded_items.append(itemList.lst[item_idx])

        has_hospital_triage_unit = any(item.name == "Triage" for item in loaded_items)
        has_hospital_triage_unit_score = 1 if has_hospital_triage_unit else -1  # award if hospital triage unit is loaded, otherwise give a penalty

        hospital_parts_cnt = sum(
            [1 for item in loaded_items if item.name == "Hospital I" or item.name == "Hospital II"])
        take_both_or_none_hospital_parts_score = 1 if (
                hospital_parts_cnt != 1) else -1  # award if zero or two hospital parts are loaded, otherwise give a penalty

        fuel_items_cnt = sum(
            [1 for item in loaded_items if (item.name in ["Petrol44a", "Petrol44b", "Petrol20", "Guzzoline e10"])])
        fuel_items_score = (min(fuel_items_cnt, 2) / 2)  # award according to the number of petrol items loaded

        critical_items_cnt = sum([1 for item in loaded_items if item.importance == "C"])
        very_important_items_cnt = sum([1 for item in loaded_items if item.importance == "V"])
        important_items_cnt = sum([1 for item in loaded_items if item.importance == "I"])

        not_important_items_cnt = sum([1 for item in loaded_items if item.importance == "N"])
        critical_items_score = critical_items_cnt / g.NUM_OF_ITEMS * 4 * 1  # award a high score base on number of critical items loaded
        very_important_items_score = very_important_items_cnt / g.NUM_OF_ITEMS * 4 * 0.3  # award a medium score base on number of very important items loaded
        important_items_score = important_items_cnt / g.NUM_OF_ITEMS * 4 * 0.1  # award a small score base on number of important items loaded
        not_important_items_score = not_important_items_cnt / g.NUM_OF_ITEMS * 4 * -1  # give a penalty on number of not important items loaded
        priority_score = critical_items_score + very_important_items_score + important_items_score + not_important_items_score

        total_items_size_in_trucks = [sum([item.size for item in truck]) for truck in trucks]
        size_score = [((1.0 - (g.TRUCK_CAPACITY - total_size) / g.TRUCK_CAPACITY) if total_size <= g.TRUCK_CAPACITY
                       else -1 * total_size / g.TRUCK_CAPACITY) for total_size in
                      total_items_size_in_trucks]  # give a penalty if overloaded, award if underloaded

        self.score = (has_hospital_triage_unit_score + take_both_or_none_hospital_parts_score + fuel_items_score + sum(
            size_score)) * 3 + priority_score

        return self.score

    def cross_over(self, parent2, rng):
        """ bred with parent2 to create 2 new offspring

        :return: 2 new offspring
        """
        child1 = self.copy(rng)
        child2 = parent2.copy(rng)
        for i in range(g.NUM_OF_ITEMS):
            if rndInt(rng, 0, 7) == 0:
                child1.genes[i] = self.genes[i]
                child2.genes[i] = parent2.genes[i]
            else:
                child2.genes[i] = self.genes[i]
                child1.genes[i] = parent2.genes[i]

        return [child1, child2]

    def copy(self, rng):
        """ make a copy """
        clone = Genome(rng)
        clone.genes = self.genes.copy()
        clone.score = g.marker
        clone.generation = self.generation
        clone.mutations = self.mutations
        return clone

    def mutate(self, rng):
        """ perform 5 mutagenic operations """
        for i in range(5):
            n = rndInt(rng, 0, 3)
            if n == 0:
                # replace 1 randome selected gene
                item_idx = rndInt(rng, 0, g.NUM_OF_ITEMS)
                self.genes[item_idx] = rndInt(rng, 0, g.NUM_OF_TRUCKS + 1)
            elif n == 1:
                # swap 2 random selected genes
                item_idx = rndInt(rng, 0, g.NUM_OF_ITEMS)
                item_idx1 = rndInt(rng, 0, g.NUM_OF_ITEMS)
                tmp = self.genes[item_idx]
                self.genes[item_idx] = self.genes[item_idx1]
                self.genes[item_idx1] = tmp
            else:
                item_idx = rndInt(rng, 0, g.NUM_OF_ITEMS)
                self.genes[item_idx] = 0
        self.mutations += 1

    def is_equal(self, genome1):
        """ check if current genome have the same genes as another genome or not"""
        return all(self.genes[i] == genome1.genes[i] for i in range(g.NUM_OF_ITEMS))

    def __str__(self):
        retv = "["
        for gene in self.genes:
            retv += str(gene) + ", "
        retv += "]"
        return retv
    
    def show(self):
        print(self.__str__())

    def display(self):
        print('[', end='')
        for gene in self.genes:
            print(gene, end=',')
        print(']')


class Population:
    pop = []  # the genomes of the population
    generation = 0
    deduplicated_cnt = 0

    def __init__(self, rng):
        self.pop = [Genome(rng) for i in range(g.POPULATION)]
        deduplicated_cnt = 0
        generation = 0

    def idOfBest(self, itemList):  # highest score
        """ return id of the best individual """
        retv = 0
        for ind_idx in range(g.POPULATION):
            if self.pop[ind_idx].calcScore(itemList) > self.pop[retv].calcScore(itemList):
                retv = ind_idx
        return retv

    def calcScore(self, itemList):
        """ return the sum of the scores of all individuals in the population """
        retv = 0
        for i in range(0, g.POPULATION):  # for each genome in the population
            retv += self.pop[i].calcScore(itemList)  # add the score of the current genome to the total score
        return retv

    def select_parent(self, itemList, rng):
        """ Select a parent using tournament selection method
        1. Select a random set of 3 individuals
        2. take the best individual as a parent
        """
        tournament_size = 3
        tournament = [rndInt(rng, 0, g.POPULATION) for i in range(tournament_size)]
        best = max(tournament, key=lambda x: self.pop[x].calcScore(itemList))
        return self.pop[best]

    def selection(self, itemList, rng):
        """ Create a new generation from the current generation """
        new_pop = []
        for i in range(g.POPULATION // 2):
            # select 2 parents
            parent1 = self.select_parent(itemList, rng)
            parent2 = self.select_parent(itemList, rng)
            # create 2 new children
            [child1, child2] = parent1.cross_over(parent2, rng)
            # add 2 new children to the new population
            new_pop.append(child1)
            new_pop.append(child2)
        assert len(new_pop) == g.POPULATION
        self.pop = new_pop
        self.generation += 1

    def mutate(self, rng):
            """ each individual has a small probability to be mutated """
            print("\nbegin to mutate the population in the generation {}:".format(self.generation))
            for individual_idx in range(g.POPULATION):
                if rnd(rng, 0, 100) < g.MUTATIONPERCENT:
                    print("genome {} is being seleted to mutate".format(individual_idx))
                    print("before mutating: {}".format(self.pop[individual_idx]))
                    self.pop[individual_idx].mutate(rng)
                    print("after mutating : {}".format(self.pop[individual_idx]))
                    g.mutations += 1

    def deduplicate(self, rng):
        """ mutate the duplicated genes in the gene pool"""
        print("\nbegin to mutate all duplicated genes in the generation {}".format(self.generation))
        for i in range(g.POPULATION):
            for j in range(i + 1, g.POPULATION):
                if self.pop[i].is_equal(self.pop[j]):  # two genome are the same
                    print("genome {} and {} are the same, so perform mutation on genome {}".format(i, j, j))
                    print("genome {} before mutating: {}".format(j, self.pop[j]))
                    self.pop[j].mutate(rng)
                    print("genome {} after mutating : {}".format(j, self.pop[j]))
                    self.deduplicated_cnt += 1
