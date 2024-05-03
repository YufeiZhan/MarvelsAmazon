from flask import current_app as app

class InventoryItem:
    def __init__(self, iid, pid, seller_id, product_name, unit_price, quantity_available, description, type, image_url):
        self.iid = iid
        self.pid = pid
        self.seller_id = seller_id
        self.product_name = product_name
        self.unit_price = unit_price
        self.quantity_available = quantity_available
        self.description = description
        self.type = type
        self.image_url = image_url

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
    Inventory.unit_price, Inventory.quantity_available, Products.description, Products.type, Products.image_url
    FROM Inventory
    JOIN Products ON Inventory.pid = Products.pid
    WHERE Inventory.seller_id = :seller_id
    ORDER BY Inventory.iid
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

    @staticmethod
    def update_quantity(iid, quantity_available, seller_id):
        if quantity_available < 0:
            return False 
        try:
            app.db.execute('''
            UPDATE Inventory
            SET quantity_available = :quantity_available
            WHERE iid = :iid AND seller_id = :seller_id
            ''', iid= iid, quantity_available= quantity_available, seller_id= seller_id)
            return True
        except Exception as e:
            print(f"Error updating inventory: {str(e)}")
            return False

    @staticmethod
    def delete(iid, seller_id):
        try:
            app.db.execute('''
            DELETE FROM Cartitems
            WHERE iid = :iid
            ''', iid=iid)

            app.db.execute('''
            DELETE FROM OrderItems
            WHERE iid = :iid
            ''', iid= iid)

            app.db.execute('''
            DELETE FROM ProductReview
            WHERE iid = :iid
            ''', iid= iid)

            app.db.execute('''
            DELETE FROM Inventory
            WHERE iid = :iid AND seller_id = :seller_id
            ''', iid= iid, seller_id= seller_id)
            return True
        except Exception as e:
            print(f"Error deleting inventory item: {str(e)}")
            return False

    @staticmethod
    def get_current_quantity(iid, seller_id):
        result = app.db.execute('''
        SELECT quantity_available
        FROM Inventory
        WHERE iid = :iid
        ''', iid= iid, seller_id= seller_id)
        if result:
            return result[0][0]
        else:
            return None

    def get_sale_orders(seller_id, page, per_page):
        offset = (page - 1) * per_page
        rows = app.db.execute("""
        SELECT Orders.oid, address, time_placed, 
        ROUND(CAST(SUM(OrderItems.quantity_purchased * Inventory.unit_price * Orders.discount) AS NUMERIC), 2) AS total_amount,
        SUM(OrderItems.quantity_purchased) AS total_items,
        CASE
                WHEN COUNT(CASE WHEN OrderItems.item_status = 'fulfilled' THEN 1 END) = COUNT(*) THEN 'Fulfilled'
                WHEN COUNT(CASE WHEN OrderItems.item_status = 'cancelled' THEN 1 END) = COUNT(*) THEN 'Canceled'
                WHEN COUNT(CASE WHEN OrderItems.item_status = 'placed' THEN 1 END) = COUNT(*) THEN 'Placed'
                WHEN COUNT(CASE WHEN OrderItems.item_status = 'in delivery' THEN 1 END) = COUNT(*) THEN 'In Delivery'
                ELSE 'Pending'
            END AS fulfillment_status
        FROM Orders
        INNER JOIN  
            OrderItems ON Orders.oid = OrderItems.oid
        INNER JOIN
            Inventory ON OrderItems.iid = Inventory.iid
        WHERE seller_id = :seller_id
        GROUP BY Orders.oid
        ORDER BY time_placed DESC
        LIMIT :limit OFFSET :offset
        """, seller_id = seller_id, 
        limit=per_page, offset = offset
        )
        return rows

    def count_sale_orders(seller_id):
        result = app.db.execute("""
        SELECT COUNT(DISTINCT Orders.oid)
        FROM Orders
        INNER JOIN OrderItems ON Orders.oid = OrderItems.oid
        INNER JOIN Inventory ON OrderItems.iid = Inventory.iid
        WHERE Inventory.seller_id = :seller_id
        """, seller_id = seller_id)
        return result[0][0]

    def get_order_details(oid, seller_id):
        rows = app.db.execute("""
        SELECT Orders.oid, OrderItems.oiid, firstname, lastname, email, address, 
            time_placed, 
            quantity_purchased, 
            Products.name as product_name, 
            unit_price,
            item_status,
            ROUND(CAST(SUM(OrderItems.quantity_purchased * Inventory.unit_price * Orders.discount) OVER (PARTITION BY Orders.oid) AS NUMERIC), 2) as total_amount,
            SUM(OrderItems.quantity_purchased) OVER (PARTITION BY Orders.oid) as total_items,
            image_url
        FROM Orders
        INNER JOIN OrderItems ON Orders.oid = OrderItems.oid
        INNER JOIN Inventory ON OrderItems.iid = Inventory.iid
        INNER JOIN Products ON Inventory.pid = Products.pid
        INNER JOIN Users ON Orders.uid = Users.uid
        WHERE Orders.oid = :oid AND Inventory.seller_id = :seller_id
        """, oid= oid, seller_id = seller_id)
        return rows


    def mark_as_fulfilled(oiid, seller_id):
        try:
            result = app.db.execute("""
            UPDATE OrderItems SET item_status = 'fulfilled'
            WHERE oiid = :oiid AND iid IN (
                SELECT iid FROM Inventory WHERE seller_id = :seller_id
            )
            """, oiid= oiid, seller_id = seller_id)
            return result > 0
        except Exception as e:
            print(f"Error updating order item status: {e}")
            return False

        
    def get_product_popularity(seller_id):
        rows = app.db.execute("""
        SELECT Products.name, 
        SUM(OrderItems.quantity_purchased) AS total_sold,
        Inventory.unit_price
        FROM OrderItems
        JOIN Orders ON OrderItems.oid = Orders.oid
        JOIN Inventory ON OrderItems.iid = Inventory.iid
        JOIN Products ON Inventory.pid = Products.pid
        WHERE Inventory.seller_id = :seller_id
        GROUP BY Products.name, Inventory.unit_price
        ORDER BY total_sold DESC
        """, seller_id = seller_id)

        return rows
        