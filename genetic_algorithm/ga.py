import random
import numpy as np
import logging

from collections import defaultdict
from copy import deepcopy
from deap import algorithms, base, creator, tools

from constraints.subject import Subject
from constraints.instructor import Instructor
from constraints.room import Room

from genetic_algorithm.individual import Individual as _Individual, Individual
from genetic_algorithm.mutation import mutation

from schedule.schedule import Schedule


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.FileHandler('app.log')
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s: %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


WEEKDAYS = {
    "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
    "Friday": 4, "Saturday": 5, "Sunday": 6
}


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
        logger.log(level=logging.INFO, msg=f"Individual created: {_individual.chromosomes}")
        return individual

    @staticmethod
    def room_fitness(schedule: Schedule) -> int:
        satisfied_subjects = defaultdict(set)
        unsatisfied_subjects = defaultdict(set)
        score = 0
        for room_id, day in schedule:
            for slots in day:
                # if our room is full we consider it as a good gene
                if slots.is_full():
                    score -= 15
                for subject, slot, room, instructor in slots:
                    if not subject:
                        continue
                    if room.room_type in subject.preferred_rooms:
                        score -= 10
                        satisfied_subjects[subject.subject_full_id].add(room.room_id)
                    else:
                        score += 15
                        unsatisfied_subjects[subject.subject_full_id].add(room.room_id)

        for satisfied_subject in satisfied_subjects.values():
            if len(satisfied_subject) == 1:
                score -= 35
            else:
                score += len(satisfied_subject) * 25

        for unsatisfied_subject in unsatisfied_subjects.values():
            score += len(unsatisfied_subject) * 45

        return score

    @staticmethod
    def subject_fitness(schedule: Schedule) -> int:
        score = 0

        # A happens in row: A Monday and A on Tuesday

        for subject_id, slots in schedule.subject_map.items():
            if not slots:
                continue
            nested_subjects = [0] * 7
            for slot in slots:
                nested_subjects[WEEKDAYS[slot.week_day]] += 1

            for v in nested_subjects:
                nested_subjects.append(v)
                if v >= 1:
                    break

            left = 0

            while left < len(nested_subjects):
                if nested_subjects[left] == 0:
                    left += 1
                    continue
                else:
                    right = left + 1
                    while right < len(nested_subjects) and nested_subjects[right] == 0:
                        right += 1
                    delta = right - left
                    if delta >= 5:
                        if 1 <= left and right < 4:
                            score -= 10 * delta
                        else:
                            score += 60
                    elif delta == 1:
                        score += 60
                    else:
                        score -= 10 * delta

                    if left < len(WEEKDAYS):
                        if nested_subjects[left] == 1:
                            score -= 20
                        else:
                            if len(slots) >= 5:
                                score += 12 * pow(nested_subjects[left], nested_subjects[left])
                            else:
                                score += 10 * pow(nested_subjects[left], nested_subjects[left])
                    left = right

        return score

    def instructor_fitness(self, schedule: Schedule) -> int:
        ...

    def fitness_function(self, individual: Individual):
        schedule = Schedule(self.rooms)
        score = 0
        # print(individual)
        for subject, slot, room, instructor in individual:
            is_assigned = schedule.assign_event(
                subject=subject,
                slot=slot,
                room=room,
                instructor=instructor,
            )
            if not is_assigned:
                score += 50

        score += self.room_fitness(schedule)
        score += self.subject_fitness(schedule)

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
