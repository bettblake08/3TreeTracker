""" This module hosts the function responsible of generating test data """
from app.database.models import RepoFolderModel
from app.database.factory import product, tag, repo_file, repo_folder, admin_user


def generate_test_data():
    """ This function is the main function called to generate all test data"""

    generate_initial_data()

    steps = [
        "Generate Admin Data : {}",
        "Generate Repo Data : {}",
        "Generate Tag Data : {}",
        "Generate Product Data : {}"
    ]

    if admin_user.generate_admin_user():
        print(steps[0].format("Success"))
    else:
        print(steps[0].format("Failed"))

    if generate_repo_data():
        print(steps[1].format("Success"))
    else:
        print(steps[1].format("Failed"))

    if tag.generate_tag():
        print(steps[2].format("Success"))
    else:
        print(steps[2].format("Failed"))

    if product.generate_product():
        print(steps[3].format("Success"))
    else:
        print(steps[3].format("Failed"))


def generate_repo_data():
    """ This function handles the generation of repo data """
    repo_folder.generate_repo_folders()
    repo_file.generate_repo_file()

    return True

def generate_initial_data():
    """ This function is the main function called to generate the inital data. """
    RepoFolderModel("root").save()


def teardown_test_data():
    repo_file.teardown_repo_file()
