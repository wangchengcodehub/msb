from bin import create_app
from flask import request
from flask import make_response
from com.tools import format_registration_data

# 工厂函数创建 flask app
app = create_app(flask_conf="MsbConfig", log_name="msb.log")


# 服务注册接口：
@app.route('/api/microservices/v1/services', methods=["POST"])
def services_registration():
    # 格式化注册数据：
    reg_data = format_registration_data(**request.json)

    # 将格式化好的数据写入到etcd中
    key = reg_data["key"]
    value = reg_data["value"]
    stat_code, _ = app.etcd_client.etcd_put(key=key, value=value)
    if stat_code == -1:
        raise _
    else:
        app.logger.info(f"PUT ETCD -- {key}:{value}")
    response = make_response(f"{key}: {value}")
    return response


if __name__ == '__main__':
    app.run(
        host=app.config["HANDLER_ADDR"],
        port=app.config["HANDLER_PORT"],
        debug=app.config["DEBUG"],
        threaded=app.config["THREADED"]
    )
