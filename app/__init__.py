
from flask import Flask

app = Flask(__name__)

app.config["SECRET_KEY"] = "lab4_secret_key_2026"

from app import views

from app.users import users_bp
from app.products import products_bp

app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(products_bp, url_prefix="/products")
