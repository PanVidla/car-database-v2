from flask import Blueprint

blueprint = Blueprint("iii_hot_pursuit", __name__, url_prefix="/iii-hot-pursuit")

from games.need_for_speed.iii_hot_pursuit import routes
from games.need_for_speed.iii_hot_pursuit.models import events, instance, records, tracks
