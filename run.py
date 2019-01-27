import os

from app import create_app
from app.database import (create_test_database, create_database)

from app.database.factory import generate_test_data, generate_initial_data, teardown_test_data
from app.database.db import DATABASE

APP = create_app(os.getenv("APP_ENV"))

@APP.cli.command("db:init:test")
def db_init_test():
    create_test_database()

    DATABASE.create_all()
    generate_test_data()

    try:
        
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
    APP.run()
