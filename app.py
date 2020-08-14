import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from db import DB

# Configure application
app = Flask(__name__)

#assign db source
db = DB("drawthis.db")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "GET":
        table_names = db.tables
        selected_table = request.args.get("table")
        if selected_table:
            table = db.get_all_from(selected_table)
        else:
            table = None
        return render_template("admin.html", table_names = table_names, table = table)
