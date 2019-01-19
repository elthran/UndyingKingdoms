from setuptools import setup

setup(
    name='undyingkingdoms',
    version='0.0.02',
    packages=['undyingkingdoms'],
    include_package_data=True,
    install_requires=[
        'flask',
        'Flask-JSON',
        'flask-sqlalchemy',
        'mysqlclient',
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
        'pytest',
        'numpy',
        'pandas',
        'flask-sslify',
        'maxminddb',
        'sqlalchemy-utils',
        'PyJWT',
        'requests',
        'flask-script'
    ],
)

# Open your venv and run $ python setup.py install
__doc__ = '''
To run the game, enter your virtual environment and then
$ source venv/bin/activate
$ python manage.py runserver 
For more information try
$ python manage.py --help
'''