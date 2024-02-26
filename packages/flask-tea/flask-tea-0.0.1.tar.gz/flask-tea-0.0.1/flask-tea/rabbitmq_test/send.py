import time

import pika
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.dirname(__file__) + os.sep + '../')

# 使用非本机mq时，默认生产环境，需要登录(用户名和密码)
credentials = pika.PlainCredentials('admin_zqs', 'zqs123')

# 与rabbitmq建立连接
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.40.16', 5672, '/zqs', credentials))

# 建立连接通道
channel = connection.channel()

# 声明queue
channel.queue_declare(queue='hello')

for i in range(1000):
    time.sleep(0.5)
    # 发布消息
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body='Hello World!')
    print(" [x] Sent 'Hello World!'")

# 断开连接
connection.close()
