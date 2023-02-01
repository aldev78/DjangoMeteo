from datetime import date, timedelta

from .meteo_common import MeteoCommon


class MeteoUtils:
    # ------------------------------
    # méthodes
    # ------------------------------
    @staticmethod
    def get_statut_meteo(avis_meteo_actuel):
        """
        Renvoi la valeur de la constante représentant le statut applicatif de l'avis météo actuel (constante), si l'avis météo n'est pas reconnu,
        alors une exception est levée (ValueError)
        :param avis_meteo_actuel: l'avis météo actuel
        :return: la valeur de la constante représentant le statut applicatif de l'avis météo actuel
        """
        if avis_meteo_actuel == MeteoCommon.STATUT_API_NUAGEUX:
            return MeteoCommon.STATUT_IMAGE_METEO_NUAGEUX
        elif avis_meteo_actuel == MeteoCommon.STATUT_API_PEU_NUAGEUX:
            return MeteoCommon.STATUT_IMAGE_METEO_ECLAIRCIES
        elif avis_meteo_actuel == MeteoCommon.STATUT_API_PARTIELLEMENT_NUAGEUX:
            return MeteoCommon.STATUT_IMAGE_METEO_ECLAIRCIES
        elif avis_meteo_actuel == MeteoCommon.STATUT_API_CIEL_DEGAGE:
            return MeteoCommon.STATUT_IMAGE_METEO_SOLEIL
        elif avis_meteo_actuel == MeteoCommon.STATUT_API_LEGERE_PLUIE:
            return MeteoCommon.STATUT_IMAGE_METEO_PLUIE
        elif avis_meteo_actuel == MeteoCommon.STATUT_API_LEGERE_COUVERT:
            return MeteoCommon.STATUT_IMAGE_METEO_NUAGEUX
        elif avis_meteo_actuel == MeteoCommon.STATUT_API_BRUME:
            return MeteoCommon.STATUT_IMAGE_METEO_NUAGEUX
        else:
            raise ValueError("l'image pour la prévision actuelle n'est pas configurée, pensez à mettre à jour le code")

    @staticmethod
    def get_texte_meteo_file_name(value):
        if value == MeteoCommon.STATUT_IMAGE_METEO_NEIGE:
            return "neige.txt"
        elif value == MeteoCommon.STATUT_IMAGE_METEO_ORAGE:
            return "orage.txt"
        elif value == MeteoCommon.STATUT_IMAGE_METEO_PLUIE:
            return "pluie.txt"
        elif value == MeteoCommon.STATUT_IMAGE_METEO_SOLEIL:
            return "soleil.txt"
        elif value == MeteoCommon.STATUT_IMAGE_METEO_NUAGEUX:
            return "nuageux.txt"
        elif value == MeteoCommon.STATUT_IMAGE_METEO_ECLAIRCIES:
            return "eclaircies.txt"
        else:
            raise ValueError("l'image pour la prévision actuelle n'est pas configurée, pensez à mettre à jour le code")

    @staticmethod
    def get_image_meteo_file_name(value):
        if value == MeteoCommon.STATUT_IMAGE_METEO_NEIGE:
            return "neige.png"
        elif value == MeteoCommon.STATUT_IMAGE_METEO_ORAGE:
            return "orage.png"
        elif value == MeteoCommon.STATUT_IMAGE_METEO_PLUIE:
            return "pluie.png"
        elif value == MeteoCommon.STATUT_IMAGE_METEO_SOLEIL:
            return "soleil.png"
        elif value == MeteoCommon.STATUT_IMAGE_METEO_NUAGEUX:
            return "nuageux.png"
        elif value == MeteoCommon.STATUT_IMAGE_METEO_ECLAIRCIES:
            return "eclaircies.png"
        else:
            raise ValueError("l'image pour la prévision actuelle n'est pas configurée, pensez à mettre à jour le code")

    @staticmethod
    def usage():
        """
        Afficher les informations permettant l'utilisation du programme en ligne de commande
        """
        print("Voici les options possibles (mettre la liste des options : )")
        print("\t-h ou --help : affichage de ce menu")
        print("\t-s ou --search : affiche la liste des villes trouvées et leur identifiants (vous devez spécifier le nom de la ville recherchée après l'option")
        print("\t-i ou --interactive : permet l'exécution classique du programme en mode interactif avec l'utilisateur")
        print("\t-d ou --display : affiche la météo de la ville passée en paramètre après l'option (utiliser des doubles quotes si il existe des espaces dans le nom de la ville)")
        print("\t-e ou --export : export la météo de la ville passée en paramètre après l'option (au format html)")
        print("\t-w ou --web : démarrage du serveur web pour réponses aux demandes de pages web")
        print("")

    @staticmethod
    def get_jour_from_period(period):
        """
        Renvoi la date en fonction de la période (J, J+1, J+2, etc...)
        :param period: J, J+1, J+2, etc... 0 étant aujourd'hui, 1 étant J+1, etc...
        :return:
        """
        if period == 0:
            return date.today()
        else:
            return date.today() + timedelta(days=period)

    @staticmethod
    def get_correspondance_type_temperature_API_BDD(type_API):
        """
        Les choix fait en base de données demande une correspondance des types de températures car ils ne sont pas
        exactement les même que ceux de l'API
        :param type_API:
        :return: la correspondance du type présent en BDD en fonction du type de l'API fournit en paramètre
        """
        if type_API == MeteoCommon.TEMPERATURE:
            return "temperature"
        if type_API == MeteoCommon.TEMPERATURE_RESSENTIE:
            return "temperature"
        if type_API == MeteoCommon.PREVISION_TEMPERATURE_JOUR:
            return "temperature"
        if type_API == MeteoCommon.PREVISION_TEMPERATURE_MINI:
            return "temperature_min"
        if type_API == MeteoCommon.PREVISION_TEMPERATURE_MAXI:
            return "temperature_max"
        if type_API == MeteoCommon.PREVISION_TEMPERATURE_NUIT:
            return "temperature_nuit"
        if type_API == MeteoCommon.PREVISION_TEMPERATURE_MATIN:
            return "temperature_matin"
        if type_API == MeteoCommon.PREVISION_TEMPERATURE_APRES_MIDI:
            return "temperature_apres_midi"
