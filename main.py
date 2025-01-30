import os
import secrets

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    FloatField,
    IntegerField,
    StringField,
    SubmitField,
    URLField,
)
from wtforms.validators import URL, DataRequired

app = Flask(__name__)

app.config["SECRET_KEY"] = secrets.token_hex(16)


# Forms
class AddNewCafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = URLField("Map Url", validators=[DataRequired(), URL()])
    img_url = URLField("Image Url", validators=[DataRequired(), URL()])
    location = StringField("Location", validators=[DataRequired()])
    has_sockets = BooleanField("Has Sockets")
    has_toilet = BooleanField("Has Toilet")
    has_wifi = BooleanField("Has Wifi")
    can_take_calls = BooleanField("Can Take Calls")
    seats = IntegerField("Seats", validators=[DataRequired()])
    coffee_price = FloatField("Coffee Price", validators=[DataRequired()])
    submit = SubmitField("Add Cafe")


@app.route("/")
def hello_world():
    return render_template("home.html")


@app.route("/add-cafe", methods=["GET", "POST"])
def add_cafe():
    form = AddNewCafeForm()
    print("Validate on submit:", form.validate_on_submit())
    if form.validate_on_submit():
        print("Form Data:", form.data)
    return render_template("add_cafe.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
