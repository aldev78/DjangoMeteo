import pyowm
from pyowm.utils.config import get_default_config
from pyowm.utils import measurables
from datetime import date, timedelta
from meteosite.previsions.utils import meteo_common
from meteosite.previsions.data import meteo_data

# initialisation des variables du module (le "_" devant le nom des variables est une convention
# pour indiquer qu'elle doivent être utilisées à titre privé dans le module
APIKEY = '58e0e8ebda9c67eadecece78e50275f3'
_meteo_api_initialized = False
_meteo_api = None  # On force la valeur à "None" pour permettre les tests par la suite (Null dans les autres langages le plus souvent)
_meteo_villes = {}  # Permet de garder en mémoire les informations météo d'une ville, pour ne pas redemander les données à chaque appel (car il existe une limitation d'appel côté API à préserver)


def _get_meteo_api():
    """
    Intialise l'objet _meteo_api qui permet de dialoguer avec l'API de OpenWeatherMap
    :return:
    """

    # les variables sont déclarées global car les valeurs être stockées sont au niveau des variables du module
    # ainsi les autres fonctions du module pour utiliser les variables du module initialisées ici
    # NB : nécessaire car sinon la durée de vie des variables est celle de la durée de vie de la fonction
    global _meteo_api_initialized
    global _meteo_api

    # on vérifie par le boulon que l'initialisation n'a pas été déjà faite, pour ne pas faire
    # des traitements inutiles (consommation de ressources alors qu'on les a déjà)
    if not _meteo_api_initialized:
        config_dict = get_default_config()
        config_dict['language'] = 'fr'
        _meteo_api = pyowm.OWM(APIKEY, config_dict)
        _meteo_api_initialized = True

    # on obtient l'objet API si il avait déjà été initialisé ou bien si il vient juste de l'être
    # NB : c'est une bonne pratique, ainsi les autres fonction appeleront celle ci pour obtenir l'objet plutôt
    # que d'y accéder directement dans le module.
    # cela évite les accès multiple à la même variable sans contrôle, ainsi on donne un seul point d'accès à la
    # variable d'API météo, en s'assurant que tout les traitement nécessaires ont été effectué (et si il y a un bug,
    # il sera corrigé à un seul endroit (ici dans cette fonction)
    return _meteo_api


def recherche_ville(ville):
    """
    recherche les villes correspondant à la chaîne de caractère donnée en paramètre
    :param ville: chaîne de carcatère qui est le nom de la ville (ou une partie du nom)
    :return: liste des villes trouvées, liste vide si aucun résultat de recherche
    """
    meteo = _get_meteo_api()
    if meteo is not None:
        reg = meteo.city_id_registry()
        villes = reg.ids_for(ville, country='FR', matching='like')  # matching='like' permet de faire une recherche même si on ne connaît pas le nom complet de la ville
        new_list = []
        for ville in villes:
            if ville[1] not in new_list:
                new_list.append(ville[1])  # ville[1] contient le nom de la ville trouvée, se référent à la documentation de l'API pour les détails des valeurs retournées
        return new_list
    else:
        print("Erreur : l'API météo n'est pas initialisée")


def _get_meteo_ville(ville):
    '''
    Obtient les informations météo courantes d'une ville
    :param ville: nom de la ville
    :return: les informations météo courantes d'une ville
    '''
    global _meteo_villes

    # si la météo d'une ville a déjà été consulté, renvoyé le resultat déjà mémorisé
    if ville in _meteo_villes:
        return _meteo_villes[ville]

    meteo = _get_meteo_api()

    # par sécurité, avant d'utiliser une variable contenant un objet (ici celui d'API), on vérifie qu'il
    # a bien été initialisé au préalable, pour éviter des erreurs techniques
    if meteo is not None:
        # on recherche l'emplacement de la ville (contient lattitude et longitude)
        reg = meteo.city_id_registry()
        emplacements = reg.geopoints_for(ville)
        emplacement = emplacements[0]

        # on obtient les informations météos de la ville
        mgr = meteo.weather_manager()
        meteo_ville = mgr.one_call(lat=emplacement.lat, lon=emplacement.lon, units='metrics')

        # on enregistre en mémoire pour la prochaine demande
        _meteo_villes[ville] = meteo_ville

        # on enregistre en base de données
        save_meteo_ville(ville, meteo_ville)

        # on renvoi la météo demandée pour la ville
        return meteo_ville
    else:
        print("Erreur : l'API météo n'est pas initialisée")


def get_temperature_actuelle(ville):
    """
    Obtient la températue actuelle d'une ville en degrés celsius
    :param ville: chaine de caractère représentant la ville sur laquelle porte la recherche
    :return: la témpérature, en degré celsius
    """

    # avant toute chose, on vérifie si les informations météo concernant la ville existent en base de données,
    # afin de ne pas soliciter l'API inutilement et utiliser des quotas limités.
    need_refresh = _need_refresh_data(ville)

    if need_refresh:
        meteo_ville = _get_meteo_ville(ville)
        return meteo_ville.current.temperature('celsius').get('temp', None)
    else:
        donnees_bdd = _read_meteo_ville(ville)
        return donnees_bdd[0]["temperature"]




def get_temperature_prevision(ville, type_temperature, period):
    """
    Obtient la température prévue pour une ville
    :param ville: chaine de caractère représentant la ville sur laquelle porte la recherche
    :param type_temperature: TEMPERATURE, TEMPERATURE_RESSENTIE, PREVISION_TEMPERATURE_MINI, etc... voir valeurs dans meteo_common.py
    :param period: PREVISION_AUJOURDHUI, PREVISION_J_PLUS_1, PREVISION_J_PLUS_2, etc... voir valeurs dans meteo_common.py
    :return: la température en degrés celsius
    """


    # avant toute chose, on vérifie si les informations météo concernant la ville existent en base de données,
    # afin de ne pas soliciter l'API inutilement et utiliser des quotas limités.
    need_refresh = _need_refresh_data(ville)

    if need_refresh:
        meteo_ville = _get_meteo_ville(ville)
        temperature = meteo_ville.forecast_daily[period].temperature('celsius').get(type_temperature, None)
        return temperature
    else:
        donnees_bdd = _read_meteo_ville(ville)
        return donnees_bdd[period][_get_correspondance_type_temperature_API_BDD(type_temperature)]


def get_avis_meteo(ville):
    """
    obtient une descrption courte de l'avis météo sous forme de chapine de caractère
    :param ville: chaine de caractère représentant la ville sur laquelle porte la recherche
    :return: chaîne de caractère qui est la description courte de l'avis météo
    """

    meteo_ville = _get_meteo_ville(ville)
    return meteo_ville.current.status


def get_avis_meteo_detaille(ville):
    """
    obtient l'avis météo détaillé pour la ville recherchée
    :param ville: chaine de caractère représentant la ville sur laquelle porte la recherche
    :return: avis détaillé
    """

    meteo_ville = _get_meteo_ville(ville)
    return meteo_ville.current.detailed_status


def get_avis_meteo_detaille_prevision(ville, period):
    """
    Obtient la prévision météo détaillée pour une ville et un jour donnés (J, J+1, J+2, etc...)
    :param ville: chaine de caractère représentant la ville sur laquelle porte la recherche
    :param period: PREVISION_AUJOURDHUI, PREVISION_J_PLUS_1, PREVISION_J_PLUS_2, etc... voir valeurs dans meteo_common.py
    :return:
    """

    meteo_ville = _get_meteo_ville(ville)
    return meteo_ville.forecast_daily[period].detailed_status


def get_humidite_prevision(ville, period):
    """
    Obtient la prévision d'humidité pour une ville et un jour donnés (J, J+1, J+2, etc...)
    :param ville: chaine de caractère représentant la ville sur laquelle porte la recherche
    :param period: PREVISION_AUJOURDHUI, PREVISION_J_PLUS_1, PREVISION_J_PLUS_2, etc... voir valeurs dans meteo_common.py
    :return:
    """

    meteo_ville = _get_meteo_ville(ville)
    return meteo_ville.forecast_daily[period].humidity


def get_pression_athmospherique_prevision(ville, period):
    """
    Obtient la prévision de pression athmosphérique pour une ville et un jour donnés (J, J+1, J+2, etc...)
    :param ville: chaine de caractère représentant la ville sur laquelle porte la recherche
    :param period: PREVISION_AUJOURDHUI, PREVISION_J_PLUS_1, PREVISION_J_PLUS_2, etc... voir valeurs dans meteo_common.py
    :return:
    """

    meteo_ville = _get_meteo_ville(ville)
    return meteo_ville.forecast_daily[period].pressure.get('press')


def get_vent_vitesse_prevision(ville, period):
    """
    Obtient la prévision de vitesse du vent pour une ville et un jour donnés (J, J+1, J+2, etc...)
    :param ville: chaine de caractère représentant la ville sur laquelle porte la recherche
    :param period: PREVISION_AUJOURDHUI, PREVISION_J_PLUS_1, PREVISION_J_PLUS_2, etc... voir valeurs dans meteo_common.py
    :return:
    """

    # avant toute chose, on vérifie si les informations météo concernant la ville existent en base de données,
    # afin de ne pas soliciter l'API inutilement et utiliser des quotas limités.
    need_refresh = _need_refresh_data(ville)

    if need_refresh:
        meteo_ville = _get_meteo_ville(ville)
        kmhour_wind_dict = measurables.metric_wind_dict_to_km_h(
            meteo_ville.forecast_daily[period].wnd)  # permet d'avoir la vitesse en km/h
        return kmhour_wind_dict.get('speed', None)
    else:
        donnees_bdd = _read_meteo_ville(ville)
        return donnees_bdd[period]["force_vent"]


def get_vent_orientation_prevision(ville, period):
    """
    Obtient la prévision d'orientation du vent pour une ville et un jour donnés (J, J+1, J+2, etc...)
    :param ville: chaine de caractère représentant la ville sur laquelle porte la recherche
    :param period: PREVISION_AUJOURDHUI, PREVISION_J_PLUS_1, PREVISION_J_PLUS_2, etc... voir valeurs dans meteo_common.py
    :return:
    """

    # avant toute chose, on vérifie si les informations météo concernant la ville existent en base de données,
    # afin de ne pas soliciter l'API inutilement et utiliser des quotas limités.
    need_refresh = _need_refresh_data(ville)

    if need_refresh:
        meteo_ville = _get_meteo_ville(ville)
        return meteo_ville.forecast_daily[period].wnd.get('deg', None)
    else:
        donnees_bdd = _read_meteo_ville(ville)
        return donnees_bdd[period]["direction_vent"]


def get_probabilite_precipitation_prevision(ville, period):
    """
    Obtient la prévision de la probabilité de précipitation du vent pour une ville et un jour donnés (J, J+1, J+2, etc...)
    :param ville: chaine de caractère représentant la ville sur laquelle porte la recherche
    :param period: PREVISION_AUJOURDHUI, PREVISION_J_PLUS_1, PREVISION_J_PLUS_2, etc... voir valeurs dans meteo_common.py
    :return:
    """

    meteo_ville = _get_meteo_ville(ville)
    return meteo_ville.forecast_daily[period].precipitation_probability

def save_meteo_ville(ville, meteo_ville):
    """
    On enregistre les prévisions de la ville (d'aujourd'hui et des prochaines jours) en base de données
    :param ville: le nom de la ville
    :param meteo_ville: les données concernant la ville provenant de l'API d'Open Weather Map
    :return:
    """

    id_ville = 0
    # on vérifie si le nom de la ville venant des données de Open Weather Map existe dans la base de données
    # si la correspondance n'existe pas, il n'est pas possible d'enregistrer mété associées à cette ville.
    # on prévient alors le programme en générant une exception
    # dans le cas contraire, on récupère l'id de la ville en base de données, qui correspond à l'enregistrement
    # correspondant au nom de la ville (sera utile plus tard pour enregistrer les informations).
    if not meteo_data.ville_exists(ville):
        raise Exception("save_meteo_ville: La ville ne possède pas de correspondance en base de données")
    else:
        id_ville = meteo_data.get_id_ville(ville)

    # d'abord, on supprimer les prévisions en base de données pour la ville concernée
    meteo_data.delete_prevision_ville(ville)

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

        period = i #permet de dire le jour de prévision souhaité

        # pour le jour actuel, on prend la températude actuel, sinon la température prévisionnel du jour
        if period == 0:
            prevision_jour["temperature"] = meteo_ville.current.temperature('celsius').get('temp', None)
        else:
            prevision_jour["temperature"] = meteo_ville.forecast_daily[period].temperature('celsius').get(
                meteo_common.PREVISION_TEMPERATURE_JOUR, None)

        prevision_jour["description"] = meteo_ville.forecast_daily[period].detailed_status
        prevision_jour["direction_vent"] = meteo_ville.forecast_daily[period].wnd.get('deg', None)
        prevision_jour["force_vent"] = (measurables.metric_wind_dict_to_km_h(meteo_ville.forecast_daily[period].wnd))["speed"]  # permet d'avoir la vitesse en km/h
        prevision_jour["temperature_min"] = meteo_ville.forecast_daily[period].temperature('celsius').get(
            meteo_common.PREVISION_TEMPERATURE_MINI, None)
        prevision_jour["temperature_max"] = meteo_ville.forecast_daily[period].temperature('celsius').get(
            meteo_common.PREVISION_TEMPERATURE_MAXI, None)
        prevision_jour["temperature_matin"] = meteo_ville.forecast_daily[period].temperature('celsius').get(
            meteo_common.PREVISION_TEMPERATURE_MATIN, None)
        prevision_jour["temperature_apres_midi"] = meteo_ville.forecast_daily[period].temperature('celsius').get(
            meteo_common.PREVISION_TEMPERATURE_APRES_MIDI, None)
        prevision_jour["temperature_nuit"] = meteo_ville.forecast_daily[period].temperature('celsius').get(
            meteo_common.PREVISION_TEMPERATURE_NUIT, None)

        #définition du jour de la prévision
        if period > 0:
            prevision_jour["jour"] = date.today() + timedelta(days=period)

        #insertion des valeurs en base de données
        meteo_data.ajout_prevision_ville(id_ville, prevision_jour["temperature"], prevision_jour["temperature_min"], prevision_jour["temperature_max"], prevision_jour["temperature_matin"], prevision_jour["temperature_apres_midi"], prevision_jour["temperature_nuit"], prevision_jour["description"], prevision_jour["direction_vent"], prevision_jour["force_vent"], prevision_jour["jour"])


def _need_refresh_data(ville):
    """
    Indique si les données pour la ville ont été mises à jour il y a moins de 24 heures
    :param ville: nom de la ville
    :return: True ou False
    """

    date_derniere_mise_a_jour = meteo_data.get_last_update(ville)

    if date_derniere_mise_a_jour is None:
        return True     #cela veux dire qu'on a pas trouvé l'information en BDD, donc oui il est nécessaire de rafraîchir les données :-)
    else:
        delta_heures = date.today() - date_derniere_mise_a_jour

        if delta_heures.days > 1:
            return True
        else:
            return False

def _read_meteo_ville(ville):
    """
    Construit un dictionnaire facilement exploitable pour consulter les données en mémoire, chargées à partir
    de la base de données pour une ville donnée.

    NB : les constantes définies dans meteo_common.py peuvent être reprises aisément afin de consulter le dictionnaire
    grâce à la période :

    PREVISION_AUJOURDHUI = 0
    PREVISION_J_PLUS_1 = 1
    PREVISION_J_PLUS_2 = 2
    PREVISION_J_PLUS_3 = 3
    PREVISION_J_PLUS_4 = 4
    PREVISION_J_PLUS_5 = 5
    PREVISION_J_PLUS_6 = 6
    PREVISION_J_PLUS_7 = 7

    :param ville: nom de la ville
    :return: Dictionnaire contenant les prévisions météo de la ville pour le jour même et les 7 jours suivant
    """

    previsions_ville = meteo_data.read_meteo_ville(ville)

    dict_prevision_ville = dict()
    period = 0

    for prevision in previsions_ville:

        prevision_jour = dict()

        prevision_jour["temperature"] = prevision[0]
        prevision_jour["temperature_min"] = prevision[1]
        prevision_jour["temperature_max"] = prevision[2]
        prevision_jour["temperature_matin"] = prevision[3]
        prevision_jour["temperature_apres_midi"] = prevision[4]
        prevision_jour["temperature_nuit"] = prevision[5]
        prevision_jour["description"] = prevision[6]
        prevision_jour["direction_vent"] = prevision[7]
        prevision_jour["force_vent"] = prevision[8]
        prevision_jour["jour"] = prevision[9]

        dict_prevision_ville[period] = prevision_jour
        period += 1

    return dict_prevision_ville

def _get_correspondance_type_temperature_API_BDD(type_API):
    """
    Les choix fait en base de données demande une correspondance des types de températures car ils ne sont pas
    exactement les même que ceux de l'API
    :param type_API:
    :return: la correspondance du type présent en BDD en fonction du type de l'API fournit en paramètre
    """
    if type_API == meteo_common.TEMPERATURE:
        return "temperature"
    if type_API == meteo_common.TEMPERATURE_RESSENTIE:
        return "temperature"
    if type_API == meteo_common.PREVISION_TEMPERATURE_JOUR:
        return "temperature"
    if type_API == meteo_common.PREVISION_TEMPERATURE_MINI:
        return "temperature_min"
    if type_API == meteo_common.PREVISION_TEMPERATURE_MAXI:
        return "temperature_max"
    if type_API == meteo_common.PREVISION_TEMPERATURE_NUIT:
        return "temperature_nuit"
    if type_API == meteo_common.PREVISION_TEMPERATURE_MATIN:
        return "temperature_matin"
    if type_API == meteo_common.PREVISION_TEMPERATURE_APRES_MIDI:
        return "temperature_apres_midi"
