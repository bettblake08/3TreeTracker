import os
from app import create_app

APP = create_app(os.getenv("APP_ENV"))

if __name__ == "__main__":
    APP.run(extra_files=[APP.config["WEBPACK_MANIFEST_PATH"]])
