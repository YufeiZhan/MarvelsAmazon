from flask import render_template, request
from flask_login import current_user
import datetime

from ..models.product import Product

from flask import Blueprint
bp = Blueprint('products', __name__)


@bp.route('/products')
def k_items():
    k = request.args.get('k', default=1, type=int)
    products = Product.get_top_expensive(k)
    return render_template('product.html',
                           avail_products=products)