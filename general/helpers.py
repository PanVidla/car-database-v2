from flask import redirect, url_for, flash

from games.crazy_taxi.crazy_taxi.models.instance import InstanceCT
from general import cardb
from general.models.instance import Instance


def create_instance_based_on_game(game):

    if game.name_full == "Crazy Taxi":
        new_instance = InstanceCT()

    return new_instance


def get_game_specific_instance(instance):

    if instance.game.name_full == "Crazy Taxi":
        instance = InstanceCT.query.get(instance.id)
        return instance

    else:
        flash("There was and error returning a game-specific instance. Maybe the game isn't mapped?")
        return redirect("overview_instances")


def get_no_of_instances_in_game(game_id):

    instances = Instance.query\
        .filter(Instance.game_id == game_id,
                Instance.is_deleted != True)\
        .all()
    return len(instances)


def get_no_of_instances_of_car(car_id):

    instances = Instance.query\
        .filter(Instance.car_id == car_id,
                Instance.is_deleted != True)\
        .all()
    return len(instances)


def return_redirect_to_details_based_on_game(game, instance_id):

    if game.name_full == "Crazy Taxi":
        return redirect(url_for("crazy_taxi.crazy_taxi_1.detail_instance", id=instance_id))

    else:
        flash("There was an error redirecting to the detail of the instance. Maybe the detail method is not mapped?",
              "danger")
        return redirect(url_for("overview_instances"))
