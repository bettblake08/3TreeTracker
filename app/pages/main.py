""" This modules hosts the main pages blueprint. """

from os import path
from flask import Blueprint, render_template, send_from_directory
from instance.config import Config

MAIN_PAGES = Blueprint("MAIN_PAGES", __name__)

HERE = path.abspath("./")

@MAIN_PAGES.route("/")
def index():
    return render_template("main/home.html")


@MAIN_PAGES.route('/product/<string:param>')
def product_page(param):
    return render_template('main/Product.html', ProductId=param)


@MAIN_PAGES.route("/assets/<path:filename>")
def send_asset(filename):
    return send_from_directory(path.join(HERE, "public/assets"), filename)


@MAIN_PAGES.route("/repo/<path:filename>")
def send_repo_files(filename):
    return send_from_directory(path.join(HERE, Config.REPO_DIR + "/upload"), filename)
