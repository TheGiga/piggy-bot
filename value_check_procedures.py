def empty_check(value=None):
    return True


def cooldown_value_check(value: str | int):
    try:
        formatted_value = int(value)
    except ValueError:
        return False

    # Cooldown value should be in minutes, and correspond to specific parameters.
    return 5 <= formatted_value <= 4320
