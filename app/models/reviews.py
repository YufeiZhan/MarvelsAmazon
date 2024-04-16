from flask import current_app as app

class Reviews:
    entry_per_page = 5

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
''', buyer_id=buyer_id)
        return [Reviews(*(r)) for r in rows] if rows else None
    
    def get_reviews_for_seller_count(buyer_id):
        rows = app.db.execute('''
SELECT COUNT(*)
FROM SellerReview as sr
WHERE sr.buyer_id = :buyer_id
''', buyer_id=buyer_id)
        return rows[0][0]
    
    def get_reviews_for_seller_by_page(buyer_id, page):
        offset = (page-1)* Reviews.entry_per_page
        rows = app.db.execute('''
SELECT sr.seller_id, sr.buyer_id, sr.rating, sr.review_time, sr.upvotes, sr.content
FROM SellerReview as sr
WHERE sr.buyer_id = :buyer_id
ORDER BY sr.review_time DESC
OFFSET :offset                            
LIMIT :entry_per_page
''', buyer_id=buyer_id, offset=offset, entry_per_page=Reviews.entry_per_page)
        return [Reviews(*(r)) for r in rows] if rows else None
    
    def get_reviews_for_products(buyer_id):
        rows = app.db.execute('''
SELECT pr.iid, pr.buyer_id, pr.rating, pr.review_time, pr.upvotes, pr.content
FROM ProductReview as pr
WHERE pr.buyer_id = :buyer_id
ORDER BY pr.review_time DESC
''', buyer_id=buyer_id)
        return [Reviews(*(r)) for r in rows] if rows else None

    def get_reviews_for_products_count(buyer_id):
        rows = app.db.execute('''
SELECT COUNT(*)
FROM ProductReview as pr
WHERE pr.buyer_id = :buyer_id
''', buyer_id=buyer_id)
        return rows[0][0]

    def get_reviews_for_products_by_page(buyer_id, page):
        offset = (page-1)* Reviews.entry_per_page
        rows = app.db.execute('''
SELECT pr.iid, pr.buyer_id, pr.rating, pr.review_time, pr.upvotes, pr.content
FROM ProductReview as pr
WHERE pr.buyer_id = :buyer_id
ORDER BY pr.review_time DESC
OFFSET :offset                            
LIMIT :entry_per_page
''', buyer_id=buyer_id, offset=offset, entry_per_page=Reviews.entry_per_page)
        return [Reviews(*(r)) for r in rows] if rows else None
    
    def get_reviews_received(seller_id):
        rows = app.db.execute('''
SELECT sr.seller_id, sr.buyer_id, sr.rating, sr.review_time, sr.upvotes, sr.content
FROM SellerReview as sr
WHERE sr.seller_id = :seller_id
ORDER BY sr.review_time DESC
''', seller_id=seller_id)
        return [Reviews(*(r)) for r in rows] if rows else None
    
    def get_reviews_received_count(seller_id):
        rows = app.db.execute('''
SELECT COUNT(*)
FROM SellerReview as sr
WHERE sr.seller_id = :seller_id
''', seller_id=seller_id)
        return rows[0][0]

    def get_reviews_received_by_page(seller_id, page):
        offset = (page-1)* Reviews.entry_per_page
        rows = app.db.execute('''
SELECT sr.seller_id, sr.buyer_id, sr.rating, sr.review_time, sr.upvotes, sr.content
FROM SellerReview as sr
WHERE sr.seller_id = :seller_id
ORDER BY sr.review_time DESC
OFFSET :offset                            
LIMIT :entry_per_page
''', seller_id=seller_id, offset=offset, entry_per_page=Reviews.entry_per_page)
        return [Reviews(*(r)) for r in rows] if rows else None