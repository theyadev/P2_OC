def get_star_rating(value: str) -> int:
    """Get the star rating from the string."""
    if value == "One":
        return 1
    elif value == "Two":
        return 2
    elif value == "Three":
        return 3
    elif value == "Four":
        return 4
    elif value == "Five":
        return 5
    else:
        return 0
