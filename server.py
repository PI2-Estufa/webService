import os
import db
from flask_cors import CORS
from flask import Flask, jsonify, request, render_template, flash
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

    response = {
        "temperatures": temperatures,
        "humidities": humidities,
        "pHs": pHs,
        "iluminations": iluminations,
        "water_temperatures": water_temperatures,
        "water_levels": water_levels,
        "drawer_statuses": drawer_statuses
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
    return "Ok"

@app.route('/temperatures')
def temperatures():
    day = True
    week = False
    if(day):
        temperatures_day = db.session.query(db.Temperature.created_date).filter(
        (db.Temperature.created_date) >= datetime.date.today())
        temperatureses_day = [t.created_date for t in temperatures_day]
        response = {
            "temperatureses_day": temperatureses_day
        }
        #return render_template('show_temperatures.html', temperatures=temperatures_day) 
        return jsonify(response)
    elif(week):
        passdate = datetime.date.today() - timedelta(days=7)
        temperatures_week = db.session.query(db.Temperature.created_date).filter(
        (db.Temperature.created_date) >= passdate)
        return render_template('show_temperatures.html', temperatures=temperatures_week)
    else:
        passdate = datetime.date.today() - timedelta(days=30)
        temperatures_month = db.session.query(db.Temperature.created_date).filter(
        (db.Temperature.created_date) >= passdate)
        return render_template('show_temperatures.html', temperatures=temperatures_month)


app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))