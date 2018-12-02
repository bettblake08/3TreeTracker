""" This module hosts all the tests for the admin api endpoints """
from app.tests.v1.admin.delete_admin_user_endpoint import \
    TestDeleteAdminUserEndpoint
from app.tests.v1.admin.post_new_admin_user_endpoint import \
    TestPostNewAdminUserEndpoint
from app.tests.v1.admin.post_new_product_endpoint import \
    TestPostNewProductEndpoint
from app.tests.v1.admin.retrieve_repo_content_by_folder_endpoint import \
    TestRetrieveRepoContentByFolderEndpoint
from app.tests.v1.admin.soft_delete_repo_file_endpoint import \
    TestSoftDeleteRepoFileEndpoint
from app.tests.v1.admin.update_product_endpoint import \
    TestUpdateProductEndpoint
from app.tests.v1.admin.hard_delete_repo_file_endpoint import TestHardDeleteRepoFileEndpoint
