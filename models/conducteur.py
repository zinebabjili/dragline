class Conducteur:
    """A sample Employee class"""

    def __init__(self, first, last, password, poste):
        self.first = first
        self.last = last
        self.password = password
        self.poste = poste

    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def __repr__(self):
        return "Conducteur('{}', '{}', {})".format(self.first, self.last, self.password, self.poste)
