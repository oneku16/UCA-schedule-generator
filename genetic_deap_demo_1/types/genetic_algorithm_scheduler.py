from deap import base, creator, tools, algorithms
import random
import numpy as np
from genetic_deap_demo_1.models.schedule import Schedule


class GeneticAlgorithmScheduler:
    def __init__(self, classrooms, groups, teachers, subjects):
        self.classrooms = classrooms
        self.groups = groups
        self.teachers = teachers
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
        groups, subjects, teachers, classrooms = self.groups, self.subjects, self.teachers, self.classrooms
        individual = creator.Individual()
        for group in groups:
            for subject in subjects:
                if (group.course != subject.course):
                    continue
                for _ in range(subject.number_of_hours // 2):  # Prioritize 2-hour blocks
                    teacher_id = subject.teachers
                    teacher = next(t for t in teachers if t.id == teacher_id)
                    classroom = random.choice(classrooms)
                    day = random.choice(range(6))
                    slot = random.choice(range(10))  # Allow space for 2-hour blocks
                    individual.append((group, subject, teacher, classroom, day, slot))
                    individual.append((group, subject, teacher, classroom, day, slot + 1))
        return individual

    def fitness_function(self, individual):
        score = 0
        groups, subjects, teachers, classrooms = self.groups, self.subjects, self.teachers, self.classrooms
        schedule = Schedule(groups)
        teacher_idle_time = {teacher.id: 0 for teacher in teachers}
        teacher_workload = {teacher.id: 0 for teacher in teachers}

        for item in individual:
            group, subject, teacher, classroom, day, slot = item

            for group_course in range(1, 5):
                cell = schedule.slots[group_course][day][slot]
                if (not cell):
                    continue
                # print(cell['subject'], subject.id)
                if (cell['subject'] == subject.id):
                    score += 10

                if (cell['teacher'] == teacher.id):
                    score += 10
                if (cell['classroom'] == classroom.id):
                    score += 10

            if slot == 5:
                score += 60

            if str(day) not in teacher.working_days:
                score += 1

            score += slot

            if teacher.working_graphic == "AFTER" and slot < 6:
                score += 1
            elif teacher.working_graphic == "BEFORE" and slot >= 6:
                score += 1

            if classroom.capacity < group.number_of_students:
                score += 1

            if schedule.slots[group.course][day][slot]:
                score += 10

            schedule.slots[group.course][day][slot] = {'subject': subject.id, 'teacher': teacher.id,
                                                       'classroom': classroom.id}

        for hour in range(11):  # Update the loop range to 10
            for course in range(1, 5):
                for day in range(0, 6):
                    cell = schedule.slots[course][day][hour]
                    if (hour < 10):
                        nextcell = schedule.slots[course][day][hour + 1]
                        if cell and nextcell and cell['subject'] == nextcell['subject'] and cell['classroom'] ==\
                                nextcell['classroom']:
                            score -= 10  # Decrease score for consecutive subject slots (2-hour block)

                    if (not schedule.slots[course][day][hour]):
                        if (hour != 5):
                            score += 5 * (10 - hour)

                    if (hour > 0):
                        prevcell = schedule.slots[course][day][hour - 1]
                        if (not prevcell and not cell and prevcell != cell):
                            score += 5

        for course, group_schedule in schedule.slots.items():
            subject_hours = {subject.id: 0 for subject in subjects}
            for day_schedule in group_schedule:
                for cell in day_schedule:
                    if cell:
                        subject_hours[cell['subject']] += 1
            for subject in subjects:
                if course == subject.course:
                    if subject_hours[subject.id] != subject.number_of_hours:
                        score += 5 * abs(subject_hours[subject.id] - subject.number_of_hours)

        # Minimize teacher idle time
        for day in range(6):
            for teacher in teachers:
                last_slot = -1
                for hour in range(11):
                    for course in range(1, 5):
                        cell = schedule.slots[course][day][hour]
                        if cell and cell['teacher'] == teacher.id:
                            if last_slot != -1 and (hour - last_slot > 1):
                                teacher_idle_time[teacher.id] += (hour - last_slot - 1)
                            last_slot = hour
                            teacher_workload[teacher.id] += 1

        # Balance teacher workload
        max_workload = max(teacher_workload.values())
        min_workload = min(teacher_workload.values())

        # Minimize consecutive classes
        consecutive_classes = 0
        for course in range(1, 5):
            for day in range(6):
                for hour in range(1, 11):
                    cell = schedule.slots[course][day][hour]
                    prevcell = schedule.slots[course][day][hour - 1]
                    if cell and prevcell and cell['teacher'] == prevcell['teacher']:
                        consecutive_classes += 1

        # Apply penalties for the new constraints
        score += sum(teacher_idle_time.values()) * 2
        score += (max_workload - min_workload) * 10
        score += consecutive_classes * 5
        return score,

    def run(self):
        random.seed(42)
        pop = self.toolbox.population()

        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)

        pop, logbook = algorithms.eaSimple(pop, self.toolbox, self.cx_prob, self.mut_prob, self.num_generations,
                                           stats=stats, verbose=True)

        best_individual = tools.selBest(pop, 1)[0]
        print("Best Schedule Fitness Score: ", best_individual.fitness.values)
        return best_individual
