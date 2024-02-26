import pika
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.dirname(__file__) + os.sep + '../')


# 使用非本机mq时，默认生产环境，需要登录(用户名和密码)
credentials = pika.PlainCredentials('admin', '123')

# 与rabbitmq建立连接
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.40.16', 5672, '/abc', credentials))

# 建立连接通道
channel = connection.channel()

# 声明queue
channel.queue_declare(queue='hello')


# 定义回调函数
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


# 消费消息
channel.basic_consume('hello', callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
