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
from db.SessionController import SessionController
from controller import Controller

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
ctrl = Controller(db)
#routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        new_language = request.args.get("lang")
        if new_language:
            draw.change_language("_" + new_language)
        draw.pick()
        cards = draw.card
        instruction = draw.instruction_card
        level = draw.level
        return render_template("index.html", cards = cards, level = level, instruction=instruction)

    else:
        draw.level = int(request.form.get("level"))
        instruction = request.form.get("instructions")
        if instruction:
            print("instruction:" + instruction)
            draw.instructions = True
        return redirect("/")

@app.route("/gallery")
def gallery():
    images_data = ctrl.uploads.list()
    return render_template("gallery.html", images=images_data)

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
        USER = SessionController(db, session["user_id"])
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
                session["user_uploads"] = ctrl.uploads.all_from_user(session['user_id'])
                print(session["user_uploads"])
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
    uploads = ctrl.uploads.all_from_user(session["user_id"])
    bookmarks = ctrl.bookmarks.all_from_user(session["user_id"])
    return render_template("home.html", user = session["username"], uploads=uploads, bookmarks=bookmarks)

@app.route("/my_bookmarks", methods=["GET", "POST"])
def bookmarks():
    if request.method == "GET":
        content = ctrl.bookmarks.all_from_user(session["user_id"])
        return render_template("my_bookmarks.html", content = content)
    else:
        action = request.form.get("action")
        bookmark_id = request.form.get("id")
        if action == "delete":
            ctrl.bookmarks.delete(bookmark_id);
            return redirect("/my_bookmarks")
        else:
            return redirect("/upload")

@app.route("/home_")
@login_required
def edit():
    edit = request.args.get("edit")
    if edit == "uploads":
        content = ctrl.uploads.all_from_user(session['user_id'])
    elif edit == "saves":
        content = USER.saves.data
    else:
        content = USER.decks.data
    return render_template("home_.html", content = content)

@app.route("/upload")
@login_required
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
@login_required
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
          file_db = ctrl.create_upload(session['user_id'], extention)
          file_path = os.path.join(images.dir, file_db['filename'])
          #saves file
          file.save( file_path )
          #updates image path in db
          ctrl.uploads.update( file_db['id'], {'path':file_path})
          return redirect("/image?img=" + str(file_db['id']))

@app.route('/image', methods=['GET', 'POST'])
def image():
    if request.method == "GET":
        img_id = int(request.args.get("img"))
        image = ctrl.uploads.find(img_id)
        if image:
            return render_template("image.html", image=image)
        else:
            return render_template("image.html", error = "image not found")

    else:

        action = request.form.get('button')
        image_id = int(request.form.get('image_id'))
        if action == 'delete':
            ctrl.delete_upload(image_id)
        else:
            cards = request.form.get('cards')
            data_dict = {'cards': cards}
            ctrl.uploads.update(image_id, data_dict)
        return redirect("home_?edit=uploads")

@app.route('/save', methods=['GET','POST'])
def save():
    if request.method == 'POST':
        cards = request.form.get('cards')
        print(cards)
        ctrl.create_bookmark(session['user_id'], cards)
        flash("cards successfully bookmarked")
        return redirect("/")

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
