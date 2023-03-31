from games.crazy_taxi.crazy_taxi.models.instance import InstanceCT


def create_instance_based_on_game(game):

    if game.name_full == "Crazy Taxi":
        new_instance = InstanceCT()

    return new_instance
