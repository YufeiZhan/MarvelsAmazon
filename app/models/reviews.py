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

    ########## Seller reviews
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

    ########## Product reviews
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

    def get_all_reviews_for_some_product(iid, page):
        offset = (page-1)* Reviews.entry_per_page
        rows = app.db.execute('''
SELECT pr.iid, pr.buyer_id, pr.rating, pr.review_time, pr.upvotes, pr.content
FROM ProductReview as pr
WHERE pr.iid = :iid
ORDER BY pr.review_time DESC
OFFSET :offset                            
LIMIT :entry_per_page
''', iid=iid, offset=offset, entry_per_page=Reviews.entry_per_page)
        return [Reviews(*(r)) for r in rows] if rows else None    

    def get_all_reviews_for_some_product_count(iid):
        rows = app.db.execute('''
SELECT COUNT(*)
FROM ProductReview as pr
WHERE pr.iid = :iid
''', iid=iid)
        return rows[0][0]
    
    def get_summary_for_product(iid):
        rows = app.db.execute('''
SELECT AVG(pr.rating), COUNT(pr.rating)
FROM ProductReview as pr
WHERE pr.iid = :iid;
''', iid=iid)
        avg_rating = rows[0][0]
        num_reviews = rows[0][1]
        rows = app.db.execute('''
SELECT pr.rating, COUNT(pr.rating)
FROM ProductReview as pr
WHERE pr.iid = :iid
GROUP BY pr.rating;
''', iid=iid)
        return {"avg_rating":avg_rating,
                "num_reviews":num_reviews,
                "hist":rows}

    ########## Reviews received
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
    
    def get_summary_for_seller(seller_id):
        rows = app.db.execute('''
SELECT AVG(sr.rating), COUNT(sr.rating)
FROM SellerReview as sr
WHERE sr.seller_id = :seller_id;
''', seller_id=seller_id)
        avg_rating = rows[0][0]
        num_reviews = rows[0][1]
        rows = app.db.execute('''
SELECT sr.rating, COUNT(sr.rating)
FROM SellerReview as sr
WHERE sr.seller_id = :seller_id
GROUP BY sr.rating;
''', seller_id=seller_id)
        return {"avg_rating":avg_rating,
                "num_reviews":num_reviews,
                "hist":rows}

    ########## Modify the reviews
    def update_content(buyer_id, target_id, target_type, new_content, new_rating, last_edit):
        if target_type:
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
    
    def insert_content(buyer_id, target_id, target_type, new_content, new_rating, last_edit):
        if target_type:
            rows = app.db.execute('''
INSERT INTO SellerReview (seller_id, buyer_id, content, rating, review_time, upvotes)
VALUES (:seller_id, :buyer_id, :new_content, :new_rating, :last_edit, 0);
''', seller_id=target_id, buyer_id=buyer_id, new_content=new_content, new_rating=new_rating, last_edit=last_edit)
        else:
            rows = app.db.execute('''
INSERT INTO ProductReview (buyer_id, iid, content, rating, review_time, upvotes)
VALUES (:buyer_id, :iid, :new_content, :new_rating, :last_edit, 0);
''', iid=target_id, buyer_id=buyer_id, new_content=new_content, new_rating=new_rating, last_edit=last_edit)
        return rows
    
    def isexist(buyer_id, target_id, target_type):
        if target_type:
            count = app.db.execute('''
SELECT COUNT(*)
FROM SellerReview                                   
WHERE seller_id = :seller_id AND buyer_id = :buyer_id;                                  
''', seller_id=target_id, buyer_id=buyer_id)
        else:
            count = app.db.execute('''
SELECT COUNT(*)
FROM ProductReview                                   
WHERE iid = :iid AND buyer_id = :buyer_id;                 
''', iid=target_id, buyer_id=buyer_id)
        return count[0][0]
    
    def upvote(target_id, target_type, buyer_id, user_id):
        count = app.db.execute('''
SELECT COUNT(*)
FROM Upvotes                                   
WHERE target_id=:target_id AND target_type=:target_type 
AND buyer_id=:buyer_id AND user_id=:user_id;                                
''', target_id=target_id, target_type=target_type, buyer_id=buyer_id, user_id=user_id)
        if count[0][0] > 0:
            action = app.db.execute('''
UPDATE Upvotes SET upvote_status = -1 * upvote_status + 1 
WHERE target_id=:target_id AND target_type=:target_type 
AND buyer_id=:buyer_id AND user_id=:user_id;
''', target_id=target_id, target_type=target_type, buyer_id=buyer_id, user_id=user_id)
            status = app.db.execute('''
SELECT upvote_status
FROM Upvotes                                   
WHERE target_id=:target_id AND target_type=:target_type 
AND buyer_id=:buyer_id AND user_id=:user_id;                                
''', target_id=target_id, target_type=target_type, buyer_id=buyer_id, user_id=user_id)
            status=status[0][0]
        else:
            action = app.db.execute('''
INSERT INTO Upvotes (target_id, target_type, buyer_id, user_id, upvote_status) 
VALUES (:target_id, :target_type, :buyer_id, :user_id, 1);
''', target_id=target_id, target_type=target_type, buyer_id=buyer_id, user_id=user_id)
            status = 1
        if target_type==1:
            ## Update seller review table
            rows = app.db.execute('''
UPDATE SellerReview
SET upvotes = upvotes + (2 * :status-1)
WHERE seller_id = :seller_id AND buyer_id = :buyer_id;
''', seller_id=target_id, buyer_id=buyer_id, status=status)
            new_upvotes = app.db.execute('''
SELECT upvotes
FROM SellerReview
WHERE seller_id = :seller_id AND buyer_id = :buyer_id;
''', seller_id=target_id, buyer_id=buyer_id)
        else:
            ## Update product review table
            rows = app.db.execute('''
UPDATE ProductReview
SET upvotes = upvotes + (2 * :status-1)
WHERE iid = :iid AND buyer_id = :buyer_id;
''', iid=target_id, buyer_id=buyer_id, status=status)
            new_upvotes = app.db.execute('''
SELECT upvotes
FROM ProductReview
WHERE iid = :iid AND buyer_id = :buyer_id;
''', iid=target_id, buyer_id=buyer_id)
        return status, new_upvotes[0][0]

    def check_upvote(target_id, target_type, buyer_id, user_id):
        status = app.db.execute('''
SELECT upvote_status
FROM Upvotes                                   
WHERE target_id=:target_id AND target_type=:target_type 
    AND buyer_id=:buyer_id AND user_id=:user_id;                                
''', target_id=target_id, target_type=target_type, buyer_id=buyer_id, user_id=user_id)
        return status
    
    def iscustomer(target_id, buyer_id, target_type):
        if target_type:
            count = app.db.execute('''
SELECT COUNT(*)
FROM Orders as o
LEFT JOIN OrderItems as oi ON o.oid = oi.oid
LEFT JOIN Inventory as i ON oi.iid = i.iid
WHERE i.seller_id = :seller_id AND o.uid = :buyer_id;                                  
''', seller_id=target_id, buyer_id=buyer_id)
        else:
            count = app.db.execute('''
SELECT COUNT(*)
FROM Orders as o
LEFT JOIN OrderItems as oi ON o.oid = oi.oid
WHERE oi.iid = :iid AND o.uid = :buyer_id;                                  
''', iid=target_id, buyer_id=buyer_id)
        return count[0][0] > 0