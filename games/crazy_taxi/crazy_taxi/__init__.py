from flask import Blueprint

blueprint = Blueprint("crazy_taxi_1", __name__, url_prefix="/crazy-taxi")

from games.crazy_taxi.crazy_taxi import routes
from games.crazy_taxi.crazy_taxi.models import instance
