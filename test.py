import sqlite3
from data import db_session
from data.users import User
from data.needs import get_hashed_password, check_password

db_session.global_init("db/astronomy.db")
db_sess = db_session.create_session()
email = "Shirosik@yandex.ru"
password = "nnn"
s = db_sess.query(User).filter(User.email == email).first()
b = s.hashed_password

print(check_password(password, b))


