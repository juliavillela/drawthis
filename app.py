import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from cs50 import SQL
from helpers import apology, login_required

from db.controller import TablesController
from db.cards_picker import CardsPicker

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///db/drawthis.db")
tables = TablesController(db, "_en")
draw = CardsPicker(tables)

#routes
@app.route("/")
def index():
    new_language = request.args.get("lang")
    new_level = request.args.get("level")

    if new_language:
        draw.change_language("_" + new_language)
    if new_level:
        draw.change_level(new_level)

    cards = draw.pick()
    level = draw.level
    return render_template("index.html", cards = cards, level = level)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        hash = generate_password_hash(password)

        db.execute("INSERT INTO users (username, hash, type) VALUES (:username, :hash, 'user')", username = username, hash=hash)
        session["user_id"] = db.execute("SELECT id FROM users WHERE username = :username", username = username)
        session["username"] = username
        return redirect("/home")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        user_row = db.execute("SELECT * FROM users WHERE username = :username", username = username)
        if len(user_row) == 1:
            if check_password_hash(user_row[0]['hash'], password):
                session["user_id"] = user_row[0]["id"]
                session["username"] = username
                if user_row[0]["type"] == "admin":
                    session["admin"] = True
                return redirect("/home")
            else:
                return redirect("/login", message = "please check password and username and try again. :)")


@app.route("/home")
@login_required
def home():
    return render_template("home.html", user = session["username"])

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "GET":
        #if user selected table, display table, else, display only table links
        selected_table = request.args.get("table")
        table_names = tables.tables
        if selected_table:
            table = tables.get_table(selected_table)
        else:
            table = None
        return render_template("admin.html", table_names = table_names, table = table)

    else:
        table_name = request.form.get("table_name")
        action = request.form.get("button")
        if action == "add":
            input_data = {}
            table_columns = tables.tables[table_name].columns
            for name in table_columns:
                input = request.form.get(name)
                if input:
                    input_data[name] = input

            tables.add(table_name, input_data)

        else:
            item_id = request.form.get("item_id")
            tables.destroy(table_name,item_id)

        return redirect("/admin?table=" + table_name)
