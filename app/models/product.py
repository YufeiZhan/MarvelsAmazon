from flask import current_app as app



class Product:
    entry_per_page = 10
    
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
                p.pid, p.name, p.description, p.type, p.creator_id
            ORDER BY 
                p.pid ASC;
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
                p.pid, p.name, p.description, p.type, p.creator_id
            ORDER BY 
                p.pid ASC;
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

    @staticmethod
    def get_search(query):
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
            WHERE
                p.name = :query
            GROUP BY 
                p.pid, p.name, p.description, p.type, p.creator_id
            ORDER BY 
                p.pid ASC;
            ''', query=query)

        return [Product(*row) for row in rows]

    @staticmethod
    def get_page(n):
        offset = (n-1)* Product.entry_per_page
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
            LIMIT :n OFFSET :start;
            ''', n=Product.entry_per_page, start=offset)

        return [Product(*row) for row in rows]

    @staticmethod
    def get_page_with_type(n, product_type):
        offset = (n-1)* Product.entry_per_page
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
            WHERE 
                p.type = :type
            GROUP BY 
                p.pid, p.name, p.description, p.type, p.creator_id
            ORDER BY 
                avg_unit_price DESC
            LIMIT :n OFFSET :start;
            ''', n=Product.entry_per_page, start=offset, type=product_type)

        return [Product(*row) for row in rows]

    @staticmethod
    def get_all_with_type(product_type):
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
                p.type = :type
            GROUP BY 
                p.pid, p.name, p.description, p.type, p.creator_id
            ORDER BY 
                p.pid ASC;
            ''', type=product_type)
        return [Product(*row) for row in rows]