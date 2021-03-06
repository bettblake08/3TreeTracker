from setuptools import setup, find_packages


__version__ = "0.0.1"


setup(
    name="Longrich",
    version=__version__,
    description="A longrich advertising portal",
    author="Brian K. Bett",
    author_email="bettblake08@hotmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask>=1.0.2",
        "Flask-JWT-Extended>=3.12.1",
        "Flask-RESTful>=0.3.6",
        "Flask-SQLAlchemy>=2.3.2",
        "psycopg2",
        "Pillow>=5.2.0",
        "pymysql",
        "pytest",
        "coveralls",
        "pytest-cov"
    ]
)
