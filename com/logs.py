import os
import logging
from logging.handlers import RotatingFileHandler
from logging import StreamHandler

LOG_PATH = "/var/log/msb/"
LOG_FILE_MAX_BYTES = 100 * 1024 * 1024
LOG_FILE_BACKUP_COUNT = 10


class Logger(object):

    @staticmethod
    def init_app(app, log_name):

        formatter = logging.Formatter(
            '%(asctime)s [%(thread)u:%(threadName)s] [%(levelname)s]: %(message)s'
        )
        if not os.path.exists(LOG_PATH):
            os.mkdir(LOG_PATH)

        file_handler = RotatingFileHandler(
            filename=os.path.join(LOG_PATH, log_name),
            mode='a',
            maxBytes=LOG_FILE_MAX_BYTES,
            backupCount=LOG_FILE_BACKUP_COUNT,
            encoding='utf-8'
        )

        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.NOTSET)

        stream_handler = StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.NOTSET)

        for logger in (
                app.logger,
                logging.getLogger('sqlalchemy'),
                logging.getLogger('werkzeug')
        ):
            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)