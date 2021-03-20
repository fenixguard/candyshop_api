from application import db


class CourierRegionAssoc(db.Model):
    __tablename__ = "courier_region_association"

    courier_id: int = db.Column(db.Integer, db.ForeignKey('couriers.courier_id'), primary_key=True)
    region_id: int = db.Column(db.Integer, primary_key=True)

    def __init__(self, region_id: int):
        self.region_id = region_id
