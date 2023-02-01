import datetime

from meteosite.previsions.utils.meteo_utils import MeteoUtils

EXPORT_PATH = "/media/nicolas/DATA/coder pour changer de vie/FORMATION/code/ProjetMeteo"
IMAGES_PATH = "ressources/images"


def export(ville, avis_meteo_actuel):
    """
    Génère une page html concernant les informations météo de la ville concernée
    :param ville: la ville concernée
    :param avis_meteo_actuel: l'avis météo actuel
    """
    date = datetime.datetime.today().strftime('%Y%m%d%H')
    filename = date + "-" + ville + ".html"
    image_filename = MeteoUtils.get_image_meteo_file_name(MeteoUtils.get_statut_meteo(avis_meteo_actuel))

    page_html = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{ville}</title></head>'
    page_html += f'<body><center><H1>Ville : {ville}</h1><div>Date : {datetime.datetime.today().strftime("%Y-%m-%d %H:%M")}</div>'
    page_html += f'<p>Actuellement le temps est : {avis_meteo_actuel}</p>'
    page_html += f'<div><img src=\"{IMAGES_PATH + "/" + image_filename}\"></img></div>'
    page_html += f'</center></body></html>'

    file = open(EXPORT_PATH + "/" + filename, "w")
    file.write(page_html)
    file.close()
