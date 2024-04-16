from flask import render_template, request
from flask_login import current_user
import datetime

from ..models.product import Product
from ..models.user import User
from ..models.buyerProduct import BuyerProduct

from flask import Blueprint
bp = Blueprint('buyerProduct', __name__)

@bp.route('/buyerProduct')
def seller_info():
    product_name = request.args.get('product_name')
    products_info = BuyerProduct.get_buyer_products(product_name)
    return render_template('buyerProduct.html',
                           avail_products=products_info,
                           role=User.getRole(current_user.id))