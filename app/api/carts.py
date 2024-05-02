from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_required

from ..models.cart import Cart, CartWithPrice
from ..models.user import User
from ..models.seller import InventoryItem

from flask import Blueprint
bp = Blueprint('carts', __name__)


# @bp.route('/cart/<int:page>')
@bp.route('/cart/')
@login_required
# flask_login's login_required decorator returns login page automatically if user not logged in
# this saves long code to check if user is logged in and return
def lookup(page=1):
    # Get all carts items for the current user/seller
    cart_items = Cart.get_all_by_uid_with_price(current_user.id)
    total_price = CartWithPrice.get_total_price(cart_items)
    return render_template('cart.html', cart_items=cart_items, role=User.getRole(current_user.id), total_price=total_price, user=current_user)




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
    rowsNo = Cart.increase_item(uid, iid)
    if (rowsNo == 0):
        return jsonify(max = True)
    else:
        return jsonify(max = False)
    
@bp.route('/cart/remove/<int:uid>/all')
@login_required
def remove_all(uid):
    Cart.remove_all(uid)
    return jsonify({'message':'Cart is cleaned.'})