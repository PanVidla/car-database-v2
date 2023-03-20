from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

cardb = Flask(__name__, static_folder="./static")
cardb.config.from_object(Config)

bootstrap = Bootstrap(cardb)
database = SQLAlchemy(cardb)
migrate = Migrate(cardb, database)

from general.models import blueprint as models_general_blueprint
cardb.register_blueprint(models_general_blueprint)

from general import routes
