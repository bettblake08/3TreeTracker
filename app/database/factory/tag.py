from app.database.models import TagModel

def generate_tag():
    """ This function handles the generation of tag test data """
    try:
        TagModel("Soap").save()
        return True

    except:
        return False
