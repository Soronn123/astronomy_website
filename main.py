import datetime
from flask import Flask, render_template, request, redirect, session
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from data import db_session
from data.users import User
from data.create_post import Post
from data.needs import check_password, get_hashed_password
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import string
import secrets


app = Flask(__name__)
app.config['SECRET_KEY'] = 'astrnomy_secret_key'
app.permanent_session_lifetime = datetime.timedelta(days=8)
#app.config["SOLALCHEMY_DATABASE_URI"] = "sqlite:///astronomy.db"

login_manager = LoginManager(app)

code_for_email = ""
param_for_user = []


def main():
    db_session.global_init("db/astronomy.db")
    app.run(port=8080, host='127.0.0.1', debug=True)


def settings_user():
    if current_user.is_authenticated:
        pass


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/')
def index():
    user = "гость"
    if current_user.is_authenticated:
        user = db_session.create_session().query(User).filter(User.id == current_user.id).first().nickname
    return render_template("main.html", user=user)


@app.route('/lecture')
def str_1():
    return render_template("lecture.html")


@app.route('/lecture')
def str_2():
    return render_template("lecture.html")


@app.route('/scientist')
def str_3():
    return render_template("scientist.html")


@app.route('/shop')
def str_4():
    return render_template("shop.html")


@app.route('/guest', methods=['POST', 'GET'])
@login_required
def str_5():
    if request.method == 'POST':
        redirect()
    else:
        users = db_session.create_session().query(User).filter(User.id == current_user.id).first()
        return render_template("guest.html", nickname=users.nickname, id=users.id, email=users.email,
                               user=users.nickname, img="../static/img/ava/" + str(users.avatar),
                               role=users.role)


@app.route("/create_post")
def str_6():
    if request.method == "POST":
        title = request.form["title"]
        intro = request.form["intro"]
        text = request.form["text"]

        create_post = ()
    else:
        return render_template("create_post.html")


@app.route("/register", methods=['POST', 'GET'])
def str_7():
    global code_for_email, param_for_user
    message = ""
    if request.method == 'POST':
        nickname = request.form["nickname"]
        email = request.form["email"]
        password = request.form["password"]
        rep_password = request.form["rep_password"]

        if password != rep_password:
            message = "Пароли не совпадают"
            return render_template('register.html', message=message, )

        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == email).first():
            message = "Такой пользователь уже есть"
            return render_template('register.html', message=message)

        if len(email) == 0 or len(nickname) == 0 or len(password) == 0:
            message = "Не заполнены поля"
            return render_template('register.html', message=message)

        sender = "bratsk.post@yandex.ru"
        password_sender = "post-bratsk2023"

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = email
        msg['Subject'] = 'Код подтверждения почты!'

        alphabet = string.ascii_letters + string.digits
        body = ''.join(secrets.choice(alphabet) for i in range(8))
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
        server.login(sender, password_sender)
        server.send_message(msg)
        server.quit()
        code_for_email = body
        param_for_user = [nickname, email, password]
        return redirect("/register_2_step")
    else:
        return render_template('register.html', message=message)


@app.route("/register_2_step", methods=['POST', 'GET'])
def str_8():
    message = ""
    if request.method == 'POST':
        code_for_email2 = request.form["code_for_email"]
        if code_for_email == code_for_email2:
            db_sess = db_session.create_session()

            user = User(
                nickname=param_for_user[0],
                email=param_for_user[1],
                hashed_password=get_hashed_password(param_for_user[2])
            )

            db_sess.add(user)
            db_sess.commit()

            login_user(user, remember=True)

            return redirect("/")
        else:
            message = "Код неправильный"
            return render_template('register_2_step.html', message=message)
    else:
        return render_template('register_2_step.html', message=message)


@app.route("/login", methods=['POST', 'GET'])
def str_9():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]

        db_sess = db_session.create_session()

        if not(db_sess.query(User).filter(User.email == email).first()):
            message = "Такого пользователь нет"
            return render_template('login.html', message=message)
        check_user = db_sess.query(User).filter(User.email == email).first()

        if not(check_password(password, check_user.hashed_password)):
            message = "Пароли не совпадают"
            return render_template('login.html', message=message)

        login_user(check_user, remember=True)

        return redirect("/guest")
    else:
        return render_template("login.html")


if __name__ == '__main__':
    main()