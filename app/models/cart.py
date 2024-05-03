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
        rowsNo = app.db.execute(
            '''
            UPDATE CartItems
            SET quantity = quantity + 1
            WHERE uid = :uid AND iid = :iid AND (SELECT quantity_available FROM Inventory WHERE iid = :iid) > quantity;
            ''', uid=userid, iid=inventoryid)
        
        return rowsNo
    
    @staticmethod
    def remove_all(userid):
        rows = app.db.execute(
            '''
            DELETE FROM CartItems
            WHERE uid = :uid
            ''', uid=userid)

    @staticmethod
    def get_inventories(userid):
        rows = app.db.execute(
            '''
            SELECT c.iid, c.quantity, i.quantity_available
            FROM CartItems c
            INNER JOIN Inventory i ON c.iid = i.iid
            WHERE c.uid = :uid
            ''', uid = userid
        )

        return [*rows]
    
    @staticmethod
    def decrease_inventories(iid,amount):
        app.db.execute(
            '''
            UPDATE Inventory
            SET quantity_available = quantity_available - :reduction
            WHERE iid = :iid;
            ''', iid=iid, reduction=amount)
    
    @staticmethod
    def create_order(uid,address):
        app.db.execute(
            '''
            INSERT INTO Orders(uid, address)
            VALUES (:uid, :address);
            ''', uid = uid, address = address)
        
        oid = app.db.execute(
            '''
            SELECT oid FROM Orders
            WHERE uid = :uid
            ORDER BY time_placed DESC
            LIMIT 1;
            ''', uid=uid
        )[0][0]
        return oid
    
    @staticmethod
    def create_orderitem(oid,iid,quantity):
        result = app.db.execute(
            '''
            INSERT INTO OrderItems(oid,iid,quantity_purchased)
            VALUES (:oid, :iid, :quantity)
            ''', oid=oid, iid=iid, quantity=quantity)
        return result
    
    @staticmethod
    def get_all(uid):
        rows = app.db.execute(
            '''
            SELECT iid, quantity
            FROM CartItems
            WHERE uid=:uid AND status=1
            ''', uid=uid)

        return ([*rows])

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