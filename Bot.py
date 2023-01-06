from Water import Water
from Coordinates import Coordinates


class Bot:
    pass


def x():
    city = 'Оренбург'
    coordinates = Coordinates()
    water = Water()
    geo_tag = coordinates.check_coordinates(city)
    msg = water.check_weather(geo_tag)
    return msg
