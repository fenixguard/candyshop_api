from typing import List

from application import db
from application.model.delivery_time import DeliveryTime


class Orders(db.Model):
    __tablename__ = "orders"

    order_id: int = db.Column(db.Integer, primary_key=True)
    weight: float = db.Column(db.Float)
    region: int = db.Column(db.Integer)
    delivery_hours: List[DeliveryTime] = db.relationship("DeliveryTime", cascade="all,delete-orphan")
    assign: int = db.Column(db.Integer, default=0, nullable=True)
    complete: int = db.Column(db.Integer, default=0, nullable=True)
    courier_id: int = db.Column(db.Integer, db.ForeignKey('couriers.courier_id'), default=None)
    courier_coef: int = db.Column(db.Integer, default=None)

    def __init__(self, order_id: int, weight: float, region: int, delivery_hours: list, assign: int = 0, complete: int = 0):
        self.order_id = order_id
        self.weight = weight
        self.region = region
        self.delivery_hours = delivery_hours
        self.assign = assign
        self.complete = complete
