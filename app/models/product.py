from flask import current_app as app


class Product:
    def __init__(self, id, name, description, product_type, creator_id, avg_price):
        self.id = id
        self.name = name
        self.description = description
        self.type = product_type
        self.creator_id = creator_id
        self.avg_price = avg_price

    @staticmethod
    def get(id):
        rows = app.db.execute(
            '''
            SELECT 
                p.pid, 
                p.name, 
                p.description, 
                p.type, 
                p.creator_id, 
                ROUND(AVG(i.unit_price), 2)
            FROM 
                Products p
            JOIN 
                Inventory i ON p.pid = i.pid
            WHERE 
                p.pid = :id
            GROUP BY 
                p.pid, p.name, p.description, p.type, p.creator_id;
            ''', id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all():
        rows = app.db.execute(
            '''
            SELECT 
                p.pid, 
                p.name, 
                p.description, 
                p.type, 
                p.creator_id, 
                ROUND(AVG(i.unit_price), 2)
            FROM 
                Products p
            JOIN 
                Inventory i ON p.pid = i.pid
            GROUP BY 
                p.pid, p.name, p.description, p.type, p.creator_id;
            ''')

        return [Product(*row) for row in rows]


    @staticmethod
    def get_top_expensive(k):
        rows = app.db.execute(
            '''
            SELECT 
                p.pid, 
                p.name, 
                p.description, 
                p.type, 
                p.creator_id, 
                ROUND(AVG(i.unit_price), 2) AS avg_unit_price
            FROM 
                Products p
            JOIN 
                Inventory i ON p.pid = i.pid
            GROUP BY 
                p.pid, p.name, p.description, p.type, p.creator_id
            ORDER BY 
                avg_unit_price DESC
            LIMIT :k;
            ''', k=k)

        return [Product(*row) for row in rows]