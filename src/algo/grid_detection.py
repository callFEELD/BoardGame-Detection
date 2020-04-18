import numpy as np

def find_close_points(r_point, points, max_radius=150, variation=0.05):
    """Find the close points to a given reference point
        Only 2d
    Arguments:
        r_point {[type]} -- [description]
        points {[type]} -- [description]
    """
    close_points = []
    distances = []

    for radius in range(max_radius):
        for point in points:
            dist = abs(np.linalg.norm(r_point - point))

            if dist == 0:
                continue

            if dist >= radius - radius*variation and dist <= radius + radius*variation:
                close_points.append(point)
                distances.append(dist)

        # check if enough points have the "same" distance
        if len(close_points) >= 3:
            return close_points
        else:
            close_points = []
            distances = []

    return close_points


def get_distance_from_point(reference, points):
    distances = []
    for point in points:
        dist = abs(np.linalg.norm(reference - point))

        distances.append(dist)

    return distances
