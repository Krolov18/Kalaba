"""Implémente les cases des paradigmes par POS."""
from collections.abc import Iterator
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import TypedDict

import yaml
from frozendict import frozendict

from pfmg.lexique.reader.Reader import Reader

d_grid = dict[str, list[str]]
l_grid = list[d_grid]
d_or_l_grid = d_grid | l_grid

SubGlose = dict[str, list[frozendict]]


class GlosesStruct(TypedDict):
    """Typage stricte du dictionnaire Gloses."""

    source: frozendict[str, str]
    destination: frozendict[str, str]


@dataclass
class Gloses(Reader):
    """Représente les cases des paradigmes.

    Quand cet objet est callé on récupère les cases
    du paradigme pour un POS donné.
    """

    source: SubGlose
    destination: SubGlose

    def __post_init__(self):
        """Validation post initialisation."""
        self.struct = {k: [dict(zip(vars(self).keys(), sigma, strict=True))
                           for sigma in
                           product(self.source[k], self.destination[k])]
                       for k in self.source.keys()
                       if k in self.source and k in self.destination}

    def __call__(
        self,
        pos: str,
    ) -> list[GlosesStruct]:
        """Rècupère un ensemble de sigma, soit un sigma par case.

        :param item: un POS valide
        :return: Les cases du paradigmes de 'item'
        """
        return self.struct[pos]

    @classmethod
    def from_disk(cls, path: Path) -> "Gloses":
        """Construit Gloses à partir d'un fichier YAML.

        :param path: Chemin vers le YAML des gloses de la grammaire.
        :return: Instance de Gloses
        """
        assert path.name.endswith("Gloses.yaml")
        with open(path, encoding="utf8") as file_handler:
            data: dict[str, dict[str, list[str]]] = yaml.safe_load(file_handler)
        source = {category: list(cls.__gridify(att_vals))
                  for category, att_vals in data["source"].items()}
        destination = {category: list(cls.__gridify(att_vals))
                       for category, att_vals in data["destination"].items()}

        return cls(
            source=source,
            destination=destination,
        )

    @staticmethod
    def __gridify(grid: d_or_l_grid) -> Iterator[frozendict]:
        """Gridify a list or a dict.

        :param grid: dictionnaire Attribut -> [Valeurs]
                     ou liste de dictionnaires Attribut -> [Valeurs]
        :return: générateur de Gloses
        """
        method_name: str = (f"_{Gloses.__name__}__gridify_"
                            f"{grid.__class__.__name__.lower()}")
        return getattr(Gloses, method_name)(grid=grid)

    @staticmethod
    def __gridify_dict(grid: d_grid) -> Iterator[frozendict]:
        """Transform un dictionnaire Attribut -> [Valeurs] en un générateur.

        :param grid: dictionnaire Attribut -> [Valeurs]
        :return: générateur de Gloses
        """
        items: list[tuple[str, list[str]]] = sorted(grid.items())

        if not grid:
            # cas où grid est un dictionnaire vide
            return frozendict()

        keys, values = zip(*items, strict=True)
        for value in product(*values):
            yield frozendict(
                [*zip(keys, value, strict=True),
                 *zip(value, keys, strict=True)],
            )

    @staticmethod
    def __gridify_list(grid: l_grid) -> Iterator[frozendict]:
        """Gridify a list.

        :param grid: liste de dictionnaires Attribut -> [Valeurs]
        :return: générateur de Gloses
        """
        if not grid:
            # cas où grid est une liste vide
            yield []
            return
        for i_grid in grid:
            yield from Gloses.__gridify_dict(i_grid)