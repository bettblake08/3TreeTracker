""" This module hosts the function responsible of generating test data """
from werkzeug.security import generate_password_hash

from app.database.models import (AdminUserModel, RepoFileModel,
                                 RepoFolderModel, TagModel, ProductModel, PostModel,
                                 ProductTagModel
                                 )


def generate_test_data():
    """ This function is the main function called to generate all test data"""

    generate_initial_data()

    steps = [
        "Generate Admin Data : {}",
        "Generate Repo Data : {}",
        "Generate Tag Data : {}",
        "Generate Product Data : {}"
    ]

    if generate_admin_user():
        print(steps[0].format("Success"))
    else:
        print(steps[0].format("Failed"))

    if generate_repo_data():
        print(steps[1].format("Success"))
    else:
        print(steps[1].format("Failed"))

    if generate_tag():
        print(steps[2].format("Success"))
    else:
        print(steps[2].format("Failed"))

    if generate_product():
        print(steps[3].format("Success"))
    else:
        print(steps[3].format("Failed"))


def generate_admin_user():
    """ This function handles the generation of admin user accounts """
    try:
        AdminUserModel(
            "johndoe2",
            generate_password_hash("johndoe@A2")
        ).save()
        return True

    except:
        return False


def generate_repo_data():
    """ This function handles the generation of repo data """
    try:
        RepoFolderModel("Test").save()

        RepoFileModel(
            "G67S5A",
            "test",
            "jpg",
            1,
            "11aa").save()
        return True

    except:
        return False


def generate_tag():
    """ This function handles the generation of tag test data """

    try:
        TagModel("Soap").save()
        return True

    except:
        return False


def generate_product():
    """ This function handles the generation of product test data """

    product = ProductModel(
        "This is a test product",
        "<p>This is a test product</p>",
        "This is a test product",
        1)

    try:
        product.save()

        post = PostModel(product.id, 1)
        post.save()

        new_tag = ProductTagModel(product.id, 1)
        new_tag.save()

        return True

    except:
        return False


def generate_initial_data():
    """ This function is the main function called to generate the inital data. """
    RepoFolderModel("root").save()
