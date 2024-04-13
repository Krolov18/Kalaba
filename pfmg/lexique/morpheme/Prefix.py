"""Prefix."""
import re
from collections.abc import Callable
from re import Match

from frozendict import frozendict
from lexique.lexical_structures.mixins.MixinDisplay import MixinDisplay
from lexique.lexical_structures.mixins.MixinEquality import MixinEquality
from lexique.lexical_structures.mixins.MixinRepresentor import MixinRepresentor
from lexique.lexical_structures.Phonology import Phonology
from lexique.lexical_structures.StemSpace import StemSpace


class Prefix(MixinDisplay, MixinEquality, MixinRepresentor):
    """Un préfixe encode une règle affixale ajoutant un élément à la gauche du Radical."""

    __PATTERN: Callable[[str], Match | None] = re.compile(
        r"^(.*)\+X$",
    ).fullmatch

    __rule: Match
    __sigma: frozendict
    __phonology: Phonology

    def __init__(
            self,
            rule: str,
            sigma: frozendict,
            phonology: Phonology,
    ) -> None:
        """Initialise rule, sigma et phonology.

        :param rule:
        :param sigma:
        :param phonology:
        """
        _rule = Prefix.__PATTERN(rule)
        if _rule is None:
            raise TypeError
        self.__rule = _rule
        self.__sigma = sigma
        self.__phonology = phonology

    def _to_string__stemspace(self, term: StemSpace) -> str:
        """Représente un Préfix sur un StemSpace.

        :param term: un espace thématique
        :return: la réalisation d'un Prefix
        """
        return f"{self.__rule.group(1)}{term.stems[0]}"

    def _to_string__str(self, term: str) -> str:
        return f"{self.__rule.group(1)}{term}"

    def get_sigma(self) -> frozendict:
        """Récupère le sigma d'un préfixe.

        :return: le sigma d'un préfixe
        """
        return self.__sigma

    def _repr_params(self) -> str:
        """Write some doc."""
        return self.__rule.string

    def get_rule(self) -> Match:
        """Récupère la règle.
        
        :return: le Match de la rule
        """
        return self.__rule