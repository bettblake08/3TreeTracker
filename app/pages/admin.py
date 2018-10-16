from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required

ADMIN_PAGES = Blueprint("ADMIN_PAGES", __name__)


@ADMIN_PAGES.route('/admin/repo')
@jwt_required
def admin_repo_page():
    return render_template('admin/repo.html')


@ADMIN_PAGES.route('/admin/products')
@jwt_required
def products_page():
    return render_template('admin/products.html')


@ADMIN_PAGES.route('/admin/accounts')
@jwt_required
def accounts_page():
    return render_template('admin/accounts.html')


@ADMIN_PAGES.route("/admin/login")
def admin_login_page():
    return render_template('admin/login.html')
