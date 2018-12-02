from werkzeug.security import generate_password_hash

from app.database.models import AdminUserModel


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
