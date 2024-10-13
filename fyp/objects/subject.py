class Subject:
    def __init__(self, subject_id: str, subject_name: str, cohort: str, is_prime: bool = False):
        self.subject_id = subject_id
        self.subject_name = subject_name
        self.cohort = cohort
        self.is_prime = is_prime
