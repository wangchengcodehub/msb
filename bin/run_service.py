import sys
from os import path
sys.path.insert(0, path.dirname(path.dirname(path.realpath(__file__))))
from bin import app
from flask import jsonify
from gevent import monkey
from com.logs import get_logger
from gevent.pywsgi import WSGIServer

monkey.patch_all()
LOG = get_logger(__name__)


@app.route('/')
def route_map():
    """
    根路由: 获取所有路由规则
    """
    return jsonify({rule.endpoint: rule.rule for rule in app.url_map.iter_rules()})


def main():
    # app.run(debug=True)
    listener = (app.config["HANDLER_ADDR"], app.config["HANDLER_PORT"])
    LOG.info(f"Running on http://{listener[0]}:{listener[1]}/ (Press CTRL+C to quit)")
    WSGIServer(listener=listener, application=app).serve_forever()


if __name__ == '__main__':
    main()
