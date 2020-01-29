import random


class Genetic:
    miss_start = -1
    miss_end = -1
    genome_length = 0
    notes_before = []
    notes_after = []
    mutation_rate = 0.1

    def __init__(self, song):
        for index, note in enumerate(song):
            if note == 0 and self.miss_start == -1:
                self.miss_start = index
            if note != 0 and self.miss_start != -1 and self.miss_end == -1:
                self.miss_end = index

        self.genome_length = self.miss_end - self.miss_start

        self.notes_before = song[self.miss_start - 20:self.miss_start]
        self.notes_after = song[self.miss_end:self.miss_end + 20]

        self.max = max(song)
        for index, note in enumerate(song):
            if note == 0:
                song[index] = self.max
        self.min = min(song)

    def make_population(self, count):
        populations = []
        for i in range(count):
            temp_list = [random.randint(self.min, self.max) for iter in range(self.genome_length)]
            populations.append(temp_list)
        print("generated {} populations with length of {}!".format(count, self.genome_length))
        return populations

    def score_population(self, pop):
        return random.randint(0, 100)

    def mutate_population(self, pop):
        rand_position = random.randint(0, self.genome_length-1)
        random_note = random.randint(self.min, self.max)
        # print("mutating a population at position {} with the note {}!".format(rand_position, random_note))
        pop[rand_position] = random_note
        # print(pop[rand_position])
        return pop

    def mix_genomes(self, g1, g2):
        pivot1 = random.randint(0, self.genome_length / 2)
        pivot2 = random.randint(pivot1 + (self.genome_length / 4), self.genome_length)

        rg1 = g1.copy()  # return genome 1
        rg2 = g2.copy()  # return genome 2

        rg1[pivot1:pivot2] = g2[pivot1: pivot2]
        rg2[pivot1:pivot2] = g1[pivot1: pivot2]

        # print("-----------")
        # print(pivot1, pivot2)
        # print(g1)
        # print(rg1)
        # print(g2)
        # print(rg2)
        mutation_rand = random.uniform(0.00, 10.00)
        if mutation_rand <= (self.mutation_rate * 10):
            rg1 = self.mutate_population(rg1)
            # print("mutate rg1!")
        mutation_rand = random.uniform(0.00, 10.00)
        if mutation_rand <= (self.mutation_rate * 10):
            rg2 = self.mutate_population(rg2)
            # print("mutate rg2!")

        return rg1, rg2

    def run(self, iterations_count=5):
        populations_count = 100
        populations = self.make_population(populations_count)
        scores = [0] * populations_count

        i = 0
        while True:
            # score each population
            for j, pop in enumerate(populations):
                scores[j] = self.score_population(populations[j])
            # sort populations by score. since the lower the score the better population is, first 30 are the best
            populations = [x for _, x in sorted(zip(scores, populations))]
            # after sorting populations break if the iteration counts are finished
            if i > iterations_count:
                break
            new_population = [0] * populations_count
            # mix the first 30 for the first 60 of populations
            for index, pop in enumerate(populations[:int(0.3 * populations_count)]):
                couple_pop = populations[int(0.6 * populations_count) - index]
                # print(index, int(0.6 * populations_count) - index)
                new_population[index * 2], new_population[(index * 2) + 1] = self.mix_genomes(pop, couple_pop)
            # make 40 new genomes for the least 40 populations
            new_population[int(0.6 * populations_count):] = self.make_population(int(0.4 * populations_count))
            populations = new_population
            i += 1
