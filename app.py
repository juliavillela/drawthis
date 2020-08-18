import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

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

# session['language'] = "en"
#assign db source
db = TablesController("_en")
draw = CardsPicker(db)

#routes
@app.route("/")
def index():
    new_language = request.args.get("lang")
    new_level = request.args.get("level")

    if new_language:
        draw.change_language("_" + new_language)
    if new_level:
        draw.change_level(new_level)

    cards = draw.draw_cards()
    level = draw.level
    return render_template("index.html", cards = cards, level = level)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "GET":
        #if user selected table, display table, else, display only table links
        selected_table = request.args.get("table")
        table_names = db.tables
        if selected_table:
            table = db.get_table(selected_table)
        else:
            table = None
        return render_template("admin.html", table_names = table_names, table = table)

    else:
        table_name = request.form.get("table_name")
        action = request.form.get("button")
        if action == "add":
            input_data = {}
            table_columns = db.tables[table_name].columns
            for name in table_columns:
                input = request.form.get(name)
                if input:
                    input_data[name] = input

            db.add(table_name, input_data)

        else:
            item_id = request.form.get("item_id")
            db.destroy(table_name,item_id)

        return redirect("/admin?table=" + table_name)
