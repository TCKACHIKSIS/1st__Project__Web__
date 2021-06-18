from flask import Flask, render_template, redirect, request, jsonify, url_for, send_from_directory
from datetime import datetime
import sqlite3
import os
from db.database import Database
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

DATABASE = 'db/sota.db'

app = Flask(__name__)
MAX_CONTENT_LENGHT = 1024 * 1024
db = Database(DATABASE)
db.init_db()
accounts = db.get_accounts() #Кол-во всех аккаунтов 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

flag_enter = False

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def title():
    return render_template('/title_frame/title_frame.html')

@app.route("/fail")
def title_fail():
    return render_template('/title_frame/title_frame_fail.html')

@app.route('/upload_n', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['img']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            send_from_directory(app.config['UPLOAD_FOLDER'], filename)
            return redirect('/')
    


@app.route("/check_enter", methods=['post'])
def check_enter():
    global flag_enter
    if request.form:
        login = request.form.get('login')
        password = request.form.get('password')

        user = db.get_account(login, password)
        if user == None:
            return redirect("/fail")
        else:
            flag_enter = True
            id = db.get_id(login,password)
            return redirect(f'/user_page/{id}') 

@app.route("/forgotten_password")
def for_password():
    return render_template('forgotten_password/forgotten_password.html')

@app.route("/register", methods=['post'])
def register():
    global accounts
    if request.form:
        mail = request.form.get('mail')
        login = request.form.get('login')
        password = request.form.get('password')
        user = {'login': login, 'mail': mail, 'password': password}
        db.insert_account(user)
        accounts = db.get_accounts()
    return redirect("/")


@app.route('/add')
def post_add():
    return render_template('register_form/register_form.html')


@app.route("/user_page/<int:id>")
def user_page(id):
    if id not in range(1, accounts + 1):
        return "", 404
    else:
        if flag_enter == False:
            return redirect("/")
        else:
            return render_template('user_page/user_page.html',account = db.get_account_by_Id(id))


@app.route("/messange/<int:id>")
def for_messanges(id):
    if id not in range(1, accounts + 1):
        return "", 404
    else:
        if flag_enter == False:
            return redirect("/")
        else:
            return render_template('messange_page/messange_page.html',account = db.get_account_by_Id(id))


@app.route("/followers/<int:id>")
def for_followers(id):
    if id not in range(1, accounts + 1):
        return "", 404
    else:
        if flag_enter == False:
            return redirect("/")
        else:
            return render_template('my_followers/my_followers.html',account = db.get_account_by_Id(id))


@app.route("/me_following/<int:id>")
def for_following(id):
    if id not in range(1, accounts + 1):
        return "", 404
    else:
        if flag_enter == False:
            return redirect("/")
        else:
            return render_template('me_following/me_following.html',account = db.get_account_by_Id(id))


@app.route("/news/<int:id>")
def for_news(id):
    if id not in range(1, accounts + 1):
        return "", 404
    else:
        if flag_enter == False:
            return redirect("/")
        else:
            return render_template('news/news.html',account = db.get_account_by_Id(id))
