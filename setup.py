from setuptools import setup

setup(
    name='undyingkingdoms',
    packages=['undyingkingdoms'],
    include_package_data=True,
    install_requires=[
        'flask',
        'Flask-JSON',
        'flask-sqlalchemy',
        'flask-wtf',
        'flask-login',
        'flask_mail',
        'sqlalchemy',
        'werkzeug',
        'wtforms',
        'Pillow',
        'pandas',
        'fuzzywuzzy',
        'python-Levenshtein',
        'pytest'
    ],
)

# Open your venv and run $ python setup.py install
