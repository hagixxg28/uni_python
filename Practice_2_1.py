def something(first: int, delta: int, last: int) -> int:
    if first == last:
        return delta
    return something(first=first + 1, delta=delta, last=last)
