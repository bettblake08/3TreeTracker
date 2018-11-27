from flask_sqlalchemy import sqlalchemy
from flask import current_app
from instance.config import APP_CONFIG
from app.database.factory import generate_test_data, generate_initial_data

import os

config = APP_CONFIG[os.getenv("APP_ENV")]

engine = sqlalchemy.create_engine(
    "postgresql://{}:{}@{}/".format(
        config.DB_USER,
        config.DB_PASSWORD,
        config.DB_HOST
    ))

def create_database(name):
    try:
        conn = engine.connect()
        conn.execute("COMMIT")

        conn.execute("CREATE DATABASE %s" % name)
        conn.close()

        print("Successfully created the {} database!".format(name))

    except:
        print("Failed to create the {} database!".format(name))


def create_test_database():
    create_database(APP_CONFIG["TEST"].DB_NAME)
    