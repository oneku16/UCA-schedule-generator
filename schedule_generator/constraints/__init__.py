"""
constraints package

This package provides classes for managing constraints related to scheduling, such as rooms, subjects, time slots, and instructors.

Classes:
    - Room: Represents a room with its ID, capacity, type, and additional constraints.
    - SubjectPattern: Represents a pattern for creating subjects, including their types, durations, and instructors.
    - Subject: Represents a subject with its ID, name, cohort, duration, and other attributes.
    - Slot: Represents a time slot with its duration, weekday, and start/end times.
    - Instructor: Represents an instructor with their name, email, ID, and assigned cohorts/courses.
"""

# Expose all relevant classes and utilities from the constraints package
from .room import Room
from .subject_pattern import SubjectPattern
from .subject import Subject
from .slot import Slot
from .instructor import Instructor

# Optional: Add a list of all public classes for easier introspection
__all__ = [
    "Room",
    "SubjectPattern",
    "Subject",
    "Slot",
    "Instructor",
]
