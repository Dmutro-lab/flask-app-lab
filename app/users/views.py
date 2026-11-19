
from flask import (
    render_template, request, redirect,
    url_for, session, flash, make_response
)
from flask_login import (
    login_user, logout_user, login_required, current_user
)

from app import db, bcrypt
from app.users import users_bp
from app.users.models import User
from app.users.forms import RegistrationForm


@users_bp.route("/hi/<name>")
def greetings(name):
    age = request.args.get("age", type=int)

    return render_template(
        "users/hi.html",
        name=name,
        age=age
    )


@users_bp.route("/admin")
def admin():
    return redirect(
        url_for(
            "users.greetings",
            name="administrator",
            age=45
        )
    )


# Лабораторна №9. Реєстрація користувачів
@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash("Реєстрацію успішно завершено!", "success")
        return redirect(url_for("users.account"))

    return render_template("users/register.html", form=form)


# Лабораторна №9. Вхід користувачів
@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)

            flash("Вхід виконано успішно!", "success")
            return redirect(url_for("users.account"))

        flash("Неправильне ім'я користувача або пароль!", "danger")
        return redirect(url_for("users.login"))

    return render_template("users/login.html")


# Лабораторна №9. Сторінка облікового запису
@users_bp.route("/account")
@login_required
def account():
    return render_template(
        "users/account.html",
        user=current_user
    )


# Лабораторна №9. Список усіх користувачів
@users_bp.route("/all-users")
@login_required
def all_users():
    users = User.query.order_by(User.id).all()
    users_count = User.query.count()

    return render_template(
        "users/all_users.html",
        users=users,
        users_count=users_count
    )


# Лабораторна №9. Профіль користувача
@users_bp.route("/profile")
@login_required
def profile():
    cookies = request.cookies

    theme = request.cookies.get("theme", "light")

    if theme not in ("light", "dark"):
        theme = "light"

    return render_template(
        "users/profile.html",
        username=current_user.username,
        cookies=cookies,
        theme=theme
    )


# Лабораторна №9. Вихід із системи
@users_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()

    flash("Ви успішно вийшли із системи!", "success")
    return redirect(url_for("users.login"))


# Додавання cookie
@users_bp.route("/add-cookie", methods=["POST"])
@login_required
def add_cookie():
    key = request.form.get("key", "").strip()
    value = request.form.get("value", "")
    max_age = request.form.get("max_age", type=int)

    if not key or not value or max_age is None or max_age <= 0:
        flash("Заповніть правильно всі поля cookie!", "danger")
        return redirect(url_for("users.profile"))

    if key == "session":
        flash("Не можна змінювати службову cookie session!", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))

    response.set_cookie(
        key,
        value,
        max_age=max_age,
        path="/"
    )

    flash(f"Cookie '{key}' успішно додано!", "success")
    return response


# Видалення cookie за ключем
@users_bp.route("/delete-cookie", methods=["POST"])
@login_required
def delete_cookie():
    key = request.form.get("key", "").strip()

    if not key:
        flash("Введіть ключ cookie!", "danger")
        return redirect(url_for("users.profile"))

    if key == "session":
        flash("Службову cookie session не можна видаляти окремо!", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.delete_cookie(key, path="/")

    flash(f"Cookie '{key}' видалено!", "success")
    return response


# Видалення всіх cookies
@users_bp.route("/delete-all-cookies", methods=["POST"])
@login_required
def delete_all_cookies():
    response = make_response(redirect(url_for("users.profile")))

    for key in request.cookies:
        if key != "session":
            response.delete_cookie(key, path="/")

    flash("Всі користувацькі cookies видалено!", "success")
    return response


# Зміна кольорової схеми
@users_bp.route("/change-theme/<theme>", methods=["POST"])
@login_required
def change_theme(theme):
    if theme not in ("light", "dark"):
        flash("Невідома кольорова схема!", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))

    response.set_cookie(
        "theme",
        theme,
        max_age=30 * 24 * 60 * 60,
        path="/"
    )

    flash("Кольорову схему успішно змінено!", "success")
    return response
