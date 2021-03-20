from flask import Blueprint
from flask_restplus import Api

api = Blueprint('api', __name__, url_prefix='/api')
apii = Api(api)


from .couriers import *
from .orders import *
from .utils import *
