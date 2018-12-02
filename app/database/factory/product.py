from app.database.models import ProductModel, PostModel, ProductTagModel, RepoFileModel

def generate_product():
    """ This function handles the generation of product test data """
    products = [
        {
            "name": "This is a test product",
            "description": "<p>This is a test product</p>",
            "summary": "This is a test product",
            "image": 1,
            "tags": [1]
        }
    ]

    try:
        for p in products:
            product = ProductModel(
                p['name'],
                p['description'],
                p['summary'],
                p['image'])

            product.save()

            post = PostModel(product.id, 1)
            post.save()

            for tag in p['tags']:
                new_tag = ProductTagModel(product.id, tag)
                new_tag.save()

            repo_file = RepoFileModel.find_by_id(products[0]['image'])
            repo_file.increase_users()

        return True

    except:
        return False
