from random import random, choice

from constraints.instructor import Instructor
from constraints.room import Room
from genetic_algorithm.individual import Individual


def mutation(
        indpb: float,
        instructors: list[Instructor],
        rooms: list[Room],
        individual: Individual,
) -> Individual:
    for gene in individual:
        subject, slot, room, instructor = gene
        if room.room_type not in subject.preferred_rooms:
            if 'physical_training' in subject.preferred_rooms:
                for r in rooms:
                    if r.room_type == 'room_type':
                        room = r
            else:
                while new_room := choice(rooms):
                    if new_room.room_type in subject.preferred_rooms:
                        if random() < indpb:
                            break
                room = new_room
        if instructor and instructor.cohorts and subject.cohort not in instructor.cohorts:
            while new_instructor := choice(instructors):
                if new_instructor and new_instructor.cohorts and subject.cohort in new_instructor.cohorts:
                    if random() < indpb:
                        break
            instructor = new_instructor

        if random() < indpb:
            slot.update_values()

        gene[2] = room
        gene[3] = instructor
    return individual,