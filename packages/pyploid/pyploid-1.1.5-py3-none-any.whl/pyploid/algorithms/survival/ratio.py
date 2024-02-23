"""
Survival mechanisms based on ratios.
"""
from collections.abc import Sequence
from functools import partial
from math import floor
from operator import itemgetter
from typing import cast

from toolz import take

from pyploid.types.algorithms.fitness import Fitness
from pyploid.types.algorithms.survival import Survival
from pyploid.types.individual import IndividualType, Population


def top_n_percent_survive(
        ratio: float,
        fitness: Fitness[IndividualType],
        population: Population[IndividualType]
) -> Sequence[IndividualType]:
    """
    Survival mechanism where a top percentage of the population survives, rounded down. If two individuals have the same
    rank in the population regarding their fitness, their position relative to themselves is undefined. In the extreme
    case of a population where all members have the same fitness, the survivors are picked randomly.
    Args:
        ratio: Survivor ratio between 0 and 1 (exclusive)
        fitness: Fitness function to determine an individual's rank in the population.
        population: Population to determine survivors from.

    Returns:
        Sequence[IndividualType]: Survivors
    """
    survivor_count: int = floor(len(population.members) * ratio)
    fitness_values: dict[int, float] = dict(
        sorted(
            ((i, fitness(member)) for i, member in enumerate(population.members)),
            key=itemgetter(1)
        )
    )
    return list(
        take(survivor_count, (population.members[i] for i in fitness_values))
    )


def create_ratio_survival(ratio: float) -> Survival[IndividualType]:
    """
    Creates a survival mechanism based on a ratio of individuals that survive.
    Args:
        ratio: Survivor ratio between 0 and 1 (exclusive)

    Returns:
        Sequence[IndividualType]: Survivors
    """
    return cast(Survival[IndividualType], partial(top_n_percent_survive, ratio))