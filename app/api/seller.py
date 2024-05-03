from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_user, login_required
import math
from ..models.seller import InventoryItem
from ..models.user import User

from flask import Blueprint
bp = Blueprint('seller', __name__)

@bp.route('/seller_inventory')
@bp.route('/seller_inventory/<int:page>')
@login_required
def seller_inventory(page = 1):    
    per_page = 8
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

@bp.route('/update_quantity/<int:iid>', methods=['POST'])
@login_required
def update_quantity(iid):
    action = request.form.get('change')
    current_quantity = InventoryItem.get_current_quantity(iid)
    if action == 'increase':
        new_quantity = current_quantity + 1
    elif action == 'decrease':
        new_quantity = current_quantity - 1 if current_quantity > 0 else 0

    InventoryItem.update_quantity(iid, new_quantity, current_user.id)
    flash('Quantity updated successfully!')
    return redirect(url_for('seller.seller_inventory'))

@bp.route('/delete_inventory/<int:iid>', methods=['POST'])
@login_required
def delete_inventory(iid):
    status = InventoryItem.delete(iid, current_user.id)
    # print(status)
    flash('Product removed successfully!')
    return redirect(url_for('seller.seller_inventory'))

@bp.route('/sale_history')
@bp.route('/sale_history/<int:page>')
@login_required
def sale_history(page = 1):
    per_page = 6
    orders = InventoryItem.get_sale_orders(current_user.id, page, per_page)
    # print(orders)
    # print(orders)
    total_items = InventoryItem.count_sale_orders(current_user.id)
    max_page = math.ceil(total_items / per_page)
    return render_template('sale_history.html', title='Sale History', orders=orders, 
                        role=User.getRole(current_user.id),
                        page = page, max_page = max_page)

@bp.route('/order_details/<int:oid>')
@login_required
def order_details(oid):
    order_details= InventoryItem.get_order_details(oid, current_user.id)
    # order_details = [dict(rows) for row in rows]
    if all(item[10] == 'fulfilled' for item in order_details):
        fulfillment_status = 'FULFILLED'
    elif all(item[10] == 'cancelled' for item in order_details):
        fulfillment_status = 'CANCELLED'
    elif all(item[10] == 'placed' for item in order_details):
        fulfillment_status = 'PLACED'
    elif all(item[10] == 'in delivery' for item in order_details):
        fulfillment_status = 'IN DELIVERY'
    else: 
        fulfillment_status = 'PENDING'
    if not order_details:
        flash('No order found or you do not have permission to view this order.', 'error')
        return redirect(url_for('seller.sale_history'))
    return render_template('sale_order_details.html', order_details=order_details, fulfillment_status = fulfillment_status, role=User.getRole(current_user.id))

@bp.route('/mark_as_fulfilled/<int:oiid>/<int:oid>', methods=['POST'])
@login_required
def mark_as_fulfilled(oiid,oid):
    status = InventoryItem.mark_as_fulfilled(oiid, current_user.id)
    # print(status)
    if status:
        flash('Order item has been marked as fulfilled.', 'success')
    else:
        flash('Failed to update the order item status.', 'error')
    return redirect(url_for('seller.order_details', oid=oid))

@bp.route('/popularity')
def get_product_popularity():
    rows = InventoryItem.get_product_popularity(current_user.id)
    results = []
    for row in rows:
        results.append({
            'name': row[0],  
            'total_sold': row[1],  
            'unit_price': float(row[2]) 
        })
    # print(results)
    return jsonify(results)