
from tinydb import Query
from datetime import datetime
from pathlib import Path
from uuid import uuid4
from decimal import Decimal

from flask import render_template, abort, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename

from app.products import products_bp
from app.products.forms import ProductForm
from app.products.storage import get_products_table


CATEGORY_NAMES = {
    "electronics": "Електроніка",
    "computers": "Комп'ютери",
    "phones": "Смартфони",
    "accessories": "Аксесуари",
    "other": "Інше"
}


def _find_product(product_id):
    Product = Query()
    return get_products_table().get(Product.id == product_id)


def _save_image(file_storage):
    if not file_storage or not file_storage.filename:
        return None

    file_storage.stream.seek(0, 2)
    size = file_storage.stream.tell()
    file_storage.stream.seek(0)

    max_size = current_app.config["MAX_PRODUCT_IMAGE_SIZE"]

    if size > max_size:
        raise ValueError("Розмір зображення перевищує дозволений ліміт 2 МБ.")

    original_name = secure_filename(file_storage.filename)
    extension = Path(original_name).suffix.lower()

    if extension not in {".png", ".jpg", ".jpeg"}:
        raise ValueError("Дозволені формати зображень: PNG, JPG і JPEG.")

    filename = f"{uuid4().hex}{extension}"

    upload_dir = Path(current_app.config["PRODUCT_UPLOAD_FOLDER"])
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_storage.save(upload_dir / filename)

    return f"uploads/{filename}"


def _delete_image(image_path):
    if not image_path:
        return

    upload_root = Path(current_app.config["PRODUCT_UPLOAD_FOLDER"]).resolve()
    target = (upload_root / Path(image_path).name).resolve()

    if target.parent == upload_root and target.exists():
        target.unlink()


@products_bp.route("", methods=["GET"], endpoint="product_list")
def product_list():
    products = sorted(
        get_products_table().all(),
        key=lambda item: item["id"]
    )

    return render_template(
        "products/products.html",
        products=products,
        category_names=CATEGORY_NAMES
    )


@products_bp.route("/add", methods=["GET", "POST"])
def product_add():
    form = ProductForm()

    if form.validate_on_submit():
        image_path = None

        try:
            image_path = _save_image(form.image.data)

            table = get_products_table()
            products = table.all()

            product_id = max(
                (item["id"] for item in products),
                default=0
            ) + 1

            product = {
                "id": product_id,
                "name": form.name.data.strip(),
                "content": form.content.data.strip(),
                "price": str(form.price.data.quantize(Decimal("0.01"))),
                "category": form.category.data,
                "quantity": form.quantity.data,
                "image": image_path,
                "created_at": datetime.now().astimezone().isoformat(timespec="seconds")
            }

            table.insert(product)

            flash("Товар успішно додано.", "success")

            return redirect(url_for("products.product_list"))

        except (OSError, ValueError) as error:
            if image_path:
                _delete_image(image_path)

            flash(f"Не вдалося додати товар: {error}", "danger")

    elif request.method == "POST":
        flash("Перевірте правильність заповнення форми.", "danger")

    return render_template(
        "products/product_form.html",
        form=form,
        heading="Додавання товару"
    )


@products_bp.route("/<int:product_id>", methods=["GET"])
def product_detail(product_id):
    product = _find_product(product_id)

    if product is None:
        abort(404)

    return render_template(
        "products/detail_product.html",
        product=product,
        category_names=CATEGORY_NAMES
    )


@products_bp.route("/<int:product_id>/edit", methods=["GET", "POST"])
def product_edit(product_id):
    product = _find_product(product_id)

    if product is None:
        abort(404)

    form = ProductForm()

    if request.method == "GET":
        form.name.data = product["name"]
        form.content.data = product["content"]
        form.price.data = Decimal(str(product["price"]))
        form.category.data = product["category"]
        form.quantity.data = product["quantity"]

    if form.validate_on_submit():
        new_image_path = None

        try:
            image_path = product.get("image")

            if form.image.data and form.image.data.filename:
                new_image_path = _save_image(form.image.data)
                image_path = new_image_path

            updated = {
                "name": form.name.data.strip(),
                "content": form.content.data.strip(),
                "price": str(form.price.data.quantize(Decimal("0.01"))),
                "category": form.category.data,
                "quantity": form.quantity.data,
                "image": image_path
            }

            Product = Query()

            get_products_table().update(
                updated,
                Product.id == product_id
            )

            if new_image_path:
                _delete_image(product.get("image"))

            flash("Зміни товару збережено.", "success")

            return redirect(
                url_for(
                    "products.product_detail",
                    product_id=product_id
                )
            )

        except (OSError, ValueError) as error:
            if new_image_path:
                _delete_image(new_image_path)

            flash(f"Не вдалося зберегти зміни: {error}", "danger")

    elif request.method == "POST":
        flash("Перевірте правильність заповнення форми.", "danger")

    return render_template(
        "products/product_form.html",
        form=form,
        heading="Редагування товару",
        product=product
    )


@products_bp.route("/<int:product_id>/delete", methods=["POST"])
def product_delete(product_id):
    product = _find_product(product_id)

    if product is None:
        abort(404)

    Product = Query()

    get_products_table().remove(
        Product.id == product_id
    )

    _delete_image(product.get("image"))

    flash("Товар видалено.", "success")

    return redirect(url_for("products.product_list"))
