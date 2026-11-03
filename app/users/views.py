
from flask import (
    render_template, request, redirect,
    url_for, session, flash, make_response
)

from app.users import users_bp


# Лабораторна №3
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


# Завдання 1. Авторизація
@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "12345":
            session["username"] = username

            flash("Вхід виконано успішно!", "success")
            return redirect(url_for("users.profile"))

        flash("Неправильний логін або пароль!", "danger")
        return redirect(url_for("users.login"))

    return render_template("users/login.html")


@users_bp.route("/profile")
def profile():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "danger")
        return redirect(url_for("users.login"))

    username = session["username"]


    cookies = request.cookies

    theme = request.cookies.get("theme", "light")

    if theme not in ("light", "dark"):
        theme = "light"

    return render_template(
        "users/profile.html",
        username=username,
        cookies=cookies,
        theme=theme
    )


# Завдання 1. Вихід
@users_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)

    flash("Ви успішно вийшли із системи!", "success")
    return redirect(url_for("users.login"))


# Завдання 2. Додавання cookie
@users_bp.route("/add-cookie", methods=["POST"])
def add_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "danger")
        return redirect(url_for("users.login"))

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


# Завдання 2. Видалення cookie за ключем
@users_bp.route("/delete-cookie", methods=["POST"])
def delete_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "danger")
        return redirect(url_for("users.login"))

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


# Завдання 2. Видалення всіх cookies
@users_bp.route("/delete-all-cookies", methods=["POST"])
def delete_all_cookies():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "danger")
        return redirect(url_for("users.login"))

    response = make_response(redirect(url_for("users.profile")))


    for key in request.cookies:
        if key != "session":
            response.delete_cookie(key, path="/")

    flash("Всі користувацькі cookies видалено!", "success")
    return response


# Завдання 3. Зміна кольорової схеми
@users_bp.route("/change-theme/<theme>", methods=["POST"])
def change_theme(theme):
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "danger")
        return redirect(url_for("users.login"))

    if theme not in ("light", "dark"):
        flash("Невідома кольорова схема!", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))

    # Зберігаємо тему на 30 днів
    response.set_cookie(
        "theme",
        theme,
        max_age=30 * 24 * 60 * 60,
        path="/"
    )

    flash("Кольорову схему успішно змінено!", "success")
    return response
