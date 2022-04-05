import logging


class Config:
    SECRET_KEY = 'bgcegy3yg2d3ue2uwccuby2ubwcchjsbgvcwcuwbc2whbuwb'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bd.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
    LOGFILE = 'logs/development/Development.log'
    LOGGER_LEVEL = logging.DEBUG
    DEBUG = True


class ProductionConfig(Config):
    LOGFILE = 'logs/production/Production.log'
    LOGGER_LEVEL = logging.INFO
    DEBUG = False
