from converter import Converter
from brute_force_3.patterns import SubjectPattern
from brute_force_3.rooms import Room, get_room, TutorialRoom
from brute_force_3.schedule_generator import ScheduleGenerator
from brute_force_3.xlsx_generator.table_generator import TableGenerator
from config import ROOMS
from brute_force_3.serializer import Serializer
from pprint import pprint


from deap import algorithms, base, creator, tools
import random
import numpy as np


class GeneticAlgorithmScheduler:
    def __init__(self, rooms: list[Room], subjects: list[SubjectPattern]):
        self.rooms = rooms
        self.subjects = subjects
        self.population_size = 100
        self.num_generations = 25
        self.cx_prob = 0.8
        self.mut_prob = 0.4
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        self.toolbox = base.Toolbox()
        self.toolbox.register("individual", self.create_individual)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual, n=self.population_size)
        self.toolbox.register("mate", tools.cxOnePoint)
        self.toolbox.register("evaluate", self.fitness_function)
        self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=6)

    def create_individual(self):
        subjects, classrooms = self.subjects, self.classrooms
        individual = creator.Individual()

        for subject in subjects:
            for classroom in classrooms:
                # if subject
                ...



def main():

    from_converter = Converter().xlsx_to_json()

    subject_patterns: list[SubjectPattern] = [SubjectPattern(subject_data=subject) for subject in from_converter]
    subject_patterns.sort(key=lambda subject: subject.priority, reverse=True)
    rooms: list[Room] = [get_room(**room) for room in ROOMS]

    # pprint(subject_patterns)
    # pprint(rooms)
    subject = subject_patterns[0].subjects[0].required_rooms
    print(subject)

    #
    # schedule_generator = ScheduleGenerator(rooms=rooms, subject_patterns=subject_patterns)
    # schedule_generator.balanced_schedule()
    #
    # serializer = Serializer(rooms=schedule_generator.rooms)
    # schedules = serializer.room_mode_to_cohort()
    # # pprint(from_converter)
    # pprint(dict(schedules))
    # for cohort, schedule in schedules.items():
    #     table = TableGenerator(title=cohort, sequence=schedule)
    #     table.generate_table()


if __name__ == '__main__':
    main()
