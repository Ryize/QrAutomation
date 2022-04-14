import logging
import os
from typing import List


class Config:
    """
    Общие конфигурации сервера.
    """

    SECRET_KEY: str = 'bgcegy3yg2d3ue2uwccuby2ubwcchjsbgvcwcuwbc2whbuwb'
    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///bd.db'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = True  # Убрать предупреждения при запуске


class DevelopmentConfig(Config):
    """
    Конфигурации для разработки/тестирования.
    """

    LOGFILE: str = 'logs/development/Development.log'
    LOGGER_LEVEL: int = logging.DEBUG
    DEBUG: bool = True


class ProductionConfig(Config):
    """
    Конфигурации для продакшн сервера.
    """

    LOGFILE: str = 'logs/production/Production.log'
    LOGGER_LEVEL: int = logging.INFO
    DEBUG: bool = False


class CustomConfig:
    """
    Конфигурации под конкретную кмпанию, все имеющиеся в этом классе параметры, можно и нужно изменять.
    """

    SITE_URL: str = '127.0.0.1:5000'
    PRODUCTION: bool = True
    COMPANY_SECURE_CODE: List[str] = []  # Если кода нет, оставьте пустые скобочки []
    MAIL_ADDRESS = os.getenv('MAIL_ADDRESS')  # Только gmail, если не работает, ознакомьтесь с паролями приложений
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
