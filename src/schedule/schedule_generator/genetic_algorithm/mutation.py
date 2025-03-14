from random import random, choice

from src.schedule.schedule_generator.constraints import Subject, Slot, Room, Instructor
from src.schedule.schedule_generator.genetic_algorithm import Individual, RoomSelector


def room_mutation(g, rs: RoomSelector) -> None:
    subject, _, room, _ = g
    if 'physical_training' in subject.preferred_rooms:
        _, r = choice(rs.rooms['physical_training'])
    else:
        r = rs.get_room(subject.preferred_rooms)
    g[2] = r
    rs.put_room(room)
    rs.reduce_room(r)


def slot_mutation(g) -> None:
    _, s, _, _ = g
    s.update_values()


def instructor_mutation(g, i: list[Instructor]) -> None:
    ...


def mutation(
        indpb: float,
        instructors: list[Instructor],
        rooms: list[Room],
        individual: list[list[Subject, Slot, Room, Instructor]],
) -> Individual:
    room_selector = RoomSelector(rooms)
    for _, _, room, _ in individual:
        room_selector.reduce_room(room)

    for gene in individual:
        random_value = random()
        if random_value > indpb:
            continue

        if random() < indpb:
            room_mutation(gene, room_selector)
            slot_mutation(gene)
            instructor_mutation(gene, instructors)

    return individual,
