import os

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from cs50 import SQL
from helpers import apology, login_required

from db.controller import TablesController
from db.cards_picker import CardsPicker
from db.images import ImagesController

UPLOAD_FOLDER = 'static/images/upload'
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif'}
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = SQL("sqlite:///db/drawthis.db")
tables = TablesController(db, "_en")
draw = CardsPicker(tables)
images = ImagesController(db, app.config["UPLOAD_FOLDER"])

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

@app.route("/logout")
def logout():
    session.clear();
    return redirect("/")


@app.route("/home")
@login_required
def home():
    uploads = images.filter_by_user(session["user_id"])
    return render_template("home.html", user = session["username"], uploads=uploads)

@app.route("/gallery")
def gallery():
    images_data = images.list()
    print("-------------------")
    print(images_data)
    print("-------------------")
    return render_template("gallery.html", images=images_data)

@app.route("/upload")
@login_required
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
   if request.method == 'POST':
      #gets file from upload form
      file = request.files['file']
      #checks file extention
      extention = os.path.splitext(file.filename)[1]
      if extention not in ALLOWED_EXTENSIONS:
          return redirect("/upload")
      else:
          #writes file to db, gets filename and id
          file_db = images.create(session["user_id"], extention)
          file_path = os.path.join(images.dir, file_db["filename"])
          #saves file
          file.save( file_path )
          #updates image path in db
          images.update(file_db["id"], file_path)
          return redirect("/image?path=" + file_db["filename"])

@app.route('/image')
def image():
    img_path = request.args.get("path")
    return render_template("image.html", img_path=img_path, dir = app.config["UPLOAD_FOLDER"])

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
