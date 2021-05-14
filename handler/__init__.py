from flask import Blueprint
from flask_restful import Api
from handler.mab_handler import RegMbrResource


# 创建蓝图对象:
msb_bp = Blueprint('msb', __name__)

# 创建Api对象:
msb_api = Api(msb_bp)


# msb server Interface:
msb_api.add_resource(RegMbrResource, "/api/microservices/v1/services")
