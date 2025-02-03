import os
import secrets

from flask import Flask, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
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
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"


# SQLAlchemy setup
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Database Models
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    short_description: Mapped[str] = mapped_column(String, nullable=True)
    map_url: Mapped[str] = mapped_column(String, nullable=False)
    img_url: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str] = mapped_column(String(100), nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    seats: Mapped[int] = mapped_column(Integer, nullable=False)
    coffee_price: Mapped[float] = mapped_column(Float, nullable=False)


with app.app_context():
    db.create_all()


# Forms
class CafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    short_description = StringField("Short Description")
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
def home():
    all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
    return render_template("home.html", cafes=all_cafes)


@app.route("/add-cafe", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    print("Validate on submit:", form.validate_on_submit())
    if form.validate_on_submit():
        new_cafe = Cafe()
        new_cafe.name = form.data.get("name")
        new_cafe.short_description = form.data.get("short_description")
        new_cafe.map_url = form.data.get("map_url")
        new_cafe.img_url = form.data.get("img_url")
        new_cafe.location = form.data.get("location")
        new_cafe.has_sockets = form.data.get("has_sockets")
        new_cafe.has_toilet = form.data.get("has_toilet")
        new_cafe.has_wifi = form.data.get("has_wifi")
        new_cafe.can_take_calls = form.data.get("can_take_calls")
        new_cafe.seats = form.data.get("seats")
        new_cafe.coffee_price = form.data.get("coffee_price")

        db.session.add(new_cafe)
        db.session.commit()
        # print("Form Data:", form.data)
        return redirect("/")
    return render_template("add_cafe.html", form=form)


@app.route("/edit-cafe/<int:id>", methods=["GET", "POST"])
def edit_cafe(id):
    cafe = db.session.execute(db.select(Cafe).where(Cafe.id == id)).scalar()
    form = CafeForm()

    print("Validate on submit:", form.validate_on_submit())
    if form.validate_on_submit():
        cafe.name = form.data.get("name")
        cafe.short_description = form.data.get("short_description")
        cafe.map_url = form.data.get("map_url")
        cafe.img_url = form.data.get("img_url")
        cafe.location = form.data.get("location")
        cafe.has_sockets = form.data.get("has_sockets")
        cafe.has_toilet = form.data.get("has_toilet")
        cafe.has_wifi = form.data.get("has_wifi")
        cafe.can_take_calls = form.data.get("can_take_calls")
        cafe.seats = form.data.get("seats")
        cafe.coffee_price = form.data.get("coffee_price")

        db.session.commit()
        return redirect(f"/view-cafe/{id}")

    form.name.data = cafe.name
    form.short_description.data = cafe.short_description
    form.map_url.data = cafe.map_url
    form.img_url.data = cafe.img_url
    form.location.data = cafe.location
    form.has_sockets.data = cafe.has_sockets
    form.has_toilet.data = cafe.has_toilet
    form.has_wifi.data = cafe.has_wifi
    form.can_take_calls.data = cafe.can_take_calls
    form.seats.data = cafe.seats
    form.coffee_price.data = cafe.coffee_price
    form.submit.label.text = "Update Cafe"

    return render_template("add_cafe.html", form=form, is_edit=True, cafe=cafe)


@app.route("/view-cafe/<int:cafe_id>")
def view_cafe(cafe_id):
    the_cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
    return render_template("cafe_details.html", cafe=the_cafe)


if __name__ == "__main__":
    app.run(debug=True)
