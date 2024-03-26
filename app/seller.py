from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user
import datetime

from .models.seller import InventoryItem
from .models.product import Product
from .models.user import User

from flask import Blueprint
bp = Blueprint('seller', __name__)


@bp.route('/seller_inventory')
def seller_inventory():
    if not current_user.is_authenticated:
        # If the user is not authenticated,  redirect to login page
        return redirect(url_for('users.login'))
    
    # Get all inventory items for the current seller:
    inventory_items = InventoryItem.get_all_by_seller_id(current_user.id)

    return render_template('seller.html',
                           inventory_items=inventory_items)
