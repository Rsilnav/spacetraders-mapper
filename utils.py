from math import sqrt


def distance(wp1, wp2) -> int:
    return int(sqrt((wp1["x"] - wp2["x"]) ** 2 + (wp1["y"] - wp2["y"]) ** 2))


def distance_tuple(wp1, wp2) -> int:
    return int(sqrt((wp1[0] - wp2[0]) ** 2 + (wp1[1] - wp2[1]) ** 2))


def hours(d) -> float:
    return (15 + 3.333 * d) / 3600
