import os
import json
from com.vars import ETCD
from etcd.etcd import etcd_client
from com.setting import Config
from com.tools import TemplateHandle
from com.tools import create_dir
from com.tools import format_nginx_conf_data


# 监听 ETCD 注册信息, 每当 ETCD 有数据更新时，会全局渲染 Nginx conf：
def watch(key):
    events_iterator, cancel = etcd_client.watch_prefix(key)
    for event in events_iterator:
        if event.__dict__.get("_event").type == ETCD.DELETE:
            print("DELETE")
        if event.__dict__.get("_event").type == ETCD.PUT:
            conf_data(etcd_client.get_prefix(ETCD.NAMESPACE))


# 预留触发接口：
def trigger(data=None):
    if data:
        conf_data(data)
    else:
        conf_data(etcd_client.get_prefix(ETCD.NAMESPACE))


def conf_data(services):
    service_objs_tcp = {"service_objs": []}
    service_objs_http = {"listen": Config.LOCAL_MSB_GATEWAY_PORT, "service_objs": []}
    for service in services:
        service = json.loads(service[0].decode())
        protocol = service.get("protocol")
        if protocol.lower() == "tcp":
            service_objs_tcp["service_objs"].append(format_nginx_conf_data(service).to_dict())
        if protocol.lower() == "http":
            service_objs_http["service_objs"].append(format_nginx_conf_data(service).to_dict())
    else:
        tcp_template_abs_path = os.path.abspath("../template/conf/tcp-conf.d/default.conf.j2")
        http_template_abs_path = os.path.abspath("../template/conf/http-conf.d/default.conf.j2")

        create_dir(_path=os.path.dirname(Config.NGINX_TCP_CONF_PATH))
        tcp_template_handle = TemplateHandle(
            s_path=tcp_template_abs_path,
            d_path=Config.NGINX_TCP_CONF_PATH,
            kwargs=service_objs_tcp
        )
        tcp_template_handle.delete()
        tcp_template_handle.create()

        create_dir(_path=os.path.dirname(Config.NGINX_HTTP_CONF_PATH))
        http_template_handle = TemplateHandle(
            s_path=http_template_abs_path,
            d_path=Config.NGINX_HTTP_CONF_PATH,
            kwargs=service_objs_http
        )
        tcp_template_handle.delete()
        http_template_handle.create()


def test():
    import sys
    from os import path
    sys.path.insert(0, path.dirname(path.dirname(path.realpath(__file__))))

    service = [
        (b"""{
            "service_name": "mbr",
            "version": "v1",
            "url": "/mbr/v1",
            "protocol": "HTTP",
            "nodes": {"ip":"192.168.3.8", "port": "8080"},
            "visual_range": "0",
            "publish_port": "172.16.150.9999"
        }""", ""),
        (b"""{
            "service_name": "dsm",
            "version": "v1",
            "url": "/dsm/v1",
            "protocol": "tcp",
            "nodes": {"ip": "172.16.150.11", "port": "873"},
            "visual_range": "0",
            "publish_port": "1873"
        }""", ""),
    ]

    conf_data(service)


if __name__ == '__main__':
    # test()
    trigger()
