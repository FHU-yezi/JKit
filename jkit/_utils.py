def only_one(*args: object) -> bool:
    return len(tuple(filter(None, args))) == 1
