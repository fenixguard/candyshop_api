from http import HTTPStatus
from datetime import datetime, timedelta
from dateutil.parser import parse
from typing import List

from flask import make_response, jsonify
from flask_restplus import Resource

from application import db
from application.model.courier_type import CourierCoef, CourierType
from application.model.couriers import Couriers
from application.model.delivery_time import DeliveryTime
from application.model.orders import Orders
from application.persistence.couriers_repo import CouriersRepo
from application.persistence.orders_repo import OrdersRepo
from . import apii
from .parsers import orders_parser, orders_assign_parser, orders_complete_parser

ord_ns = apii.namespace("orders", description="Orders operations")


@ord_ns.route('')
class OrdersRoute(Resource):
    def post(self):
        args = orders_parser.parse_args()
        orders_list: List[dict] = args["data"]
        invalid_orders = list()
        valid_orders = list()
        for order in orders_list:
            order_id = order.get("order_id")
            weight = order.get("weight")
            region = order.get("region")
            delivery_hours = order.get("delivery_hours")
            exist_order = OrdersRepo.get_by_id(order_id)
            if ((exist_order is not None) or (weight is None or (weight > 50 or weight < 0.01)) or (region is None) or
                    (delivery_hours is None or len(delivery_hours) == 0) or len(order) != 4):
                invalid_orders.append({"id": order_id})
            else:
                valid_orders.append({"id": order_id})

                order_delivery = [DeliveryTime(delivery) for delivery in delivery_hours]
                order_entry = Orders(order_id=order_id, weight=weight, region=region,
                                     delivery_hours=order_delivery)
                db.session.add(order_entry)
            db.session.commit()

        if len(invalid_orders):
            return make_response(jsonify({"validation_error":
                        {
                            "orders": invalid_orders
                        }
                   }), HTTPStatus.BAD_REQUEST)

        return make_response(jsonify({"orders": valid_orders}), HTTPStatus.CREATED)


@ord_ns.route('/assign')
class OrderAssignRoute(Resource):
    def post(self):
        args = orders_assign_parser.parse_args()
        courier_id: int = args.get('courier_id')
        courier_entry: Couriers = CouriersRepo.get_by_id(courier_id)
        if courier_entry is None:
            return make_response('', HTTPStatus.BAD_REQUEST)

        all_orders = OrdersRepo.get_orders_for_assign(courier_entry)
        orders_for_assign = list()
        courier_weight = courier_entry.courier_type
        for order in all_orders:
            if order[2] > 0:
                courier_weight -= order[1]
            elif courier_weight >= order[1]:
                courier_weight -= order[1]
                orders_for_assign.append(order[0])
        if orders_for_assign:
            assign_time_for_db = int((datetime.utcnow() + timedelta(hours=3)).timestamp())
            assign_time_for_resp = datetime.isoformat(datetime.fromtimestamp(assign_time_for_db))
            courier_coef = CourierCoef[CourierType(courier_entry.courier_type).name].value
            OrdersRepo.assign_orders(courier_id, assign_time_for_db, courier_coef, orders_for_assign)
            orders_ids = list(map(lambda x: {'id': x.order_id}, OrdersRepo.get_assigned_orders(courier_id)))

            return make_response(jsonify({"orders": orders_ids, "assign_time": assign_time_for_resp}), HTTPStatus.OK)

        return make_response(jsonify({"orders": []}), HTTPStatus.OK)


@ord_ns.route('/complete')
class OrderCompleteRoute(Resource):
    def post(self):
        args = orders_complete_parser.parse_args()
        courier_id: int = args.get('courier_id')
        order_id: int = args.get('order_id')
        complete_time: str = args.get('complete_time')
        if order_id is None or complete_time is None:
            return make_response('', HTTPStatus.BAD_REQUEST)

        order_entry = OrdersRepo.get_by_courier_order_ids(courier_id, order_id)
        if order_entry is None:
            return make_response('', HTTPStatus.BAD_REQUEST)

        if order_entry.complete == 0:
            order_entry.complete = int(parse(complete_time).timestamp())
            db.session.commit()

        return make_response(jsonify({"order_id": order_id}), HTTPStatus.OK)
