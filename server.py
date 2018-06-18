import os
import db
from flask_cors import CORS
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "./uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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

    water_temperature_query = db.session.query(db.WaterTemperature).order_by(db.WaterTemperature.id.desc()).limit(5)
    water_temperatures = [i.value for i in water_temperature_query]

    water_level_query = db.session.query(db.WaterLevel).order_by(db.WaterLevel.id.desc()).limit(5)
    water_levels = [w.value for w in water_level_query]

    drawer_status_query = db.session.query(db.DrawerStatus).order_by(db.DrawerStatus.id.desc()).limit(5)
    drawer_statuses = [d.value for d in drawer_status_query]

    images = os.listdir('./uploads')

    response = {
        "temperatures": temperatures,
        "humidities": humidities,
        "pHs": pHs,
        "iluminations": iluminations,
        "water_temperatures": water_temperatures,
        "water_levels": water_levels,
        "drawer_statuses": drawer_statuses,
        "images": images
    }
    return jsonify(response)

@app.route("/picture", methods=["POST"])
def pictures():
    if "picture" not in request.files:
        return "No file in request"

    file = request.files["picture"]
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    return filename
