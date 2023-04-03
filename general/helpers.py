from flask import redirect, url_for, flash

from games.crazy_taxi.crazy_taxi.models.instance import InstanceCT


def create_instance_based_on_game(game):

    if game.name_full == "Crazy Taxi":
        new_instance = InstanceCT()

    return new_instance


def return_redirect_to_details_based_on_game(game, instance_id):

    if game.name_full == "Crazy Taxi":
        return redirect(url_for("crazy_taxi.crazy_taxi_1.detail_instance", id=instance_id))

    else:
        flash("There was an error redirecting to the detail of the instance. Maybe the detail method is not mapped?",
              "danger")
        return redirect(url_for("overview_instances"))
