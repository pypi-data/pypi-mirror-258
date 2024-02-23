"""
Full Cytogenetic Index, the most flexible and complex type of cytogenetic index.
"""
from collections.abc import Iterator
from dataclasses import dataclass, replace
from typing import Self

from pyploid.types.cytogenetic_index import ComplexPolyploidCytogeneticIndex


@dataclass(frozen=True)
class FullCytogeneticIndex(ComplexPolyploidCytogeneticIndex):
    """
    Cytogenetic Index that resembles the genetic layout of most highly developed organisms. Genes are found on
    chromosomes which come in pairs.
    """
    #: Chromosome number in the karyotype.
    chromosome_number: int
    #: Chromosome number in the set of chromosomes.
    set_index: int
    #: Index of the gene on the chromosome.
    index: int

    def __iter__(self) -> Iterator[int | str]:
        return iter((self.chromosome_number, self.index))

    def __lt__(self, other: Self) -> bool:
        return tuple(self) < tuple(other)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FullCytogeneticIndex):
            return NotImplemented
        return tuple(self) == tuple(other)

    def qualifier(self) -> tuple[int]:
        return self.chromosome_number,

    def reindex(self, chromosome_number: int, set_index: int, index: int) -> Self:
        """
        Returns a copy of the cytogenetic index with the positions altered.
        Args:
            chromosome_number: New chromosome number.
            set_index: New set index.
            index: New index.

        Returns:
            Copy with altered positions.
        """
        return replace(self, chromosome_number=chromosome_number, set_index=set_index, index=index)

    @classmethod
    def from_index(cls, chromosome_number: int, set_index: int, index: int) -> 'FullCytogeneticIndex':
        """
        Creates a FullCytogeneticIndex from positional data.
        Args:
            chromosome_number: Chromosome number in the karyotype.
            set_index: Index of the chromosome in the chromosome set.
            index: Position of the gene on the chromosome.

        Returns:
            FullCytogeneticIndex with the positional data specified.
        """
        return cls(chromosome_number, set_index, index)