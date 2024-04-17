from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_user, login_required
import math

from ..models.cart import Cart, CartWithPrice
from ..models.user import User

from flask import Blueprint
bp = Blueprint('carts', __name__)


# @bp.route('/cart/<int:page>')
@bp.route('/cart/')
@login_required
# flask_login's login_required decorator returns login page automatically if user not logged in
# this saves long code to check if user is logged in and return
def lookup(page=1):
    # Get items on the specified page
    # items = Cart.get_page(current_user.id,page)
    # max_page = math.ceil(len(Cart.get_all_by_uid(current_user.id))/Cart.entry_per_page)

    # Get all carts items for the current user/seller
    cart_items = Cart.get_all_by_uid_with_price(current_user.id)
    total_price = CartWithPrice.get_total_price(cart_items)
    # return render_template('cart.html', cart_items=items, role=User.getRole(current_user.id), page=page, max_page=max_page)
    return render_template('cart.html', cart_items=cart_items, role=User.getRole(current_user.id), total_price=total_price)


@bp.route('/cart/remove/<int:inventoryid>')
@login_required
def remove_item(inventoryid):
    Cart.remove_item(current_user.id, inventoryid)
    return jsonify({'message': 'Item removed successfully'})

@bp.route('/cart/decrease/<int:uid>/<int:iid>')
@login_required
def decrease_item(uid,iid):
    Cart.decrease_item(uid, iid)
    return jsonify({'message': 'Item decreased successfully'})

@bp.route('/cart/increase/<int:uid>/<int:iid>')
@login_required
def increase_item(uid,iid):
    Cart.increase_item(uid, iid)
    return jsonify({'message': 'Item increased successfully'})