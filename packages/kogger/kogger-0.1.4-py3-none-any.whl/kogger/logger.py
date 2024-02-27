"""
A very simple logger.

@author: bochengz
@date: 2023/04/11
@email: bochengzeng@bochengz.top
"""
import logging


class Logger:
    LEVEL_MAPPING = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    filename: str = None
    level: str = 'info'
    fmt: str = '[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s'
    datafmt: str = '%Y-%m-%d %H:%M:%S'

    @staticmethod
    def basic_config(filename=None, level='info',
                 fmt='[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s',
                 datafmt='%Y-%m-%d %H:%M:%S'):
        Logger.filename = filename
        Logger.level = level
        Logger.fmt = fmt
        Logger.datafmt = datafmt

    @staticmethod
    def get_logger(name):
        logger = logging.getLogger(name)
        logger.setLevel(Logger.LEVEL_MAPPING[Logger.level])
        fmt = logging.Formatter(Logger.fmt, Logger.datafmt)
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        logger.addHandler(sh)

        if Logger.filename is not None:
            fh = logging.FileHandler(Logger.filename)
            fh.setFormatter(fmt)
            logger.addHandler(fh)
        return logger

