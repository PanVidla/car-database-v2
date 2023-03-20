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

from games.need_for_speed import blueprint as need_for_speed_blueprint
from games.need_for_speed.iii_hot_pursuit import blueprint as need_for_speed_iii_hot_pursuit_blueprint
need_for_speed_blueprint.register_blueprint(need_for_speed_iii_hot_pursuit_blueprint)
cardb.register_blueprint(need_for_speed_blueprint)

from games.need_for_speed.iii_hot_pursuit.models import events, instance, records, tracks
