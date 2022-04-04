import logging
import os
import zipfile
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler

from app import app


class ZipTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False,
                 atTime=None):
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc, atTime)

    def make_zip(self) -> None:
        dir_path, base_filename = os.path.split(self.baseFilename)
        logs_list = [f for f in os.listdir(dir_path)
                     if all([f.startswith(base_filename), f != base_filename, not f.endswith('.zip')])]
        if len(logs_list) >= self.backupCount:
            with zipfile.ZipFile('archive_{}.zip'.format(logs_list[0]), 'w') as zip_file:
                for f in logs_list:
                    file = os.path.join(dir_path, f)
                    zip_file.write(file, os.path.base_filename(file), compress_type=zipfile.ZIP_DEFLATED)
                    os.remove(file)

    def doRollover(self) -> None:
        if self.backupCount > 0:
            self.make_zip()
        super().doRollover()

    def getFilesToDelete(self) -> list:
        return []


def _clear_existing_logger_handler() -> None:
    logger = logging.getLogger(__name__)
    if logger.hasHandlers():
        logger.handlers.clear()


def get_logger_handler():
    _clear_existing_logger_handler()

    handler = ZipTimedRotatingFileHandler(app.config['LOGFILE'], when="midnight", interval=1, backupCount=3)

    handler.setLevel(app.config['LOGGER_LEVEL'])
    handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s '))

    return handler