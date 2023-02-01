# from business.components.meteo_ville import MeteoVille
from meteosite.previsions.data.meteo_pyowm import MeteoPyowm
from meteosite.previsions.utils.meteo_common import MeteoCommon
import meteosite.previsions.business.components.meteo_ville


class Meteo:
    # ------------------------------
    # constructeur
    # ------------------------------
    def __init__(self):
        self._meteo_pyowm = MeteoPyowm()
        self._meteo_villes = []

    # ------------------------------
    # méthodes
    # ------------------------------
    def recherche_ville(self, nom_ville):
        """
        Renvoie la liste des villes suite à la recherche sur le nom de la ville
        :param ville: tout ou partie du nom de la ville recherchée
        :return:
        """
        return self._meteo_pyowm.recherche_ville(nom_ville)

    def _get_meteo_ville(self, nom_ville):
        """
        Obtient une instance de l'objet MeteoVille correspondant à la ville définit en paramètre.
        Si cette instannce est présente dans la liste des objets MeteoVille, alors on l'a choisi et on renvoie l'instance trouvée dans la liste.
        Sinon on crée une nouvelle instance, on l'ajoute à la liste des instances dans la classe et on la renvoie au code appellant.

        NB : la liste des instances MeteoVille est "self._meteo_villes" déclarée dans le constructeur.

        :param nom_ville: nom exact de la ville
        :return: l'instance de l'objet MeteoVille correspondant.
        """

        # on recherhce l'instance de l'objet MeteoVille correspondant dans la liste locale à la classe
        # si on la trouve, on la renvoie directement sans avoir besoin de terminer le parcours de la liste
        for meteo_ville in self._meteo_villes:
            if meteo_ville.ville.nom == nom_ville:
                return meteo_ville

        # si on est ici, c'est que l'instance de l'objet MeteoVille n'a pas été trouvée dans la liste,
        # alors on la créee, on l'ajoute à la liste locale à la classe et on la renvoie au code appellant.
        # NB : en créant une instance de la classe MeteoVille, elle s'initialise de facto par elle même pour réucupérer les informations météo.
        meteo_ville = meteosite.previsions.business.components.meteo_ville.MeteoVille(nom_ville)  #  ici on passe par le nom du module python + class pour éviter un problème d'import (référence circulaire)
        self._meteo_villes.append(meteo_ville)

        return meteo_ville

    def get_temperature_actuelle(self, nom_ville):

        meteo_ville = self._get_meteo_ville(nom_ville)
        return meteo_ville.get_temperature_for_period(MeteoCommon.PREVISION_TEMPERATURE_JOUR, MeteoCommon.PREVISION_AUJOURDHUI)

    def get_avis_meteo(self, nom_ville):
        """
        Méthode gardée pour compatibilité de code, renvoie maintenant l'avais d'étaillé
        :param nom_ville: chaine de caractère représentant la ville sur laquelle porte la recherche
        :return: avis détaillé
        """
        return self.get_avis_meteo_detaille(nom_ville)

    def get_avis_meteo_detaille(self, nom_ville):
        """
        obtient l'avis météo détaillé pour la ville recherchée
        :param nom_ville: chaine de caractère représentant la ville sur laquelle porte la recherche
        :return: avis détaillé
        """
        return self.get_avis_meteo_detaille_prevision(nom_ville, MeteoCommon.PREVISION_AUJOURDHUI)

    def get_avis_meteo_detaille_prevision(self, nom_ville, period):
        """
        Obtient la prévision météo détaillée pour une ville et un jour donnés (J, J+1, J+2, etc...)
        :param nom_ville: chaine de caractère représentant la ville sur laquelle porte la recherche
        :param period: PREVISION_AUJOURDHUI, PREVISION_J_PLUS_1, PREVISION_J_PLUS_2, etc... voir valeurs dans meteo_common.py
        :return:
        """

        meteo_ville = self._get_meteo_ville(nom_ville)
        return meteo_ville.get_description_for_period(period)

    def get_temperature_prevision(self, nom_ville, type_temperature, period):
        meteo_ville = self._get_meteo_ville(nom_ville)
        return meteo_ville.get_temperature_for_period(type_temperature, period)

    def get_humidite_prevision(self, nom_ville, period):

        meteo_ville = self._get_meteo_ville(nom_ville)
        return meteo_ville.get_humidite_for_period(period)

    def get_pression_athmospherique_prevision(self, nom_ville, period):

        meteo_ville = self._get_meteo_ville(nom_ville)
        return meteo_ville.get_pression_atmospherique_for_period(period)

    def get_vent_vitesse_prevision(self, nom_ville, period):

        meteo_ville = self._get_meteo_ville(nom_ville)
        return meteo_ville.get_force_vent_for_period(period)

    def get_vent_orientation_prevision(self, nom_ville, period):

        meteo_ville = self._get_meteo_ville(nom_ville)
        return meteo_ville.get_direction_vent_for_period(period)

    def get_probabilite_precipitation_prevision(self, nom_ville, period):

        meteo_ville = self._get_meteo_ville(nom_ville)
        return meteo_ville.get_probabilite_precipitation_for_period(period)
