import os


class Config(object):
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = 'subair'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:subair@localhost/blog-api-db"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
