from flask_login import UserMixin, login_required
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from .. import login

class User(UserMixin):
    entry_per_page = 10

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
    def topup(id):
        try:
            rows = app.db.execute(
                """
                UPDATE Users
                SET balance = balance + 100
                WHERE uid = :id
                """,
                id=id
            )
            return rows
        except Exception as e:
            print(str(e))
            return None
    
    @staticmethod
    def withdraw(id, amount):
        try:
            rows = app.db.execute(
                """
                UPDATE Users
                SET balance = balance - :amount
                WHERE uid = :id
                """,
                id=id, amount=amount
            )
            return rows
        except Exception as e:
            print(str(e))
            return None
        
    @staticmethod
    def get_balance_history(id):
        try:
            records = app.db.execute("""SELECT balance, balance_timestamp FROM BalanceHistory WHERE uid = :id""", id=id)
            return records
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def update_balance_history(id):
        try:
            new_balance = app.db.execute("""SELECT balance FROM Users WHERE uid = :id""", id=id)[0][0]
            curr_timestamp = datetime.now()
            result = app.db.execute(
                """
                INSERT INTO BalanceHistory (uid, balance, balance_timestamp)
                VALUES (:uid, :new_balance, :curr_timestamp)
                """,
                uid=id, new_balance=new_balance, curr_timestamp=curr_timestamp
            )
            return result
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def update_user_info(id, email, password, firstname, lastname):
        if any(not c.isalnum()for word in firstname.split() for c in word ) or any(not c.isalnum() for word in lastname.split() for c in word)\
            or any(keyword in firstname.lower() for keyword in ['select', 'update', 'delete', 'insert'])\
            or any(keyword in lastname.lower() for keyword in ['select', 'update', 'delete', 'insert']):
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
    def check_id_with_email(email):
        rows = app.db.execute(
            """
            SELECT uid
            FROM Users
            WHERE email = :email
            """,
            email=email
        )
        return rows[0][0]

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
        if any(not c.isalnum()for word in firstname.split() for c in word ) or any(not c.isalnum() for word in lastname.split() for c in word)\
            or any(keyword in firstname.lower() for keyword in ['select', 'update', 'delete', 'insert'])\
            or any(keyword in lastname.lower() for keyword in ['select', 'update', 'delete', 'insert']):
            return None        
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
            SELECT uid, email, firstname, lastname, password, balance, role_indicator
            FROM Users
            WHERE uid = :uid
            """, 
            uid=uid)

        if not rows:
            return None
        else:
            return User(*rows[0])
    
    @staticmethod
    def get_all_public_info_by(role):
        rows = app.db.execute(
            f"""
            SELECT uid, email, firstname, lastname
            FROM Users
            WHERE role_indicator = :role
            """,
            role=role
        )
        return rows
    

    @staticmethod
    def get_balance(uid):
        rows = app.db.execute(
            """
            SELECT balance
            FROM Users
            WHERE uid = :uid
            """,
            uid=uid
        )[0][0]
        return rows

    @staticmethod
    def get_order_page(uid, n):
        offset = (n-1)* User.entry_per_page
        rows = app.db.execute(
            """
            SELECT
                o.oid AS order_id,
                o.time_placed AS order_placing_time,
                ROUND(CAST(SUM(oi.quantity_purchased * i.unit_price * o.discount) AS NUMERIC), 2) AS total_amount,
                SUM(oi.quantity_purchased) AS total_items,
            CASE
                WHEN COUNT(CASE WHEN oi.item_status = 'fulfilled' THEN 1 END) = COUNT(*) THEN 'Fulfilled'
                WHEN COUNT(CASE WHEN oi.item_status = 'canceled' THEN 1 END) = COUNT(*) THEN 'Canceled'
                WHEN COUNT(CASE WHEN oi.item_status = 'placed' THEN 1 END) = COUNT(*) THEN 'Placed'
                WHEN COUNT(CASE WHEN oi.item_status = 'in delivery' THEN 1 END) = COUNT(*) THEN 'In Delivery'
                ELSE 'Pending'
            END AS fulfillment_status
            FROM Orders o
            INNER JOIN
                OrderItems oi ON o.oid = oi.oid
            INNER JOIN
                Inventory i ON oi.iid = i.iid
            WHERE o.uid = :uid
            GROUP BY o.oid
            ORDER BY o.time_placed DESC
            LIMIT :n OFFSET :start;
            """,
            uid=uid, n=User.entry_per_page, start=offset)
        
        return rows
    
    @staticmethod
    def get_all_order(uid):
        rows = app.db.execute(
            """
            SELECT *
            FROM Orders o
            WHERE o.uid = :uid
            """, uid=uid)
    
        return rows

    @staticmethod
    def getRole(uid):
        role = app.db.execute(
            """
            SELECT role_indicator
            FROM Users
            WHERE uid = :uid
            """, uid=uid)[0][0]

        return role

    @staticmethod
    def update_user_role(id, role):
        app.db.execute(
                """
                UPDATE Users
                SET role_indicator = :role
                WHERE uid = :id
                """, role=role, id=id)

    @staticmethod
    def get_order_detail(oid):
        rows = app.db.execute(
            '''
            SELECT oiid, iid, quantity_purchased, item_status
            FROM OrderItems
            WHERE oid=:oid;
            ''', oid=oid)
        
        return ([*rows])
    
    @staticmethod
    def get_order_total(oid):
        total = app.db.execute(
            '''
            SELECT ROUND(CAST(SUM(i.unit_price * oi.quantity_purchased) AS NUMERIC),2)
            FROM OrderItems oi
            INNER JOIN Inventory i ON oi.iid=i.iid
            WHERE oid = :oid;
            ''', oid = oid
        )[0][0]

        return total