from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, login_required
import datetime

from ..models.seller import InventoryItem
from ..models.user import User

from flask import Blueprint
bp = Blueprint('seller', __name__)


@bp.route('/seller_inventory')
@login_required # Requires a user to be logged in to access this page otherwise redirect to defined login page automatically
def seller_inventory():    
    # Get all inventory items for the current seller:
    inventory_items = InventoryItem.get_all_by_seller_id(current_user.id)

    return render_template('seller.html',
                           inventory_items=inventory_items,
                           role = User.getRole(current_user.id))
