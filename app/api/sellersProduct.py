from flask import render_template, request
from flask_login import current_user
import datetime

from ..models.product import Product
from ..models.user import User
from ..models.sellersProduct import SellersProduct

from flask import Blueprint
bp = Blueprint('sellersProduct', __name__)

@bp.route('/sellersProduct')
def seller_products():
    product_name = request.args.get('product_name')
    products_info = SellersProduct.get_seller_products(product_name)
    return render_template('sellersProduct.html',
                           avail_products=products_info,
                           role=User.getRole(current_user.id))