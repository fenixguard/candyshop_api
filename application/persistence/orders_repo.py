from typing import List, Optional, NoReturn

import sqlalchemy as sa

from application import db
from application.model.couriers import Couriers
from application.model.orders import Orders


class OrdersRepo:

    @staticmethod
    def get_orders_for_assign(courier: Couriers) -> List[tuple]:
        query = sa.text("SELECT DISTINCT orders.order_id, orders.weight, orders.assign FROM orders "
                        "INNER JOIN delivery_time dt on orders.order_id = dt.order_id "
                        "JOIN working_time wt on wt.courier_id = :courier_id AND dt.from_hours <= wt.to_hours AND dt.to_hours >= wt.from_hours "
                        "WHERE (region IN (SELECT region_id FROM courier_region_association WHERE courier_id = :courier_id)) "
                        "AND weight <= :weight AND (orders.courier_id IS NULL OR orders.courier_id = :courier_id) AND orders.complete = 0 "
                        "ORDER BY orders.assign DESC, orders.weight DESC;")
        values = {'courier_id': courier.courier_id, 'weight': courier.courier_type}

        result = db.engine.execute(query, values).fetchall()

        return list(map(lambda order: (order[0], order[1], order[2]), result))

    @staticmethod
    def get_by_id(order_id: int) -> Optional[Orders]:
        return Orders.query.get(order_id)

    @staticmethod
    def get_by_courier_id(courier_id: int) -> List[Orders]:
        return Orders.query.filter(Orders.courier_id == courier_id, Orders.complete == 0).all()

    @staticmethod
    def get_by_courier_order_ids(courier_id: int, order_id: int) -> Optional[Orders]:
        return Orders.query.filter(Orders.order_id == order_id, Orders.courier_id == courier_id).first()

    @staticmethod
    def assign_orders(courier_id: int, assign_time: int, courier_coef: int, orders_ids: list) -> NoReturn:
        query = sa.text("UPDATE orders "
                        "SET assign = :assign, courier_id = :courier_id, courier_coef = :courier_coef "
                        "WHERE order_id IN :orders_ids AND courier_id IS NULL;")
        values = {'courier_id': courier_id, 'assign': assign_time, "courier_coef": courier_coef,
                  'orders_ids': tuple(orders_ids)}

        db.engine.execute(query, values)

    @staticmethod
    def get_assigned_orders(courier_id: int):
        return Orders.query.filter(Orders.courier_id == courier_id, Orders.complete == 0).all()

    @staticmethod
    def count_completed_orders(courier_id: int):
        return Orders.query.filter(Orders.courier_id == courier_id, Orders.complete != 0).count()
