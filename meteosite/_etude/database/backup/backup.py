# Track Manager by Luc ANDRIANIAZY
# This module does a backup of the database

import os
from datetime import datetime

if __name__ == '__main__':
    now = datetime.now()
    now_string = now.strftime("%Y-%m-%d_%H_%M_%S")
    print("Backup date / time:", now_string)

    SERVER = "127.0.0.1"
    PORT = 5432
    USER = "dev"
    PASSWORD = "starfou-Michel87"
    DATABASE = "django_meteo_db"
    POSTGRESQL_BIN = "C:\\Program Files\\PostgreSQL\\13\\bin\\"
    SAVEPATH = "C:\\Users\\Luc\\Documents\\DEV\\PROJETS\\PERSO\\DjangoMeteo\\meteosite\\_etude\\database\\backup\\"

    # move into the postgres bin diretory
    os.chdir(POSTGRESQL_BIN)

    # set the password for current session (on Windows, password cannot be sent with command line)
    os.environ["PGPASSWORD"] = PASSWORD

    print("Current working directory : " + os.getcwd())

    # backup of the database with pg_dump
    command = f"pg_dump -h {SERVER} -p {PORT} -U {USER} {DATABASE} > {SAVEPATH}db_save_{now_string}.txt "
    print(command)
    os.system(command)

    print(f"{DATABASE} saved !")







