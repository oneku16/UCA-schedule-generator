class NoEmptySlotError(Exception):
    def __init__(self, message: str = ""):
        self.message = message or "No empty slot"
        super().__init__(self.message)
