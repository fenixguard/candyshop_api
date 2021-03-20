from http import HTTPStatus
from typing import List

from flask import make_response, jsonify
from flask_restplus import Resource

from application import db
from application.apis.utils import get_min_avg_time
from application.model.courier_region_association import CourierRegionAssoc
from application.model.courier_type import CourierType
from application.model.couriers import Couriers
from application.model.orders import Orders
from application.model.time_interval import prepare_time_to_view, prepare_time_to_db
from application.model.working_time import WorkingTime
from application.persistence.couriers_repo import CouriersRepo
from application.persistence.orders_repo import OrdersRepo
from . import apii
from .parsers import couriers_parser, couriers_patch_parser

cour_ns = apii.namespace("couriers", description="Couriers operations")


@cour_ns.route('')
class CouriersPostRoute(Resource):
    def post(self):
        args = couriers_parser.parse_args()
        couriers_list: List[dict] = args["data"]
        invalid_couriers = list()
        valid_couriers = list()
        for courier in couriers_list:
            courier_id = courier.get("courier_id")
            courier_type = courier.get("courier_type")
            regions = courier.get("regions")
            working_hours = courier.get("working_hours")
            if ((courier_type is None or len(courier_type) == 0) or (regions is None or len(regions) == 0) or (
                    working_hours is None or len(working_hours) == 0) or len(courier) != 4):
                invalid_couriers.append({"id": courier_id})
            else:
                valid_couriers.append({"id": courier_id})
                courier_type = CourierType[courier_type].value

                courier_regions = [CourierRegionAssoc(region) for region in regions]
                courier_working = [WorkingTime(work) for work in working_hours]

                courier_entry = Couriers(courier_id, courier_type, courier_regions, courier_working)
                db.session.add(courier_entry)
            db.session.commit()

        if len(invalid_couriers):
            return make_response(jsonify({"validation_error":
                {
                    "couriers": invalid_couriers
                }
            }), HTTPStatus.BAD_REQUEST)

        return make_response(jsonify({"couriers": valid_couriers}), HTTPStatus.CREATED)


@cour_ns.route('/<int:courier_id>')
class CouriersActionRoute(Resource):
    def get(self, courier_id: int):
        courier_entry = CouriersRepo.get_by_id(courier_id)
        if courier_entry is None:
            return make_response('', HTTPStatus.BAD_REQUEST)

        regions = [reg.region_id for reg in courier_entry.regions]
        working_hours = list()
        for work in courier_entry.working_hours:
            working_hours.append(prepare_time_to_view([work.from_hours, work.to_hours]))

        if OrdersRepo.count_completed_orders(courier_id) == 0:
            return make_response(jsonify({"courier_id": courier_id,
                                          "courier_type": CourierType(courier_entry.courier_type).name,
                                          "regions": regions,
                                          "working_hours": working_hours}), HTTPStatus.OK)

        assign_complete_times = CouriersRepo.get_assign_complete_times(courier_id)
        min_avg_time = get_min_avg_time(assign_complete_times)
        rating = round((60 * 60 - min(min_avg_time, 60 * 60)) / (60 * 60) * 5, 2)
        coefficients = CouriersRepo.get_courier_coefficients_for_deliver(courier_id)
        earnings = 0
        for c in coefficients:
            earnings += 500 * c[1]

        return make_response(jsonify({"courier_id": courier_id,
                                      "courier_type": CourierType(courier_entry.courier_type).name,
                                      "regions": regions,
                                      "working_hours": working_hours,
                                      "rating": rating,
                                      "earnings": earnings}), HTTPStatus.OK)

    def patch(self, courier_id: int):
        args = couriers_patch_parser.parse_args()
        courier_type = args.get("courier_type")
        regions = args.get("regions")
        working_hours = args.get("working_hours")
        courier_entry: Couriers = CouriersRepo.get_by_id(courier_id)
        if (courier_type is not None and len(courier_type) == 0) or (regions is not None and len(regions) == 0) or (
                working_hours is not None and len(working_hours) == 0):
            return make_response('', HTTPStatus.BAD_REQUEST)

        type_change = False
        if courier_type is not None:
            courier_entry.courier_type = CourierType[courier_type].value
            type_change = True
        else:
            courier_type = CourierType(courier_entry.courier_type).name

        regions_change = False
        if regions is not None:
            courier_entry.regions = [CourierRegionAssoc(region) for region in regions]
            regions_change = True
        else:
            regions = [reg.region_id for reg in courier_entry.regions]

        work_hours_change = False
        if working_hours is not None:
            courier_entry.working_hours = [WorkingTime(work) for work in working_hours]
            work_hours_change = True
        else:
            working_hours = list()
            for work in courier_entry.working_hours:
                working_hours.append(prepare_time_to_view([work.from_hours, work.to_hours]))
        db.session.commit()

        if regions_change:
            courier_orders: List[Orders] = OrdersRepo.get_by_courier_id(courier_id)
            if courier_orders is not None:
                for order in courier_orders:
                    if order.region not in regions:
                        order.assign = 0
                        order.courier_id = None
                        order.courier_coef = None
                db.session.commit()

        if work_hours_change:
            courier_orders: List[Orders] = OrdersRepo.get_by_courier_id(courier_id)
            if courier_orders is not None:
                new_working_hours = [prepare_time_to_db(work) for work in working_hours]
                for order in courier_orders:
                    exist = False
                    for d_hours in order.delivery_hours:
                        for w_hours in new_working_hours:
                            if d_hours.from_hours <= w_hours[1] and d_hours.to_hours >= w_hours[0]:
                                exist = True
                                break
                    if not exist:
                        order.assign = 0
                        order.courier_id = None
                        order.courier_coef = None
                db.session.commit()

        if type_change:
            courier_orders: List[Orders] = OrdersRepo.get_by_courier_id(courier_id)
            if courier_orders is not None:
                new_weight = courier_entry.courier_type
                old_weight = round(sum([order.weight for order in courier_orders]), 2)
                diff_weight = old_weight - new_weight
                if new_weight < old_weight:
                    for order in sorted(courier_orders, key=lambda x: x.weight, reverse=True):
                        if diff_weight > 0:
                            diff_weight -= order.weight
                            order.assign = 0
                            order.courier_id = None
                            order.courier_coef = None
            db.session.commit()

        return make_response(jsonify({"courier_id": courier_id,
                                      "courier_type": courier_type,
                                      "regions": regions,
                                      "working_hours": working_hours}), HTTPStatus.OK)
