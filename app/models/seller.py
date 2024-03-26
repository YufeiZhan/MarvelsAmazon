from flask import current_app as app

class InventoryItem:
    def __init__(self, iid, pid, seller_id, product_name, unit_price, quantity_available, description, type):
        self.iid = iid
        self.pid = pid
        self.seller_id = seller_id
        self.product_name = product_name
        self.unit_price = unit_price
        self.quantity_available = quantity_available
        self.description = description
        self.type = type

    @staticmethod
    def get_all_by_seller_id(seller_id):
        rows = app.db.execute('''
SELECT Inventory.iid, Inventory.pid, Inventory.seller_id, Products.name, Inventory.unit_price, Inventory.quantity_available, Products.description, Products.type
FROM Inventory
JOIN Products ON Inventory.pid = Products.pid
WHERE Inventory.seller_id = :seller_id
''',
                              seller_id=seller_id)
        return [InventoryItem(*row) for row in rows]
