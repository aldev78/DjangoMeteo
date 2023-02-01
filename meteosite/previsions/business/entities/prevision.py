from .ville import Ville

class Prevision:
    # ------------------------------
    # constructeur
    # ------------------------------
    def __init__(self):
        self.temperature = -100
        self.temperature_min = -100
        self.temperature_max = -100
        self.temperature_matin = -100
        self.temperature_apres_midi = -100
        self.temperature_nuit = -100
        self.temperature_actuelle = -100
        self.description = "description à définir"
        self.direction_vent = 0.0
        self.force_vent = 0.0
        self.jour = None
        self.ville = Ville()
        self.period = -1
        self.humidite = -1
        self.pression_atmospherique = -1
        self.probabilite_precipitation = -1

        # ------------------------------
    # propriétés
    # ------------------------------
    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._temperature = value

    @property
    def temperature_min(self):
        return self._temperature_min

    @temperature_min.setter
    def temperature_min(self, value):
        self._temperature_min = value

    @property
    def temperature_max(self):
        return self._temperature_max

    @temperature_max.setter
    def temperature_max(self, value):
        self._temperature_max = value

    @property
    def temperature_matin(self):
        return self._temperature_matin

    @temperature_matin.setter
    def temperature_matin(self, value):
        self._temperature_matin = value

    @property
    def temperature_apres_midi(self):
        return self._temperature_apres_midi

    @temperature_apres_midi.setter
    def temperature_apres_midi(self, value):
        self._temperature_apres_midi = value

    @property
    def temperature_nuit(self):
        return self._temperature_nuit

    @temperature_nuit.setter
    def temperature_nuit(self, value):
        self._temperature_nuit = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def direction_vent(self):
        return self._direction_vent

    @direction_vent.setter
    def direction_vent(self, value):
        self._direction_vent = value

    @property
    def force_vent(self):
        return self._force_vent

    @force_vent.setter
    def force_vent(self, value):
        self._force_vent = value

    @property
    def jour(self):
        return self._jour

    @jour.setter
    def jour(self, value):
        self._jour = value

    @property
    def ville(self):
        return self._ville

    @ville.setter
    def ville(self, value):
        self._ville = value

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        self._period = value

    @property
    def humidite(self):
        return self._humidite

    @humidite.setter
    def humidite(self, value):
        self._humidite = value

    @property
    def pression_atmospherique(self):
        return self._pression_atmospherique

    @pression_atmospherique.setter
    def pression_atmospherique(self, value):
        self._pression_atmospherique = value

    @property
    def probabilite_precipitation(self):
        return self._probabilite_precipitation

    @probabilite_precipitation.setter
    def probabilite_precipitation(self, value):
        self._probabilite_precipitation = value
