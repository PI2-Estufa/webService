from flask import Flask, jsonify
from flask_cors import CORS
import db


app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    temperature_query = db.session.query(db.Temperature).order_by(db.Temperature.id.desc()).limit(5)
    temperatures = [t.value for t in temperature_query]

    humidity_query = db.session.query(db.Humidity).order_by(db.Humidity.id.desc()).limit(5)
    humidities = [h.value for h in humidity_query]

    ph_query = db.session.query(db.Ph).order_by(db.Ph.id.desc()).limit(5)
    pHs = [p.value for p in ph_query]

    response = {
        "temperatures": temperatures,
        "humidities": humidities,
        "pHs": pHs
    }
    return jsonify(response)
