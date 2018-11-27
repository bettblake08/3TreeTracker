import os

from flask import current_app
from flask_sqlalchemy import sqlalchemy

from app.database.factory import generate_initial_data, generate_test_data
from instance.config import APP_CONFIG

CONFIG = APP_CONFIG[os.getenv("APP_ENV")]

ENGINE = sqlalchemy.create_engine(
    "postgresql://{}:{}@{}/".format(
        CONFIG.DB_USER,
        CONFIG.DB_PASSWORD,
        CONFIG.DB_HOST
    ))

def create_database(name):
    try:
        conn = ENGINE.connect()
        conn.execute("COMMIT")

        conn.execute("CREATE DATABASE %s" % name)
        conn.close()

        print("Successfully created the {} database!".format(name))

    except:
        print("Failed to create the {} database!".format(name))


def create_test_database():
    create_database(APP_CONFIG["TEST"].DB_NAME)
