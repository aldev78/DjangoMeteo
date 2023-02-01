class Departement:
    # ------------------------------
    # constructeur
    # ------------------------------
    def __init__(self):
        self.nom = "nom département"
        self.code = "000"

    # ------------------------------
    # propriétés
    # ------------------------------
    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, value):
        self._nom = value

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value
