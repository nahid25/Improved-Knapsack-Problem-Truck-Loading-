import Genome
import random
import Items

rng = random.Random(101)
items = Items.ItemList()
items.setItems()


def test_genome():
    chr = Genome.Genome(rng)
    print(chr.calcScore(items))


def test_population():
    population = Genome.Population(rng)
    parent1 = population.pop[0]
    parent2 = population.pop[1]
    parent1.display()
    parent2.display()
    [child1, child2] = parent1.cross_over(parent2, rng)
    child1.display()
    child2.display()
    # for i in range(10):
    #     parent = population.select_parent(items, rng)
    #     parent.display()
    #     print(parent.calcScore(items))
    for gen in range(1000):
        population.selection(items, rng)
        print(population.pop[population.idOfBest(items)].calcScore(items))
        population.mutate(rng)
        population.deduplicate(rng)


if __name__ == "__main__":
    test_genome()
    test_population()
