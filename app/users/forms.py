
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from sqlalchemy import select

from app import db
from app.users.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Ім'я користувача",
        validators=[
            DataRequired(),
            Length(min=3, max=80)
        ]
    )

    email = StringField(
        "Електронна пошта",
        validators=[
            DataRequired(),
            Email(),
            Length(max=254)
        ]
    )

    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )

    confirm_password = PasswordField(
        "Підтвердження пароля",
        validators=[
            DataRequired(),
            EqualTo("password", message="Паролі повинні збігатися.")
        ]
    )

    submit = SubmitField("Зареєструватися")

    def validate_username(self, username):
        user = db.session.scalar(
            select(User).where(User.username == username.data)
        )

        if user:
            raise ValidationError("Це ім'я користувача вже зайняте.")

    def validate_email(self, email):
        user = db.session.scalar(
            select(User).where(User.email == email.data)
        )

        if user:
            raise ValidationError("Ця електронна пошта вже зареєстрована.")

