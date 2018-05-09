from flask import Flask
from kombu import Connection, Queue, Exchange, Consumer

app = Flask(__name__)

temperature = 0

def callback(body, msg):
    global temperature
    temperature = body
    msg.ack()


conn = Connection("amqp://rabbit")
exchange = Exchange("main", "direct", durable=True)
queue = Queue("temperature_queue", exchange=exchange)
consumer = Consumer(channel=conn, queues=[queue], callbacks=[callback])


@app.route("/")
def index():
    conn.connect()
    consumer.consume()
    conn.drain_events()
    return str(temperature)
