"""
-------------------------------------------------------------------------------
DECLARATIONS DES CONSTANTES UTILES POUR L'ENSEMBLE DE L'APPLICATION
-------------------------------------------------------------------------------
"""


class MeteoCommon:

    "ici, toutes les variables sont des variables de class (et non d'instance)"

    TEMPERATURE = 0
    TEMPERATURE_RESSENTIE = 1
    PREVISION_TEMPERATURE_JOUR = "day"
    PREVISION_TEMPERATURE_MINI = "min"
    PREVISION_TEMPERATURE_MAXI = "max"
    PREVISION_TEMPERATURE_NUIT = "night"
    PREVISION_TEMPERATURE_MATIN = "morn"
    PREVISION_TEMPERATURE_APRES_MIDI = "eve"
    PREVISION_TEMPERATURE_RESSENTIE_JOUR = "feels_like_day"
    PREVISION_TEMPERATURE_RESSENTIE_NUIT = "feels_like_night"
    PREVISION_TEMPERATURE_RESSENTIE_MATIN = "feels_like_morn"
    PREVISION_TEMPERATURE_RESSENTIE_APRES_MIDI = "feels_like_eve"

    PREVISION_AUJOURDHUI = 0
    PREVISION_J_PLUS_1 = 1
    PREVISION_J_PLUS_2 = 2
    PREVISION_J_PLUS_3 = 3
    PREVISION_J_PLUS_4 = 4
    PREVISION_J_PLUS_5 = 5
    PREVISION_J_PLUS_6 = 6
    PREVISION_J_PLUS_7 = 7

    STATUT_API_NUAGEUX = "nuageux"
    STATUT_API_PEU_NUAGEUX = "peu nuageux"
    STATUT_API_PARTIELLEMENT_NUAGEUX = "partiellement nuageux"
    STATUT_API_CIEL_DEGAGE = "ciel dégagé"
    STATUT_API_LEGERE_PLUIE = "légère pluie"
    STATUT_API_LEGERE_COUVERT = "couvert"
    STATUT_API_BRUME = "brume"
    STATUT_API_PLUIE_MODEREE = "pluie modérée",
    STATUT_API_FORTE_PLUIE = "forte pluie",

    STATUT_IMAGE_METEO_PLUIE = 0
    STATUT_IMAGE_METEO_ORAGE = 1
    STATUT_IMAGE_METEO_NEIGE = 2
    STATUT_IMAGE_METEO_SOLEIL = 3
    STATUT_IMAGE_METEO_NUAGEUX = 4
    STATUT_IMAGE_METEO_ECLAIRCIES = 5
