import json
import os
import yaml
from .vars import Namespace

# 读取 ini 配置文件
def read_ini_conf():
    pass

# 读取 yaml 配置文件：
def read_yaml_conf():
    file_name_path = os.path.split(os.path.realpath(__file__))[0]
    yaml_path = os.path.join(file_name_path, 'config.yaml')
    with open(file=yaml_path, mode="r", encoding="utf-8") as file:
        data = yaml.load(file.read())
    return data

# 格式化注册字符串：
def format_registration_data(**kwargs):
    # 注册参数解析：
    url = kwargs.get("url", None)                    # 服务 URL
    nodes = kwargs.get("nodes", "*")                 # 服务实例列表
    version = kwargs.get("version", None)            # 服务版本
    protocol = kwargs.get("protocol", None)          # 协议
    visual_range = kwargs.get("visualRange", None)   # 网络平面
    service_name = kwargs.get("serviceName", None)   # 服务名
    publish_port = kwargs.get("publish_port", None)  # 发布端口

    # key 的统一前缀：
    head = Namespace + service_name + "/" + version

    # 格式化注册参数:
    reg_dict = {
        "url": url,
        "nodes": nodes[0],
        "version": version,
        "protocol": protocol,
        "visual_range": visual_range,
        "service_name": service_name,
        "publish_port": publish_port
    }

    # 最终在那个写入etcd的数据格式：
    return  {"key": head, "value": json.dumps(reg_dict)}