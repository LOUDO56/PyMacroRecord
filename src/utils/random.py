import math
import random


def update_random_seed(seed=None, version=2):
    """Update the random package seed.
    At arbitrary times the randomness should update its seed so that it is harder to reverse-engineer the randomized value usage.

    Args:
        seed (int|float|str|bytes|bytearray, optional): The seed to be used. None will default to using system time. Defaults to None (aka, system time).
        version (1|2, optional): the version for the generation of seeding algorithm, the higher means the more advanced. Defaults to the maximum valid value.
    """
    random.seed(a=seed, version=version)

def get_weighted_random_float(distribution, lower_bound=0, upper_bound=1):
    """
    Select a continuous random float between lower_bound and upper_bound
    according to the weighted distribution.

    distribution:
        List of [x, weight] pairs, where x is normalized to [0, 1].
        Example: [[0.0, 1], [0.5, 5], [1.0, 2]]

    lower_bound, upper_bound: float
        The lower and upper bounds (inclusive) for the range to choose a value from.

    The x positions define the shape of the distribution. The weights are
    linearly interpolated between points to form a continuous probability
    density function.
    """
    if lower_bound > upper_bound:
        lower_bound, upper_bound = upper_bound, lower_bound
    if lower_bound == upper_bound:
        return lower_bound
    points = sorted((float(x), max(0.0, float(weight))) for x, weight in distribution)
    if not points:
        return random.uniform(lower_bound, upper_bound)
    # Merge duplicate x positions.
    merged = []
    for x, weight in points:
        if merged and x == merged[-1][0]:
            merged[-1][1] = weight
        else:
            merged.append([x, weight])
    points = merged
    # Clamp the distribution to the usable normalized range.
    if points[0][0] > 0.0:
        points.insert(0, [0.0, points[0][1]])
    if points[-1][0] < 1.0:
        points.append([1.0, points[-1][1]])
    points = [
        [max(0.0, min(1.0, x)), weight]
        for x, weight in points
    ]
    # Calculate the area under the piecewise-linear probability density.
    total_area = 0.0
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        total_area += (x2 - x1) * (y1 + y2) / 2.0
    if total_area <= 0.0:
        return random.uniform(lower_bound, upper_bound)
    # Select a random area under the density curve.
    target_area = random.random() * total_area
    accumulated_area = 0.0
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        width = x2 - x1
        if width <= 0.0:
            continue
        segment_area = width * (y1 + y2) / 2.0
        if accumulated_area + segment_area >= target_area:
            # Solve for x within this piecewise-linear segment.
            target = target_area - accumulated_area
            slope = (y2 - y1) / width
            if abs(slope) < 1e-12:
                dx = target / y1 if y1 > 0.0 else 0.0
            else:
                # Integral from 0 to dx:
                # y1 * dx + 0.5 * slope * dx^2 = target
                discriminant = y1 * y1 + 2.0 * slope * target
                dx = (-y1 + math.sqrt(max(0.0, discriminant))) / slope
            x = x1 + max(0.0, min(width, dx))
            return lower_bound + x * (upper_bound - lower_bound)
        accumulated_area += segment_area
    return upper_bound

def generate_weighted_random_func(distribution, lower_bound=0.0, upper_bound=1.0):
    """
    Create and return a callable that generates random floats between
    lower_bound and upper_bound according to a weighted distribution.

    distribution:
        List of [x, weight] pairs, where x is normalized to [0, 1].

        Example:
            [[0.0, 1], [0.5, 5], [1.0, 2]]

    The x positions define the shape of a piecewise-linear probability
    density function. The weights are linearly interpolated between points.

    Example:
        random_value = generate_weighted_random_func(
            [[0.0, 1], [0.5, 5], [1.0, 2]],
            lower_bound=10,
            upper_bound=20,
        )

        value = random_value()
    """

    if lower_bound > upper_bound:
        lower_bound, upper_bound = upper_bound, lower_bound

    lower_bound = float(lower_bound)
    upper_bound = float(upper_bound)

    # Prepare the distribution once when creating the generator.
    points = [
        (
            max(0.0, min(1.0, float(x))),
            max(0.0, float(weight)),
        )
        for x, weight in distribution
    ]

    # If there is no usable distribution, use a uniform distribution.
    if not points:
        return lambda: random.uniform(lower_bound, upper_bound)

    # Sort and merge duplicate x positions.
    points.sort(key=lambda point: point[0])

    merged = []
    for x, weight in points:
        if merged and x == merged[-1][0]:
            merged[-1][1] = weight
        else:
            merged.append([x, weight])

    points = merged

    # Extend the distribution to cover the full normalized range.
    if points[0][0] > 0.0:
        points.insert(0, [0.0, points[0][1]])

    if points[-1][0] < 1.0:
        points.append([1.0, points[-1][1]])

    # Calculate the total area under the density curve.
    total_area = sum(
        (x2 - x1) * (y1 + y2) / 2.0
        for (x1, y1), (x2, y2) in zip(points, points[1:])
    )

    # Fall back to uniform sampling if the density has no area.
    if total_area <= 0.0:
        return lambda: random.uniform(lower_bound, upper_bound)

    def sample():
        """Generate one random value using the prepared distribution."""

        # Handle a zero-width output range.
        if lower_bound == upper_bound:
            return lower_bound

        target_area = random.random() * total_area
        accumulated_area = 0.0

        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            width = x2 - x1

            if width <= 0.0:
                continue

            segment_area = width * (y1 + y2) / 2.0

            if accumulated_area + segment_area >= target_area:
                target = target_area - accumulated_area
                slope = (y2 - y1) / width

                if abs(slope) < 1e-12:
                    # Constant-density segment.
                    dx = target / y1 if y1 > 0.0 else 0.0
                else:
                    # Solve:
                    #
                    # y1 * dx + 0.5 * slope * dx² = target
                    #
                    discriminant = y1 * y1 + 2.0 * slope * target
                    dx = (-y1 + math.sqrt(max(0.0, discriminant))) / slope

                dx = max(0.0, min(width, dx))
                normalized_value = x1 + dx

                return (
                    lower_bound
                    + normalized_value * (upper_bound - lower_bound)
                )

            accumulated_area += segment_area

        return upper_bound

    # Return a new callable function instance.
    return sample
