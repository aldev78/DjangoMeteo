from ..meteo_common import MeteoCommon
from ..meteo_utils import MeteoUtils


class UIHelper:

    @staticmethod
    def icon_from_weather_status(weather_status: str) -> str:
        if weather_status == MeteoCommon.STATUT_API_NUAGEUX:
            return "fas fa-clouds"
        elif weather_status == MeteoCommon.STATUT_API_PARTIELLEMENT_NUAGEUX:
            return "fas fa-cloud"
        elif weather_status == MeteoCommon.STATUT_API_PEU_NUAGEUX:
            return "fas fa-cloud-sun"
        elif weather_status == MeteoCommon.STATUT_API_CIEL_DEGAGE:
            return "fas fa-sun"
        elif weather_status == MeteoCommon.STATUT_API_LEGERE_PLUIE:
            return "fas fa-cloud-drizzle"
        elif weather_status == MeteoCommon.STATUT_API_BRUME:
            return "fas fa-cloud-fog"
        else:
            return "fas seal-question"

    @staticmethod
    def image_from_weather_status(weather_status: str) -> str:
        if weather_status == MeteoCommon.STATUT_API_NUAGEUX:
            return "cloudy-day-3.svg"
        elif weather_status == MeteoCommon.STATUT_API_PARTIELLEMENT_NUAGEUX:
            return "cloudy-day-2.svg"
        elif weather_status == MeteoCommon.STATUT_API_PEU_NUAGEUX:
            return "cloudy-day-1.svg"
        elif weather_status == MeteoCommon.STATUT_API_CIEL_DEGAGE:
            return "day.svg"
        elif weather_status == MeteoCommon.STATUT_API_LEGERE_PLUIE:
            return "rainy-4.svg"
        elif weather_status == MeteoCommon.STATUT_API_BRUME:
            return "brume.svg"
        elif weather_status == MeteoCommon.STATUT_API_LEGERE_COUVERT:
            return "couvert.svg"
        elif weather_status == MeteoCommon.STATUT_API_PLUIE_MODEREE:
            return "rainy-6.svg"
        elif weather_status == MeteoCommon.STATUT_API_FORTE_PLUIE:
            return "rainy-7.svg"
        else:
            return "Icon-round-Question_mark.svg"

    @staticmethod
    def day_of_the_week_from_period(period: int) -> str:
        day = MeteoUtils.get_jour_from_period(period).strftime("%A")

        if day == "Monday":
            return "Lundi"
        if day == "Tuesday":
            return "Mardi"
        if day == "Wednesday":
            return "Mercredi"
        if day == "Thursday":
            return "Jeudi"
        if day == "Friday":
            return "Vendredi"
        if day == "Saturday":
            return "Samedi"
        if day == "Sunday":
            return "Dimanche"
