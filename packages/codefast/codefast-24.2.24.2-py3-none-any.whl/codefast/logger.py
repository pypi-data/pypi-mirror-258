import logging

import colorlog


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class MyLogger(metaclass=SingletonMeta):
    def __init__(self,
                 level: str = 'INFO',
                 log_path: str = 'cf.log',
                 max_size: int = 100 * 1024 * 1024,
                 max_backup: int = 3,
                 *args,
                 **kwargs):
        LOGGING_CONFIG = {
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': {
                'standard': {
                    'format':
                    '%(asctime)s, %(levelname)s, %(filename)s-%(lineno)s-%(funcName)s💦 %(message)s'
                },
            },
            'handlers': {
                'default': {
                    'level': level,
                    'formatter': 'standard',
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout',  # Default is stderr
                },
                'rotate': {
                    'level': level,
                    'formatter': 'standard',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': log_path,
                    'maxBytes': max_size,
                    'backupCount': max_backup,
                    'encoding': 'utf8',
                }
            },
            'loggers': {
                '': {  # root logger
                    'handlers': ['default', 'rotate'],
                    'level': level,
                    'propagate': False
                },
                'my.packg': {
                    'handlers': ['default', 'rotate'],
                    'level': 'INFO',
                    'propagate': False
                },
                '__main__': {  # if __name__ == '__main__'
                    'handlers': ['default', 'rotate'],
                    'level': 'DEBUG',
                    'propagate': False
                },
            }
        }

        import logging.config
        logging.config.dictConfig(LOGGING_CONFIG)

        self.logger = logging.getLogger(__name__)

    def get_logger(self):
        return self.logger


def get_logger(level: str = 'INFO',
               log_path: str = '/tmp/cf.log',
               max_size: int = 100 * 1024 * 1024,
               max_backup: int = 3):
    return MyLogger(level, log_path, max_size, max_backup).get_logger()


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = colorlog.ColoredFormatter(
    '%(asctime)s%(log_color)s [%(levelname).1s]%(reset)s [%(filename)s-%(lineno)d] %(message)s',
    datefmt='%m%d/%H:%M:%S',
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow,bold',
        'ERROR': 'red,bold',
        'CRITICAL': 'red,bg_yellow,bold'
    },
    secondary_log_colors={},
    style='%')

console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
info = logger.info
debug = logger.debug
warning = logger.warning
error = logger.error
critical = logger.critical
