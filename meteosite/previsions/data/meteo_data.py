from datetime import date
import psycopg2


class MeteoData:

    # ------------------------------
    # constructeur
    # ------------------------------
    def __init__(self):

        # constantes pour les connexions à la base de données
        self._host = "localhost"
        self._database = "application_meteo_db"
        self._user = "dev"
        self._password = "starfou-Michel87"
        self._port = 5432

    def connect(self):
        """
        Fonction qui permet de valider la connexion à la base de données
        """
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._host, database=self._database, user=self._user, password=self._password, port=self._port)

            # obtentention d'un curseur, c'est à dire l'objet qui va recueillir les lignes en réponse des requêtes envoyées
            # au serveur de base de données
            cursor = connection.cursor()

            # exécution de la requête
            print('Version du serveur PostgreSQL:')
            cursor.execute('SELECT version()')

            # récupération des valeurs + affichage
            db_version = cursor.fetchone()
            print(db_version)


        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()
                print('Connection à la base de données fermée.')

    def ajout_prevision_ville(self, id_ville,
                              temperature,
                              temperature_min,
                              temparature_max,
                              temperature_matin,
                              temperature_apres_midi,
                              temperature_nuit,
                              description,
                              direction_vent,
                              force_vent,
                              jour):
        """
        Fonction qui permet d'ajouter un enregistrement dans la table prévision
        :param id_ville: (nom du champ se suffit à la même)
        :param temperature: (nom du champ se suffit à la même)
        :param temperature_min: (nom du champ se suffit à la même)
        :param temparature_max: (nom du champ se suffit à la même)
        :param temperature_matin: (nom du champ se suffit à la même)
        :param temperature_apres_midi: (nom du champ se suffit à la même)
        :param temperature_nuit: (nom du champ se suffit à la même)
        :param description: indication retournée par Open Weather Map, c'est un description courte de la météo (nuageaux, etc.)
        :param direction_vent: (nom du champ se suffit à la même)
        :param force_vent: (nom du champ se suffit à la même)
        :param jour: (nom du champ se suffit à la même)
        """

        sql = """ INSERT INTO prevision (id_ville, temperature, temperature_min, temperature_max, temperature_matin, temperature_apres_midi, temperature_nuit, description, direction_vent, force_vent, jour, last_update) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._host, database=self._database, user=self._user, password=self._password, port=self._port)
            # create a new cursor
            cursor = connection.cursor()
            record_to_insert = (id_ville, round(temperature, 2), round(temperature_min, 2), round(temparature_max, 2),
                                round(temperature_matin, 2), round(temperature_apres_midi, 2), round(temperature_nuit, 2), description, direction_vent,
                                round(force_vent, 2), jour, date.today())
            cursor.execute(sql, record_to_insert)

            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur ajout_prevision_ville:")
            print(sql)
            print(record_to_insert)
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def ville_exists(self, nom_ville):
        """
        Nous indique si la ville existe en base de données en fonction de son nom
        :param nom_ville: nom de la ville
        :return: True ou False
        """
        sql = "SELECT id_ville FROM VILLE where nom='{0}';".format(nom_ville)

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._host, database=self._database, user=self._user, password=self._password, port=self._port)
            # create a new cursor
            cursor = connection.cursor()

            cursor.execute(sql, nom_ville)
            row = cursor.fetchone()

            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

            if row is not None:
                return True
            return False


        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur ville_exists:")
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def get_id_ville(self, nom_ville):
        """
        retourne l'id de la ville en fonction de son nom
        :param nom_ville: nom de la ville
        :return: id de la ville
        """
        sql = "SELECT id_ville FROM VILLE where nom='{0}';".format(nom_ville)

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._host, database=self._database, user=self._user, password=self._password, port=self._port)
            # create a new cursor
            cursor = connection.cursor()

            cursor.execute(sql, nom_ville)
            row = cursor.fetchone()

            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

            return row[0]

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur get_id_ville:")
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def get_last_update(self, nom_ville):
        """
        Recherche la date de mise à jour des informations de la ville
        :param nom_ville:
        :return: renvoie la date si trouvée, sinon renvoie None
        """

        sql = f"select prevision.last_update from prevision inner join ville on prevision.id_ville = ville.id_ville where ville.nom = '{nom_ville}' limit 1;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._host, database=self._database, user=self._user, password=self._password, port=self._port)
            # create a new cursor
            cursor = connection.cursor()

            cursor.execute(sql, nom_ville)
            row = cursor.fetchone()

            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

            if row is None:
                return None
            return row[0]

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur get_last_update:")
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def read_meteo_ville(self, nom_ville):
        """
        Lecteure des données météo d'une ville en rapprochant les données de la table prevsion avec celles de la table ville, uniquement sur les colonnes utiles
        concernant les information météo de la ville
        :param nom_ville:
        :return: un objet row contenant les valeurs sélectionnées
        """

        sql = f"select prevision.temperature, prevision.temperature_min, prevision.temperature_max, prevision.temperature_matin, prevision.temperature_apres_midi, prevision.temperature_nuit, prevision.description, prevision.direction_vent, prevision.force_vent, prevision.jour from prevision inner join ville on prevision.id_ville = ville.id_ville where ville.nom = '{nom_ville}' order by prevision.jour;"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._host, database=self._database, user=self._user, password=self._password, port=self._port)
            # create a new cursor
            cursor = connection.cursor()

            cursor.execute(sql, nom_ville)
            row = cursor.fetchall()

            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

            return row

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur read_meteo_ville:")
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def delete_prevision_ville(self, nom_ville):
        """
        Supprime les prévisions météo pour une ville
        :param nom_ville: nom de la ville
        :return:
        """
        sql = f"DELETE FROM prevision WHERE id_ville in (select id_ville from ville where nom = '{nom_ville}');"

        connection = None
        try:
            # obtention de la connexion à la base de données
            connection = psycopg2.connect(host=self._host, database=self._database, user=self._user, password=self._password, port=self._port)
            # create a new cursor
            cursor = connection.cursor()

            cursor.execute(sql, nom_ville)

            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur delete_prevision_ville:")
            print(error)
        finally:
            if connection is not None:
                connection.close()
