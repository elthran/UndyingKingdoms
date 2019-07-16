from setuptools import setup

setup(
    name='undyingkingdoms',
    version='0.1.00',
    packages=['app'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-shell-ipython',
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
        'SQLAlchemy-Utils',
        'PyJWT',
        'pytest-xdist',
        'requests',
        'Flask-Script',
        'Flask-Mobility',
        'flask-cors',
        'sendgrid',
        'requests',
        'Faker',
        'factory_boy',
        'roman',
        'ipdb',
        'flask-shell-ipython'
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
