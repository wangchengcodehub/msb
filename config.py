
class DefaultConfig:
    """
    默认配置
    """
    def __init__(self):
        pass

    # etcd connection configuration
    ETCD_CLIENT = {
        "host": "172.16.200.43",
        "port": 2379
    }


class MsbConfig(DefaultConfig):
    """
    Msb 配置：
    """
    # flask server listening configuration
    DEBUG = True                # 调试模式
    THREADED = True             # 多线程启动
    HANDLER_PORT = "8080"       # 监听端口
    HANDLER_ADDR = "127.0.0.1"  # 监听地址


EXTRA_ENV_CONFIG = 'ENV_CONFIG'  # 额外配置对应的环境变量名

config_dict = {
    "Default": DefaultConfig,
    "MsbConfig": MsbConfig,
}