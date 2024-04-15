from flask import current_app as app

class Reviews:
    def __init__(self, target_id, buyer_id, rating, review_time, upvotes, content):
        self.buyer_id = buyer_id
        self.target_id = target_id
        self.rating = rating
        self.review_time = review_time
        self.upvotes = upvotes
        self.content = content
        pass

    def get_reviews_for_seller(buyer_id):
        rows = app.db.execute('''
SELECT sr.seller_id, sr.buyer_id, sr.rating, sr.review_time, sr.upvotes, sr.content
FROM SellerReview as sr
WHERE sr.buyer_id = :buyer_id
ORDER BY sr.review_time DESC
LIMIT 5
''', buyer_id=buyer_id)
        return [Reviews(*(r)) for r in rows] if rows else None
    
    def get_reviews_for_products(buyer_id):
        rows = app.db.execute('''
SELECT pr.iid, pr.buyer_id, pr.rating, pr.review_time, pr.upvotes, pr.content
FROM ProductReview as pr
WHERE pr.buyer_id = :buyer_id
ORDER BY pr.review_time DESC
LIMIT 5
''', buyer_id=buyer_id)
        return [Reviews(*(r)) for r in rows] if rows else None
    
    def get_reviews_received(seller_id):
        rows = app.db.execute('''
SELECT sr.seller_id, sr.buyer_id, sr.rating, sr.review_time, sr.upvotes, sr.content
FROM SellerReview as sr
WHERE sr.seller_id = :seller_id
ORDER BY sr.review_time DESC
LIMIT 5
''', seller_id=seller_id)
        return [Reviews(*(r)) for r in rows] if rows else None