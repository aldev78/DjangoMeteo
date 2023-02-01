from .meteo_ville import MeteoVille
from ...utils.meteo_common import MeteoCommon


class MeteoVillePrevisions:

    def __init__(self, nom_ville):
        self._meteo_ville = MeteoVille(nom_ville)

    def _get_temperature_prevision(self, type_temperature, period):
        return self._meteo_ville.get_temperature_for_period(type_temperature, period)

    def _get_vent_vitesse_prevision(self, period):
        return self._meteo_ville.get_force_vent_for_period(period)

    def _get_description_for_period(self, period):
        return self._meteo_ville.get_description_for_period(period)

    def _get_previsions(self, type_temperature):
        previsions = {}

        previsions[MeteoCommon.PREVISION_AUJOURDHUI] = self._get_temperature_prevision(type_temperature, MeteoCommon.PREVISION_AUJOURDHUI)
        previsions[MeteoCommon.PREVISION_J_PLUS_1] = self._get_temperature_prevision(type_temperature, MeteoCommon.PREVISION_J_PLUS_1)
        previsions[MeteoCommon.PREVISION_J_PLUS_2] = self._get_temperature_prevision(type_temperature, MeteoCommon.PREVISION_J_PLUS_2)
        previsions[MeteoCommon.PREVISION_J_PLUS_3] = self._get_temperature_prevision(type_temperature, MeteoCommon.PREVISION_J_PLUS_3)
        previsions[MeteoCommon.PREVISION_J_PLUS_4] = self._get_temperature_prevision(type_temperature, MeteoCommon.PREVISION_J_PLUS_4)
        previsions[MeteoCommon.PREVISION_J_PLUS_5] = self._get_temperature_prevision(type_temperature, MeteoCommon.PREVISION_J_PLUS_5)
        previsions[MeteoCommon.PREVISION_J_PLUS_6] = self._get_temperature_prevision(type_temperature, MeteoCommon.PREVISION_J_PLUS_6)
        previsions[MeteoCommon.PREVISION_J_PLUS_7] = self._get_temperature_prevision(type_temperature, MeteoCommon.PREVISION_J_PLUS_7)

        return previsions

    def _get_previsions_force_vent(self):
        previsions = {}

        previsions[MeteoCommon.PREVISION_AUJOURDHUI] = self._get_vent_vitesse_prevision(MeteoCommon.PREVISION_AUJOURDHUI)
        previsions[MeteoCommon.PREVISION_J_PLUS_1] = self._get_vent_vitesse_prevision(MeteoCommon.PREVISION_J_PLUS_1)
        previsions[MeteoCommon.PREVISION_J_PLUS_2] = self._get_vent_vitesse_prevision(MeteoCommon.PREVISION_J_PLUS_2)
        previsions[MeteoCommon.PREVISION_J_PLUS_3] = self._get_vent_vitesse_prevision(MeteoCommon.PREVISION_J_PLUS_3)
        previsions[MeteoCommon.PREVISION_J_PLUS_4] = self._get_vent_vitesse_prevision(MeteoCommon.PREVISION_J_PLUS_4)
        previsions[MeteoCommon.PREVISION_J_PLUS_5] = self._get_vent_vitesse_prevision(MeteoCommon.PREVISION_J_PLUS_5)
        previsions[MeteoCommon.PREVISION_J_PLUS_6] = self._get_vent_vitesse_prevision(MeteoCommon.PREVISION_J_PLUS_6)
        previsions[MeteoCommon.PREVISION_J_PLUS_7] = self._get_vent_vitesse_prevision(MeteoCommon.PREVISION_J_PLUS_7)

        return previsions

    def _get_previsions_description(self):
        previsions = {}

        previsions[MeteoCommon.PREVISION_AUJOURDHUI] = self._get_description_for_period(MeteoCommon.PREVISION_AUJOURDHUI)
        previsions[MeteoCommon.PREVISION_J_PLUS_1] = self._get_description_for_period(MeteoCommon.PREVISION_J_PLUS_1)
        previsions[MeteoCommon.PREVISION_J_PLUS_2] = self._get_description_for_period(MeteoCommon.PREVISION_J_PLUS_2)
        previsions[MeteoCommon.PREVISION_J_PLUS_3] = self._get_description_for_period(MeteoCommon.PREVISION_J_PLUS_3)
        previsions[MeteoCommon.PREVISION_J_PLUS_4] = self._get_description_for_period(MeteoCommon.PREVISION_J_PLUS_4)
        previsions[MeteoCommon.PREVISION_J_PLUS_5] = self._get_description_for_period(MeteoCommon.PREVISION_J_PLUS_5)
        previsions[MeteoCommon.PREVISION_J_PLUS_6] = self._get_description_for_period(MeteoCommon.PREVISION_J_PLUS_6)
        previsions[MeteoCommon.PREVISION_J_PLUS_7] = self._get_description_for_period(MeteoCommon.PREVISION_J_PLUS_7)

        return previsions

    def get_previsions_force_vent(self):
        return self._get_previsions_force_vent()

    def get_previsions_description(self):
        return self._get_previsions_description()

    def get_previsions_jour(self):
        return self._get_previsions(MeteoCommon.PREVISION_TEMPERATURE_JOUR)

    def get_previsions_min(self):
        return self._get_previsions(MeteoCommon.PREVISION_TEMPERATURE_MINI)

    def get_previsions_max(self):
        return self._get_previsions(MeteoCommon.PREVISION_TEMPERATURE_MAXI)

    def get_previsions_matin(self):
        return self._get_previsions(MeteoCommon.PREVISION_TEMPERATURE_MATIN)

    def get_previsions_midi(self):
        return self._get_previsions(MeteoCommon.PREVISION_TEMPERATURE_APRES_MIDI)

    def get_previsions_soir(self):
        return self._get_previsions(MeteoCommon.PREVISION_TEMPERATURE_NUIT)