from setuptools import setup

setup(
    name='undyingkingdoms',
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
    ],
)

# Open your venv and run $ python setup.py install

'''
db.metadata.create_all(db.engine, tables=[
	Users.__table__,
	Counties.__table__
])
'''
