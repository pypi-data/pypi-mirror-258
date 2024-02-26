import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 秘钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dgsaherherge'
    # 配置
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 500

    MQ_USER = 'admin'
    MQ_PWD = 'abc123'
    MQ_HOST = '192.168.40.16'
    MQ_PORT = '5672'
    VIRTUAL_HOST = '/abc'


# 开发测试环境配置
class DevelopConfig(Config):
    DEBUG = True
    SERVER_URL = ""
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@192.168.40.16/mq?charset=utf8mb4'
    SENTRY_DSN = ''


# 生产环境配置
class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopConfig,
    'production': ProductionConfig,
    'default': ProductionConfig if os.environ.get("PRODUCT_SERVICE") else DevelopConfig
}
