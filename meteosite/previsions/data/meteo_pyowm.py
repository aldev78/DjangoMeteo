import pyowm
from pyowm.utils.config import get_default_config
from pyowm.utils import measurables

class MeteoPyowm:
    # ------------------------------
    # constructeur
    # ------------------------------
    def __init__(self):
        self._apikey = '58e0e8ebda9c67eadecece78e50275f3'
        self._meteo_api_initialized = False
        self._meteo_api = None

        # on initialise l'objet qui fait le lien avec l'API OpenWeatherMap via la librairie pyowm
        self._get_meteo_api()

    # ------------------------------
    # propriétés
    # ------------------------------

    # ------------------------------
    # méthodes
    # ------------------------------
    def _get_meteo_api(self):
        # on vérifie par le boulon que l'initialisation n'a pas été déjà faite, pour ne pas faire
        # des traitements inutiles (consommation de ressources alors qu'on les a déjà)
        if not self._meteo_api_initialized:
            config_dict = get_default_config()
            config_dict['language'] = 'fr'
            self._meteo_api = pyowm.OWM(self._apikey, config_dict)
            self._meteo_api_initialized = True

        # on obtient l'objet API si il avait déjà été initialisé ou bien si il vient juste de l'être
        # NB : c'est une bonne pratique, ainsi les autres fonction appeleront celle ci pour obtenir l'objet plutôt
        # que d'y accéder directement dans le module.
        # cela évite les accès multiple à la même variable sans contrôle, ainsi on donne un seul point d'accès à la
        # variable d'API météo, en s'assurant que tout les traitement nécessaires ont été effectué (et si il y a un bug,
        # il sera corrigé à un seul endroit (ici dans cette fonction)
        return self._meteo_api

    def recherche_ville(self, ville):
        """
        recherche les villes correspondant à la chaîne de caractère donnée en paramètre
        :param ville: chaîne de carcatère qui est le nom de la ville (ou une partie du nom)
        :return: liste des villes trouvées, liste vide si aucun résultat de recherche
        """
        meteo = self._get_meteo_api()
        if meteo is not None:
            reg = meteo.city_id_registry()
            villes = reg.ids_for(ville, country='FR',
                                 matching='like')  # matching='like' permet de faire une recherche même si on ne connaît pas le nom complet de la ville
            new_list = []
            for ville in villes:
                if ville[1] not in new_list:
                    # ville[1] contient le nom de la ville trouvée, se référent à la documentation de l'API pour les détails des valeurs retournées
                    new_list.append(ville[1])
            return new_list
        else:
            raise Exception("MeteoPyowm:recherche_ville: Erreur,l'API météo n'est pas initialisée")

    def get_meteo_ville(self, ville):

        meteo = self._get_meteo_api()

        # par sécurité, avant d'utiliser une variable contenant un objet (ici celui d'API), on vérifie qu'il
        # a bien été initialisé au préalable, pour éviter des erreurs techniques
        if meteo is not None:
            # on recherche l'emplacement de la ville (contient lattitude et longitude)
            reg = meteo.city_id_registry()
            print("Localisation des données géographiques de la ville...")
            emplacements = reg.geopoints_for(ville)

            # la ville n'a pas été trouvée, on génère une exception applicative qui sera gérée par les couches
            # supérieurs (business - presentation - service ...)
            if len(emplacements) == 0:
                raise ApplicationException(f"La ville de {ville} n'a pas été trouvée.")

            print("données géographiques de la ville trouvées. ")
            emplacement = emplacements[0]

            # on obtient les informations météos de la ville
            mgr = meteo.weather_manager()
            return mgr.one_call(lat=emplacement.lat, lon=emplacement.lon, units='metrics')

        else:
            raise Exception("MeteoPyowm:_get_meteo_ville: Erreur,l'API météo n'est pas initialisée")

    @staticmethod
    def get_wind_speed_from_ville_and_period_data(wind_data_from_ville_and_period):
        """
        Permet d'obtenir la vitesse du vent en fonction des données météo d'une ville, pour un jour donnée.
        C'est une méthode de conversion.
        Elle est déclarée comme static car elle n'utilise pas des données de la class.

        Elle permet de ne pas avoir à déclarer la structure "measurables" en dehors de cette classe, et permet de garder
        les dépendances à la librairie pyowm internes à la class.

        :param wind_data_from_ville_and_period: données météo d'une ville, pour un jour donnée:
        :return:
        """

        kmhour_wind_dict = measurables.metric_wind_dict_to_km_h(wind_data_from_ville_and_period)  # permet d'avoir la vitesse en km/h
        return kmhour_wind_dict.get('speed', None)
