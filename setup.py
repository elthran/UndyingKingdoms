from setuptools import setup

setup(
    name='undyingkingdoms',
    version='0.1.00',
    packages=['app'],
    include_package_data=True,
    install_requires=[
        'Faker',
        'Flask-Mobility',
        'Flask-Script',
        'Pillow',
        'PyJWT',
        'SQLAlchemy-Utils',
        'factory_boy',
        'flask',
        'flask-cors',
        'flask-login',
        'flask-shell-ipython',
        'flask-sqlalchemy',
        'flask-sslify',
        'flask-wtf',
        'flask_mail',
        'fuzzywuzzy',
        'ipdb',
        'maxminddb',
        'mysqlclient',
        'numpy',
        'pandas',
        'pandas',
        'pattern',
        'pluralize',
        'pytest',
        'pytest-xdist',
        'python-Levenshtein',
        'requests',
        'requests',
        'roman',
        'sendgrid',
        'sqlalchemy',
        'watchdog',
        'werkzeug',
        'wtforms',
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
