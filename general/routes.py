from flask import render_template

from general import cardb


@cardb.route("/", methods=['GET'])
@cardb.route("/mockup", methods=['GET'])
def overview_instances():

    return render_template("mockup_01.html")
