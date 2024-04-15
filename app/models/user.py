from flask_login import UserMixin, login_required
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login

class User(UserMixin):
    def __init__(self, uid, email, firstname, lastname, password, balance=0, role_indicator=0):
        self.id = uid
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.balance = balance
        self.role_indicator = role_indicator

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute(
            """
            SELECT uid, email, firstname, lastname, password, balance, role_indicator
            FROM Users
            WHERE email = :email
            """,
            email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][4], password):
            print(check_password_hash(rows[0][4], password))
            print(password == rows[0][4])
            # incorrect password
            return None
        else:
            return User(*rows[0])


    @staticmethod
    def update_user_info(id, email, password, firstname, lastname):
        if User.email_exists(email):
            return None
        try:
            rows = app.db.execute(
                """
                UPDATE Users
                SET email = :email, password = :password, firstname = :firstname, lastname = :lastname
                WHERE uid = :id
                """,
                email=email, firstname=firstname, lastname=lastname,
                password=generate_password_hash(password), id=id)
            return rows
        except Exception as e:
            print(str(e))
            return None
        

    @staticmethod
    def email_exists(email):
        rows = app.db.execute(
            """
            SELECT email
            FROM Users
            WHERE email = :email
            """,
            email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname, balance = 0, role_indicator = 0):
        try:
            rows = app.db.execute(
                """
                INSERT INTO Users(email, password, firstname, lastname, balance, role_indicator)
                VALUES(:email, :password, :firstname, :lastname, :balance, :role_indicator)
                RETURNING uid
                """,
                email=email,
                password=generate_password_hash(password),
                firstname=firstname, lastname=lastname,
                balance = balance, role_indicator = role_indicator)

            uid = rows[0][0]
            return User.get(uid)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(uid):
        rows = app.db.execute(
            """
            SELECT uid, email, firstname, lastname, balance, role_indicator
            FROM Users
            WHERE uid = :uid
            """, 
            uid=uid)

        if not rows:
            return None
        else:
            return User(*rows[0])

    @staticmethod
    def getRole(uid):
        role = app.db.execute(
            """
            SELECT role_indicator
            FROM Users
            WHERE uid = :uid
            """,
            uid=uid)[0][0]

        return role

    @staticmethod
    def update_user_role(id, role):
        print("model entered", role)
        app.db.execute(
                """
                UPDATE Users
                SET role_indicator = :role
                WHERE uid = :id
                """,
                role=role, id=id)