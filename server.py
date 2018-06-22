import os
import db
import hashlib
from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_jwt import JWT, jwt_required
from flask_marshmallow import Marshmallow
from werkzeug.utils import secure_filename
from datetime import timedelta
from datetime import date
import datetime
import json

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "./uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'ameixa'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=36000)
ma = Marshmallow(app)

class PlantSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('specie', 'created_at', 'observations')

plant_schema = PlantSchema()
plants_schema = PlantSchema(many=True)

def authenticate(username, password):
    user = db.session.query(db.User).filter_by(username=username).first()
    hash = hashlib.md5(password.encode())
    if user.password == hash.hexdigest():
        return user
    else:
        return None

def identity(payload):
    user = db.session.query(db.User).filter_by(id=payload["identity"]).first()
    return user

jwt = JWT(app, authenticate, identity)

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/")
@jwt_required()
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
    images.remove(".keep")

    response = {
        "temperatures": temperatures,
        "humidities": humidities,
        "pHs": pHs,
        "iluminations": iluminations,
        "water_temperatures": water_temperatures,
        "water_levels": water_levels,
        "drawer_statuses": drawer_statuses,
        "images": images,
        "warnings": [
            {
                "id": 2,
                "message": "PH elevada!",
                "level": "error"
            }
        ]
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

@app.route('/report/<report>')
@jwt_required()
def temperatures(report):
    entities = {
        "temperatures": db.Temperature,
        "humidities": db.Humidity,
        "phs": db.Ph,
        "water_temperatures": db.WaterTemperature
    }

    # path = 

    try:
        Entity = entities[report]
    except KeyError:
        return jsonify({"error": True, "message": "invalid route"})

    allowed_periods = ["day", "week", "month", "year", "lifespan"]

    period = request.args.get("period", "week")

    if period not in allowed_periods:
        return jsonify({"error": True, "message": "invalid period"})

    time_patrol = {
        "day": 0,
        "week": 7,
        "month": 30,
        "year": 365,
        "lifespan": 365 * 79
    }
    passdate = datetime.date.today() - timedelta(days=time_patrol[period])
    results = db.session.query(Entity.id, Entity.value, Entity.created_date).filter(
    (Entity.created_date) >= passdate).order_by(Entity.created_date.desc()).limit(30)
    values = [r.value for r in results]
    average = round(sum(values)/results.count(), 2)
    
    response = [{"id":t.id, "value":t.value, "date": t.created_date} for t in results]
    return jsonify({
        "average": average,
        "results": response
    })

@app.route("/plant", methods=["POST"])
def add_plant():
     specie = request.json['specie']
     created_at = request.json['created_at']
     observations = request.json['observations']
    
     new_plant = db.Plant(specie, created_at, observations)
     db.session.add(new_plant)
     db.session.commit()
     return jsonify(specie= new_plant.specie,
                    created_at= new_plant.created_at,
                    observations= new_plant.observations)

@app.route("/plant/<id>", methods=["GET"])
def plant_detail(id):
    plant = db.session.query(db.Plant).get(id)
    return jsonify(specie= plant.specie,
                   created_at= plant.created_at,
                   observations= plant.observations)

@app.route("/plant/<id>", methods=["PUT"])
def plant_update(id):
    plant = db.session.query(db.Plant).get(id)
    specie = request.json['specie']
    created_at = request.json['created_at']
    observations = request.json['observations']

    plant.specie = plant
    plant.created_at = created_at
    plant.observations = observations

    db.session.commit()
    return plant_schema.jsonify(plant)

@app.route("/plant/<id>", methods=["DELETE"])
def plant_delete(id):
    plant = db.session.query(db.Plant).get(id)
    db.session.delete(plant)
    db.session.commit()
    return plant_schema.jsonify(plant)

@app.route("/plant", methods=["GET"])
def plant_all():
    plant_query = db.session.query(db.Plant).order_by(db.Plant.id.desc()).limit(30)
    response = [{"id":p.id, "specie":p.specie, "observations": p.observations} for p in plant_query]
    return jsonify(response)

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))


