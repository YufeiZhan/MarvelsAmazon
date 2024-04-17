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

#     @staticmethod
#     def get_all_by_seller_id(seller_id):
#         rows = app.db.execute('''
# SELECT Inventory.iid, Inventory.pid, Inventory.seller_id, Products.name, Inventory.unit_price, Inventory.quantity_available, Products.description, Products.type
# FROM Inventory
# JOIN Products ON Inventory.pid = Products.pid
# WHERE Inventory.seller_id = :seller_id
# ''',
#                               seller_id=seller_id)
#         return [InventoryItem(*row) for row in rows]

    @staticmethod
    def get_page_by_seller_id(seller_id, page, per_page):
        offset = (page - 1) * per_page
        rows = app.db.execute('''
    SELECT Inventory.iid, Inventory.pid, Inventory.seller_id, Products.name, 
    Inventory.unit_price, Inventory.quantity_available, Products.description, Products.type
    FROM Inventory
    JOIN Products ON Inventory.pid = Products.pid
    WHERE Inventory.seller_id = :seller_id
    LIMIT :limit OFFSET :offset
    ''',
                            seller_id=seller_id,
                            limit=per_page,
                            offset=offset)
        return [InventoryItem(*row) for row in rows]

    @staticmethod
    def count_by_seller_id(seller_id):
        result = app.db.execute('''
    SELECT COUNT(*)
    FROM Inventory
    WHERE seller_id = :seller_id
    ''',
                            seller_id=seller_id)
        return result[0][0]

    @staticmethod
    def add_item(seller_id, product_name, unit_price, quantity_available):
        try: 
            result = app.db.execute('''
            SELECT pid FROM Products WHERE name = :name
        ''', name=product_name)
            pid = result[0][0]
            # print(pid)
            app.db.execute('''
        INSERT INTO Inventory (seller_id, pid, unit_price, quantity_available)
        VALUES (:seller_id, :pid, :unit_price, :quantity_available)
        ''',
                        seller_id=seller_id, pid=pid,
                        unit_price=unit_price, quantity_available=quantity_available)
        except Exception as e:
            return False
        return True

        
        