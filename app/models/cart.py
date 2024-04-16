from flask import current_app as app


class Cart:
    entry_per_page = 10

    def __init__(self, uid, iid, quantity, status):
        self.uid = uid
        self.iid = iid
        self.quantity = quantity
        self.status = status

    @staticmethod
    def get_all_by_uid(id):
        rows = app.db.execute(
            '''
            SELECT uid, iid, quantity, status
            FROM CartItems
            WHERE uid = :id
            ''',id=id)
        
        return [Cart(*row) for row in rows] if rows else None

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

        return [Cart(*row) for row in rows] if rows else None
