# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Departement(models.Model):
    id_departement = models.SmallAutoField(primary_key=True)
    nom = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'departement'


class Prevision(models.Model):
    id_prevision = models.AutoField(primary_key=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    temperature_min = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    temperature_max = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    temperature_matin = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    temperature_apres_midi = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    temperature_nuit = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    presion = models.IntegerField(blank=True, null=True)
    humidite = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=30)
    direction_vent = models.SmallIntegerField(blank=True, null=True)
    force_vent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    jour = models.DateField()
    last_update = models.DateField()
    id_ville = models.ForeignKey('Ville', models.DO_NOTHING, db_column='id_ville')

    class Meta:
        managed = False
        db_table = 'prevision'


class Ville(models.Model):
    id_ville = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=60, blank=True, null=True)
    id_departement = models.ForeignKey(Departement, models.DO_NOTHING, db_column='id_departement')
    code_postal = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ville'
