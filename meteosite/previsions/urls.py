from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'previsions'
urlpatterns = [
    path('', views.index, name='index'),
    path('departements/', views.departements, name='departements'),
    path('select_departement/', views.select_departement, name='select_departement'),
    path('display_villes/', views.display_villes, name='display_villes'),
    path('add_ville/', views.add_ville, name='add_ville'),
    path('login/', LoginView.as_view(next_page='/previsions/'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/previsions/login'), name='logout'),
    path('favoris/', views.favoris, name='favoris'),
    path('departement_client/', views.departement_client, name='departement_client'),
    path('display_previsions_ville/', views.display_previsions_ville, name='display_previsions_ville'),
]

