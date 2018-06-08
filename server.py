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

    ilumination_query = db.session.query(db.Ilumination).order_by(db.Ilumination.id.desc()).limit(5)
    iluminations = [i.value for i in ilumination_query]

<<<<<<< HEAD
    water_temperature_query = db.session.query(db.WaterTemperature).order_by(db.WaterTemperature.id.desc()).limit(5)
    water_temperatures = [i.value for i in water_temperature_query]
=======
    water_level_query = db.session.query(db.WaterLevel).order_by(db.WaterLevel.id.desc()).limit(5)
    water_level = [w.value for w in water_level_query]
>>>>>>> dd4c8fa5b2b270bb2483b3e11c2ad17b19155165

    response = {
        "temperatures": temperatures,
        "humidities": humidities,
        "pHs": pHs,
        "iluminations": iluminations,
<<<<<<< HEAD
        "water_temperatures": water_temperatures
=======
        "water_level": water_level
>>>>>>> dd4c8fa5b2b270bb2483b3e11c2ad17b19155165
    }
    return jsonify(response)
