from . import apii

couriers_parser = apii.parser()
couriers_parser.add_argument("data", type=list, required=True, help="The courier data", location="json")

couriers_patch_parser = apii.parser()
couriers_patch_parser.add_argument("courier_type", type=str, required=False, help="The type of courier ",
                                   location="json")
couriers_patch_parser.add_argument("regions", type=list, required=False, help="The working regions of courier",
                                   location="json")
couriers_patch_parser.add_argument("working_hours", type=list, required=False, help="The working hours of courier",
                                   location="json")

orders_parser = apii.parser()
orders_parser.add_argument("data", type=list, required=True, help="The order data", location="json")

orders_assign_parser = apii.parser()
orders_assign_parser.add_argument("courier_id", type=int, required=True, help="The couriers id for assign order",
                                  location="json")

orders_complete_parser = apii.parser()
orders_complete_parser.add_argument("courier_id", type=int, required=True, help="The couriers id for complete order",
                                    location="json")
orders_complete_parser.add_argument("order_id", type=int, required=True, help="The order id for complete order",
                                    location="json")
orders_complete_parser.add_argument("complete_time", type=str, required=True, help="The time where order is completed",
                                    location="json")
