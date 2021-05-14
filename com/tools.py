import os
import json
from jinja2 import Template
from com.vars import ETCD
from com.vars import VISUAL_RANGE
from com.vars import PROTOCOL
from com.setting import Config


# 格式化注册字符串：
def format_registration_data(**kwargs):
    # 注册参数解析：
    url = kwargs.get("url")  # 服务 URL
    nodes = kwargs.get("nodes")  # 服务实例列表
    version = kwargs.get("version")  # 服务版本
    protocol = kwargs.get("protocol")  # 协议
    visual_range = kwargs.get("visualRange")  # 网络平面
    service_name = kwargs.get("serviceName")  # 服务名
    publish_port = kwargs.get("publish_port")  # 发布端口

    # key 的统一前缀：
    head = ETCD.NAMESPACE + service_name + "/" + version

    # 格式化注册参数:
    reg_dict = {
        "url": url,
        "nodes": nodes,
        "version": version,
        "protocol": protocol,
        "visual_range": visual_range,
        "service_name": service_name,
        "publish_port": publish_port
    }

    # 最终在那个写入etcd的数据格式：
    return {"key": head, "value": json.dumps(reg_dict)}


def create_dir(_path: str):
    """
    如果目录不存在就创建
    """
    if not os.path.exists(_path):
        os.makedirs(_path)


class TemplateHandle(object):
    """
    处理模板文件
    """

    def __init__(self, s_path, d_path, kwargs):
        self.s_path = s_path
        self.d_path = d_path
        self.kwargs = kwargs

    def create(self):
        with open(self.s_path, "r") as file:
            template = Template(file.read())
        with open(self.d_path, "w") as file:
            file.write(template.render(self.kwargs))

    def delete(self):
        if os.path.exists(self.d_path):
            os.remove(self.d_path)


class ServiceHttp(object):
    """
    HTTP 模板渲染变量对象
    """
    listen = ""
    service_name = ""
    proxy_pass_host = ""
    proxy_pass_port = ""
    proxy_pass_url = ""
    proxy_pass_version = ""

    def to_dict(self):
        data = {
            "service_name": self.service_name,
            "proxy_pass_host": self.proxy_pass_host,
            "proxy_pass_port": self.proxy_pass_port,
            "proxy_pass_url": self.proxy_pass_url,
            "proxy_pass_version": self.proxy_pass_version
        }
        return data


class ServiceTcp(object):
    """
    Tcp 模板渲染变量对象
    """
    service_name = ""
    upstream_host = ""
    upstream_port = ""
    listen_port = ""

    def to_dict(self):
        data = {
            "service_name": self.service_name,
            "upstream_host": self.upstream_host,
            "upstream_port": self.upstream_port,
            "listen_port": self.listen_port,
        }
        return data


def format_nginx_conf_data(service):
    url = service.get("url", None)
    nodes = service.get("nodes", None)
    version = service.get("version", None)
    protocol = service.get("protocol", None)
    visual_range = service.get("visual_range", None)
    service_name = service.get("service_name", None)
    publish_port = service.get("publish_port", None)

    # 服务网络平面：
    if str(visual_range) == VISUAL_RANGE.INSIDE:
        if protocol.lower() == PROTOCOL.TCP:
            assert not (service_name is None), ValueError(f"service_name value can't is {service_name}")
            assert not (nodes.get("ip") is None), ValueError(f"nodes ip value can't is {nodes.get('ip')}")
            assert not (nodes.get("port") is None), ValueError(f"nodes port value can't is {nodes.get('port')}")
            service_tcp = ServiceTcp()
            service_tcp.service_name = service_name
            service_tcp.upstream_host = nodes.get("ip")
            service_tcp.upstream_port = nodes.get("port")
            service_tcp.listen_port = nodes.get("port")
            return service_tcp
        if protocol.lower() == PROTOCOL.HTTP:
            assert not (url is None), ValueError(f"url value can't is {url}")
            assert not (service_name is None), ValueError(f"service_name value can't is {service_name}")
            assert not (version is None), ValueError(f"version value can't is {version}")
            assert not (nodes.get("ip") is None), ValueError(f"nodes ip value can't is {nodes.get('ip')}")
            assert not (nodes.get("port") is None), ValueError(f"nodes port value can't is {nodes.get('port')}")
            service_http = ServiceHttp()
            service_http.proxy_pass_url = url
            service_http.service_name = service_name
            service_http.proxy_pass_version = version
            service_http.proxy_pass_host = nodes.get("ip")
            service_http.proxy_pass_port = nodes.get("port")
            return service_http
    if str(visual_range) == VISUAL_RANGE.OUTSIDE:
        if protocol.lower() == PROTOCOL.TCP:
            assert not (service_name is None), ValueError(f"service_name value can't is {service_name}")
            assert not (publish_port is None), ValueError(f"publish_port value can't is {publish_port}")
            assert not (Config.REMOTE_MSB_GATEWAY_HOST is None), ValueError(
                f"service_name is : {Config.REMOTE_MSB_GATEWAY_HOST}")
            service_tcp = ServiceTcp()
            service_tcp.service_name = service_name
            service_tcp.listen_port = publish_port
            service_tcp.upstream_host = Config.REMOTE_MSB_GATEWAY_HOST
            service_tcp.upstream_port = publish_port
            return service_tcp
        if protocol.lower() == PROTOCOL.HTTP:
            assert not (url is None), ValueError(f"url value can't is {url}")
            assert not (service_name is None), ValueError(f"service_name value can't is {service_name}")
            assert not (version is None), ValueError(f"version value can't is {version}")
            assert not (Config.REMOTE_MSB_GATEWAY_HOST is None), ValueError(
                f"service_name is : {Config.REMOTE_MSB_GATEWAY_HOST}")
            assert not (publish_port is None), ValueError(f"publish_port value can't is {publish_port}")
            service_http = ServiceHttp()
            service_http.proxy_pass_url = url
            service_http.service_name = service_name
            service_http.proxy_pass_version = version
            service_http.proxy_pass_host = Config.REMOTE_MSB_GATEWAY_HOST
            service_http.proxy_pass_port = publish_port
            return service_http
