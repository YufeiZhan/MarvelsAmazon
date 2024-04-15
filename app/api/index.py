from flask import render_template
from flask_login import current_user
import datetime

from ..models.product import Product
from ..models.user import User

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all()

    if current_user.is_authenticated:
        return render_template('index.html',
                           avail_products=products,role=User.getRole(current_user.id))
    else:
        return render_template('index.html',
                           avail_products=products)
