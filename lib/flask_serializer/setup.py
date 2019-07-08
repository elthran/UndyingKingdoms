"""
Flask-Serializer
-------------

This is the description for that library
"""
from setuptools import setup


setup(
    name='Flask-Serializer',
    version='1.0',
    url='http://example.com/flask-Serializer/',
    license='MIT',
    author='Marlen Brunner',
    author_email='marlenspam@gmail.com',
    description='Auto-import app.name/serializers/*_serializer.py for use with flask.jsonify',
    long_description=__doc__,
    py_modules=[
        'flask_serializer',
        'base_serializer',
        'encoder_factor',
        'commands',
    ],
    # if you would be using a package instead use packages instead
    # of py_modules:
    # packages=['flask_sqlite3'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points={
        'flask.commands': [
            'create=flask_serializer.commands:create_cli'
        ],
    },
)
