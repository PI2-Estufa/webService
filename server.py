import os
import db
from flask_cors import CORS
from flask import Flask, jsonify, request, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user
from werkzeug.utils import secure_filename
from forms import LoginForm
from datetime import timedelta
from datetime import date
import datetime

app = Flask(__name__)
CORS(app)

lm = LoginManager(app)

UPLOAD_FOLDER = "./uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@lm.user_loader
def load_user(id):
    return db.session.query(db.User).filter_by(id=id).first()

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
    images.remove(".keep")

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

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(db.User).filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash("Logged in.")
            # return redirect(url_for(index)) MANDAR PARA PÁGINA PRINCIPAL
        else:
            flash("Invalid login.")
    else:
        flash("Falso valitate on submit")
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out.")
    return "DESLOGADO"
     # return redirect(url_for(index)) MANDAR PARA PÁGINA PRINCIPAL

@app.route("/picture", methods=["POST"])
def pictures():
    if "picture" not in request.files:
        return "No file in request"

    file = request.files["picture"]
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    return filename

@app.route('/report/<report>')
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

@app.route("/index_new")
def index_new():
    return render_template("index.html")

@app.route("/createpage")
def create_page():
    return render_template("create.html")

@app.route("/create_plant", methods=['GET', 'POST'])
def create_plant():
    if request.method == "POST":
        specie = request.form.get("specie")
        created_at = request.form.get("created_at")
        observations = request.form.get("observations")

        if specie and created_at:
            p = db.Plant(specie, created_at, observations)
            db.session.add(p)
            db.session.commit()
    return render_template("index.html")

@app.route("/show")
def show():
    plants = db.session.query(db.Plant).all()
    return render_template("show.html", plants=plants)

@app.route("/delete/<int:id>")
def delete(id):
    plant = db.session.query(db.Plant).filter_by(id = id).first()

    db.session.delete(plant)
    db.session.commit()

    plants = db.session.query(db.Plant).all()
    return render_template("show.html", plants=plants)

@app.route("/update/<int:id>", methods=['GET','POST'])
def update(id):
    plant = db.session.query(db.Plant).filter_by(id = id).first()

    if request.method == "POST":
        specie = request.form.get("specie")
        created_at = request.form.get("created_at")
        observations = request.form.get("observations")

        if specie and created_at:
            plant.specie = specie
            plant.created_at = created_at
            plant.observations = observations

            db.session.commit()

            return redirect(url_for("show"))

    return render_template("update.html", plant=plant)

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))
