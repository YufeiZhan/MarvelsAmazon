from flask import current_app as app


class Cart:
    entry_per_page = 10

    def __init__(self, uid, iid, quantity, status):
        self.uid = uid
        self.iid = iid
        self.quantity = quantity
        self.status = status

    @staticmethod
    def get_all_by_uid_with_price(id):
        rows = app.db.execute(
            '''
            SELECT uid, CartItems.iid, quantity, status, unit_price
            FROM CartItems
            JOIN Inventory USING (iid)
            WHERE uid = :id
            ''',id=id)
        
        return [CartWithPrice(*row) for row in rows] if rows else []

    @staticmethod
    def get_page(id,n):
        offset = (n-1)* Cart.entry_per_page

        rows = app.db.execute(
            '''
            SELECT uid, iid, quantity, status
            FROM CartItems
            WHERE uid = :id
            LIMIT :n OFFSET :start;
            ''', id=id, n=Cart.entry_per_page, start=offset)

        return [CartWithPrice(*row) for row in rows] if rows else []

    @staticmethod
    def remove_item(userid,inventoryid):
        rows = app.db.execute(
            '''
            DELETE FROM CartItems
            WHERE uid = :uid AND iid = :iid ;
            ''', uid=userid, iid=inventoryid) 

    @staticmethod
    def decrease_item(userid, inventoryid):
        rows = app.db.execute(
            '''
            UPDATE CartItems
            SET quantity = quantity - 1
            WHERE uid = :uid AND iid = :iid ;
            ''', uid=userid, iid=inventoryid)

    @staticmethod
    def increase_item(userid, inventoryid):
        rows = app.db.execute(
            '''
            UPDATE CartItems
            SET quantity = quantity + 1
            WHERE uid = :uid AND iid = :iid ;
            ''', uid=userid, iid=inventoryid)
    
    @staticmethod
    def remove_all(userid):
        rows = app.db.execute(
            '''
            DELETE FROM CartItems
            WHERE uid = :uid
            ''', uid=userid)


class CartWithPrice:

    def __init__(self, uid, iid, quantity, status, unit_price):
        self.uid = uid
        self.iid = iid
        self.quantity = quantity
        self.status = status
        self.unit_price = unit_price
    
    @staticmethod
    def get_total_price(items):
        return sum([item.unit_price * item.quantity for item in items])