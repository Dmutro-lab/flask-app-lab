from decimal import Decimal
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, SelectField, IntegerField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError


CATEGORIES = [
    ("electronics", "Електроніка"),
    ("computers", "Комп'ютери"),
    ("phones", "Смартфони"),
    ("accessories", "Аксесуари"),
    ("other", "Інше")
]


class ProductForm(FlaskForm):
    name = StringField(
        "Назва товару",
        validators=[DataRequired(message="Вкажіть назву товару."), Length(min=3, max=100, message="Назва повинна містити від 3 до 100 символів.")]
    )
    content = TextAreaField(
        "Опис товару",
        validators=[DataRequired(message="Вкажіть опис товару."), Length(max=3000)]
    )
    price = DecimalField(
        "Ціна",
        places=2,
        rounding=None,
        validators=[DataRequired(message="Вкажіть ціну."), NumberRange(min=Decimal("0.01"), message="Ціна повинна бути додатною.")]
    )
    category = SelectField(
        "Категорія",
        choices=CATEGORIES,
        validators=[DataRequired(message="Оберіть категорію.")]
    )
    quantity = IntegerField(
        "Кількість",
        validators=[DataRequired(message="Вкажіть кількість."), NumberRange(min=0, message="Кількість не може бути від'ємною.")]
    )
    image = FileField(
        "Зображення",
        validators=[FileAllowed(["jpg", "jpeg", "png"], "Дозволені формати: PNG, JPG, JPEG.")]
    )
    submit = SubmitField("Зберегти товар")

    def validate_price(self, field):
        raw_value = field.raw_data[0] if field.raw_data else ""
        if raw_value and "." in raw_value and len(raw_value.rsplit(".", 1)[1]) > 2:
            raise ValidationError("Ціна повинна мати не більше двох знаків після коми.")

    def validate_content(self, field):
        if field.data and not field.data.strip():
            raise ValidationError("Опис товару не може складатися лише з пробілів.")

    def validate_name(self, field):
        if field.data and not field.data.strip():
            raise ValidationError("Назва товару не може складатися лише з пробілів.")
