from flask_login import current_user, login_user, login_required
from flask import render_template, redirect, url_for

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
        

@bp.route('/reviews')
@login_required # Requires a user to be logged in to access this page otherwise redirect to defined login page automatically
def reviews():
    seller_reviews = Reviews.get_reviews_for_seller(current_user.id)
    product_reviews = Reviews.get_reviews_for_products(current_user.id)
    reviews_received = Reviews.get_reviews_received(current_user.id)
    role = User.getRole(current_user.id)
    return render_template('review.html', 
                            seller_reviews=seller_reviews, 
                            product_reviews=product_reviews, 
                            reviews_received=reviews_received,
                            role=User.getRole(current_user.id))
        