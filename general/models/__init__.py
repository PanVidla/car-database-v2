from flask import Blueprint

blueprint = Blueprint("models", __name__)

from general.models import car, event, game, info, instance, misc, part
