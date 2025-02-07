import os
import secrets
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import (
    BooleanField,
    EmailField,
    FloatField,
    IntegerField,
    PasswordField,
    StringField,
    SubmitField,
    URLField,
)
from wtforms.validators import URL, DataRequired, Email

from email_sender import EmailSender

load_dotenv()

# Get env
my_email = os.getenv("EMAIL")
my_password = os.getenv("PASSWORD")

# Initialize EmailSender
email_sender = EmailSender(
    smtp_host="smtp.gmail.com", sender_email=my_email, sender_password=my_password
)

# Flask App
app = Flask(__name__)
# FLask app configs
app.config["SECRET_KEY"] = secrets.token_hex(16)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

# Login Setup
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


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


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)


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


class ReqCafeForm(CafeForm):
    extra_info = StringField("Additional Info")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    repeat_password = PasswordField("Repeat Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


def admin_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.id == 1:
            return f(*args, **kwargs)
        else:
            return abort(403)

    return wrapper


@app.route("/")
def home():
    all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
    return render_template("home.html", cafes=all_cafes)


@app.route("/add-cafe", methods=["GET", "POST"])
@admin_only
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
    return render_template("cafe_form.html", form=form)


@app.route("/edit-cafe/<int:id>", methods=["GET", "POST"])
@admin_only
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

    return render_template("cafe_form.html", form=form, is_edit=True, cafe=cafe)


@app.route("/req-cafe", methods=["GET", "POST"])
def req_cafe():
    form = ReqCafeForm()
    form.submit.label.text = "Request New Cafe / Change"

    print("Validate on submit:", form.validate_on_submit())
    if form.validate_on_submit():
        name = form.data.get("name")
        short_description = form.data.get("short_description")
        map_url = form.data.get("map_url")
        img_url = form.data.get("img_url")
        location = form.data.get("location")
        has_sockets = form.data.get("has_sockets")
        has_toilet = form.data.get("has_toilet")
        has_wifi = form.data.get("has_wifi")
        can_take_calls = form.data.get("can_take_calls")
        seats = form.data.get("seats")
        coffee_price = form.data.get("coffee_price")
        extra_info = form.data.get("extra_info")

        email_sender.send_email(
            recipient_email=my_email,
            subject="Request for a New Cafe / Update existing Cafe.",
            email_body=f"""Cafe Name: {name}
Cafe Description: {short_description}
Cafe Map URL: {map_url}
Cafe Img URL: {img_url}
Cafe Location: {location}
Cafe has Sockets: {has_sockets}
Cafe has Toilet: {has_toilet}
Cafe has Wifi: {has_wifi}
Cafe Can Take Calls: {can_take_calls}
Cafe Seats: {seats}
Cafe Black Coffee Price: {coffee_price}
Cafe Extra Info: {extra_info}
""",
        )

        return render_template("cafe_form.html", form=form, is_req=True, msg_sent=True)

    return render_template("cafe_form.html", form=form, is_req=True)


@app.route("/view-cafe/<int:cafe_id>")
def view_cafe(cafe_id):
    the_cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
    return render_template("cafe_details.html", cafe=the_cafe)


@app.route("/delete-cafe/<int:id>")
@admin_only
def delete_cafe(id):
    the_cafe = db.session.execute(db.select(Cafe).where(Cafe.id == id)).scalar()
    db.session.delete(the_cafe)
    db.session.commit()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print(form.data)
        username = form.data.get("username")
        email = form.data.get("email")
        if db.session.execute(db.select(User).where(User.email == email)).scalar():
            flash("This email already is in use!")
            return render_template("register.html", form=form)
        pass1 = form.data.get("password")
        pass2 = form.data.get("repeat_password")
        if pass1 == pass2:
            new_user = User()
            new_user.username = username
            new_user.email = email
            new_user.password = generate_password_hash(
                password=pass1, method="pbkdf2:sha256:600000", salt_length=8
            )

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            flash("login Successful!")
            return redirect("/")
        else:
            flash("Password didn't match!")
            return render_template("register.html", form=form)
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.data)
        email = form.data.get("email")
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if user is None:
            flash("There is no account with this email!")
            return render_template("login.html", form=form)
        password = form.data.get("password")
        if not check_password_hash(pwhash=user.password, password=password):
            flash("Incorrect Password!")
            return render_template("login.html", form=form)

        login_user(user)
        return redirect("/")

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
