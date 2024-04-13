"""Gabarit."""
import re
from collections.abc import Callable
from re import Match

from frozendict import frozendict

from pfmg.lexique.display.MixinDisplay import MixinDisplay
from pfmg.lexique.equality.MixinEquality import MixinEquality
from pfmg.lexique.phonology.Phonology import Phonology
from pfmg.lexique.representor.MixinRepresentor import MixinRepresentor
from pfmg.lexique.stem_space.StemSpace import StemSpace


class Gabarit(MixinDisplay, MixinEquality, MixinRepresentor):
    """Le gabarit encode une règle affixale qui touche la structure du Radical.

    Dans la règle gabaritique, les consonnes comme les voyelles 
    peuvent subir des modifications phonologiques.
    """

    __PATTERN: Callable[[str], Match[str] | None]
    rule: Match[str]
    sigma: frozendict
    phonology: Phonology

    def __init__(
        self,
        rule: str,
        sigma: frozendict,
        phonology: Phonology,
    ) -> None:
        """Initialise la règle, le sigma et la phono d'un Gabarit.

        :param rule:
        :param sigma:
        :param phonology:
        """
        if not hasattr(Gabarit, "_Gabarit__PATTERN"):
            Gabarit.__PATTERN = re.compile(
                fr"^([{''.join(phonology.voyelles)}AUV1-9]{{4,9}})$",
            ).fullmatch

        _rule = Gabarit.__PATTERN(rule)
        if _rule is None:
            raise TypeError

        self.rule = _rule
        self.sigma = sigma
        self.phonology = phonology

    def _to_string__stemspace(self, term: StemSpace) -> str:
        """Stringify avec StemSpace.

        :param term:
        :return:
        """
        result = ""
        for char in self.rule.string:
            result += self.__verify(char, Gabarit.__format_default_stem(
                term.stems[0]))
        return result

    def __verify(self, char: str, stem: frozendict) -> str:
        """TODO: Pourquoi pas considérer cette fonction comme méthode à Phonology.

        :param char: Un caractère compris 
                     dans l'union [consonnes|voyelles|UAV1-9]
        :param stem: une racine au format 
                     d'un dictionnaire unique et figé
        :return: la réalisation du caractère d'une règle gabaritique 
                 appliquée à un stem (racine)
        """
        assert char
        match char:
            case "U":
                return self.phonology.apophonies[self.phonology.apophonies[stem["V"]]]
            case "A":
                return self.phonology.apophonies[stem[self.phonology.derives[char]]]
            case "1" | "2" | "3" | "V":
                return stem[char]
            case "4" | "5" | "6":
                return self.phonology.mutations[stem[str(int(char) - 3)]]
            case "7" | "8" | "9":
                return self.phonology.mutations[self.phonology.mutations[stem[str(int(char) - 6)]]]
            case _:
                return char

    @staticmethod
    def __format_default_stem(stem: str) -> frozendict:
        """Force un stem à avoir la structure 12V3.

        :param stem: CCVC
        :return: frozendict indiquant la voyelle thématique et les consonnes
        """
        return frozendict(zip("12V3", stem, strict=True))

    def get_sigma(self) -> frozendict:
        """Récupère le sigma d'un Gabarit.

        :return: le sigma
        """
        return self.sigma

    def _repr_params(self) -> str:
        """Façon de représenter un Gabarit.

        :return: les paramètres prêt pour être affichés.
        """
        return self.rule.string

    def get_rule(self) -> str:
        """Récupère la règle.

        :return: la règle sous forme de chaine de caractère
        """
        return self.rule