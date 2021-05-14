import logging
from com.setting import Config
from logging.handlers import RotatingFileHandler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(level=Config.LOG_PRINT_HANDLER)
    # 日志保存： 10M*100
    handler = RotatingFileHandler(Config.LOG_PATH + "/msb.log", maxBytes=10 * (1024 * 1024), backupCount=100)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    console = logging.StreamHandler()
    console.setLevel(Config.LOG_PRINT_CONSOLE)
    console.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(console)
    return logger
