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

from general import routes_cars, routes_companies, routes_games, routes_instances, routes_misc, routes_parts

# Crazy Taxi
from games.crazy_taxi import blueprint as crazy_taxi_blueprint
# Crazy Taxi 1
from games.crazy_taxi.crazy_taxi import blueprint as crazy_taxi_1_blueprint

crazy_taxi_blueprint.register_blueprint(crazy_taxi_1_blueprint)
cardb.register_blueprint(crazy_taxi_blueprint)

# Need for Speed
from games.need_for_speed import blueprint as need_for_speed_blueprint
# Need for Speed III: Hot Pursuit
from games.need_for_speed.iii_hot_pursuit import blueprint as need_for_speed_iii_hot_pursuit_blueprint
need_for_speed_blueprint.register_blueprint(need_for_speed_iii_hot_pursuit_blueprint)
cardb.register_blueprint(need_for_speed_blueprint)
