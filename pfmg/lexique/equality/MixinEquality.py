"""Mixin définissant l'agalité par défaut."""


from pfmg.lexique.equality.ABCEquality import ABCEquality


class MixinEquality(ABCEquality):
    """Mixin définissant l'agalité par défaut."""

    def __eq__(self, other: ABCEquality):
        """Vérifie l'égalité entre deux objets.
        
        :param other: un autre object
        :return: bool
        """
        eq_rules = self.get_rule().string == other.get_rule().string
        return (eq_rules
                and ((self.get_sigma().items()
                      <= other.get_sigma().items())
                     or (other.get_sigma().items()
                         <= self.get_sigma().items())))
