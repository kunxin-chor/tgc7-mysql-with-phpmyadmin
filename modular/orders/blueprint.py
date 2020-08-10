from flask import Blueprint, render_template

orders_page = Blueprint('orders', __name__,
                        template_folder='templates')


@orders_page.route('/')
def show_orders():
    return render_template('orders/index.template.html')
