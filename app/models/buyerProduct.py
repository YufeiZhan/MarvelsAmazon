from flask import current_app as app


class BuyerProduct:
    def __init__(self, seller_id, seller_name, product_name, unit_price, quantity_available, description, type):
        self.seller_id = seller_id
        self.seller_name = seller_name
        self.product_name = product_name
        self.unit_price = unit_price
        self.quantity_available = quantity_available
        self.description = description
        self.type = type

    @staticmethod
    def get_buyer_products(product_name):
        rows = app.db.execute(
            '''
            SELECT 
                u.uid,
                u.firstname || ' ' || u.lastname AS seller_name,
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
        return [BuyerProduct(*row) for row in rows]
