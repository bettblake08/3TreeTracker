import os

from app import create_app
from app.database import (create_test_database, generate_initial_data,
                          generate_test_data, create_database)
from app.database.db import DATABASE

APP = create_app(os.getenv("APP_ENV"))

@APP.cli.command("db:init:test")
def db_init_test():
    create_test_database()

    try:
        DATABASE.create_all()
        generate_test_data()

        print("Successfully initialized test database!")

    except:
        print("Failed to initialize test database!")


@APP.cli.command("db:create")
def db_create():
    create_database(APP.config.get("DB_NAME"))
        

@APP.cli.command("db:init")
def db_init():

    DATABASE.create_all()
    generate_initial_data() 
    
    try:

        print("Successfully initialized database!")

    except:
        print("Failed to initialize database!")


@APP.cli.command("db:teardown")
def db_teardown():
    try:
        DATABASE.drop_all()
        print("Successfully dropped all tables!")
        
    except:
        print("Failed to drop database tables!")

if __name__ == "__main__":
    APP.run(extra_files=[APP.config["WEBPACK_MANIFEST_PATH"]])
