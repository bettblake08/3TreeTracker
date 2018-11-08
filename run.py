import os

from app import create_app
from app.database import (create_test_database, generate_initial_data,
                          generate_test_data)

from db import db

APP = create_app(os.getenv("APP_ENV"))

@APP.cli.command("db:init:test")
def db_init_test():
    try:
        create_test_database()
        db.create_all()
        generate_test_data()

        print("Successfully initialized test database!")

    except:
        print("Failed to initialize test database!")  

@APP.cli.command("db:init")
def db_init():
    try:
        db.create_all()
        generate_initial_data()

        print("Successfully initialized database!")

    except:
        print("Failed to create database!")


@APP.cli.command("db:teardown")
def db_teardown():
    try:
        db.drop_all()

    except:
        print("Failed to drop database tables!")

if __name__ == "__main__":
    APP.run(extra_files=[APP.config["WEBPACK_MANIFEST_PATH"]])
