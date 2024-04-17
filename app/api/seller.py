from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, login_required
import datetime
import math
from ..models.seller import InventoryItem
from ..models.user import User

from flask import Blueprint
bp = Blueprint('seller', __name__)

@bp.route('/seller_inventory')
@bp.route('/seller_inventory/<int:page>')
@login_required
def seller_inventory(page = 1):    
    per_page = 6
    total_items = InventoryItem.count_by_seller_id(current_user.id)
    inventory_items = InventoryItem.get_page_by_seller_id(current_user.id, page, per_page)
    max_page = math.ceil(total_items / per_page)

    return render_template('seller.html',
                           inventory_items=inventory_items,
                           role = User.getRole(current_user.id),
                           page = page,
                           max_page = max_page
                           )

@bp.route('/add_inventory_item', methods=['POST'])
@login_required
def add_inventory_item():
    product_name = request.form.get('product_name')
    # type = request.form.get('type')
    # description = request.form.get('description')
    unit_price = request.form.get('unit_price')
    quantity_available = request.form.get('quantity_available')
    # print(product_name, unit_price, quantity_available)
    success = InventoryItem.add_item(current_user.id, product_name, unit_price, quantity_available)
    if success:
        flash('Product added successfully!')
    else:
        flash('Failed to add product.', 'perhaps product non existent')
    return redirect(url_for('seller.seller_inventory'))