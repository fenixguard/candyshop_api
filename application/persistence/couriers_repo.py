import sqlalchemy as sa
from application import db
from application.model.couriers import Couriers


class CouriersRepo:

    @staticmethod
    def get_by_id(courier_id: int):
        return Couriers.query.get(courier_id)

    @staticmethod
    def get_assign_complete_times(courier_id: int) -> dict:
        query = sa.text("SELECT region, assign, complete "
                        "FROM orders "
                        "WHERE courier_id = :courier_id AND complete != 0 "
                        "ORDER BY region, complete;")

        values = {'courier_id': courier_id}

        result = db.engine.execute(query, values).fetchall()
        assign_complete_times = dict()
        for region, assign, complete in result:
            if not assign_complete_times.get(region):
                assign_complete_times[region] = [[assign, complete]]
            else:
                assign_complete_times[region].append([assign, complete])

        return assign_complete_times

    @staticmethod
    def get_courier_coefficients_for_deliver(courier_id: int) -> list:
        query = sa.text("SELECT assign, courier_coef "
                        "FROM orders "
                        "WHERE courier_id = :courier_id "
                        "AND complete != 0 "
                        "GROUP BY assign, courier_coef;")

        values = {'courier_id': courier_id}

        return list(map(lambda x: (x[0], x[1]), db.engine.execute(query, values).fetchall()))
