def euclidean_distance(color1: tuple, color2: tuple) -> float:
    return ((color1[0] - color2[0]) ** 2 + (color1[1] - color2[1]) ** 2 + (color1[2] - color2[2]) ** 2) ** 0.5
