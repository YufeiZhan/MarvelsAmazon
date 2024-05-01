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

    def get_reviews_for_some_seller(buyer_id, seller_id):
        rows = app.db.execute('''
SELECT sr.seller_id, sr.buyer_id, sr.rating, sr.review_time, sr.upvotes, sr.content
FROM SellerReview as sr
WHERE sr.buyer_id = :buyer_id
    AND sr.seller_id = :seller_id
ORDER BY sr.review_time DESC
''', buyer_id=buyer_id, seller_id=seller_id)
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
    
    def remove_seller_review(seller_id, buyer_id):
        rows = app.db.execute('''
DELETE FROM SellerReview as sr
WHERE sr.seller_id = :seller_id AND sr.buyer_id = :buyer_id;
''', seller_id=seller_id, buyer_id=buyer_id)
        return rows

    def get_reviews_for_some_product(buyer_id, iid):
        rows = app.db.execute('''
SELECT pr.iid, pr.buyer_id, pr.rating, pr.review_time, pr.upvotes, pr.content
FROM ProductReview as pr
WHERE pr.buyer_id = :buyer_id
    AND pr.iid = :iid                              
ORDER BY pr.review_time DESC
''', buyer_id=buyer_id, iid=iid)
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
    
    def remove_product_review(iid, buyer_id):
        rows = app.db.execute('''
DELETE FROM ProductReview as pr
WHERE pr.iid = :iid AND pr.buyer_id = :buyer_id;
''', iid=iid, buyer_id=buyer_id)
        return rows

#     def get_reviews_received(seller_id):
#         rows = app.db.execute('''
# SELECT sr.seller_id, sr.buyer_id, sr.rating, sr.review_time, sr.upvotes, sr.content
# FROM SellerReview as sr
# WHERE sr.seller_id = :seller_id
# ORDER BY sr.review_time DESC
# ''', seller_id=seller_id)
#         return [Reviews(*(r)) for r in rows] if rows else None
    
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
    
    def update_content(buyer_id, target_id, target_type, new_content, new_rating, last_edit):
        if target_type=='1':
            rows = app.db.execute('''
UPDATE SellerReview
SET content = :new_content, rating =:new_rating, review_time =:last_edit
WHERE seller_id = :seller_id AND buyer_id = :buyer_id;
''', seller_id=target_id, buyer_id=buyer_id, new_content=new_content, new_rating=new_rating, last_edit=last_edit)
        else:
            rows = app.db.execute('''
UPDATE ProductReview
SET content = :new_content, rating =:new_rating, review_time =:last_edit
WHERE iid = :iid AND buyer_id = :buyer_id;
''', iid=target_id, buyer_id=buyer_id, new_content=new_content, new_rating=new_rating, last_edit=last_edit)
        return rows