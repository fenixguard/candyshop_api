from typing import List

from application import db
from application.model.orders import Orders
from application.model.courier_region_association import CourierRegionAssoc
from application.model.working_time import WorkingTime


class Couriers(db.Model):
    __tablename__ = "couriers"

    courier_id: int = db.Column(db.Integer, primary_key=True)
    courier_type: int = db.Column(db.Integer)
    regions: List[CourierRegionAssoc] = db.relationship("CourierRegionAssoc", cascade="all,delete-orphan")
    working_hours: List[WorkingTime] = db.relationship("WorkingTime", cascade="all,delete-orphan")
    courier_orders: List[Orders] = db.relationship("Orders", cascade="all,delete-orphan")

    def __init__(self, courier_id: int, courier_type: int, regions: list, working_hours: list):
        self.courier_id = courier_id
        self.courier_type = courier_type
        self.regions = regions
        self.working_hours = working_hours
