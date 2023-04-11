import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    # Secret key
    SECRET_KEY = os.environ.get("SECRET_KEY") or "pan-vidlas-secret-key"

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
                              'sqlite:///' + os.path.join(basedir, 'cars.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
