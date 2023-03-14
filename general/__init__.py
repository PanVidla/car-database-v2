from flask import Flask
from flask_bootstrap import Bootstrap

cardb = Flask(__name__, static_folder="./static")

bootstrap = Bootstrap(cardb)

from general import routes
