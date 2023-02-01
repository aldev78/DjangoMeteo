# Generated by Django 4.1 on 2022-11-17 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departement',
            fields=[
                ('id_departement', models.SmallAutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(blank=True, max_length=50, null=True)),
                ('code', models.CharField(max_length=3)),
            ],
            options={
                'db_table': 'departement',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Ville',
            fields=[
                ('id_ville', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(blank=True, max_length=60, null=True)),
                ('code_postal', models.IntegerField()),
                ('id_departement', models.ForeignKey(db_column='id_departement', on_delete=django.db.models.deletion.DO_NOTHING, to='previsions.departement')),
            ],
            options={
                'db_table': 'ville',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Prevision',
            fields=[
                ('id_prevision', models.AutoField(primary_key=True, serialize=False)),
                ('temperature', models.DecimalField(decimal_places=2, max_digits=5)),
                ('temperature_min', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('temperature_max', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('temperature_matin', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('temperature_apres_midi', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('temperature_nuit', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('presion', models.IntegerField(blank=True, null=True)),
                ('humidite', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(max_length=30)),
                ('direction_vent', models.SmallIntegerField(blank=True, null=True)),
                ('force_vent', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('jour', models.DateField()),
                ('last_update', models.DateField()),
                ('id_ville', models.ForeignKey(db_column='id_ville', on_delete=django.db.models.deletion.DO_NOTHING, to='previsions.ville')),
            ],
            options={
                'db_table': 'prevision',
                'managed': True,
            },
        ),
    ]
