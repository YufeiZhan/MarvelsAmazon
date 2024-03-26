from flask import current_app as app

class Reviews:
    def __init__(self, buyer_id, seller_id, rating, review_time, upvotes, content):
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.rating = rating
        self.review_time = review_time
        self.upvotes = upvotes
        self.content = content
        pass

    def get_reviews_for_seller(buyer_id):
        rows = app.db.execute('''
SELECT sr.buyer_id, sr.seller_id, sr.rating, sr.review_time, sr.upvotes, sr.content
FROM SellerReview as sr
WHERE sr.buyer_id = :buyer_id                                                       
''', buyer_id=buyer_id)
        return [Reviews(*(r)) for r in rows] if rows else None