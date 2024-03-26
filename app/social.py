from flask_login import current_user, login_user
from flask import render_template

from .models.reviews import Reviews

from flask import Blueprint
bp = Blueprint('social', __name__)

class User():
    def __init__(self):
        self.is_active = True
        self.is_authenticated = True
        pass

    def get_id(self):
        return self.id
        

@bp.route('/reviews')
def reviews():
    dummy_user = User()
    dummy_user.id = 1
    dummy_user.name = "Dummy User"
    dummy_user.email = "dummy@example.com"

    # Log in the dummy user
    login_user(dummy_user)
    if current_user.is_authenticated:
        results = Reviews.get_reviews_for_seller(current_user.id)
        return render_template('review.html', reviews=results)
    else:
        return render_template('base.html')