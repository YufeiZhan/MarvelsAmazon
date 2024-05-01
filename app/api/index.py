from flask import render_template, request
from flask_login import current_user
import datetime
import math
from flask import current_app as app

from ..models.product import Product
from ..models.user import User

from flask import Blueprint
bp = Blueprint('index', __name__)

@bp.route('/<int:page>')
@bp.route('/')
def index(page=1):
    # products
    products = Product.get_page(page)
    max_page = math.ceil(len(Product.get_all())/Product.entry_per_page)
    
    # all product types
    result = app.db.execute('SELECT DISTINCT type FROM Products')
    types = [row[0] for row in result]

    if current_user.is_authenticated:
        return render_template('index.html',
                           products_on_page=products,role=User.getRole(current_user.id),page=page,max_page=max_page, types=types, product_type=None)
    else:
        return render_template('index.html',
                           products_on_page=products,page=page,max_page=max_page, types=types, product_type=None)

@bp.route('/index/products_by_type/<int:page>')
@bp.route('/index/products_by_type')
def products_by_type(page=1):
    product_type = request.args.get('type', default=None, type=str)
    max_page = math.ceil(len(Product.get_all_with_type(product_type))/Product.entry_per_page)
    if page > max_page:  # Check if the requested page exceeds available pages
        page = max_page

    if product_type:
        products = Product.get_page_with_type(page, product_type)

    # all product types
    result = app.db.execute('SELECT DISTINCT type FROM Products')
    types = [row[0] for row in result]

    if current_user.is_authenticated:
        return render_template('index.html',
                           products_on_page=products,role=User.getRole(current_user.id),page=page,max_page=max_page, types=types, product_type=product_type)
    else:
        return render_template('index.html',
                           products_on_page=products,page=page,max_page=max_page, types=types, product_type=product_type)