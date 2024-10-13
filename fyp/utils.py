
def get_slots(slots: int = 4) -> list[str]:
    assert slots >= 2
    """
    creates slots names and returns.
    example: ["slot_1", "slot_2", ..., "slot_n"]
    """
    slots: list[str] = [f"slot_{number}" for number in range(1, slots + 1)]

    return slots


def get_weekdays(start_day: str = "monday", end_day: str = "friday") -> list[str]:
    """
    creates weekdays names and returns.
    example: ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    """
    days: list[str] = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    assert start_day != end_day
    assert days.index(start_day) < days.index(end_day)
    assert start_day in days and end_day in days

    return days[days.index(start_day):days.index(end_day) + 1]
