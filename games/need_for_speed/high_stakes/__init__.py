from flask import Blueprint

blueprint = Blueprint("high_stakes", __name__, url_prefix="/high-stakes", template_folder='templates')

# from games.need_for_speed.high_stakes import routes
from games.need_for_speed.high_stakes.models import event, instance, record, track
