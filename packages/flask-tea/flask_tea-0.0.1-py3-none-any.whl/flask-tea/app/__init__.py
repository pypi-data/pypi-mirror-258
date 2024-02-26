from threading import Thread

import pika
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.app = app
    db.init_app(app)
    mq_thread = Thread(target=consume_message, args=(app,))
    mq_thread.start()

    from .test import api as api_test_blueprint
    app.register_blueprint(api_test_blueprint, url_prefix='/')
    return app


def consume_message(app):
    # 使用非本机mq时，默认生产环境，需要登录(用户名和密码)
    credentials = pika.PlainCredentials(app.config['MQ_USER'], app.config['MQ_PWD'])

    # 与rabbitmq建立连接
    connection = pika.BlockingConnection(pika.ConnectionParameters(app.config['MQ_HOST'], app.config['MQ_PORT'],
                                                                   app.config['VIRTUAL_HOST'], credentials))

    # 建立连接通道
    channel = connection.channel()

    # 声明queue
    channel.queue_declare(queue='hello')

    # 定义回调函数
    def callback(ch, method, properties, body):
        import time
        print('开始接收')
        time.sleep(5)
        print(" [x] Received %r" % body)

    # 消费消息
    channel.basic_consume('hello', callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
