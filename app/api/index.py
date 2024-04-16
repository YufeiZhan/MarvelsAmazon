from flask import render_template
from flask_login import current_user
import datetime
import math

from ..models.product import Product
from ..models.user import User

from flask import Blueprint
bp = Blueprint('index', __name__)

@bp.route('/<int:page>')
@bp.route('/')
def index(page=1):
    # get all available products for sale:
    products = Product.get_page(page)
    max_page = math.ceil(len(Product.get_all())/Product.entry_per_page)

    if current_user.is_authenticated:
        return render_template('index.html',
                           products_on_page=products,role=User.getRole(current_user.id),page=page,max_page=max_page)
    else:
        return render_template('index.html',
                           products_on_page=products,page=page,max_page=max_page)