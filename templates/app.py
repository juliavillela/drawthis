import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from models.db import DB
from db_requests import get_cards
# Configure application
app = Flask(__name__)
db = DB("drawthis.db")
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#routes
@app.route("/")
def index():
    cards = get_cards()
    return render_template("index.html", cards=cards)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "GET":
        table = db.table_names
        adjectives = db.get_all_from('adjectives')
        subjects = db.get_all_from('subjects')
        tables = [subjects, adjectives]
        return render_template("admin.html", tables = tables)
    else:
        data = request.form
