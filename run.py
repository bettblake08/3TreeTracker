import os

from app import create_app
from app.database import (create_test_database, generate_initial_data,
                          generate_test_data, create_database)
from app.database import DATABASE

APP = create_app(os.getenv("APP_ENV"))

@APP.cli.command("db:init:test")
def db_init_test():
    create_test_database()

    try:
        db.create_all()
        generate_test_data()

        print("Successfully initialized test database!")

    except:
        print("Failed to initialize test database!")


@APP.cli.command("db:create")
def db_create():
    try:
        create_database(APP.config.get("DB_NAME"))
        
        print("Successfully created the database!")

    except:
        print("Failed to create the database!")


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
        print("Successfully dropped all tables!")
    except:
        print("Failed to drop database tables!")

if __name__ == "__main__":
    APP.run(extra_files=[APP.config["WEBPACK_MANIFEST_PATH"]])
