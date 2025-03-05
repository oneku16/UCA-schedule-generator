from array import array
from logging import getLogger

from collections import defaultdict, Counter
from random import choice

from numpy.ma.core import empty

from converter import Converter
from brute_force_3.patterns import SubjectPattern
from brute_force_3.rooms import Room, get_room, TutorialRoom, LaboratoryRoom, LectureRoom, PhysicalTrainingRoom
from config import ROOMS, DAYS
from pprint import pprint
from brute_force_3.subject import Subject


from deap import algorithms, base, creator, tools
import random
import numpy as np


from fyp.objects import room as rm
from fyp.objects import subject as sbj
from fyp.objects import cohorts_schedule as sched
from fyp.objects import slot as sl

from copy import deepcopy


logger = getLogger(__name__)


# class GeneticAlgorithmScheduler:
#     def __init__(self, rooms: list[rm.Room], subjects: list[sbj.Subject], cohort_schedule: sched.CohortsSchedule):
#         self.rooms = rooms
#         self.subjects = subjects
#         self.cohort_schedule = cohort_schedule
#         self.population_size = 1
#         self.num_generations = 24
#         self.cx_prob = 0.8
#         self.mut_prob = 0.4
#
#         creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
#         creator.create("Individual", list, fitness=creator.FitnessMin)
#
#         self.toolbox = base.Toolbox()
#         self.toolbox.register("individual", self.create_individual)
#         self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual, n=self.population_size)
#         self.toolbox.register("mate", tools.cxOnePoint)
#         self.toolbox.register("evaluate", self.fitness_function)
#         self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
#         self.toolbox.register("select", tools.selTournament, tournsize=6)
#
#     def mutate(self, individual):
#         print(1112)
#
#     def create_individual(self):
#         cohort_schedule = deepcopy(self.cohort_schedule)
#         subjects = deepcopy(self.subjects)
#         rooms = deepcopy(self.rooms)
#
#         individual: list[tuple[str, sbj.Subject, rm.Room, str, sl.Slot, int]] = creator.Individual()
#
#         for cohort, schedule in cohort_schedule:
#             for subject in subjects:
#                 if cohort != subject.cohort:
#                     continue
#                 while room := choice(rooms):
#                     if room.is_empty_slot():
#                         room_empty_slot_1, room_empty_slot_2 = room.get_empty_slots(subject=subject)
#                         schedule_empty_slot = schedule.get_empty_slots()
#                         is_allocated = False
#                         common = defaultdict(list)
#                         for day, quarters in schedule_empty_slot.items():
#                             if day in room_empty_slot_1:
#                                 empty_slots = [quarter for quarter in quarters if quarter in room_empty_slot_1[day]]
#                                 if empty_slots:
#                                     common[day].extend(empty_slots)
#                                     is_allocated = True
#                             elif day in room_empty_slot_2 and not common:
#                                 empty_slots = [quarter for quarter in quarters if quarter in room_empty_slot_2[day]]
#                                 if empty_slots:
#                                     common[day].extend(empty_slots)
#                                     is_allocated = True
#                         if is_allocated:
#
#                             day = choice(list(common.keys()))
#                             index = choice(common[day])
#                             slot = schedule[day]
#
#                             room.add_subject(day, index, subject)
#                             schedule.add_subject(day, index, {'subject': subject, 'room': room})
#
#                             individual.append((cohort, subject, room, day, slot, index))
#                             break
#
#         return individual
#
#     def subject_fitness(self):
#         score = 0
#         for cohort, schedule in self.cohort_schedule:
#             # fitness for same subject allocated more than 1 time in a day.
#             counter_in_day = defaultdict(Counter)
#             for day, slots in schedule:
#                 for slot_index, slot in slots:
#                     if not slot:
#                         continue
#                     counter_in_day[day][slot["subject"].subject_id] += 15
#             for key, value in counter_in_day.items():
#                 score += sum(value.values())
#
#             # fitness for the same subjects in a row, example: [monday: calculus, tuesday: calculus]
#             counter_in_row = Counter()
#             for day_index in [1, 2]:
#                 prev_day = DAYS[day_index - 1]
#                 curr_day = DAYS[day_index]
#                 next_day = DAYS[day_index + 1]
#                 prev_day_slots = schedule[prev_day]
#                 curr_day_slots = schedule[curr_day]
#                 next_day_slots = schedule[next_day]
#                 prev_day_subjects = Counter(prev_day_slots.subjects)
#                 curr_day_subjects = Counter(curr_day_slots.subjects)
#                 next_day_subjects = Counter(next_day_slots.subjects)
#                 # prev_day_subjects + curr_day_subjects
#                 counter_in_row.update(
#                     {key: value * 5 for key, value in
#                      (prev_day_subjects + curr_day_subjects).items()
#                      if value >= 2}
#                 )
#                 # curr_day_subjects + next_day_subjects
#                 counter_in_row.update(
#                     {key: value * 5 for key, value in
#                      (curr_day_subjects + next_day_subjects).items()
#                      if value >= 2}
#                 )
#                 # prev_day_subjects + curr_day_subjects + next_day_subjects
#                 counter_in_row.update(
#                     {key: value * 10 for key, value in
#                      (prev_day_subjects + curr_day_subjects + next_day_subjects).items()
#                      if value >= 2}
#                 )
#             score -= sum(counter_in_row.values())
#
#         return score
#
#     def room_fitness(self):
#         score = 0
#         for room in self.rooms:
#             if room.is_empty_slot():
#                 score -= 30
#             for slots in room.room_schedule.values():
#                 for _, slot in slots:
#                     is_room_match, is_requirements_match, is_optional_requirements_match = room.subject_match(slot['subject'])
#                     if is_room_match and is_requirements_match and is_optional_requirements_match:
#                         score -= 15
#                         score -= 14
#                         score -= 10
#                     elif not is_room_match:
#                         score += 25
#                     elif not is_requirements_match:
#                         score += 75
#
#         return score
#
#     def fitness_function(self, individual):
#         score = 0
#         schedule = sched.CohortsSchedule(cohorts_list=self.cohort_schedule.cohorts_list)
#
#         for cohort, subject, room, day, slot, index in individual:
#             ...
#
#         return score,
#
#     def run(self):
#         random.seed(42)
#         pop = self.toolbox.population()
#
#         stats = tools.Statistics(lambda ind: ind.fitness.values)
#         stats.register("avg", np.mean)
#         stats.register("std", np.std)
#         stats.register("min", np.min)
#         stats.register("max", np.max)
#
#         pop, logbook = algorithms.eaSimple(pop, self.toolbox, self.cx_prob, self.mut_prob, self.num_generations,
#                                            stats=stats, verbose=True)
#
#         best_individual = tools.selBest(pop, 1)[0]
#         print("Best Schedule Fitness Score: ", best_individual.fitness.values)
#         return best_individual
#         # return tools.selBest(pop, 2)


def main():

    from_converter = Converter().xlsx_to_json()
    # pprint(from_converter)

    subject_patterns: list[SubjectPattern] = [SubjectPattern(subject_data=subject) for subject in from_converter]
    subject_patterns.sort(key=lambda subject: subject.priority, reverse=True)
    rooms: list[Room] = [get_room(**room) for room in ROOMS]
    subjects: list[Subject] = list()

    SELECTOR = {
            'lecture': ('lecture', 'tutorial'),
            'tutorial': ('lecture', 'tutorial'),
            'laboratory': ('laboratory',),
            'physical_training': ('physical_training',)
    }
    for pattern in subject_patterns:
        for subject in pattern.subjects:
            subject.required_rooms = SELECTOR[subject.required_rooms]
            if subject.unique_id.endswith('Physical training'):
                subject.required_rooms = SELECTOR['physical_training']
            subjects.append(subject)

    mapped_rooms: defaultdict[str, list[Room]] = defaultdict(list)

    for room in rooms:
        class_name = room.__class__.__name__
        mapped_rooms[class_name].append(room)

    cohort_names = frozenset({subject.cohort for subject in subjects})
    subjects_2: list[sbj.Subject] = list()
    rooms_2: list[rm.Room] = list()
    cohorts_2: sched.CohortsSchedule = sched.CohortsSchedule(cohort_names)

    from genetic_algorithm.ga import GA
    from constraints.subject import Subject
    from constraints.room import Room
    from constraints.instructor import Instructor

    subjects_3: list[Subject] = list()

    for subject in subjects:
        subjects_2.append(
            Subject(
                subject_id=subject.id,
                subject_name=subject.title,
                cohort=subject.cohort,
                duration=subject.duration,
                preferred_rooms=subject.required_rooms,
            )
        )

    for param in ROOMS:
        rooms_2.append(Room(**param))

    # for s in subjects_2:
    #     ...
    ga = GA(subjects=subjects_2, rooms=rooms_2, instructors=[None] * 28)
    res = ga.run()
    pprint(res)
    # print(list(filter(lambda x: 'physical_training' in x.preferred_rooms, subjects_2)))
    # print(cohorts_2)
    # print([type(s) for s in subjects_2])
    # print([r for r in rooms_2])
    # genetic_algorithm_scheduler = GeneticAlgorithmScheduler(subjects=subjects_2, rooms=rooms_2, cohort_schedule=cohorts_2)
    # result = genetic_algorithm_scheduler.run()
    #
    # pprint(result)

    # schedule: dict[str, Schedule] = {cohort_name: Schedule(cohort_name) for cohort_name in cohort_names}

    # print(subjects)
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
