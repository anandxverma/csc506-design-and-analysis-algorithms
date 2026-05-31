# Data Generator for Sorting Algorithm Analysis
#
# Produces four dataset types commonly used to benchmark sorting algorithms:
#   - random:           uniformly shuffled integers (average case)
#   - sorted:           ascending order (best case for many algorithms)
#   - reverse_sorted:   descending order (worst case for bubble/insertion sort)
#   - partially_sorted: mostly sorted with a few swaps (near-best case)

import random


def random_dataset(size, low=1, high=1000):
    """Return a list of `size` random integers in the range [low, high]."""
    return [random.randint(low, high) for _ in range(size)]


def sorted_dataset(size, low=1, high=1000):
    """Return a fully sorted (ascending) list of `size` random integers."""
    return sorted(random_dataset(size, low, high))


def reverse_sorted_dataset(size, low=1, high=1000):
    """Return a fully sorted (descending) list of `size` random integers."""
    return sorted(random_dataset(size, low, high), reverse=True)


def partially_sorted_dataset(size, low=1, high=1000, sorted_fraction=0.8):
    """Return a mostly sorted list with a controlled amount of disorder.

    sorted_fraction controls what proportion of elements stay in place.
    At 0.8 (default), roughly 20% of elements are displaced via random swaps.
    """
    data = sorted_dataset(size, low, high)

    # Compute how many swap pairs are needed to disrupt sorted_fraction of the list.
    num_swaps = max(1, int(size * (1 - sorted_fraction)))

    # Pick distinct positions to swap; cap at list length to avoid duplicates.
    indices = random.sample(range(size), min(num_swaps * 2, size))

    # Swap elements at consecutive index pairs to introduce disorder.
    for i in range(0, len(indices) - 1, 2):
        data[indices[i]], data[indices[i + 1]] = data[indices[i + 1]], data[indices[i]]

    return data


# Registry mapping dataset type names to their generator functions.
# Add new generators here to make them available via generate().
GENERATORS = {
    "random": random_dataset,
    "sorted": sorted_dataset,
    "reverse_sorted": reverse_sorted_dataset,
    "partially_sorted": partially_sorted_dataset,
}


def generate(dataset_type, size, **kwargs):
    """Generate a dataset of the given type and size.

    Extra keyword arguments (e.g. low, high, sorted_fraction) are forwarded
    to the underlying generator function.

    Raises ValueError if dataset_type is not recognized.
    """
    if dataset_type not in GENERATORS:
        raise ValueError(f"Unknown type '{dataset_type}'. Choose from: {list(GENERATORS)}")
    return GENERATORS[dataset_type](size, **kwargs)


if __name__ == "__main__":
    # Accept size interactively; keep prompting until a valid positive integer is given.
    while True:
        try:
            size = int(input("Enter dataset size: "))
            if size <= 0:
                print("Size must be a positive integer. Try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print()
    for name, fn in GENERATORS.items():
        data = fn(size)
        print(f"{name:20s}: {data}")
    print()
