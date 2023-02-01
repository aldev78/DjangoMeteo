from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
import logging

from .business.components.meteo_ville_previsions import MeteoVillePrevisions
from .models import Ville
from .models import Departement
from .forms import VilleForm, DepartClientForm
from .utils.helper.ui_helper import UIHelper

logger = logging.getLogger("django")


@login_required(login_url=f'/previsions/login/?next=/previsions/login/')
def index(request):
    logger.debug("entrée dans la view 'Index'")
    template = loader.get_template('previsions/index.html')
    context = {}
    logger.warning('le contexte pour la view est vide')

    # ajout des villes favorites à la sessions utilisateur (simulation d'une sélection
    # déjà faite par l'utilisateur
    logger.info(f"Définition des villes favorites pour l'utilisateur")
    liste_villes_favorites = ['Paris', 'Lyon', 'Strasbourg']
    request.session['favoris'] = liste_villes_favorites

    logger.debug("sortie dans la view 'Index', rendu du tempate...")

    return HttpResponse(template.render(context, request))


def departements(request):
    # on obtient ici toutes les villes dont la clée étrangère est égale à 1
    #
    # ce qui correspond à la requête SQL :
    # select * from ville where id_departement = 1
    villes_du_departement = Ville.objects.filter(id_departement=1).order_by('nom')
    nom_departement = "Ain"

    # maintenant que nous avons les données, nous allons les associer
    # au context. Ainsi le Template pourra les utiliser pour générer l'affichage
    # avec les données.
    context = {
        'villes_du_departement': villes_du_departement,
        'nom_departement': nom_departement,
    }

    # nous pouvons utiliser un objet template pour générer l'affichage puis
    # le retourner via un objet HttpResponse mais... django propose
    # une methode 'render' qui le fait pour nous, alors utilisons la :-)
    return render(request, 'previsions/departements.html', context)


def select_departement(request):
    # on obtient la liste de tous les départements en BDD
    #
    # Se référer à la documentation django pour les requêtes de sélection d'objets
    # https://docs.djangoproject.com/fr/4.1/topics/db/queries/
    #
    liste_departements = Departement.objects.all()

    # on associe les données au context pour que le template puisse les utiliser
    context = {
        'liste_departements': liste_departements,
    }

    # on s'appuie sur Djangon pour initialiser le template et renvoyer le résultat
    return render(request, 'previsions/select_departement.html', context)


def display_villes(request):
    # on récupère le choix réalisé par l'utilisateur dans le formulaire
    # via l'objet request.
    # NB : le nom de l'élément HTML "select" est id_departement, la valeur ici
    # est celle de l'élément "option" choisi par l'utilisateur
    id_departement = request.POST['id_departement']

    # on obtient la liste de tous les départements en BDD
    #
    # Se référer à la documentation django pour les requêtes de sélection d'objets
    # https://docs.djangoproject.com/fr/4.1/topics/db/queries/
    #
    departement = Departement.objects.get(pk=id_departement)
    villes_du_departement = Ville.objects.filter(id_departement=id_departement).order_by('nom')

    # on associe les données au context pour que le template puisse les utiliser
    context = {
        'villes_du_departement': villes_du_departement,
        'departement': departement,
    }

    # on s'appuie sur Djangon pour initialiser le template et renvoyer le résultat
    return render(request, 'previsions/display_villes.html', context)


def add_ville(request):
    save_error = False
    is_create = True

    if request.method == 'POST':

        # on reçoit les données du formulaire, donc on n'est pas en mode création pour l'ajout
        # d'une nouvelle ville en BDD
        is_create = False

        # crée une instance du formulaire et remplie les champs avec les données présentes dans l'objet request
        form = VilleForm(request.POST)
        # la class form de Django permet de valider automatiquement les données utilisateur
        # lors de la saisie dans la navigateur, mais aussi lors de l'enregistrement en base de données
        if form.is_valid():

            # récupération des valeur du formulaire
            nom = form.cleaned_data["nom"]
            code_postal = form.cleaned_data["code_postal"]
            departement = form.cleaned_data["departement"]

            try:
                # enregistrement en base de données
                print("enregistrement de la ville en BDD...")
                ville = Ville()
                ville.nom = nom
                ville.code_postal = code_postal
                ville.id_departement = departement
                ville.save()

                print("enregistrement ok.")

                # maintenant que l'enregistrement est réalisé, on en permet un nouveau en créeant une nouvelle instance
                # pour cela
                form = VilleForm()

            except:
                save_error = True


    # Si l'on est pas sur la soumission de données, alors c'est que nous sommes en saisie de données
    # dans le formulaire, on fournit donc une instance de forumulaire
    else:
        form = VilleForm()

    return render(request, 'previsions/add_ville.html',
                  {'form': form, 'save_error': save_error, 'is_create': is_create})


def favoris(request):
    # Récupération des favoris depuis la liste stockée en session
    liste_villes_favorites = request.session['favoris']

    context = {
        'favoris': liste_villes_favorites,
    }

    return render(request, 'previsions/favoris.html', context)


def departement_client(request):
    # instanciation du formulaire
    form = DepartClientForm()

    liste_departements = Departement.objects.all()
    id_departement = 0
    page_obj = {}

    if request.method == 'POST':
        # crée une instance du formulaire et remplie les champs avec les données présentes dans l'objet request
        form = DepartClientForm(request.POST)

        # la class form de Django permet de valider automatiquement les données utilisateur
        # lors de la saisie dans la navigateur, mais aussi lors de l'enregistrement en base de données
        if form.is_valid():  # Forms only get a cleaned_data attribute when is_valid() has been called
            id_departement = form.cleaned_data["departement"]
            villes_du_departement = Ville.objects.filter(id_departement=id_departement).order_by('nom')
            paginator = Paginator(villes_du_departement, 20)

            page_number = request.GET.get('page')

            page_obj = paginator.get_page(page_number)

    context = {
        'liste_departements': liste_departements,
        'id_departement': id_departement,
        'form': form,
        'page_obj': page_obj,
    }

    return render(request, 'previsions/departement_client.html', context)


def display_previsions_ville(request):
    # on récupère la ville provenant du formulaire
    nom_ville = request.POST['ville']

    # on récupère les prévisions associées à la ville depuis la couche business
    meteo_ville_previsions = MeteoVillePrevisions(nom_ville)

    previsions_jour = meteo_ville_previsions.get_previsions_jour()
    previsions_force_vent = meteo_ville_previsions.get_previsions_force_vent()
    previsions_description = meteo_ville_previsions.get_previsions_description()

    # on construit une liste contenant des dictionnaires afin de pouvoir utiliser
    # les données dans le template
    #
    # /!\ la manipulation des éléments Python dans le template n'est pas du pure Python,
    #     c'est une syntaxe propre au langage de template de Django
    #
    #     ainsi, pour consulter dans la template une information de dictionnaire,
    #     on utilisera le "." pour définir la clé.
    #
    #     ce qui donne dans le code python
    #     ma_variable[ma_cle] = "valeur"
    #
    #     et dans le template, accédera à la valeur ainsi :
    #     {{ ma_variable.ma_cle }}

    previsions_affichage = []
    for jour in range(7):
        prevision_jour = {}
        prevision_jour["temperature"] = previsions_jour[jour]
        prevision_jour["force_vent"] = previsions_force_vent[jour]
        prevision_jour["description"] = previsions_description[jour]
        prevision_jour["jour"] = UIHelper.day_of_the_week_from_period(jour)
        prevision_jour["icon"] = "previsions/images/" + UIHelper.image_from_weather_status(previsions_description[jour])

        previsions_affichage.append(prevision_jour)

    context = {
        'ville': nom_ville,
        'previsions_affichage': previsions_affichage,
    }

    return render(request, 'previsions/display_previsions_ville.html', context)
