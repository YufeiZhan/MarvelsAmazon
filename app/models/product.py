from flask import current_app as app



class Product:
    entry_per_page = 8
    
    def __init__(self, id, name, description, product_type, creator_id, avg_price, image_url):
        self.id = id
        self.name = name
        self.description = description
        self.type = product_type
        self.creator_id = creator_id
        self.avg_price = avg_price
        self.image_url = image_url

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
                ROUND(AVG(i.unit_price), 2),
                p.image_url
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
                ROUND(AVG(i.unit_price), 2) AS avg_unit_price,
                p.image_url
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
        # Prepare the query string with wildcard characters for partial matching
        search_query = f"%{query}%"
        rows = app.db.execute(
            '''
            SELECT 
                p.pid, 
                p.name, 
                p.description, 
                p.type, 
                p.creator_id, 
                ROUND(AVG(i.unit_price), 2) AS avg_unit_price,
                p.image_url
            FROM 
                Products p
            JOIN 
                Inventory i ON p.pid = i.pid
            WHERE
                p.name LIKE :query OR
                p.description LIKE :query
            GROUP BY 
                p.pid, p.name, p.description, p.type, p.creator_id
            ORDER BY 
                p.pid ASC;
            ''',
            query=search_query  # Use the prepared search_query with wildcards
        )
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
                ROUND(AVG(i.unit_price), 2) AS avg_unit_price,
                p.image_url
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
                ROUND(AVG(i.unit_price), 2) AS avg_unit_price,
                p.image_url
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
                ROUND(AVG(i.unit_price), 2),
                p.image_url
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

    @staticmethod
    def get_page_with_sort(n, product_sort):
        offset = (n-1) * Product.entry_per_page

        # Define the base SQL query without the ORDER BY clause
        base_sql = """
            SELECT 
                p.pid, 
                p.name, 
                p.description, 
                p.type, 
                p.creator_id, 
                ROUND(AVG(i.unit_price), 2) AS avg_unit_price,
                p.image_url
            FROM 
                Products p
            JOIN 
                Inventory i ON p.pid = i.pid
            GROUP BY 
                p.pid, p.name, p.description, p.type, p.creator_id
        """

        # Determine the ORDER BY clause based on product_sort
        if product_sort == 'Lowest Price':
            order_clause = "ORDER BY avg_unit_price ASC"
        else:
            order_clause = "ORDER BY avg_unit_price DESC"

        # Combine the base SQL with the ORDER BY clause and pagination
        full_sql = f"{base_sql} {order_clause} LIMIT :n OFFSET :start"

        # Execute the query
        rows = app.db.execute(full_sql, n=Product.entry_per_page, start=offset)
        return [Product(*row) for row in rows]

    @staticmethod
    def post_product(id, name, description, type, image_url):
        result = app.db.execute(
            '''
            INSERT INTO Products (name, description, type, creator_id, image_url)
            VALUES (:name, :description, :type, :id, :image_url);
            ''',
            name=name, 
            description=description, 
            type=type,
            id=id,
            image_url=image_url
        )
        return result

    @staticmethod
    def get_product(id):
        row = app.db.execute(
            '''
            SELECT 
                p.name, 
                p.description, 
                p.type
            FROM 
                Products p
            WHERE 
                p.pid = :id
            ''', id=id)
        return [*row]

    @staticmethod
    def edit_product(id, name, description, type, image_url):
        result = app.db.execute(
            '''
            UPDATE Products
            SET name = :name, 
                description = :description, 
                type = :type,
                image_url = :image_url
            WHERE pid = :id;
            ''',
            name=name, 
            description=description, 
            type=type,
            id=id,
            image_url=image_url)
        return result