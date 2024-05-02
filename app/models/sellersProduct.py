from flask import current_app as app


class SellersProduct:
    def __init__(self, seller_id, seller_name, inventory_id, product_name, unit_price, quantity_available, description, type):
        self.seller_id = seller_id
        self.seller_name = seller_name
        self.inventory_id = inventory_id
        self.product_name = product_name
        self.unit_price = unit_price
        self.quantity_available = quantity_available
        self.description = description
        self.type = type

    @staticmethod
    def get_seller_products(product_name):
        rows = app.db.execute(
            '''
            SELECT 
                u.uid,
                u.firstname || ' ' || u.lastname AS seller_name,
                i.iid, 
                p.name,
                i.unit_price,
                i.quantity_available,
                p.description,
                p.type
            FROM
                Products p
            JOIN
                Inventory i ON i.pid = p.pid
            JOIN 
                Users u ON i.seller_id = u.uid
            WHERE 
                p.name = :product_name
            ORDER BY 
                seller_name;
            ''', product_name=product_name)
        return [SellersProduct(*row) for row in rows]

    # ON CONFLICT (uid, iid) DO UPDATE
    # SET quantity = CartItems.quantity + :quantity
    # WHERE CartItems.iid = :iid AND CartItems.uid = :uid;
    @staticmethod
    def add_cart(userid, inventoryid, quantity):
        rows = app.db.execute(
            '''
            INSERT INTO CartItems (uid, iid, quantity, status)
            VALUES (:uid, :iid, :quantity, 1);
            ''',
            uid=userid, 
            iid=inventoryid, 
            quantity=quantity
        )
        return rows