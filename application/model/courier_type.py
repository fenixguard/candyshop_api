from enum import Enum


class CourierType(Enum):
    foot = 10
    bike = 15
    car = 50


class CourierCoef(Enum):
    foot = 2
    bike = 5
    car = 9
