from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user

from .models.cart import Cart
from .models.user import User

from flask import Blueprint
bp = Blueprint('carts', __name__)


@bp.route('/cart')
def lookup():
    if current_user.is_authenticated:
        # Get all inventory items for the current user/seller
        cart_items = Cart.get_all_by_uid(current_user.id)
        return render_template('cart.html', cart_items=cart_items)
    else:
        # If the user is not authenticated,  redirect to login page
        return redirect(url_for('users.login'))
