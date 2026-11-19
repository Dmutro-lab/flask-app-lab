
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import MetaData

from app.config import config


db = SQLAlchemy(
    metadata=MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s"
        }
    )
)

migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config["development"]))
    app.config["SQLALCHEMY_ECHO"] = True
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from app.views import main_bp
    from app.users import users_bp
    from app.products import products_bp
    from app.posts import post_bp
    from app.posts.models import Post, Tag
    from app.users.models import User
    from app.products.models import Product

    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(products_bp, url_prefix="/product")
    app.register_blueprint(post_bp)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(413)
    def request_entity_too_large(error):
        if request.path.startswith("/product/"):
            flash("Файл завеликий. Максимальний розмір — 2 МБ.", "danger")
            return redirect(request.referrer or url_for("products.product_add"))
        return "Завантажений файл завеликий.", 413

    @app.route("/products/")
    @app.route("/products")
    def legacy_products_list():
        from flask import render_template
        from app.products.storage import get_products_table
        from app.products.views import CATEGORY_NAMES

        products = sorted(
            get_products_table().all(),
            key=lambda item: item["id"]
        )

        return render_template(
            "products/products.html",
            products=products,
            category_names=CATEGORY_NAMES
        )

    @app.route("/products/<int:product_id>")
    def legacy_product_detail(product_id):
        from flask import abort, render_template
        from app.products.storage import get_products_table
        from app.products.views import CATEGORY_NAMES

        product = get_products_table().get(doc_id=product_id)

        if product is None:
            abort(404)

        return render_template(
            "products/detail_product.html",
            product=product,
            category_names=CATEGORY_NAMES
        )

    return app
