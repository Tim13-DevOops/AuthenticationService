from setuptools import setup, find_packages

setup(
    name="authentication-app",
    version="0.1.0",
    description="Setting up a python package",
    author="Branislav Andjelic, Dusan Milunovic",
    author_email="branislav.andjelic@uns.ac.rs",
    packages=find_packages(),
    setup_requires=[
        "pytest-runner",
    ],
    tests_require=["pytest"],
    install_requires=[
        "flask-restful",
        "flask-cors",
        "flask-migrate",
        "psycopg2-binary",
        "flask-sqlalchemy",
        "flask-jwt-extended",
        "bcrypt",
        "requests-mock",
        "requests",
        "prometheus-flask-exporter",
        "flask",
    ],
    entry_points={
        "console_scripts": [
            "start_server=app.app:main",
            "flask_migrate=app.app:db_migrate",
        ]
    },
)
