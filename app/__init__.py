from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)

    from .api.index import bp as index_bp
    app.register_blueprint(index_bp)

    from .api.users import bp as user_bp
    app.register_blueprint(user_bp)

    from .api.carts import bp as cart_bp
    app.register_blueprint(cart_bp)

    from .api.products import bp as products_bp
    app.register_blueprint(products_bp)

    from .api.sellersProduct import bp as sellersProduct_sp
    app.register_blueprint(sellersProduct_sp)

    from .api.seller import bp as seller_bp
    app.register_blueprint(seller_bp)

    from .api.social import bp as social_bp
    app.register_blueprint(social_bp)
    
    return app
