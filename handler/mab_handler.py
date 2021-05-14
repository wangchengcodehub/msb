from com.vars import Status
from flask import current_app
from flask import make_response
from com.logs import get_logger
from flask_restful import Resource
from com.tools import format_registration_data
from flask_restful.reqparse import RequestParser

LOG = get_logger(name=__name__)


class RegMbrResource(Resource):
    """
    : 组件注册接口
    : URL: POST
    """

    @staticmethod
    def post():
        # 参数校验：
        parser = RequestParser()
        parser.add_argument('serviceName', required=True, location='json', type=str, default=None)
        parser.add_argument('version', required=True, location='json', type=str, default=None)
        parser.add_argument('url', required=True, location='json', type=str, default=None)
        parser.add_argument('publish_port', required=False, location='json', type=str, default=None)
        parser.add_argument('protocol', required=True, location='json', type=str, default=None)
        parser.add_argument('nodes', required=True, location='json', type=list, default="*")
        parser.add_argument('visualRange', required=True, location='json', type=str, default=None)
        args = parser.parse_args()

        # 参数提取：
        service_name = args.serviceName
        version = args.version
        url = args.url
        publish_port = args.publish_port
        protocol = args.protocol
        nodes = args.nodes[0]
        visual_range = args.visualRange

        data = {
            "serviceName": service_name,
            "version": version,
            "url": url,
            "nodes": nodes,
            "publish_port": publish_port,
            "protocol": protocol,
            "visualRange": visual_range
        }

        # 格式化注册数据：
        reg_data = format_registration_data(**data)

        # 将格式化好的数据写入到etcd中
        key = reg_data["key"]
        value = reg_data["value"]
        stat_code, _ = current_app.etcd_client.etcd_put(key=key, value=value)
        if stat_code == -1:
            raise _
        else:
            LOG.info(f"PUT ETCD: {key}:{value}")
        response = make_response(f"{key}: {value}")
        response.status = Status.OK
        return response
