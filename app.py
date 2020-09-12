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
from db.deck import Deck

# from db.SessionController import SessionController
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
app_db = SQL("sqlite:///drawthis_app.db")

tables = TablesController(db, "_en")
picker = CardsPicker(tables)
ctrl = Controller(app_db)

@app.route("/", methods=["GET", "POST"])
@app.route("/custom/<deck_id>/<lvl>", methods=["GET", "POST"])
def index(deck_id="", lvl=""):
    #if request for custom deck id
    if deck_id != "":
        #chech deck exists
        deck = ctrl.decks.find(deck_id)[0]
        if deck:
            #if deck has not been loaded yet, load deck
            if session.get('deck_id') or session.get('deck_id') != deck_id:
                ctrl.custom_deck(session['user_id'],deck_id)
                session['deck_id'] = deck_id
        #set value of draw to alt_picker
        draw = ctrl.alt_picker
        if lvl != "_":
            draw.level = int(lvl)
    #if no request for custom deck
    else:
        #set draw to default picker
        draw = picker

    if request.method == "GET":
        #shuffles and then gets values of cards.
        draw.pick()
        cards = draw.card
        #details returns info on the current deck, level etc.
        details = draw.details()
        return render_template("index.html", cards = cards, details = details)

    #if method is POST
    else:
        custom_deck = request.form.get('custom-deck')
        level = int(request.form.get('level'))
        print("------------- ELSE IN APP:")
        print(custom_deck)
        print(level)

        if custom_deck == "True":
            print("custom_deck = True")
            deck = request.form.get('deck')
            return redirect(url_for('index', deck_id=int(deck), lvl=int(level)))

        else:
            print("custom_deck not true")
            draw = picker
            draw.change_level(level)
            new_language = request.form.get('language')
            if new_language and new_language != request.form.get('curr_language'):
                draw.change_language(new_language)
            return redirect("/")

@app.route("/gallery")
def gallery():
    images_data = ctrl.read(ctrl.uploads.gallery())
    return render_template("gallery.html", images=images_data)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        usernames = ctrl.users.usernames()
        return render_template("register.html", usernames = usernames)
    else:
        #saves form data to a dict
        data={}
        data['username'] = request.form.get("username")
        #hasehs password and stores hash
        password = request.form.get("password")
        data['hash'] = generate_password_hash(password)
        #default user type
        data['type'] = "user"
        #writes data to db
        session['user_id'] = ctrl.create_user(data)
        user = ctrl.users.find(session['user_id'])[0]
        session['username'] = user['username']
        session['avatar'] = user['avatar']
        return redirect("/home")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        user_row = app_db.execute("SELECT * FROM users WHERE username = :username", username = username)
        if len(user_row) != 1:
            flash("username and or password don't match :/")
            return redirect("/login")
        if check_password_hash(user_row[0]['hash'], password):
            session["user_id"] = user_row[0]["id"]
            session["username"] = username
            user = ctrl.users.find(session['user_id'])[0]
            session["avatar"] = user["avatar"]
            session["decks"] = ctrl.decks.all_from_user(session['user_id'])
            if user_row[0]["type"] == "admin":
                session["admin"] = True
            return redirect("/home")
        else:
            flash("username and or password don't match :/")
            return redirect("/login")

@app.route("/logout")
def logout():
    session.clear();
    return redirect("/")

@app.route("/home")
@login_required
def home():
    return render_template("home.html")

@app.route("/my_bookmarks", methods=["GET", "POST"])
@login_required
def bookmarks():
    if request.method == "GET":
        content = ctrl.user_bookmarks(session["user_id"])
        return render_template("my_bookmarks.html", content = content)
    else:
        action = request.form.get("action")
        bookmark_id = request.form.get("id")
        if action == "delete":
            ctrl.bookmarks.delete(bookmark_id);
            return redirect("/my_bookmarks")
        else:
            return redirect("/upload")

@app.route("/my_uploads")
@login_required
def uploads():
    content = ctrl.read(ctrl.uploads.all_from_user(session['user_id']))
    return render_template("my_uploads.html", content = content)

@app.route("/my_decks", methods=["GET", "POST"])
@login_required
def decks():
    if request.method =="GET":
        content = ctrl.decks.all_from_user(session['user_id'])
        return render_template("my_decks.html", content = content)
    else:
        action = request.form.get('action')

        if action == 'create':
            deck = {}
            deck['name']=request.form.get('name')
            deck['user_id'] = session['user_id']
            deck_id = ctrl.decks.add(deck)
            if deck_id:
                session["decks"] = ctrl.decks.all_from_user(session['user_id'])
                session['deck_id'] = deck_id
                ctrl.custom_deck(session['user_id'], deck_id)
                flash("deck successfully created")
                return redirect("/backstage")
            else:
                flash("something went wrong")
                return redirect('/my_decks')

        elif action == 'delete':
            deck_id = request.form.get('id')
            ctrl.delete_deck(deck_id)
            session["decks"] = ctrl.decks.all_from_user(session['user_id'])
            flash("deck successfully deleted")
            return redirect('/my_decks')

        else:
            deck_id = request.form.get('id')
            session['deck_id'] = deck_id
            ctrl.custom_deck(session['user_id'], deck_id)
            return redirect("/backstage")

@app.route("/my_settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "GET":
        usernames = ctrl.users.usernames()
        return render_template("my_settings.html", usernames = usernames)
    else:
        action = request.form.get('action')
        #updates avatar id in db and gets new path saved in session
        if action == 'avatar':
            ctrl.update_user_avatar(session['user_id'])
            user = ctrl.users.find(session['user_id'])[0]
            session['avatar'] = user['avatar']
            return redirect('/my_settings')
        else:
            #for password and username updates, password validation is required
            validate = request.form.get('validate')
            user = ctrl.users.find(session['user_id'])[0]
            data={}
            if check_password_hash(user['hash'], validate):
                if action == 'change password':
                    #hashes new password and saves hash to db.
                    new_password = request.form.get('password')
                    data['hash'] = generate_password_hash(new_password)
                else:
                    #updates username in db
                    new_username = request.form.get('username')
                    data['username'] = new_username

                ctrl.users.update(session['user_id'], data)
                user = ctrl.users.find(session['user_id'])[0]
                session['username'] = user['username']
                flash("changes were successfully applied :D")
            else:
                flash("sorry, we could not validate your password")
            return redirect('/my_settings')

@app.route("/backstage", methods=["GET", "POST"])
def backstage():
    src = ctrl.alt_deck
    deck_info = ctrl.decks.find(session['deck_id'])[0]
    if request.method == "GET":
        table_names = src.table_names
        selected_table = request.args.get("table")
        if selected_table:
            table = src.get_table(selected_table)
            print(table)
        else:
            table = None
        return render_template("backstage.html", table_names = table_names, table = table, name = deck_info['name'])
    else:
        table_name = request.form.get("table_name")
        action = request.form.get("button")
        if action == "add":
            input_data = {}
            table_columns = src.tables[table_name].columns
            for name in table_columns:
                input = request.form.get(name)
                if input:
                    input_data[name] = input

            src.add(table_name, input_data)

        else:
            item_id = request.form.get("item_id")
            src.destroy(table_name,item_id)

        return redirect("/backstage?table=" + table_name)

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
          file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_db['filename'])
          #saves file
          file.save( file_path )
          #updates image path in db
          ctrl.uploads.update( file_db['id'], {'path':file_path})
          return redirect("/image?img=" + str(file_db['id']))

@app.route('/image', methods=['GET', 'POST'])
def image():
    if request.method == "GET":
        img_id = int(request.args.get("img"))
        image = ctrl.read(ctrl.uploads.find(img_id))
        if image:
            return render_template("image.html", image=image[0])
        else:
            return render_template("image.html", error = "image not found")

    else:

        action = request.form.get('button')
        image_id = int(request.form.get('image_id'))
        #deletes image entry in db and image file
        if action == 'delete':
            ctrl.delete_upload(image_id)
            return redirect("/my_uploads")
        else:
            #updates image data and displays updated
            form = request.form
            ctrl.update_upload(image_id, form)
            return redirect("/image?img=" + str(image_id))

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
