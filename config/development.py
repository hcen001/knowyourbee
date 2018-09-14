import os

DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY') or 'not-the-droid-youre-looking-for'

POSTGRES = {
    'user': 'pr_test',
    'pw': 'test',
    'db': 'pr_test',
    'host': '131.94.128.214',
    'port': '5432',
}

SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO=False
