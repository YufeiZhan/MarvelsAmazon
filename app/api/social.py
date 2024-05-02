import math
import json

from flask_login import current_user, login_required
from flask import render_template, redirect, url_for, flash, request, jsonify

from ..models.user import User
from ..models.reviews import Reviews

from flask import Blueprint
bp = Blueprint('social', __name__)

# class User():
#     def __init__(self):
#         self.is_active = True
#         self.is_authenticated = True
#         pass

#     def get_id(self):
#         return self.id
        
@bp.route('/reviews/<int:page_sr><int:page_pr><int:page_rr>')
@bp.route('/reviews')
@login_required # Requires a user to be logged in to access this page otherwise redirect to defined login page automatically
def reviews(page_sr=1, page_pr=1, page_rr=1):
    seller_reviews = Reviews.get_reviews_for_seller_by_page(current_user.id, page_sr)
    product_reviews = Reviews.get_reviews_for_products_by_page(current_user.id, page_pr)
    reviews_received = Reviews.get_reviews_received_by_page(current_user.id, page_rr)
    max_page_sr = math.ceil(Reviews.get_reviews_for_seller_count(current_user.id)/Reviews.entry_per_page)
    max_page_pr = math.ceil(Reviews.get_reviews_for_products_count(current_user.id)/Reviews.entry_per_page)
    max_page_rr = math.ceil(Reviews.get_reviews_received_count(current_user.id)/Reviews.entry_per_page)
    role = User.getRole(current_user.id)
    return render_template('myreview.html',
                            seller_reviews=seller_reviews, page_sr=page_sr, max_page_sr=max_page_sr,
                            product_reviews=product_reviews, page_pr=page_pr, max_page_pr=max_page_pr,
                            reviews_received=reviews_received, page_rr=page_rr, max_page_rr=max_page_rr,
                            role=role)

@bp.route('/reviews/delete/<int:buyer_id>/<int:target_id>/<int:target_type>', methods=['GET','POST'])
def reviews_delete(buyer_id, target_id, target_type):
    if target_type:
        if Reviews.remove_seller_review(seller_id=target_id, buyer_id=buyer_id):
            return redirect(url_for('social.reviews'))
        else:
            flash("Failed to remove the item.")
    else:
        if Reviews.remove_product_review(iid=target_id, buyer_id=buyer_id):
            return redirect(url_for('social.reviews'))
        else:
            flash("Failed to remove the item.")

@bp.route('/reviews/review_edit/<int:buyer_id>/<int:target_id>/<int:target_type>', methods=['GET','POST'])
def reviews_edit(buyer_id,target_id,target_type):
    if target_type:
        one_review = Reviews.get_reviews_for_some_seller(buyer_id, target_id)
    else:
        one_review = Reviews.get_reviews_for_some_product(buyer_id, target_id)
    role = User.getRole(current_user.id)
    return render_template('review_edit.html',
                            buyer_id=one_review[0].buyer_id,
                            target_id=one_review[0].target_id,
                            content=one_review[0].content,
                            review_time=one_review[0].review_time,
                            rating=one_review[0].rating,
                            target_type=target_type,
                            role=role,
                            isnew=0)

@bp.route('/update-review', methods=['GET'])
def reviews_submit():
    buyer_id = request.args.get('buyer_id')
    target_id = request.args.get('target_id')
    target_type = int(request.args.get('target_type'))
    new_content = request.args.get('content')
    rating = request.args.get('rating')
    last_edit = request.args.get('time')
    isnew = int(request.args.get('isnew'))

    try:
        if not isnew:
            success = Reviews.update_content(buyer_id, target_id, target_type, new_content, rating, last_edit)
            if success:
                return jsonify({'message': 'Review updated successfully'}), 200
            else:
                return jsonify({'error': 'Update failed'}), 400
        else:
            success = Reviews.insert_content(buyer_id, target_id, target_type, new_content, rating, last_edit)
            if success:
                return jsonify({'message': 'New review created successfully'}), 200
            else:
                return jsonify({'error': 'Create failed'}), 400
    except Exception as e:
        return jsonify({'error': 'Server error', 'details': str(e)}), 500
    
@bp.route('/reviews/review_create/<int:buyer_id>/<int:target_id>/<int:target_type>', methods=['GET','POST'])
def reviews_create(buyer_id,target_id,target_type):
    role = User.getRole(current_user.id)
    return render_template('review_edit.html',
                            buyer_id=buyer_id,
                            target_id=target_id,
                            content="",
                            review_time=None,
                            rating=0,
                            target_type=target_type,
                            role=role,
                            isnew=1)
    
@bp.route('/seller_review/<int:seller_id>/<int:page_rr>', methods=['GET','POST'])
@bp.route('/seller_review/<int:seller_id>', methods=['GET','POST'])
def seller_reviews_summary(seller_id, page_rr=1):
    seller_reviews = Reviews.get_reviews_received_by_page(seller_id, page_rr)
    max_page_rr = math.ceil(Reviews.get_reviews_received_count(seller_id)/Reviews.entry_per_page)
    summary = Reviews.get_summary_for_seller(seller_id)
    role = User.getRole(current_user.id)
    data = summary["hist"]
    ratings_data_dict = {k: v for k, v in data}
    hist = json.dumps(ratings_data_dict)
    lst_upvote_status = []
    review_status_zip = None
    if seller_reviews:
        for r in seller_reviews:
            upvote_status = Reviews.check_upvote(seller_id, 1, r.buyer_id, current_user.id)
            if len(upvote_status) == 0:
                upvote_status = 0
            else:
                upvote_status = upvote_status[0][0]
            lst_upvote_status.append(upvote_status)
        review_status_zip = zip(seller_reviews, lst_upvote_status)
    iscustomer=Reviews.iscustomer(seller_id, current_user.id, 1)
    isexist = Reviews.isexist(current_user.id, seller_id, 1)
    return render_template('seller_review.html',
                           reviews_received=seller_reviews,review_status_zip=review_status_zip,
                           page_rr=page_rr, max_page_rr=max_page_rr,
                           avg_rating=summary["avg_rating"],
                           num_reviews=summary["num_reviews"],
                           hist=hist,
                           role=role,
                           user_id=current_user.id,
                           iscustomer=iscustomer,
                           isexist=isexist
                           )

@bp.route('/product_review/<int:iid>/<int:page_rr>', methods=['GET','POST'])
@bp.route('/product_review/<int:iid>', methods=['GET','POST'])
def product_reviews_summary(iid, page_rr=1):
    product_reviews = Reviews.get_all_reviews_for_some_product(iid, page_rr)
    max_page_rr = math.ceil(Reviews.get_all_reviews_for_some_product_count(iid)/Reviews.entry_per_page)
    summary = Reviews.get_summary_for_product(iid)
    role = User.getRole(current_user.id)
    data = summary["hist"]
    ratings_data_dict = {k: v for k, v in data}
    hist = json.dumps(ratings_data_dict)
    lst_upvote_status = []
    review_status_zip = None
    if product_reviews:
        for r in product_reviews:
            upvote_status = Reviews.check_upvote(iid, 0, r.buyer_id, current_user.id)
            if len(upvote_status) == 0:
                upvote_status = 0
            else:
                upvote_status = upvote_status[0][0]
            lst_upvote_status.append(upvote_status)
        review_status_zip = zip(product_reviews, lst_upvote_status)
    iscustomer=Reviews.iscustomer(iid, current_user.id, 0)
    isexist = Reviews.isexist(current_user.id, iid, 0)
    return render_template('product_review.html',
                           reviews_received=product_reviews, review_status_zip=review_status_zip, page_rr=page_rr, max_page_rr=max_page_rr,
                           avg_rating=summary["avg_rating"],
                           num_reviews=summary["num_reviews"],
                           hist=hist,
                           role=role,
                           user_id=current_user.id,
                           iscustomer=iscustomer,
                           isexist=isexist
                           )

@bp.route('/upvote', methods=['GET'])
def upvote_action():
    buyer_id = request.args.get('buyer_id')
    target_id = request.args.get('target_id')
    target_type = int(request.args.get('target_type'))
    user_id = request.args.get('user_id')

    status, new_upvotes = Reviews.upvote(target_id, target_type, buyer_id, user_id)
    return jsonify(status=status, new_upvotes=new_upvotes)
 