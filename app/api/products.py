from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired

from ..models.product import Product
from ..models.user import User

from flask import Blueprint
bp = Blueprint('products', __name__)


@bp.route('/products')
def k_items():
    k = request.args.get('k', default=1, type=int)
    products = Product.get_top_expensive(k)
    return render_template('product.html',
                           avail_products=products,
                           role=User.getRole(current_user.id))

@bp.route('/products/search')
def search():
    query = request.args.get('query')
    search_results = Product.get_search(query)
    return render_template('product.html', avail_products=search_results)

@bp.route('/post/<id>', methods=['GET', 'POST'])
def post(id):
    form = ProductForm()
    if form.validate_on_submit():
        if Product.post_product(id, form.name.data, form.description.data, form.type.data):
            flash('Successfully Created!')
            return redirect(request.referrer)
    return render_template('postProduct.html', form=form, role=User.getRole(current_user.id))

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    submit = SubmitField('Submit')

@bp.route('/edit_product/<int:pid>', methods=['GET', 'POST'])
def edit_product(pid):
    product = Product.get_product(pid)[0]

    form = ProductForm(obj=product)
    if form.validate_on_submit():
        if Product.edit_product(pid, form.name.data, form.description.data, form.type.data):
            flash('Successfully updated!')
            return redirect(request.referrer)

    return render_template('product_edit.html', form=form, product=product)
