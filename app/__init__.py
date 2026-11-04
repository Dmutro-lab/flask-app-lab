from pathlib import Path
from flask import Flask
from flask_wtf.csrf import CSRFProtect

BASE_DIR = Path(__file__).resolve().parent.parent

app = Flask(__name__)
app.config.update(
    SECRET_KEY="lab5_flask_wtf_secret_key_change_me",
    MAX_CONTENT_LENGTH=2 * 1024 * 1024 + 65536,
    MAX_PRODUCT_IMAGE_SIZE=2 * 1024 * 1024,
    PRODUCTS_DB_PATH=str(BASE_DIR / "data" / "products.json"),
    PRODUCT_UPLOAD_FOLDER=str(Path(__file__).resolve().parent / "products" / "static" / "uploads")
)

csrf = CSRFProtect(app)

from app import views
from app.users import users_bp
from app.products import products_bp

app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(products_bp, url_prefix="/product")


@app.errorhandler(413)
def request_entity_too_large(error):
    from flask import flash, redirect, url_for, request
    flash("Файл завеликий. Максимальний розмір — 2 МБ.", "danger")
    if request.path.startswith("/product/"):
        return redirect(request.referrer or url_for("products.product_add"))
    return "Завантажений файл завеликий.", 413


@app.route("/products/")
@app.route("/products")
def legacy_products_list():
    from flask import render_template
    from app.products.storage import get_products_table
    from app.products.views import CATEGORY_NAMES
    products = sorted(get_products_table().all(), key=lambda item: item["id"])
    return render_template("products/products.html", products=products, category_names=CATEGORY_NAMES)


@app.route("/products/<int:product_id>")
def legacy_product_detail(product_id):
    from flask import render_template, abort
    from app.products.views import CATEGORY_NAMES
    from app.products.storage import get_products_table
    product = get_products_table().get(doc_id=product_id)
    if product is None:
        abort(404)
    return render_template("products/detail_product.html", product=product, category_names=CATEGORY_NAMES)
