from app.database.models import RepoFolderModel

def generate_repo_folders():
    """ This function handles the generation of repo folders """
    try:
        RepoFolderModel("Test").save()
        RepoFolderModel("Main").save()
        RepoFolderModel("Upload").save()
        return True

    except:
        return False
