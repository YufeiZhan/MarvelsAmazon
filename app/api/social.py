import math

from flask_login import current_user, login_required
from flask import render_template, redirect, url_for, flash

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
    return render_template('review.html',
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

