from flask import Blueprint

crazy_taxi_1 = Blueprint("crazy_taxi_1", __name__, url_prefix="/crazy-taxi", template_folder='templates')

from games.crazy_taxi.crazy_taxi import routes
from games.crazy_taxi.crazy_taxi.models import instance
