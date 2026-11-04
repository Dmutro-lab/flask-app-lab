from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField(
        "Ім'я",
        validators=[DataRequired(message="Вкажіть ім'я."), Length(max=100)]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(message="Вкажіть email."), Email(message="Введіть коректну email-адресу."), Length(max=254)]
    )
    subject = SelectField(
        "Тема звернення",
        choices=[
            ("question", "Запитання"),
            ("proposal", "Пропозиція"),
            ("cooperation", "Співпраця"),
            ("other", "Інше")
        ],
        validators=[DataRequired(message="Оберіть тему звернення.")]
    )
    message = TextAreaField(
        "Повідомлення",
        validators=[DataRequired(message="Введіть повідомлення."), Length(max=3000)]
    )
    submit = SubmitField("Надіслати повідомлення")
