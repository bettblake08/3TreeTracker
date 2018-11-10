from flask_sqlalchemy import sqlalchemy
from flask import current_app
from instance.config import TestingConfig
from app.database.factory import generate_test_data, generate_initial_data

engine = sqlalchemy.create_engine(
    "postgresql://{}:{}@{}/".format(
        TestingConfig.DB_USER,
        TestingConfig.DB_PASSWORD,
        TestingConfig.DB_HOST
    ))


def create_test_database():

    try:
        conn = engine.connect()
        conn.execute("COMMIT")

        conn.execute("CREATE DATABASE %s" % TestingConfig.DB_NAME)
        conn.close()

        print("Successfully created test database!")

    except:
        print("Failed to created test database!")
