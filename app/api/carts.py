from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, login_required

from ..models.cart import Cart
from ..models.user import User

from flask import Blueprint
bp = Blueprint('carts', __name__)


@bp.route('/cart')
@login_required
# flask_login's login_required decorator returns login page automatically if user not logged in
# this saves long code to check if user is logged in and return
def lookup():
    # Get all inventory items for the current user/seller
    cart_items = Cart.get_all_by_uid(current_user.id)
    return render_template('cart.html', cart_items=cart_items if cart_items else [], role=User.getRole(current_user.id))
