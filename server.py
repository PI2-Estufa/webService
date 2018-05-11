from flask import Flask, jsonify
from flask_cors import CORS
from kombu import Connection, Queue, Exchange, Consumer


app = Flask(__name__)
CORS(app)

temperatures = []

def callback(body, msg):
    global temperatures
    temperatures.append(body)
    msg.ack()


@app.route("/")
def index():
    global temperatures
    temperatures = []

    conn = Connection("amqp://rabbit")
    exchange = Exchange("main", "direct", durable=True)
    queue = Queue("temperature_queue", exchange=exchange)
    consumer = Consumer(channel=conn, queues=[queue], callbacks=[callback])

    if not conn.connected:
        conn.connect()
    
    consumer.consume()
    
    for i in list(range(5)):
        try:
            conn.drain_events(timeout=1)
        except:
            break
    response = { "temperatures" : temperatures }
    conn.release()
    return jsonify(response)
