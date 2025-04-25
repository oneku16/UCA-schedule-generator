import numpy as np
import random
import logging
from collections import defaultdict
from copy import deepcopy
from deap import algorithms, base, creator, tools
from schedule.schedule_generator.constraints import Subject, Slot, Room, Instructor
from schedule.schedule_generator.genetic_algorithm import Individual as _Individual, mutation
from schedule.schedule_generator.schedule import Schedule

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.FileHandler('app.log')
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s: %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Constants
WEEKDAYS = {
    "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
    "Friday": 4, "Saturday": 5, "Sunday": 6
}


class GeneticAlgorithm:
    """
    A class for implementing a genetic algorithm to generate optimal schedules.

    The algorithm evaluates schedules based on room, subject, and instructor constraints,
    and evolves a population of schedules over multiple generations to find the best solution.
    Attributes:
        rooms (list[Room]): A list of Room instances to include in the schedule.
        subjects (list[Subject]): A list of Subject instances to include in the schedule.
        instructors (list[Instructor]): A list of Instructor instances to include in the schedule.
        population_size (int): The size of the population for the genetic algorithm.
        num_generations (int): The number of generations to evolve the population.
        cx_prob (float): The probability of crossover.
        mut_prob (float): The probability of mutation.
        independent_probability (float): The probability of independent mutation.
        toolbox (base.Toolbox): A DEAP toolbox for registering genetic operations.
    """
    def __init__(
            self,
            rooms: list[Room],
            subjects: list[Subject],
            instructors: list[Instructor],
    ):
        """
        Initializes a GeneticAlgorithm instance.
        Args:
            rooms (list[Room]): A list of Room instances.
            subjects (list[Subject]): A list of Subject instances.
            instructors (list[Instructor]): A list of Instructor instances.
        """
        self.rooms = rooms
        self.subjects = subjects
        self.instructors = instructors
        self.population_size = 100
        self.num_generations = 100
        self.cx_prob = 0.5
        self.mut_prob = 0.3
        self.independent_probability = .2

        # Create DEAP fitness and individual types
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        # Configure the DEAP toolbox
        self.toolbox = base.Toolbox()
        self.toolbox.register("individual", self.create_individual)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual, n=self.population_size)
        self.toolbox.register("mate", tools.cxOnePoint)
        self.toolbox.register("evaluate", self.fitness_function)
        self.toolbox.register("mutate", mutation, self.independent_probability, self.instructors, self.rooms)
        self.toolbox.register("select", tools.selTournament, tournsize=6)

    def create_individual(self):
        """
        Creates an individual for the genetic algorithm.
        Returns:
            creator.Individual: An individual representing a schedule.
        """
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
        """
        Evaluates the fitness of a schedule based on room constraints.
        Args:
            schedule (Schedule): The schedule to evaluate.
        Returns:
            int: The fitness score for room constraints.
        """
        satisfied_subjects = defaultdict(set)
        unsatisfied_subjects = defaultdict(set)
        score = 0
        for room_id, day in schedule:
            for slots in day:
                # If the room is full, consider it a good gene
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

        # Penalize or reward based on subject-room assignments
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
        """
        Evaluates the fitness of a schedule based on subject constraints.
        Args:
            schedule (Schedule): The schedule to evaluate.
        Returns:
            int: The fitness score for subject constraints.
        """
        score = 0

        # Evaluate subject distribution across days
        for subject_id, slots in schedule.subject_map.items():
            if not slots:
                continue
            nested_subjects = [0] * 7
            for slot in slots:
                nested_subjects[WEEKDAYS[slot.week_day]] += 1

            # Extend the list to handle circular evaluation
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
        """
        Evaluates the fitness of a schedule based on instructor constraints.

        Args:
            schedule (Schedule): The schedule to evaluate.

        Returns:
            int: The fitness score for instructor constraints.
        """
        # TODO: Implement instructor fitness logic
        return 0

    def fitness_function(self, individual: list[list[Subject, Slot, Room, Instructor]]) -> tuple[int]:
        """
        Evaluates the fitness of an individual (schedule).
        Args:
            individual (list[list[Subject, Slot, Room, Instructor]]): The individual to evaluate.
        Returns:
            tuple[int]: The fitness score for the individual.
        """
        schedule = Schedule(self.rooms)
        score = 0
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
        score += self.instructor_fitness(schedule)

        return (score,)

    def run(self):
        """
        Runs the genetic algorithm to evolve a population of schedules.

        Returns:
            creator.Individual: The best individual (schedule) found.
        """
        random.seed(42)
        population = self.toolbox.population()
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)

        # Evolve the population
        pop, logbook = algorithms.eaSimple(
            population, self.toolbox, self.cx_prob, self.mut_prob, self.num_generations,
            stats=stats, verbose=True
        )

        # Select the best individual
        best_individual = tools.selBest(pop, 1)[0]
        print("Best Schedule Fitness Score: ", best_individual.fitness.values)
        with open('fitness.txt', 'w') as file:
            file.write(f'best fitness value: {best_individual.fitness.values[0]}\n')
        return best_individual
