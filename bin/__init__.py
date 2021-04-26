from flask import Flask
from client.etcd import EtcdClient
from config import config_dict
from config import EXTRA_ENV_CONFIG
from com.logs import Logger


def flask_app_load(flask_conf: str, flask_app: Flask):
    """
    Flask app configuration
    """
    # 默认配置（从配置子类中加载）
    flask_app.config.from_object(config_dict[flask_conf])

    # 额外配置（从环境变量中加载）
    flask_app.config.from_envvar(EXTRA_ENV_CONFIG, silent=True)


def register_extensions(log_name: str, flask_app: Flask):
    """
    Component initialization
    """
    # etcd 初始化
    flask_app.etcd_client = EtcdClient(**flask_app.config["ETCD_CLIENT"])

    # Logging 初始化
    Logger().init_app(flask_app, log_name=log_name)


def create_app(flask_conf: str, log_name: str):
    """
    Create application and component initialization
    """
    # Flask App 创建：
    flask_app = Flask(__name__)

    # flask加载配置
    flask_app_load(flask_conf=flask_conf, flask_app=flask_app)

    # 组件初始化
    register_extensions(flask_app=flask_app, log_name=log_name)

    return flask_app
