from flask import redirect, url_for, flash

from games.crazy_taxi.crazy_taxi.models.instance import InstanceCT
from games.need_for_speed.iii_hot_pursuit.models.instance import InstanceNFS3
# from general import cardb
from general.models.instance import Instance


def create_instance_based_on_game(game):

    if game.name_full == "Crazy Taxi":
        new_instance = InstanceCT()

    if game.name_full == "Need for Speed III: Hot Pursuit":
        new_instance = InstanceNFS3(acceleration=0,
                                    top_speed=0,
                                    handling=0,
                                    braking=0,
                                    average=0)

    return new_instance


def get_game_specific_instance(instance):

    if instance.game.name_full == "Crazy Taxi":
        instance = InstanceCT.query.get(instance.id)
        return instance

    if instance.game.name_full == "Need for Speed III: Hot Pursuit":
        instance = InstanceNFS3.query.get(instance.id)
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

    if game.name_full == "Need for Speed III: Hot Pursuit":
        return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=instance_id))

    else:
        flash("There was an error redirecting to the detail of the instance. Maybe the detail method is not mapped?",
              "danger")
        return redirect(url_for("overview_instances"))
