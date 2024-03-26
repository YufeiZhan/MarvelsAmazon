from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user

from flask import Blueprint
bp = Blueprint('carts', __name__)


@bp.route('/cart')
def lookup():
    if current_user.is_authenticated:
        return render_template('cart.html')
