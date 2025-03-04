from copy import deepcopy

from deap import algorithms, base, creator, tools
import random
import numpy as np

from constraints.subject import Subject
from constraints.slot import Slot
from constraints.instructor import Instructor
from constraints.room import Room

from genetic_algorithm.crossover import random_crossover
from genetic_algorithm.individual import Individual as _Individual, Individual
from genetic_algorithm.mutation import mutation


class GA:
    def __init__(
            self,
            rooms: list[Room],
            subjects: list[Subject],
            instructors: list[Instructor],
    ):
        self.rooms = rooms
        self.subjects = subjects
        self.instructors = instructors
        self.population_size = 100
        self.num_generations = 100
        self.cx_prob = 0.8
        self.mut_prob = 0.4
        self.indpb = .15

        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        self.toolbox = base.Toolbox()
        self.toolbox.register("individual", self.create_individual)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual, n=self.population_size)
        self.toolbox.register("mate", tools.cxOnePoint)
        self.toolbox.register("evaluate", self.fitness_function)
        self.toolbox.register("mutate", mutation, self.indpb, self.instructors, self.rooms)
        self.toolbox.register("select", tools.selTournament, tournsize=6)

    def create_individual(self):
        _individual = _Individual()

        _individual.build(
            subjects=deepcopy(self.subjects),
            rooms=deepcopy(self.rooms),
            instructors=deepcopy(self.instructors),
        )
        individual = creator.Individual()
        for ind in _individual.chromosomes:
            individual.append(ind)
        # print(len(individual))
        return individual

    def fitness_function(self, individual: Individual):

        score = 0
        for subject, slot, room, instructor in individual:
            if room.room_type not in subject.preferred_rooms:
                score += 100
            if room.room_type in subject.preferred_rooms:
                score -= 50


        return (score,)

    def run(self):
        random.seed(42)
        population = self.toolbox.population()
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)

        pop, logbook = algorithms.eaSimple(
            population, self.toolbox, self.cx_prob, self.mut_prob, self.num_generations,
            stats=stats, verbose=True
        )

        best_individual = tools.selBest(pop, 1)[0]
        print("Best Schedule Fitness Score: ", best_individual.fitness.values)
        return best_individual
