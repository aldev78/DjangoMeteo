from django.contrib import admin
from .models import Ville
from .models import Departement


@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
    fields = ('nom', 'code_postal', 'id_departement')


@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    fields = ('nom', 'code')
