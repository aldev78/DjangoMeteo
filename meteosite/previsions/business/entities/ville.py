from .departement import Departement

class Ville:
    # ------------------------------
    # constructeur
    # ------------------------------
    def __init__(self):
        self.nom = "nom ville"
        self.code_postal = "00000"
        self.departement = Departement()

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
    def code_postal(self):
        return self._code_postal

    @code_postal.setter
    def code_postal(self, value):
        self._code_postal = value

    @property
    def departement(self):
        return self._departement

    @departement.setter
    def departement(self, value):
        self._departement = value
