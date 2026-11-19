from flask_wtf import FlaskForm
from wtforms import BooleanField, DateTimeLocalField, SelectField, SelectMultipleField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired(message="Введіть заголовок."), Length(max=150)])
    content = TextAreaField("Текст поста", validators=[DataRequired(message="Введіть текст поста.")])
    enabled = BooleanField("Активний пост", default=True)
    publish_date = DateTimeLocalField("Дата та час публікації", format="%Y-%m-%dT%H:%M", validators=[DataRequired(message="Оберіть дату та час.")])
    category = SelectField(
        "Категорія",
        choices=[("news", "Новини"), ("publication", "Публікація"), ("tech", "Технології"), ("other", "Інше")],
        validators=[DataRequired(message="Оберіть категорію.")],
    )
    author_id = SelectField("Автор", coerce=int, validators=[DataRequired(message="Оберіть автора.")])
    tags = SelectMultipleField("Теги", coerce=int)
    submit = SubmitField("Зберегти")
