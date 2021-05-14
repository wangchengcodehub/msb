from flask import Flask
from etcd.etcd import etcd_client
from com.setting import config_dict


def flask_app_load(flask_conf: str, flask_app: Flask):
    """
    Flask app configuration
    """
    # 加载子类配置
    flask_app.config.from_object(config_dict[flask_conf])


def register_extensions(flask_app: Flask):
    """
    Component initialization
    """
    # etcd 初始化
    flask_app.etcd_client = etcd_client


def register_bp(flask_app):
    """
    注册蓝图:
    """
    from handler import msb_bp
    flask_app.register_blueprint(msb_bp)


def create_app(flask_conf: str):
    """
    Create application and component initialization
    """
    # App 创建：
    flask_app = Flask(__name__)

    # 加载配置
    flask_app_load(flask_conf=flask_conf, flask_app=flask_app)

    # 注册蓝图：
    register_bp(flask_app)

    # 组件初始化
    register_extensions(flask_app=flask_app)

    return flask_app


app = create_app(flask_conf="MsbConfig")
