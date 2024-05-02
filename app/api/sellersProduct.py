from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, login_required

import datetime

from ..models.product import Product
from ..models.user import User
from ..models.sellersProduct import SellersProduct
from ..models.cart import Cart

from flask import Blueprint
bp = Blueprint('sellersProduct', __name__)

@bp.route('/sellersProduct')
def seller_products():
    product_name = request.args.get('product_name')
    products_info = SellersProduct.get_seller_products(product_name)
    return render_template('sellersProduct.html',
                           avail_products=products_info,
                           role=User.getRole(current_user.id))

@bp.route('/sellersProduct/increase', methods=['POST'])
@login_required
def increase_item():
    uid = request.form['userid']
    iid = request.form['inventoryid']
    quantity = request.form.get('quantity', 1)
    try:
        SellersProduct.add_cart(uid, iid, quantity)
        flash('Product added successfully!')
    except Exception as e:
        flash(f'Failed to add product: {str(e)}')
    return redirect(request.referrer)