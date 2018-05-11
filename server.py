from flask import Flask, jsonify
from kombu import Connection, Queue, Exchange, Consumer


app = Flask(__name__)

temperatures = []

def callback(body, msg):
    global temperatures
    temperatures.append(body)
    msg.ack()


conn = Connection("amqp://rabbit")
exchange = Exchange("main", "direct", durable=True)
queue = Queue("temperature_queue", exchange=exchange)
consumer = Consumer(channel=conn, queues=[queue], callbacks=[callback])


@app.route("/")
def index():
    global temperatures
    temperatures = []
    conn.connect()
    consumer.consume()
    for i in list(range(5)):
        try:
            conn.drain_events(timeout=1)
        except:
            response = { "temperatures" : temperatures }
            return jsonify(response)
    
    response = { "temperatures" : temperatures }
    
    return jsonify(response)
