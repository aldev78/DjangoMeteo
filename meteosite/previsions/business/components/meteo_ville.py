from ...data.meteo_data import MeteoData
from ...data.meteo_pyowm import MeteoPyowm
from ...utils.application_exception import ApplicationException
from ...utils.meteo_common import MeteoCommon
from ...utils.meteo_utils import MeteoUtils
from ...business.entities.prevision import Prevision
from datetime import date, timedelta

from ...business.entities.ville import Ville


class MeteoVille:
    # ------------------------------
    # constructeur
    # ------------------------------
    def __init__(self, nom_ville):
        self.ville = Ville()
        self.ville.nom = nom_ville
        self._meteo_pyowm = MeteoPyowm()
        self._meteo_data = MeteoData()
        self._meteo_ville = None  # information brut venant de pyowm
        self.previsions = []

        # On initialise les données de la classe avec les informations météo liées ) la ville
        self._init_meteo()

    # ------------------------------
    # propriétés
    # ------------------------------
    @property
    def ville(self):
        return self._ville

    @ville.setter
    def ville(self, value):
        self._ville = value

    # ------------------------------
    # méthodes
    # ------------------------------
    def _init_meteo(self):

        print(f"initialisation des données météo pour la ville : {self.ville.nom}")
        # on vérifie si les données sont en base de données et si elles sont
        # assez récentes
        need_refresh = self._need_refresh_data()

        # si on a besoin d'un refresh, on passe par pyowm pour récupérer les infomrations météo
        # NB : on les enregistre en BDD pour le prochain appel également.
        if need_refresh:

            # on obtient l'instance de la class qui permet de gérer les appels à pyowm
            print("Appel à pyowm.")
            self._meteo_ville = self._meteo_pyowm.get_meteo_ville(self.ville.nom)
            print("Obtention des données auprès de pyowm ok.")

            if self._meteo_ville is not None:

                # pour les jours de aujourd'hui à J+7
                # aujourd'hui étant 0
                # demain étant J+1, etc...
                # on intilise les prévisions avec les valeurs obtenues lors de la récupération des données
                # météo via la méthode interne à la classe : _get_meteo_ville(self, ville)
                # NB : cette méthode a été appellée dans le constructeur.
                for i in range(8):
                    prevision = Prevision()
                    prevision.ville = self.ville
                    prevision.jour = MeteoUtils.get_jour_from_period(i)
                    prevision.temperature = self._get_temperature_prevision(MeteoCommon.PREVISION_TEMPERATURE_JOUR, i)
                    prevision.temperature_matin = self._get_temperature_prevision(MeteoCommon.PREVISION_TEMPERATURE_MATIN, i)
                    prevision.temperature_apres_midi = self._get_temperature_prevision(MeteoCommon.PREVISION_TEMPERATURE_APRES_MIDI, i)
                    prevision.temperature_min = self._get_temperature_prevision(MeteoCommon.PREVISION_TEMPERATURE_MINI, i)
                    prevision.temperature_max = self._get_temperature_prevision(MeteoCommon.PREVISION_TEMPERATURE_MAXI, i)
                    prevision.temperature_nuit = self._get_temperature_prevision(MeteoCommon.PREVISION_TEMPERATURE_NUIT, i)
                    prevision.force_vent = self._get_vent_vitesse_prevision(i)
                    prevision.direction_vent = self._get_vent_orientation_prevision(i)
                    prevision.description = self._get_avis_meteo_detaille_prevision(i)
                    prevision.humidite = self._get_humidity_prevision(i)
                    prevision.pression_atmospherique = self._get_pression_atmospherique_prevision(i)
                    prevision.probabilite_precipitation = self._get_probabilite_precipitation(i)
                    prevision.period = i

                    self.previsions.append(prevision)

                # on sauvegarde en base de données pour éventuellement ne pas faire d'appel à l'API lors des prochaines demandes,
                # si les données sont estimées assez fraîches.
                self._save_meteo_ville()

            else:
                raise ApplicationException(
                    f"MeteoVille:_init_meteo: les données pour la ville {self.ville.nom} n'ont pas pu être initialisées via la librairie PyOWM.")
        else:
            # on a pas besoin d'appeler l'API Pyowm, on charle les données à partir de la base de données
            self._load_meteo_ville()

    def _get_last_prevision(self):
        if len(self.previsions) == 0:
            raise ApplicationException(
                "MeteoVille:_get_last_prevision: Il n'existe pas de prevision pour cette ville, merci d'initialiser les privisions dans le code avant d'appeler cette méthode.")

        most_recent_date = date.fromisoformat('1000-01-01')
        index = 0
        match_index = 0
        for prevision in self.previsions:
            if prevision.jour > most_recent_date:
                match_index = index
            index += 1
        return self.previsions[match_index]

    def _get_temperature_prevision(self, type_temperature, period):
        """
        Obtient la température prévue pour une ville
        :param type_temperature: TEMPERATURE, TEMPERATURE_RESSENTIE, PREVISION_TEMPERATURE_MINI, etc... voir valeurs dans meteo_common.py
        :param period: PREVISION_AUJOURDHUI, PREVISION_J_PLUS_1, PREVISION_J_PLUS_2, etc... voir valeurs dans meteo_common.py
        :return: la température en degrés celsius
        """

        return self._meteo_ville.forecast_daily[period].temperature('celsius').get(type_temperature, None)

    def _get_humidity_prevision(self, period):

        return self._meteo_ville.forecast_daily[period].humidity

    def _get_pression_atmospherique_prevision(self, period):

        return self._meteo_ville.forecast_daily[period].pressure.get('press')

    def _get_vent_vitesse_prevision(self, period):
        """
        Obtient la prévision de vitesse du vent pour une ville et un jour donnés (J, J+1, J+2, etc...)
        :param period: PREVISION_AUJOURDHUI, PREVISION_J_PLUS_1, PREVISION_J_PLUS_2, etc... voir valeurs dans meteo_common.py
        :return:
        """

        # on utilise une méthode static de la class MeteoPyowm (et non pas de l'objet self._meteo_pyowm dont on dispose dans
        # la classe actuel.
        #
        # Nous utilisons une méthode static car elle permet de faire une conversion tout en gardant les références nécessaires à
        # la librairie PyOWM à l'interieur de la classe MeteoPyowm.
        #
        # ainsi, nous n'avons pas ici de référence à la librairie PyOWM, nous passons bien par la classe MeteoPyowm
        # pour la conversion, et son instance self._meteo_pyowm lorsque nécessaire.
        return MeteoPyowm.get_wind_speed_from_ville_and_period_data(self._meteo_ville.forecast_daily[period].wnd)

    def _get_vent_orientation_prevision(self, period):
        """
        Obtient la prévision d'orientation du vent pour une ville et un jour donnés (J, J+1, J+2, etc...)
        :param period: PREVISION_AUJOURDHUI, PREVISION_J_PLUS_1, PREVISION_J_PLUS_2, etc... voir valeurs dans meteo_common.py
        :return:
        """

        return self._meteo_ville.forecast_daily[period].wnd.get('deg', None)

    def _get_avis_meteo_detaille_prevision(self, period):
        """
        Obtient la prévision météo détaillée pour une ville et un jour donnés (J, J+1, J+2, etc...)
        :param period: PREVISION_AUJOURDHUI, PREVISION_J_PLUS_1, PREVISION_J_PLUS_2, etc... voir valeurs dans meteo_common.py
        :return:
        """

        return self._meteo_ville.forecast_daily[period].detailed_status

    def _get_probabilite_precipitation(self, period):
        return self._meteo_ville.forecast_daily[period].precipitation_probability

    def _get_prevision_from_period(self, period):
        """
        Permet d'obtenir une prévision pour la période donnée
        :param period: entier, correspondant à 0 pour J+0, 1, pour J+1, etc...
        :return:
        """
        for prevision in self.previsions:
            if prevision.period == period:
                return prevision
        raise Exception(f"MeteoVille:_get_prevision_from_period: la prévision pour la periode demandée (égale à J+{period}) pour la ville {self.ville.nom} n'a pas été trouvée")

    def get_temperature_for_period(self, type_temperature, period):

        prevision = self._get_prevision_from_period(period)

        if type_temperature == MeteoCommon.PREVISION_TEMPERATURE_JOUR:
            return prevision.temperature
        elif type_temperature == MeteoCommon.PREVISION_TEMPERATURE_MATIN:
            return prevision.temperature_matin
        elif type_temperature == MeteoCommon.PREVISION_TEMPERATURE_APRES_MIDI:
            return prevision.temperature_apres_midi
        elif type_temperature == MeteoCommon.PREVISION_TEMPERATURE_MINI:
            return prevision.temperature_min
        elif type_temperature == MeteoCommon.PREVISION_TEMPERATURE_MAXI:
            return prevision.temperature_max
        elif type_temperature == MeteoCommon.PREVISION_TEMPERATURE_NUIT:
            return prevision.temperature_nuit
        else:
            raise Exception(f"MeteoVille:get_temperature_for_period:  le type de température demandé n'est pas reconnu.")

    def get_description_for_period(self, period):

        prevision = self._get_prevision_from_period(period)
        return prevision.description

    def get_humidite_for_period(self, period):

        prevision = self._get_prevision_from_period(period)
        return prevision.humidite

    def get_pression_atmospherique_for_period(self, period):

        prevision = self._get_prevision_from_period(period)
        return prevision.pression_atmospherique

    def get_force_vent_for_period(self, period):

        prevision = self._get_prevision_from_period(period)
        return prevision.force_vent

    def get_direction_vent_for_period(self, period):

        prevision = self._get_prevision_from_period(period)
        return prevision.direction_vent

    def get_probabilite_precipitation_for_period(self, period):

        prevision = self._get_prevision_from_period(period)
        return prevision.probabilite_precipitation

    def _need_refresh_data(self):
        """
        Indique si les données pour la ville ont été mises à jour il y a moins de 24 heures
        :return: True ou False
        """

        date_derniere_mise_a_jour = self._meteo_data.get_last_update(self.ville.nom)

        if date_derniere_mise_a_jour is None:
            return True  # cela veux dire qu'on a pas trouvé l'information en BDD, donc oui il est nécessaire de rafraîchir les données :-)
        else:
            delta_heures = date.today() - date_derniere_mise_a_jour

            if delta_heures.days > 1:
                return True
            else:
                return False

    def _load_meteo_ville(self):
        """
        Charge les données à partir des données de la base de données
        NB :

        PREVISION_AUJOURDHUI = 0
        PREVISION_J_PLUS_1 = 1
        PREVISION_J_PLUS_2 = 2
        PREVISION_J_PLUS_3 = 3
        PREVISION_J_PLUS_4 = 4
        PREVISION_J_PLUS_5 = 5
        PREVISION_J_PLUS_6 = 6
        PREVISION_J_PLUS_7 = 7
        """

        previsions_ville = self._meteo_data.read_meteo_ville(self.ville.nom)

        # on supprime les prévisions présentes
        self.previsions.clear()

        # on initialise le compteur des périodes (J, J+1, etc.)
        period = 0

        for prevision in previsions_ville:
            prevision_jour = Prevision()
            prevision_jour.ville = self.ville
            prevision_jour.temperature = prevision[0]
            prevision_jour.temperature_min = prevision[1]
            prevision_jour.temperature_max = prevision[2]
            prevision_jour.temperature_matin = prevision[3]
            prevision_jour.temperature_apres_midi = prevision[4]
            prevision_jour.temperature_nuit = prevision[5]
            prevision_jour.description = prevision[6]
            prevision_jour.direction_vent = prevision[7]
            prevision_jour.force_vent = prevision[8]
            prevision_jour.jour = prevision[9]
            prevision_jour.period = period

            # reste à implémenter :
            # prevision_jour.humidite
            # prevision_jour.pression_atmospherique
            # prevision_jour.probabilite_precipitation

            self.previsions.append(prevision_jour)
            period += 1


    def _save_meteo_ville(self):
        """
        On enregistre les prévisions de la ville (d'aujourd'hui et des prochaines jours) en base de données
        :return:
        """

        id_ville = 0

        # on vérifie si le nom de la ville venant des données de Open Weather Map existe dans la base de données
        # si la correspondance n'existe pas, il n'est pas possible d'enregistrer mété associées à cette ville.
        # on prévient alors le programme en générant une exception
        # dans le cas contraire, on récupère l'id de la ville en base de données, qui correspond à l'enregistrement
        # correspondant au nom de la ville (sera utile plus tard pour enregistrer les informations).
        if not self._meteo_data.ville_exists(self.ville.nom):
            raise Exception("save_meteo_ville: La ville ne possède pas de correspondance en base de données")
        else:
            id_ville = self._meteo_data.get_id_ville(self.ville.nom)

        # d'abord, on supprime les prévisions en base de données pour la ville concernée
        self._meteo_data.delete_prevision_ville(self.ville.nom)

        for i in range(8):

            # définition des variables pour récupérer les informations de la variable "meteo_ville"
            # passée en paramètre pour faciliter l'insertion en base de données.
            # => c'est une étape de simplification pour faciliter la lecture du code, les variables
            # sont proches de champs des tables en base de données.

            prevision_jour = dict()

            prevision_jour["temperature"] = -100
            prevision_jour["temperature_min"] = -100
            prevision_jour["temperature_max"] = -100
            prevision_jour["temperature_matin"] = -100
            prevision_jour["temperature_apres_midi"] = -100
            prevision_jour["temperature_nuit"] = -100
            prevision_jour["description"] = "à définir"
            prevision_jour["direction_vent"] = 0
            prevision_jour["force_vent"] = 0
            prevision_jour["jour"] = date.today()

            # maintenant que les valeurs par défaut sont définies, on lie les valeurs
            # dans la structure meteo_ville et on écrase les valeurs par défaut
            # ce principe permet de s'assurer d'avoir à minima des valeurs par défaut
            # même si la structure meteo_ville ne contient pas toutes les données requises

            period = i  # permet de dire le jour de prévision souhaité

            prevision_jour["temperature"] = self.get_temperature_for_period(MeteoCommon.PREVISION_TEMPERATURE_JOUR, period)
            prevision_jour["description"] = self.get_description_for_period(period)
            prevision_jour["direction_vent"] = self.get_direction_vent_for_period(period)
            prevision_jour["force_vent"] = self.get_force_vent_for_period(period)
            prevision_jour["temperature_min"] = self.get_temperature_for_period(MeteoCommon.PREVISION_TEMPERATURE_MINI, period)
            prevision_jour["temperature_max"] = self.get_temperature_for_period(MeteoCommon.PREVISION_TEMPERATURE_MAXI, period)
            prevision_jour["temperature_matin"] = self.get_temperature_for_period(MeteoCommon.PREVISION_TEMPERATURE_MATIN, period)
            prevision_jour["temperature_apres_midi"] = self.get_temperature_for_period(MeteoCommon.PREVISION_TEMPERATURE_APRES_MIDI, period)
            prevision_jour["temperature_nuit"] = self.get_temperature_for_period(MeteoCommon.PREVISION_TEMPERATURE_NUIT, period)

            # définition du jour de la prévision
            if period > 0:
                prevision_jour["jour"] = date.today() + timedelta(days=period)

            # insertion des valeurs en base de données
            self._meteo_data.ajout_prevision_ville(id_ville, prevision_jour["temperature"], prevision_jour["temperature_min"], prevision_jour["temperature_max"], prevision_jour["temperature_matin"],
                                                   prevision_jour["temperature_apres_midi"], prevision_jour["temperature_nuit"], prevision_jour["description"], prevision_jour["direction_vent"],
                                                   prevision_jour["force_vent"], prevision_jour["jour"])