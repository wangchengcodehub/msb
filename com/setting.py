import os
import logging


class Config(object):

    # LOG CONF:
    LOG_PRINT_HANDLER = logging.DEBUG  # handler log level
    LOG_PRINT_CONSOLE = logging.DEBUG  # console log level
    LOG_PATH = os.environ.get("LOG_PATH", "/var/log/")  # log path

    # ETCD CLIENT:
    ETCD_CLIENT_PORT = os.environ.get("ETCD_CLIENT_PORT ", "2379")  # etcd db port
    ETCD_CLIENT_HOST = os.environ.get("ETCD_CLIENT_HOST ", "127.0.0.1")  # etcd db host

    # SERVER HOST:
    MSB_CLIENT_SERVER_PORT = int(os.environ.get("MSB_CLIENT_SERVER_PORT", 8888))  # flask server port
    MSB_CLIENT_SERVER_HOST = os.environ.get("MSB_CLIENT_SERVER_HOST", "0.0.0.0")  # flask server host

    # FLASK CONF:
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", False)  # flask 调试模式
    FLASK_THREADED = os.environ.get("FLASK_THREADED", True)  # flask 多线程启动

    # NGINX CONF:
    NGINX_TCP_CONF_PATH = os.environ.get("NGINX_CONF_PATH", "/etc/nginx/tcp-conf.d/default.conf")
    NGINX_HTTP_CONF_PATH = os.environ.get("NGINX_CONF_PATH", "/etc/nginx/http-conf.d/default.conf")

    # 当有网络平面为系统间的情况才会用到这个参数
    # 对端 MSB api getaway 地址: 重要参数！ 这个参数将作为 Nginx Conf upstream server 的地址 (上游服务器地址)
    REMOTE_MSB_GATEWAY_HOST = os.environ.get("PEER_MSB_GATEWAY_HOST", "127.0.0.1")
    REMOTE_MSB_GATEWAY_PORT = os.environ.get("PEER_MSB_GATEWAY_PORT", "8989")

    # 本地 MSB api getaway 地址
    LOCAL_MSB_GATEWAY_HOST = os.environ.get("LOCAL_MSB_GATEWAY_HOST", "127.0.0.1")
    LOCAL_MSB_GATEWAY_PORT = os.environ.get("LOCAL_MSB_GATEWAY_PORT", "8989")


class DefaultConfig:
    """
    默认配置:
    """
    def __init__(self):
        pass

    # etcd connection configuration
    ETCD_CLIENT = {
        "host": Config.ETCD_CLIENT_HOST,
        "port": Config.ETCD_CLIENT_PORT
    }


class MsbConfig(DefaultConfig):
    """
    Msb 配置:
    """
    # flask server listening configuration
    DEBUG = Config.FLASK_DEBUG                    # 调试模式
    THREADED = Config.FLASK_THREADED              # 多线程启动
    HANDLER_PORT = Config.MSB_CLIENT_SERVER_PORT  # 监听端口
    HANDLER_ADDR = Config.MSB_CLIENT_SERVER_HOST  # 监听地址


config_dict = {
    "Default": DefaultConfig,
    "MsbConfig": MsbConfig,
}
