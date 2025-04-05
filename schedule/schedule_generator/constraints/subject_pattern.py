from consts import SUBJECT_PATTERNS, SELECTOR
from .subject import Subject


class SubjectPattern:
    """
    Represents a pattern for creating subjects, with a priority based on instructors and subject types.
    Attributes:
        __subjects (list[Subject]): A list of subjects created from the pattern.
        priority (list[int]): A list of priority values based on instructors and subject types.
    """
    __slots__ = (
        '__subjects',
        'priority',
    )

    def __init__(self, subject_data):
        """
        Initializes a SubjectPattern instance.
        Args:
            subject_data (dict): A dictionary containing data for creating subjects, including:
                                 - cohort (str): The cohort associated with the subjects.
                                 - id (str): The ID of the subjects.
                                 - instructors (list): A list of instructors for the subjects.
                                 - title (str): The title of the subjects.
                                 - patterns (list[dict]): A list of patterns for creating subjects.
        """
        self.priority = [0, 0, 0, 0]
        self.__subjects: list[Subject] = self.__create_subjects(**subject_data)

    def __create_subjects(self, cohort: str, subject_id: str, instructors: list, title: str, patterns: list[dict]) -> list[Subject]:
        """
        Creates a list of subjects based on the provided data.
        Args:
            cohort (str): The cohort associated with the subjects.
            subject_id (str): The ID of the subjects.
            instructors (list): A list of instructors for the subjects.
            title (str): The title of the subjects.
            patterns (list[dict]): A list of patterns for creating subjects.
        Returns:
            list[Subject]: A list of Subject instances.
        Raises:
            ValueError: If `cohort`, `subject_id`, or `patterns` are invalid.
        """
        if not isinstance(cohort, str) or not cohort:
            raise ValueError("cohort must be a non-empty string")
        if not isinstance(subject_id, str) or not subject_id:
            raise ValueError("subject_id must be a non-empty string")
        if not isinstance(patterns, list) or not all(isinstance(p, dict) for p in patterns):
            raise ValueError("patterns must be a list of dictionaries")

        subjects = list()
        if instructors:
            self.priority[0] += 1

        for subject_type, pattern, index in zip(SUBJECT_PATTERNS, patterns, (3, 2, 1)):
            try:
                classes, duration = pattern["classes"], pattern["duration"]
            except KeyError as e:
                raise ValueError(f"Missing key in pattern: {e}")

            for _ in range(classes):
                subject = Subject(
                    subject_id=subject_id,
                    subject_name=title,
                    cohort=cohort,
                    duration=duration,
                    preferred_rooms=SELECTOR[subject_type],
                )
                if subject.subject_name.endswith('Physical training'):
                    subject.preferred_rooms = frozenset(SELECTOR['physical_training'])

                self.priority[index] += 1
                subjects.append(subject)

        return subjects

    @property
    def subjects(self) -> list[Subject]:
        """
        Returns the list of subjects created from the pattern.
        Returns:
            list[Subject]: The list of subjects.
        """
        return self.__subjects

    def __repr__(self) -> str:
        return f'SubjectPattern({self.__subjects})'
